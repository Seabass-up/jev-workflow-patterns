#!/usr/bin/env python3
"""Run the reviewed Pages build checks locally, with source and per-step receipts."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import signal
import subprocess
import sys
import time
import uuid

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ".github/workflows/pages.yml"
WORKFLOW_SHA256 = "b0b0633022c070e0b57e9737fc81e188937307ba00e8f04efa310bd7dd59d250"
PAGES_IMAGE = "ghcr.io/actions/jekyll-build-pages@sha256:6791ebfd912185ed59bfb5fb102664fa872496b79f87ff8b9cfba292a7345041"
PROVENANCE = {
    "reference": "Claude's Seabass scripts/ci-local.sh, commit 873629b",
    "reference_sha256": "f071762556cd50e377f7ae6c1469259a8eb470cf3b6eaec800602877f0c958cf",
    "adaptation": "Jev Python adapter of workflow drift guards, CI shell commands, per-step logs and source receipts.",
    "original_runner_execution": False,
    "pages_action": "actions/jekyll-build-pages@v1, v1.0.13 image, github-pages 232",
}
BUILD_STEPS = [
    "Check out source",
    "Verify iteration receipts and controller tests",
    "Verify portable question kernel",
    "Verify Choice confidence, discovery measurements, and candidates",
    "Verify email contracts and preserved receipts",
    "Verify bug-hunting contracts and preserved screening",
    "Verify human-AI research contracts and frozen challenges",
    "Verify pattern collections",
    "Verify generated catalog and collection hub",
    "Configure Pages",
    "Build site with Jekyll",
    "Verify required pages",
    "Upload Pages artifact",
]
LOCAL_ACTIONS = {
    "Check out source": "local_snapshot",
    "Configure Pages": "local_configuration",
    "Build site with Jekyll": "jekyll_container",
    "Upload Pages artifact": "not_applicable_to_local_build",
}
SANDBOX = "(version 1)\n(allow default)\n(deny network*)\n"
CANARY = """import errno, socket
s = socket.socket()
s.settimeout(1)
try:
    s.connect(('192.0.2.1', 443))
except OSError as e:
    assert e.errno in (errno.EPERM, errno.EACCES), repr(e)
else:
    raise AssertionError('network sandbox allowed an external connection')
finally:
    s.close()
print('external network denied by the kernel')
"""
GIT_ENV = {
    "PATH": "/usr/bin:/bin:/usr/sbin:/sbin", "LC_ALL": "C",
    "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
    "GIT_OPTIONAL_LOCKS": "0",
}


class GuardError(Exception):
    pass


class RunInterrupted(KeyboardInterrupt):
    """Carry a termination signal through the normal child cleanup path."""


def handle_termination(signum, frame):
    raise RunInterrupted(signum)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def utc():
    return datetime.now(timezone.utc).isoformat()


def git(root, *args, stdin=None):
    return subprocess.check_output(
        ["/usr/bin/git", "-C", str(root), *args], env=GIT_ENV, stderr=subprocess.PIPE,
        input=stdin, timeout=30,
    )


def manifest(root):
    tracked = set(git(root, "ls-files", "-z", "--cached").split(b"\0"))
    untracked = set(git(root, "ls-files", "-z", "--others", "--exclude-standard").split(b"\0"))
    entries = []
    for raw in sorted((tracked | untracked) - {b""}):
        relative = os.fsdecode(raw)
        path = root / relative
        if path.is_symlink():
            try:
                path.resolve().relative_to(root)
            except ValueError:
                raise GuardError("Source symlink leaves the checkout: " + relative) from None
            entry = {"path": relative, "symlink": os.readlink(path)}
        elif path.is_file():
            entry = {"path": relative, "sha256": sha(path.read_bytes()),
                     "mode": path.stat().st_mode & 0o777}
        elif not path.exists():
            entry = {"path": relative, "deleted": True}
        else:
            raise GuardError("Unsupported source file: " + relative)
        entry["tracked"] = raw in tracked
        entries.append(entry)
    return entries


def identity(root):
    entries = manifest(root)
    return {
        "head": git(root, "rev-parse", "HEAD").decode().strip(),
        "dirty": bool(git(root, "status", "--porcelain", "--untracked-files=all")),
        "dirty_diff_sha256": sha(git(root, "diff", "--no-ext-diff", "--no-textconv", "--binary", "HEAD")),
        "content_sha256": sha(json.dumps(entries, sort_keys=True, separators=(",", ":")).encode()),
        "source_file_count": len(entries),
    }, entries


def assert_source(root, before):
    current, _ = identity(root)
    if current != before:
        raise GuardError("Source changed during local CI; the candidate cannot qualify")


def yaml_read(path):
    code = "require 'yaml'; require 'json'; puts JSON.generate(YAML.safe_load(File.read(ARGV[0]), aliases: true))"
    result = subprocess.check_output(["/usr/bin/ruby", "-e", code, str(path)],
                                     env=GIT_ENV, timeout=30)
    return json.loads(result)


def plan(root):
    workflow = root / WORKFLOW
    if sha(workflow.read_bytes()) != WORKFLOW_SHA256:
        raise GuardError("Workflow drift: review pages.yml and this adapter together before running")
    data = yaml_read(workflow)
    if set(data["jobs"]) != {"build", "deploy"}:
        raise GuardError("Unknown workflow jobs")
    steps = data["jobs"]["build"]["steps"]
    if [s["name"] for s in steps] != BUILD_STEPS:
        raise GuardError("Unknown or missing build steps")
    result = []
    for i, step in enumerate(steps, 1):
        kind = LOCAL_ACTIONS.get(step["name"], "workflow_shell")
        if kind == "workflow_shell" and not isinstance(step.get("run"), str):
            raise GuardError("Missing CI shell commands")
        result.append({**step, "id": "%02d-%s" % (i, re.sub(r"[^a-z0-9]+", "-", step["name"].lower()).strip("-")),
                       "kind": kind, "status": "not_run"})
    return result


def copy_source(root, destination, entries, head):
    destination.mkdir(mode=0o700)
    for entry in entries:
        if entry.get("deleted"):
            continue
        target = destination / entry["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        if "symlink" in entry:
            target.symlink_to(entry["symlink"])
        else:
            shutil.copy2(root / entry["path"], target)
            if sha(target.read_bytes()) != entry["sha256"]:
                raise GuardError("Source changed while copying: " + entry["path"])
    git(destination, "init", "-q")
    # The receipt evaluators read pinned ancestors. Copy their Git objects without
    # inheriting the source checkout's configuration, hooks or writable refs.
    git(destination, "-c", "protocol.allow=never", "-c", "protocol.file.allow=always",
        "fetch", "--quiet", "--no-tags", "--no-recurse-submodules", str(root), head)
    git(destination, "update-ref", "HEAD", head)
    # Start the new index from exactly the submitted tracked paths. Untracked
    # sources are available to the build and retain their original Git status.
    index_paths = b"".join(os.fsencode(e["path"]) + b"\0" for e in entries
                           if e["tracked"] and not e.get("deleted"))
    git(destination, "update-index", "--add", "-z", "--stdin", stdin=index_paths)
    if git(destination, "write-tree") != git(destination, "rev-parse", "HEAD^{tree}"):
        git(destination, "-c", "user.name=Local CI", "-c", "user.email=local-ci@invalid",
            "-c", "commit.gpgsign=false", "commit", "-q", "-m", "Disposable local CI source snapshot")
    return git(destination, "rev-parse", "HEAD").decode().strip()


def docker_executable():
    if platform.system() != "Darwin" or not Path("/usr/bin/sandbox-exec").is_file():
        raise GuardError("This adapter requires macOS sandbox-exec for the Python checks")
    docker = shutil.which("docker")
    if not docker:
        raise GuardError("Docker must already be installed")
    return docker


def local_docker_host(docker):
    context = os.environ.get("DOCKER_CONTEXT")
    endpoint = os.environ.get("DOCKER_HOST")
    if context or not endpoint:
        command = [docker, "context", "inspect", "--format", '{{(index .Endpoints "docker").Host}}']
        if context:
            command.append(context)
        endpoint = subprocess.check_output(command, text=True, timeout=15).strip()
    if not endpoint.startswith("unix:///"):
        raise GuardError("Local CI requires a Docker context with an absolute Unix socket")
    return endpoint


def clean_env(output, source, head):
    return {
        **GIT_ENV, "PATH": str(Path(sys.executable).parent) + ":" + GIT_ENV["PATH"],
        "CI": "true", "PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1",
        "PYTHONUTF8": "1", "TMPDIR": str(output / "tmp"), "RUNNER_TEMP": str(output / "tmp"),
        "GITHUB_WORKSPACE": str(source), "GITHUB_SHA": head,
        "GITHUB_REPOSITORY": "seabass-up/jev-workflow-patterns",
        "DOCKER_CONFIG": str(output / "docker-config"),
    }


def execute(command, cwd, env, log, timeout=900):
    started = time.monotonic()
    with log.open("xb") as stream:
        log.chmod(0o600)
        child = subprocess.Popen(command, cwd=cwd, env=env, stdout=stream,
                                 stderr=subprocess.STDOUT, start_new_session=True)
        try:
            code = child.wait(timeout=timeout)
        except (subprocess.TimeoutExpired, KeyboardInterrupt):
            os.killpg(child.pid, signal.SIGTERM)
            try:
                child.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(child.pid, signal.SIGKILL)
                child.wait()
            raise
    return {"exit_code": code, "elapsed_seconds": round(time.monotonic() - started, 3),
            "log": str(log), "log_sha256": sha(log.read_bytes()),
            "status": "passed" if code == 0 else "failed"}


def write_private(path, content):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(content)
    temporary.chmod(0o600)
    temporary.replace(path)


def save(output, receipt):
    write_private(output / "receipt.json", json.dumps(receipt, indent=2) + "\n")
    rows = ["# Jev local CI", "", "Result: " + receipt["status"], "",
            "Source HEAD: " + receipt["source"]["head"],
            "Source content SHA-256: " + receipt["source"]["content_sha256"], "",
            "| Step | Result | Seconds |", "| --- | --- | --- |"]
    for step in receipt["steps"]:
        rows.append("| %s | %s | %s |" % (step["name"], step["status"], step.get("elapsed_seconds", "")))
    write_private(output / "summary.md", "\n".join(rows) + "\n")


def run_step(step, command, source, env, output, receipt, timeout=900):
    log = output / "logs" / (step["id"] + ".log")
    step.update(status="running", command=command, log=str(log))
    save(output, receipt)
    step.update(execute(command, source, env, log, timeout))


def finish_error(output, receipt, status, message):
    receipt.update(status=status, error=message, finished_at=utc())
    for step in receipt["steps"]:
        if step["status"] == "running":
            step["status"] = status
            if "log" in step and Path(step["log"]).is_file():
                step["log_sha256"] = sha(Path(step["log"]).read_bytes())
    save(output, receipt)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--run", action="store_true", help="Execute the validated local build plan")
    parser.add_argument("--keep-going", action="store_true", help="Collect subsequent check results after a failed check")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    output = None
    receipt = None
    container_started = False
    container_name = "jev-ci-" + uuid.uuid4().hex
    try:
        steps = plan(root)
        if not args.run:
            print(json.dumps({"status": "plan_validated", "steps": [
                {"name": s["name"], "kind": s["kind"]} for s in steps],
                "deploy": "not_applicable_to_local_build"}, indent=2))
            return 0
        docker = docker_executable()
        before, entries = identity(root)
        output = root / ".work" / "ci-local" / (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8])
        output.mkdir(parents=True, mode=0o700)
        for name in ("tmp", "logs", "docker-config"):
            (output / name).mkdir(mode=0o700)
        source = output / "source"
        env = clean_env(output, source, before["head"])
        receipt = {"schema_version": 2, "started_at": utc(), "status": "running",
                   "source_root": str(root), "source": before,
                   "workflow_sha256": WORKFLOW_SHA256, "runner_sha256": sha(Path(__file__).read_bytes()),
                   "pages_image": PAGES_IMAGE, "provenance": PROVENANCE,
                   "host": {"system": platform.system(), "architecture": platform.machine(),
                            "python": sys.version.split()[0]},
                   "scope": "Native macOS Python checks and an offline Linux amd64 GitHub Pages build.",
                   "deploy": "not_applicable_to_local_build",
                   "limits": ["No hosted runner, Pages account setup, artifact upload or public deployment.",
                              "Tests replay preserved responses; model accuracy and independent domain qualification are not inferred."],
                   "steps": [{"name": "Verify local network denial", "id": "network-guard",
                              "kind": "local_guard", "status": "not_run"}, *steps]}
        save(output, receipt)
        endpoint = local_docker_host(docker)
        docker_command = [docker, "--host", endpoint]
        receipt["docker_host"] = endpoint
        image_id = subprocess.check_output([*docker_command, "image", "inspect", PAGES_IMAGE,
                                            "--format", "{{.Id}}"], env=env, text=True, timeout=30).strip()
        receipt["pages_image_id"] = image_id
        steps[0]["status"] = "running"
        save(output, receipt)
        receipt["snapshot_commit"] = copy_source(root, source, entries, before["head"])
        if not before["dirty"] and receipt["snapshot_commit"] != before["head"]:
            raise GuardError("Clean candidate did not reproduce its exact Git commit")
        assert_source(root, before)
        steps[0]["status"] = "passed"
        sandbox = output / "offline.sb"
        sandbox.write_text(SANDBOX)
        guard = receipt["steps"][0]
        command = ["/usr/bin/sandbox-exec", "-f", str(sandbox), sys.executable, "-c", CANARY]
        run_step(guard, command, source, env, output, receipt, timeout=15)
        save(output, receipt)
        if guard["status"] != "passed":
            raise GuardError("Kernel network-denial canary failed; refusing unchecked execution")
        failed = False
        for step in steps:
            assert_source(root, before)
            kind = step["kind"]
            if kind == "not_applicable_to_local_build":
                step["status"] = kind
            elif kind == "local_snapshot":
                step["status"] = "passed"
                step["note"] = "Verified source files and Git ancestry copied into an isolated repository."
            elif kind == "local_configuration":
                config = yaml_read(source / "_config.yml")
                if config.get("url") != "https://seabass-up.github.io" or config.get("baseurl") != "/jev-workflow-patterns":
                    raise GuardError("Local Pages URL/baseurl differs from the reviewed project configuration")
                step["status"] = "passed"
                step["note"] = "Checked local URL/baseurl; hosted Pages API configuration is outside local CI."
            elif failed and not args.keep_going:
                step["status"] = "not_run_after_failure"
            else:
                if kind == "jekyll_container":
                    container_started = True
                    command = [*docker_command, "run", "--rm", "--pull", "never", "--network", "none",
                               "--platform", "linux/amd64", "--name", container_name,
                               "--mount", "type=bind,src=" + str(source) + ",dst=/workspace",
                               "--workdir", "/workspace", "--entrypoint", "/bin/bash",
                               "-e", "JEKYLL_ENV=production", "-e", "PAGES_REPO_NWO=seabass-up/jev-workflow-patterns",
                               "-e", "JEKYLL_BUILD_REVISION=" + before["head"], image_id,
                               "-c", "exec /usr/local/bundle/bin/github-pages build --source /workspace --destination /workspace/_site"]
                else:
                    command = ["/usr/bin/sandbox-exec", "-f", str(sandbox), "/bin/bash",
                               "--noprofile", "--norc", "-eo", "pipefail", "-c", step["run"]]
                print(step["id"] + " ...", flush=True)
                run_step(step, command, source, {**env, **step.get("env", {})}, output, receipt)
                failed |= step["status"] != "passed"
                print(step["id"] + ": " + step["status"], flush=True)
            save(output, receipt)
        assert_source(root, before)
        receipt["source_unchanged"] = True
        receipt["finished_at"] = utc()
        receipt["status"] = "failed" if failed else "passed"
        if (source / "_site").is_dir():
            site = [{"path": str(p.relative_to(source / "_site")), "sha256": sha(p.read_bytes())}
                    for p in sorted((source / "_site").rglob("*")) if p.is_file()]
            receipt["site_file_count"] = len(site)
            receipt["site_content_sha256"] = sha(json.dumps(site, separators=(",", ":")).encode())
        save(output, receipt)
        print(json.dumps({"status": receipt["status"], "receipt": str(output / "receipt.json")}))
        return 1 if failed else 0
    except KeyboardInterrupt as error:
        signum = error.args[0] if isinstance(error, RunInterrupted) else signal.SIGINT
        message = "Local CI interrupted by " + signal.Signals(signum).name
        if receipt is not None:
            finish_error(output, receipt, "interrupted", message)
        print(message, file=sys.stderr)
        return 128 + signum
    except (GuardError, OSError, subprocess.SubprocessError, ValueError, KeyError) as error:
        if receipt is not None:
            finish_error(output, receipt, "blocked", str(error))
        print("ci-local: " + str(error), file=sys.stderr)
        return 2
    finally:
        if container_started:
            try:
                subprocess.run([*docker_command, "rm", "--force", container_name], env=env,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=15)
            except (OSError, subprocess.SubprocessError) as error:
                print("ci-local: could not confirm container cleanup: " + str(error), file=sys.stderr)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, handle_termination)
    raise SystemExit(main())
