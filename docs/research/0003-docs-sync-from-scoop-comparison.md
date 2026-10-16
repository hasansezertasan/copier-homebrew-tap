# Docs sync from the scoop-bucket comparison

Research snapshot: 2026-10-16, follow-up to
[0002-scoop-bucket-template-comparison](0002-scoop-bucket-template-comparison.md),
against
[hasansezertasan/copier-scoop-bucket](https://github.com/hasansezertasan/copier-scoop-bucket)
at `052992b`. File-by-file diff, documentation and README content only;
auto-generated files (`CHANGELOG.md`) and platform-specific files excluded.

## Findings applied here

- Both root `README.md` files claimed no skills install route had a recorded
  successful installation. Both skills repos' `docs/installation.md` now record
  one installation each for the Claude Code and Codex plugin routes on macOS,
  so the sentence was stale on both sides. Adopted the route list
  (Claude Code or Codex plugin, skills installer, manual clone) with the
  recorded-installation status, mirroring the scoop wording.
- Adopted the scoop "run directly" pointer for the scaffolder skill, the
  skills-as-plugin note, the operation verbs
  (adding, fixing, triaging, removing, verifying), and the explicit
  `mise install` setup step plus a formula/cask type primer in the generated
  README.
- Fixed a stale `CONTRIBUTING.md` step that pointed at `scripts/` for
  scaffolding; the Ruby files come from the `homebrew-add` scaffolder
  (see [ADR-0005](../adr/0005-keep-agent-skills-in-a-separate-repository.md)),
  and "smoke tests" was Scoop terminology for Homebrew `test` blocks.
- Added explicit `unittest` / `gen_readme_packages.py --check` checkboxes to
  the pull request template, matching the scoop template.

## Deliberately not adopted

- `blank_issues_enabled: true` (scoop) stays `false` here; issue policy, not drift.
- `*.bak-okf-*` in the scoop root `.gitignore`; origin unknown, not ported.
- Python pin / `run_windows` style block and `shellcheck`: Windows-targeted
  toolchain, no tap equivalent.
- Owner-identity via Git remote / env override: the tap resolves `owner/tap`
  from the Actions context only
  (see [ADR-0003](../adr/0003-derive-the-tap-name-at-runtime.md)).
