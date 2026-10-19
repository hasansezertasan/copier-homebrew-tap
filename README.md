# copier-homebrew-tap

A [Copier](https://copier.readthedocs.io) template for a [Homebrew](https://brew.sh)
tap that publishes Python command-line tools as formulae and macOS applications
as casks. A generated tap includes scheduled and release-triggered updates,
bottle publishing, and a generated package catalog. Formulae and casks are
scaffolded by the `homebrew-add` skill in
[`homebrew-tap-skills`](https://github.com/hasansezertasan/homebrew-tap-skills).

## For agents

Your agent is the interface. Copy this prompt into your coding agent:

```text
Install the homebrew-tap-skills skills in project scope: pick the best
installation method for you from https://github.com/hasansezertasan/homebrew-tap-skills/blob/main/docs/installation.md

Then use its homebrew-tap-setup skill to set up a Homebrew tap from
https://github.com/hasansezertasan/copier-homebrew-tap. Inspect the current
directory first, then ask me whether to adopt it or create a new directory named
homebrew-tap. Ask me for what you can't read from the repository (my GitHub
owner, and for a new tap its purpose and the first package), and ask before you
create a repository, change settings or secrets, or push.
```

The prompt points the agent at the
[installation page](https://github.com/hasansezertasan/homebrew-tap-skills/blob/main/docs/installation.md),
which lists the install routes (Claude Code or Codex plugin, a skills installer,
or a manual clone) and tells the agent how to choose and confirm one. The
Claude Code and Codex plugin routes each have one recorded installation on
macOS; the skills installer route has none.

## For humans

### Create a tap

```sh
uvx copier copy gh:hasansezertasan/copier-homebrew-tap homebrew-tap
cd homebrew-tap
git init && git remote add origin https://github.com/<owner>/homebrew-tap
mise install
```

The generated `README.md` lists the remaining setup (Actions permissions, the
first formula or cask). Add formulae and casks with the `homebrew-add` skill
from `homebrew-tap-skills`, which you can also run directly (see the generated
README).

### Adopt an existing tap

To bring a tap that was not rendered from this template under it, render over
the existing checkout from a clean working tree, then review the diff and revert
what you want to keep:

```sh
uvx copier copy gh:hasansezertasan/copier-homebrew-tap . --overwrite
git diff
```

`--overwrite` replaces files without asking. The template renders `README.md`,
`AGENTS.md`, `LICENSE`, the workflows, `scripts/` and `tests/`, so expect to
revert or merge your own versions of them, and keep your existing formulae and
casks. Regenerate the README catalog with `python3 scripts/gen_readme_packages.py`,
and commit `.copier-answers.yml` so `copier update` can merge later template
changes.

### Naming

Homebrew requires a third-party tap repository to be named `homebrew-<tap>`:
`brew tap <owner>/<tap>` resolves to `<owner>/homebrew-<tap>`, and `homebrew-tap`
is the usual choice. The template asks for the tap name as `tap_name` (the part
after `homebrew-`) and defaults it to the directory name with that prefix
stripped.

### Update a tap

Pull later template changes into a tap with:

```sh
uvx copier update
```

## Layout

| Path | Role |
|---|---|
| `copier.yml` | questions and Copier settings |
| `template/` | files rendered into a tap; `*.jinja` files are templated, the rest are copied verbatim |
| `.github/workflows/template.yml` | renders the template and runs the tap's `mise run check` |
| `.github/workflows/release.yml` | versions the template with release-please |
| `docs/` | research notes and MADR decision records behind the template's design; paths inside them are relative to a generated tap, not to this repository |

`template/.gitignore.jinja` is the Cobo-managed `.gitignore` stored under a
`.jinja` name so it does not ignore files inside `template/`. It contains no
Jinja syntax and must render byte-for-byte identical (`cobo check --strict` in
the rendered tap verifies this).

## Releases

The template is versioned with [release-please](https://github.com/googleapis/release-please).
Conventional Commits merged to `main` open a release PR; merging it tags the
commit `vX.Y.Z` and creates a GitHub Release with the changelog. Generated taps
record the tag in `.copier-answers.yml`, and `copier update` walks these tags.
Until 1.0, breaking changes and features bump the minor version and fixes bump
the patch. The first release, `v0.1.0`, is the first Copier version; history
before the conversion is not part of the changelog.

Pin a version when generating a tap:

```sh
uvx copier copy --vcs-ref v0.1.0 gh:hasansezertasan/copier-homebrew-tap homebrew-tap
```

The release PR is opened with the workflow's `GITHUB_TOKEN`, so its checks do not
start by themselves; run the **Template** workflow on the release branch from the
Actions tab if you want them before merging.

## License

MIT. See `LICENSE`.
