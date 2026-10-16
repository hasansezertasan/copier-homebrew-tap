# Keep Agent Skills in a Separate Repository

Supersedes [ADR-0002](0002-lock-project-skills.md).

## Context and Problem Statement

The template shipped its own agent skill (`homebrew-add`) and a lockfile for the
skills its maintainers use, so a generated tap inherited both. Once the
repository became a Copier template, skills for operating a tap no longer belong
in the files a tap renders, and the scaffolders they drive need to be versioned
with the skills rather than copied into every tap.

## Considered Options

* Keep the skill and the scaffolders in the template
* Move them to a separate skills repository that also installs as an agent
  plugin, and stop locking maintainer skills in this repository
* Keep the lockfile for maintainer skills and move only the tap skills

## Decision Outcome

Chosen option: "Move them to a separate skills repository", because
[`homebrew-tap-skills`](https://github.com/hasansezertasan/homebrew-tap-skills)
mirrors `scoop-bucket-skills`, versions the skills and scaffolders together, and
keeps generated taps free of agent tooling. The template's `AGENTS.md` points at
it. `skills-lock.json` and the first-party skill are removed from this
repository; maintainers install the skills they use themselves.

### Consequences

* Good, because a tap carries no skill files or lockfile and `copier update`
  never touches them.
* Good, because the scaffolders are tested and released with the skills that
  drive them.
* Bad, because the template's documented workflow depends on a second
  repository being installed.
* Bad, because maintainer skills for writing these records are no longer
  declared or hash-recorded in this repository.

## Related Research

* [Tap tooling survey](../research/0001-tap-tooling-survey.md)
