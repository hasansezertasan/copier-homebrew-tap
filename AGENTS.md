# Repository instructions

This is a Copier template for a third-party Homebrew tap. The files rendered
into a tap live under `template/`; `copier.yml` holds the questions. Nothing in
the scripts or workflows hardcodes an owner or repository name: the workflows
resolve `owner/tap` from the Actions context, so keep new code owner-agnostic.
Only `README.md` and `LICENSE` are rendered from answers.

`template/.gitignore.jinja` is the Cobo-managed `.gitignore` stored under a
`.jinja` name so it does not ignore files inside `template/`. It must render
byte-for-byte identical; `cobo check --strict` in the rendered tap verifies it.

Skills for operating a generated tap live in
[`homebrew-tap-skills`](https://github.com/hasansezertasan/homebrew-tap-skills),
not here. Persist research notes in `docs/research/` and decisions as MADR
records in `docs/adr/`. Give both sequential four-digit filename prefixes, link
each ADR to its related research when present, and commit them with the related
work.

Before opening a pull request, render the template and run the generated tap's
checks (`.github/workflows/template.yml` does the same):

```sh
uvx copier copy --defaults --vcs-ref=HEAD -d tap_name=demo -d tap_owner=example \
  -d copyright_holder=Example . /tmp/homebrew-demo
cd /tmp/homebrew-demo && git init -q && git remote add origin https://github.com/example/homebrew-demo
git add -A && mise install && mise run check
```
