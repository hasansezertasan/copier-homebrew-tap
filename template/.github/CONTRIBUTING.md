# Contributing

Add one formula or cask per pull request. Use a concise Conventional Commit title,
such as `feat: add example formula` or `chore(example): update to 1.2.3`.

Before opening a pull request:

1. Generate the Ruby file with the appropriate script in `scripts/`.
2. Review inferred metadata, system dependencies, artifact names, and smoke tests.
3. Run the relevant Homebrew audit and install/test checks.
4. Run `mise run generate-readme`.
5. Run `mise install` and `mise run check`.

Include the commands and results in the pull request's verification section.

## Automated pull requests

The update and boilerplate-drift workflows open pull requests with the repository
secret `WORKFLOW_TOKEN` if present, falling back to `GITHUB_TOKEN`. GitHub does
not start workflows for actions performed by `GITHUB_TOKEN`, so maintainers close
and reopen such a pull request (or push to its branch) to run `tests.yml` and the
other checks, or configure `WORKFLOW_TOKEN` to start them automatically.
