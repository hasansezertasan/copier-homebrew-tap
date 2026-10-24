# Leave the cobo-managed boilerplate files to the generated repository

## Context and Problem Statement

The template ships `.gitignore`, `.gitattributes`, `.editorconfig` and `cobo.lock`, rendered
by [cobo](https://github.com/hasansezertasan/cobo). The generated tap keeps them current
with its own weekly cobo workflow, which rewrites the sealed block and `cobo.lock`.
`copier update` three-way merges template-owned files, so the next change to the template's
copy would conflict with the block cobo rewrote in the repository.

## Considered Options

* Keep merging them on `copier update`: rejected, it conflicts with the cobo-managed files as
  soon as the template's copy changes.
* Drop them from the template: rejected, a fresh render would start without the boilerplate
  and without the cobo workflow's lockfile.
* Seed them once with `_skip_if_exists`, as copier-copier does: chosen.

## Decision Outcome

`.gitignore`, `.gitattributes`, `.editorconfig` and `cobo.lock` are listed in
`_skip_if_exists`. A new tap gets the template's copies, which still render byte-for-byte
as before; after that they belong to the repository: `copier update` preserves the files
that exist and does not merge template changes into them. A repository that deletes one gets
it reseeded from the template on the next update.

### Consequences

* Good, because cobo's drift pull requests and `copier update` no longer fight over the same
  lines.
* Bad, because changes to the template's boilerplate no longer reach existing taps; they
  arrive through cobo's own updates instead.
