# Optional WORKFLOW_TOKEN for Automated Pull Requests

## Context and Problem Statement

The update workflows and the boilerplate-drift workflow open pull requests with
`GITHUB_TOKEN`. GitHub does not start workflows for actions that token performs,
so those pull requests do not run `tests.yml` (the bottle build) or the other
checks until a maintainer closes and reopens them
([ADR-0004](0004-bump-in-the-tap-not-the-producer.md)). The sibling Scoop
template lets a repository secret replace the token
([research 0002](../research/0002-scoop-bucket-template-comparison.md)).

## Considered Options

* Keep `GITHUB_TOKEN` only and close and reopen each pull request
* Use `secrets.WORKFLOW_TOKEN || secrets.GITHUB_TOKEN`, so the secret is optional
* Require a GitHub App or personal access token

## Decision Outcome

Chosen option: "Optional `WORKFLOW_TOKEN`." Every `create-pull-request` step, and
the Cobo action, takes `secrets.WORKFLOW_TOKEN || secrets.GITHUB_TOKEN`. With the
secret unset nothing changes, so a tap works out of the box. The documentation
recommends a fine-grained token scoped to the tap, with **Contents: write** and
**Pull requests: write**, or an App token. The failure-issue step in the cask
dispatch workflow keeps `GITHUB_TOKEN`.

### Consequences

* Good, because a tap that sets the secret gets bottle builds and checks on every
  automated pull request without a manual step.
* Good, because the secret is optional and the template stays owner-agnostic.
* Bad, because the secret is a long-lived credential with write scope that
  someone must rotate.
* Bad, because dispatch payloads are attacker-influenced, and a pull request
  opened with the secret triggers workflows under that identity. The receivers'
  payload validation and `zizmor.yml` remain the guard.
