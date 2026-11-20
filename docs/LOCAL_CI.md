# Local CI

Run the Pages workflow's build checks locally:

    python3 scripts/ci-local.py
    python3 -m unittest discover -s scripts -p 'test_ci_local.py' -v
    python3 scripts/ci-local.py --run --keep-going

The first command validates and lists the plan. The final command runs all checks
and records each failure while continuing to collect the other results.
Exit 0 means all local checks passed, 1 means a check failed, and 2 means
configuration, source drift or a prerequisite blocked qualification.
An interrupted run records the active step, its available log and a finish time.
SIGINT exits with 130 and SIGTERM exits with 143.

## Correspondence with Claude's runner

This Jev adapter follows Claude's Seabass local CI design: a workflow drift guard,
the workflow's actual shell commands, per-step logs and source-bound receipts.
The original reference was Seabass commit 873629b and runner SHA-256
f071762556cd50e377f7ae6c1469259a8eb470cf3b6eaec800602877f0c958cf.
Its fixed Rust/Postgres project and matrix cannot execute this repository.
This independent adapter leaves that original runner unchanged.

The adapter pins the full reviewed pages.yml SHA-256 and accounts for all 13
build steps. It runs all nine shell steps directly from the workflow with
bash -eo pipefail, then uses the official GitHub Pages build image for Jekyll.
Checkout is represented by a content-verified local snapshot. Local URL/baseurl
configuration replaces hosted Pages setup. Artifact upload and the deployment
job do not apply to local CI and are explicitly recorded.

## Dependencies and execution

Python3, macOS Ruby, sandbox-exec and Docker must already be available.
The native Python checks deny all networking with a mandatory kernel canary.
Jekyll runs as Linux amd64 with Docker networking disabled. Its image is pinned:

    ghcr.io/actions/jekyll-build-pages@sha256:6791ebfd912185ed59bfb5fb102664fa872496b79f87ff8b9cfba292a7345041

This is the image used by actions/jekyll-build-pages v1.0.13, with Ruby 3.3.4
and github-pages 232. A one-time preparation can download it:

    docker pull --platform linux/amd64 ghcr.io/actions/jekyll-build-pages:v1.0.13

The runner uses the locally cached image and installed dependencies. An explicit
`DOCKER_CONTEXT` selects the endpoint first, followed by `DOCKER_HOST` and the
active Docker context. Image inspection, the build and cleanup all use the
resolved local Unix socket and the same isolated Docker configuration. The
receipt records the endpoint. Child processes receive a fixed environment.
Image provenance is documented by the [official action](https://github.com/actions/jekyll-build-pages/blob/v1/action.yml).

## Source preservation and receipts

Each run lives under ignored .work/ci-local/. Its source snapshot includes tracked
and nonignored untracked files and preserves existing deletions. Generated
catalog changes and the Jekyll site stay in that snapshot. The original source
content, Git HEAD and dirty diff are checked before each step and after the run.
The snapshot fetches the submitted HEAD and its reachable history from the
local repository. Old receipt validators can read their pinned Git objects. A
clean checkout keeps the submitted commit as its snapshot commit. If tracked
files differ, the runner records them in a disposable child commit. Untracked
files stay available on disk with their original tracking status. Version 2
source digests include each path's Git membership. The Pages
workflow also checks out full history. Before regeneration it checks that each
required catalog output is present and tracked, then compares the results to
the submitted baseline.

receipt.json and summary.md record the original source identity, dirty state,
workflow/runner/image hashes, commands, individual exits, timings, log hashes and
site-file count and aggregate digest. Log and receipt files have mode 0600. Existing source changes
are included in the tested candidate and are never represented as a clean commit.

A local pass covers the recorded Python replay/tests, generated-file consistency
and rendered site pages. It does not cover hosted-runner permissions, account
configuration, uploads, public deployment, live Jev performance or specialist
qualification. Workflow changes require a reviewed adapter update; changing only
the hash to evade a drift refusal is not a qualification.
