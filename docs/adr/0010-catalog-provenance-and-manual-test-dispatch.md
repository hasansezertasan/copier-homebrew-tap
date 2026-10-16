# Catalog Provenance and Manual Test Dispatch from the Scoop Comparison

## Context and Problem Statement

The file-by-file comparison with the sibling Scoop template
([research 0002](../research/0002-scoop-bucket-template-comparison.md),
follow-up in [research 0003](../research/0003-docs-sync-from-scoop-comparison.md))
left three portable gaps on our side: the generated package table names no
upstream provenance, the generator script misses small robustness polish, and
there is no manual way to run `tests.yml` on a pull request GitHub suppressed.

## Considered Options

* Package table: add a `Source` column derived from the package type
  (formulae build from PyPI, casks install from GitHub releases) vs. parsing
  each Ruby file's `url` stanza to classify the host.
* Generator: keep bare `read_text()`/`write_text()` and stdout notices vs.
  explicit UTF-8, stderr for `--check`, and the `mise run generate-readme`
  hint.
* Suppressed checks: keep close-and-reopen only vs. adding a
  `workflow_dispatch` trigger so maintainers can run `Tests` on the update
  branch.

## Decision Outcome

Chosen option: adopt all three, fitted to the tap.

* `Source` is type-derived, not URL-derived: the tap's documented routes are
  already "PyPI formulae, GitHub release casks," so parsing `url` hosts would
  add failure modes for no extra truth. Formulae rows also carry a `PyPI`
  project link; cask rows link through the existing homepage cell.
* The generator uses `encoding="utf-8"` everywhere, reports the `--check`
  up-to-date notice on stderr, and points at `mise run generate-readme`
  (the pinned interpreter) instead of a raw `python` invocation.
* `tests.yml` gains `workflow_dispatch`, and CONTRIBUTING plus the generated
  README document it. The bottle job stays pull-request-gated: its
  changed-formulae detection reads the pull request file list, which does not
  exist on a dispatch event. A manual run covers tap-syntax and cask audit;
  the bottle build runs once pull request checks start.

### Consequences

* Good, because the catalog now shows where each package comes from without a
  second lookup.
* Good, because maintainers get a one-click fallback for suppressed checks
  instead of a close-and-reopen dance.
* Bad, because a manual dispatch still does not build bottles, so the
  documentation must keep that caveat next to the new pointer.
