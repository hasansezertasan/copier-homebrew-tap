# Leave the cobo-managed files to the generated repository

## Context and Problem Statement

The template ships a cobo-rendered `.gitignore` and the `cobo.lock` that tracks it
([cobo](https://github.com/hasansezertasan/cobo)). The generated tap keeps both current
with its own weekly cobo workflow, which rewrites the sealed block and the lockfile.
`copier update` three-way merges template-owned files, so the next change to the template's
copy would conflict with the block cobo rewrote in the repository. `.gitattributes` and
`.editorconfig` are plain files there: the generated `cobo.lock` tracks only `.gitignore`.

## Considered Options

* Keep merging everything on `copier update`: rejected, it conflicts with the cobo-managed
  `.gitignore` and `cobo.lock` as soon as the template's copy changes.
* Also skip `.gitattributes` and `.editorconfig`: rejected, nothing in the generated
  repository updates them, so template fixes would never arrive.
* Seed `.gitignore` and `cobo.lock` once with `_skip_if_exists`, as copier-copier does for
  the cobo files it owns: chosen.

## Decision Outcome

`.gitignore` and `cobo.lock` are listed in `_skip_if_exists`. A new tap gets the
template's copies, which still render byte-for-byte as before; after that they belong to the
repository: `copier update` preserves the files that exist and does not merge template
changes into them. A repository that deletes one gets it reseeded on the next update.
`.gitattributes` and `.editorconfig` stay under Copier's ownership and keep receiving
template changes.

### Consequences

* Good, because cobo's drift pull requests and `copier update` no longer fight over the same
  lines.
* Bad, because changes to the template's `.gitignore` no longer reach existing taps; they
  arrive through cobo's own updates instead.
* If the generated `cobo.lock` ever tracks `.gitattributes` or `.editorconfig`, add them to
  `_skip_if_exists` in the same change.
