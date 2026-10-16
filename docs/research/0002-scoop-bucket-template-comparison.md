# Comparison with copier-scoop-bucket

Research snapshot: 2026-10-16, against
[hasansezertasan/copier-scoop-bucket](https://github.com/hasansezertasan/copier-scoop-bucket)
at `052992b`. Claims below come from cloning it and diffing it against this
repository file by file.

## Goal

Find what the sibling Copier template for a Scoop bucket does better, and decide
which differences are real platform differences and which are drift.

## Findings

### Most differences are platform differences

The Scoop template ships `update_manifests.py`, `url_fetch.py`, `noop.ps1`, and
`readme.yml` because Scoop has no update tooling: it must fetch URLs, compute
hashes, and rewrite JSON itself. A tap uses `brew livecheck` and
`brew bump-formula-pr`, `scripts.yml` already guards the catalog on README
edits, and `Formula/` and `Casks/` keep their directories with a `README.md`.
None of these needs a counterpart.

### Four things were drift worth fixing

- The Scoop `mise.toml` pins every tool and moves Cobo into `[tools]`, so
  Renovate can bump them; ours used `latest` and an inline `uvx cobo==0.5.0`.
- Its README gives agents a copy-paste setup prompt; ours had two sentences.
- Its `AGENTS.md` has a Layout section and explains each write scope.
- Its Cobo drift workflow opens a pull request instead of only reporting.

### Two options were weighed and not taken

- An update script. The four update workflows are not duplicated: the formula
  and dispatch workflows differ in 287 lines, the cask pair in 248, and almost
  every line is a `brew`, `jq`, or `gh` call. See
  [ADR-0008](../adr/0008-keep-the-update-workflows-as-inline-shell.md).
- A `WORKFLOW_TOKEN` secret so update pull requests start CI. It adds a
  long-lived credential and widens the blast radius of an attacker-influenced
  dispatch payload, to save closing and reopening a pull request. Deferred, not
  rejected.

## Result

The pins, README prompt, `AGENTS.md` layout, and the drift-sync pull request were
adopted; see [ADR-0007](../adr/0007-open-a-pull-request-for-boilerplate-drift.md).
