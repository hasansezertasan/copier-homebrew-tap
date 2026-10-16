# Render Identity with Copier and Resolve the Tap Name at Runtime

Supersedes [ADR-0003](0003-derive-the-tap-name-at-runtime.md).

## Context and Problem Statement

[ADR-0003](0003-derive-the-tap-name-at-runtime.md) chose runtime resolution of
`owner/tap` so the repository worked through GitHub's *Use this template* button
with no edits, and rejected generating the repository from a Copier template.
The repository is now a Copier template, because a template repository cannot
pull later changes into the taps made from it, and `copier update` can.

## Considered Options

* Keep runtime resolution only, and render nothing from answers
* Interpolate the tap name into scripts and workflows at render time
* Render identity only where a person reads it (`README.md`, `LICENSE`), and
  keep resolving the tap name at runtime everywhere else

## Decision Outcome

Chosen option: "Render identity only where a person reads it", because the
workflows keep deriving `owner/tap` from `GITHUB_REPOSITORY_OWNER` and
`GITHUB_REPOSITORY`, so a rename or transfer still needs no follow-up commit,
and `copier update` has no scripts or workflows with interpolated names to
conflict on. `README.md` and `LICENSE` are rendered from the `tap_*` and
`copyright_*` answers.

The local resolver `scripts/tap_name.py`, with its `HOMEBREW_TAP` override and
tests, moved with the scaffolders into
[`homebrew-tap-skills`](https://github.com/hasansezertasan/homebrew-tap-skills)
(see [ADR-0005](0005-keep-agent-skills-in-a-separate-repository.md)), since the
scaffolders are its only consumers.

### Consequences

* Good, because a generated tap needs no edits to its scripts or workflows, and
  it can pull template changes with `copier update`.
* Good, because the same Actions-context resolution still serves CI.
* Bad, because the repository is no longer usable through *Use this template*;
  a tap is created with `copier copy`.
* Bad, because the README's install snippet is rendered from answers and can
  drift if the repository is renamed later.

## Related Research

* [Tap tooling survey](../research/0001-tap-tooling-survey.md)
