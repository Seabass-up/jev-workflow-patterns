from contextlib import redirect_stderr, redirect_stdout
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location("ci_local", Path(__file__).with_name("ci-local.py"))
ci = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ci)


def commit(root, message):
    ci.git(root, "-c", "user.name=Test", "-c", "user.email=test@invalid",
           "-c", "commit.gpgsign=false", "commit", "-qm", message)
    return ci.git(root, "rev-parse", "HEAD").decode().strip()


class LocalCIGuards(unittest.TestCase):
    def test_workflow_drift_refuses_new_commands(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            path = root / ci.WORKFLOW
            path.parent.mkdir(parents=True)
            path.write_text("jobs:\n  new-command:\n    run: exit 0\n")
            with self.assertRaisesRegex(ci.GuardError, "Workflow drift"):
                ci.plan(root)

    def test_plan_covers_every_build_step_and_never_deploys(self):
        steps = ci.plan(ci.ROOT)
        self.assertEqual([s["name"] for s in steps], ci.BUILD_STEPS)
        self.assertEqual(sum(s["kind"] == "workflow_shell" for s in steps), 9)
        self.assertEqual(sum(s["kind"] == "jekyll_container" for s in steps), 1)
        self.assertEqual(steps[-1]["kind"], "not_applicable_to_local_build")
        self.assertFalse(any("actions/deploy-pages" in s.get("uses", "") for s in steps))

    def test_changed_source_cannot_qualify(self):
        with patch.object(ci, "identity", return_value=({"head": "changed"}, [])):
            with self.assertRaisesRegex(ci.GuardError, "Source changed"):
                ci.assert_source(Path("."), {"head": "before"})

    def test_copy_binds_untracked_files_and_preserves_source_deletion(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / "original"
            root.mkdir()
            ci.git(root, "init", "-q")
            (root / "kept.txt").write_text("original")
            (root / "deleted.txt").write_text("deleted")
            ci.git(root, "add", "--all")
            head = commit(root, "fixture")
            (root / "deleted.txt").unlink()
            (root / "new.txt").write_text("untracked")
            before, entries = ci.identity(root)
            snapshot = Path(folder) / "snapshot"
            dirty_commit = ci.copy_source(root, snapshot, entries, head)
            self.assertEqual((snapshot / "kept.txt").read_text(), "original")
            self.assertEqual((snapshot / "new.txt").read_text(), "untracked")
            self.assertEqual(ci.git(snapshot, "ls-files", "--", "new.txt"), b"")
            self.assertFalse((snapshot / "deleted.txt").exists())
            self.assertNotEqual(dirty_commit, head)
            self.assertEqual(ci.git(snapshot, "rev-parse", "HEAD^").decode().strip(), head)
            self.assertEqual(ci.git(snapshot, "show", head + ":deleted.txt"), b"deleted")
            ci.assert_source(root, before)

    def test_clean_copy_keeps_exact_commit_and_ancestor_blobs(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / "original"
            root.mkdir()
            ci.git(root, "init", "-q")
            path = root / "catalog.json"
            path.write_text("original")
            ci.git(root, "add", "catalog.json")
            parent = commit(root, "first catalog")
            path.write_text("revised")
            ci.git(root, "add", "catalog.json")
            head = commit(root, "revision")
            snapshot = Path(folder) / "copy"
            self.assertEqual(ci.copy_source(root, snapshot, ci.manifest(root), head), head)
            self.assertEqual(ci.git(snapshot, "show", parent + ":catalog.json"), b"original")
            self.assertEqual(ci.git(snapshot, "status", "--porcelain"), b"")

    def test_generated_check_rejects_a_missing_submitted_output(self):
        step = next(s for s in ci.plan(ci.ROOT) if s["name"] == "Verify generated catalog and collection hub")
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / "original"
            root.mkdir()
            ci.git(root, "init", "-q")
            outputs = ["_data/catalog_summary.json", "catalog/index.md", "collections/index.md"]
            for name in outputs:
                path = root / name
                path.parent.mkdir()
                path.write_text("generated")
            (root / "scripts").mkdir()
            (root / "scripts/build_catalog.py").write_text(
                "from pathlib import Path\nPath('_data/catalog_summary.json').write_text('generated')\n")
            (root / "scripts/build_collection_pages.py").touch()
            ci.git(root, "add", "--all")
            commit(root, "initial outputs")
            command = ["/bin/bash", "-eo", "pipefail", "-c", step["run"]]
            self.assertEqual(subprocess.run(command, cwd=root, capture_output=True).returncode, 0)
            ci.git(root, "rm", outputs[0])
            commit(root, "omit one output")
            self.assertNotEqual(subprocess.run(command, cwd=root, capture_output=True).returncode, 0)
            (root / outputs[0]).parent.mkdir(exist_ok=True)
            (root / outputs[0]).write_text("generated")
            self.assertNotEqual(subprocess.run(command, cwd=root, capture_output=True).returncode, 0)
            snapshot = Path(folder) / "copy"
            head = ci.git(root, "rev-parse", "HEAD").decode().strip()
            ci.copy_source(root, snapshot, ci.manifest(root), head)
            self.assertTrue((snapshot / outputs[0]).is_file())
            self.assertNotEqual(subprocess.run(command, cwd=snapshot, capture_output=True).returncode, 0)

    def test_failed_child_is_recorded_as_failure(self):
        with tempfile.TemporaryDirectory() as folder:
            log = Path(folder) / "failed.log"
            result = ci.execute([sys.executable, "-c", "raise SystemExit(7)"],
                                Path(folder), ci.GIT_ENV, log, 15)
            self.assertEqual(result["status"], "failed")
            self.assertEqual(result["exit_code"], 7)
            self.assertEqual(result["log_sha256"], hashlib.sha256(log.read_bytes()).hexdigest())

    def test_environment_does_not_inherit_credentials_or_python_overrides(self):
        with patch.dict(os.environ, {"GITHUB_TOKEN": "test-secret", "PYTHONPATH": "foreign",
                                     "TYPESAFE_API_KEY": "test-key"}):
            env = ci.clean_env(Path("/tmp/ci"), Path("/tmp/source"), "head")
        for key in ("GITHUB_TOKEN", "TYPESAFE_API_KEY", "PYTHONPATH", "HOME", "CODEX_HOME"):
            self.assertNotIn(key, env)
        self.assertEqual(env["PYTHONNOUSERSITE"], "1")

    def test_child_timeout_is_not_a_pass(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(subprocess.TimeoutExpired):
                ci.execute([sys.executable, "-c", "import time; time.sleep(60)"],
                           Path(folder), ci.GIT_ENV, Path(folder) / "timeout.log", 0.05)

    def test_named_context_takes_precedence_and_remote_context_is_rejected(self):
        with patch.dict(os.environ, {"DOCKER_CONTEXT": "review", "DOCKER_HOST": "unix:///other.sock"}):
            with patch.object(subprocess, "check_output", return_value="unix:///review.sock\n") as lookup:
                self.assertEqual(ci.local_docker_host("docker"), "unix:///review.sock")
                self.assertEqual(lookup.call_args.args[0][-1], "review")
            with patch.object(subprocess, "check_output", return_value="ssh://remote\n"):
                with self.assertRaisesRegex(ci.GuardError, "Unix socket"):
                    ci.local_docker_host("docker")

    def run_with_fake_docker(self, interruption=None):
        endpoint = "unix:///tmp/review-docker.sock"
        docker = "/test/docker"
        calls = []
        real_run = subprocess.run

        def run(command, **options):
            if command[0] != docker:
                return real_run(command, **options)
            calls.append((command[:4], options["env"]["DOCKER_CONFIG"]))
            return subprocess.CompletedProcess(command, 0, stdout="sha256:test\n")

        def execute(command, cwd, env, log, timeout):
            log.write_text("test output\n")
            if command[0] == docker:
                calls.append((command[:4], env["DOCKER_CONFIG"]))
                if interruption:
                    raise interruption
            return {"status": "passed", "exit_code": 0}

        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            ci.git(root, "init", "-q")
            (root / ".gitignore").write_text(".work/\n")
            workflow = root / ci.WORKFLOW
            workflow.parent.mkdir(parents=True)
            workflow.write_bytes((ci.ROOT / ci.WORKFLOW).read_bytes())
            (root / "_config.yml").write_text("url: https://seabass-up.github.io\nbaseurl: /jev-workflow-patterns\n")
            ci.git(root, "add", "--all")
            commit(root, "fixture")
            with patch.dict(os.environ, {"DOCKER_HOST": endpoint, "DOCKER_CONTEXT": ""}), \
                    patch.object(ci, "docker_executable", return_value=docker), \
                    patch.object(subprocess, "run", side_effect=run), \
                    patch.object(ci, "execute", side_effect=execute), \
                    redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                code = ci.main(["--root", str(root), "--run"])
            receipt = json.loads(next(root.glob(".work/ci-local/*/receipt.json")).read_bytes())
            self.assertEqual(receipt["docker_host"], endpoint)
            self.assertEqual([args for args, _ in calls],
                             [[docker, "--host", endpoint, op] for op in ("image", "run", "rm")])
            self.assertEqual(len({config for _, config in calls}), 1)
            return code, receipt

    def test_inspect_build_and_cleanup_share_one_explicit_endpoint(self):
        code, receipt = self.run_with_fake_docker()
        self.assertEqual((code, receipt["status"]), (0, "passed"))
        self.assertEqual(receipt["snapshot_commit"], receipt["source"]["head"])

    def test_interrupt_preserves_terminal_receipt_and_partial_log(self):
        for interruption, expected in [(KeyboardInterrupt(), 130), (ci.RunInterrupted(signal.SIGTERM), 143)]:
            with self.subTest(exit_code=expected):
                code, receipt = self.run_with_fake_docker(interruption)
                self.assertEqual((code, receipt["status"]), (expected, "interrupted"))
                self.assertIn("finished_at", receipt)
                build = next(s for s in receipt["steps"] if s["kind"] == "jekyll_container")
                self.assertEqual(build["status"], "interrupted")
                self.assertEqual(build["log_sha256"], hashlib.sha256(b"test output\n").hexdigest())


if __name__ == "__main__":
    unittest.main()
