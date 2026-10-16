# Keep the Update Workflows as Inline Shell

## Context and Problem Statement

The tap has four update workflows (`update-formulas.yml`,
`update-formula-dispatch.yml`, `update-casks.yml`, `update-cask-dispatch.yml`)
of 155 to 202 lines each. The sibling Scoop template moves its update logic into
a tested Python script
([0002](../research/0002-scoop-bucket-template-comparison.md)). Should this
template do the same?

## Considered Options

* Keep the logic as inline shell in each workflow
* Extract a shared, unit-tested Python update script
* Extract only the dispatch payload validation

## Decision Outcome

Chosen option: "Keep inline shell." The workflows are not copies of one another:
formula versus dispatch differ in 287 lines and the cask pair in 248, because the
flows differ (a livecheck loop versus a validated payload, formulae versus
casks). Nearly every line calls `brew`, `jq`, or `gh`, so a script would mostly
mock Homebrew and test the mocks. The Scoop template needs a script only because
Scoop has no `brew bump-formula-pr`.

### Consequences

* Good, because there is no second language or test layer around a Homebrew CLI.
* Good, because each workflow can be read top to bottom.
* Bad, because the formula and cask token validation patterns exist in two
  places each and nothing unit-tests them.
