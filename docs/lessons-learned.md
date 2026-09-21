# Lessons learned

## 2026-09-21 — GitHub Pages workflow runtime compatibility

- **Component:** `.github/workflows/pages.yml`.
- **Symptom:** The first successful Pages deployment carried Node.js 20 deprecation warnings even though its build and deploy jobs passed.
- **Confirmed cause:** The workflow used older major releases of the checkout, configure-pages, upload-pages-artifact, and deploy-pages actions. The composite upload action also bundled an older Node 20 upload-artifact runtime.
- **Repair:** Updated to `actions/checkout@v7`, `actions/configure-pages@v6`, `actions/upload-pages-artifact@v5`, and `actions/deploy-pages@v5`. Kept deployment restricted to the `main` branch and kept build/deploy permissions scoped to their jobs.
- **Verification:** GitHub Actions run [35657662378](https://github.com/Seabass-up/jev-workflow-patterns/actions/runs/35657662378) completed both build and deploy successfully for commit `e89ec7e82906b3bc077c339040f7f3c9667b280b`. The Node.js 20 warnings disappeared. The index and all three pattern URLs, plus all three raw skill files, returned HTTP 200. GitHub still reports that `ubuntu-latest` is scheduled to move to Ubuntu 26 on October 19, 2026; this is a future runner-image notice, not a current build failure.
- **Prevention:** When a successful workflow emits runtime warnings, inspect both direct actions and composite-action dependencies, update to supported majors, then verify a real build, deployment, and served output. Do not suppress an obsolete runtime warning as a substitute for upgrading.
