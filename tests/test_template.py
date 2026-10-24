import yaml
from conftest import REPO, copier, git

# The tap template has a required question without a default.
ANSWERS = ["--data=tap_owner=example", "--data=copyright_holder=Example"]


def test_template_renders_with_defaults(tmp_path, versioned_template):
    dest = tmp_path / "project"
    result = copier("copy", "--defaults", *ANSWERS, str(versioned_template), str(dest), cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    assert (dest / ".copier-answers.yml").exists()


def test_rendered_gitignore_keeps_the_carriage_return_patterns(tmp_path, versioned_template):
    # Jinja and editors turn a bare carriage return into a newline, which splits
    # `Icon\r` into two lines and drops the pattern.
    dest = tmp_path / "project"
    copier("copy", "--defaults", *ANSWERS, str(versioned_template), str(dest), cwd=tmp_path)
    lines = (dest / ".gitignore").read_bytes().split(b"\n")
    assert b"Icon[\r]" in lines
    assert b".HFS+ Private Directory Data[\r]" in lines


def test_readme_links_back_to_the_template(tmp_path, versioned_template):
    dest = tmp_path / "project"
    copier("copy", "--defaults", *ANSWERS, str(versioned_template), str(dest), cwd=tmp_path)
    assert (dest / "README.md").read_text().rstrip().endswith(
        "## Credits\n\nGenerated from [copier-homebrew-tap](https://github.com/hasansezertasan/copier-homebrew-tap)."
    )


def test_update_to_a_new_version_only_moves_the_answers_commit(tmp_path, versioned_template):
    dest = tmp_path / "project"
    copier("copy", "--defaults", *ANSWERS, str(versioned_template), str(dest), cwd=tmp_path)
    git("init", "-q", "-b", "main", cwd=dest)
    git("add", "-A", cwd=dest)
    git("commit", "-q", "-m", "chore: render", cwd=dest)

    git("commit", "-q", "--allow-empty", "-m", "chore: release", cwd=versioned_template)
    git("tag", "v0.0.1", cwd=versioned_template)

    result = copier("update", "--defaults", "--skip-answered", cwd=dest)
    assert result.returncode == 0, result.stderr
    changed = {line[3:] for line in git("status", "--porcelain", cwd=dest).stdout.splitlines()}
    assert changed == {".copier-answers.yml"}
    answers = yaml.safe_load((dest / ".copier-answers.yml").read_text())
    assert answers["_commit"] == "v0.0.1"


def test_formula_dispatch_reports_a_failed_bump_as_an_issue():
    workflow = yaml.safe_load(
        (REPO / "template/.github/workflows/update-formula-dispatch.yml").read_text()
    )
    job = workflow["jobs"]["update"]
    assert job["permissions"].get("issues") == "write"
    last = job["steps"][-1]
    assert last["if"] == "failure()"
    assert "gh issue create" in last["run"]


# Rendered name -> the template file it comes from.
COBO_MANAGED = {
    ".gitignore": ".gitignore.jinja",
    "cobo.lock": "cobo.lock",
}
# Plain files the generated repository's cobo workflow does not track.
TEMPLATE_OWNED = {".gitattributes": ".gitattributes", ".editorconfig": ".editorconfig"}


def test_update_leaves_cobo_managed_files_alone(tmp_path, versioned_template):
    dest = tmp_path / "project"
    result = copier("copy", "--defaults", *ANSWERS, str(versioned_template), str(dest), cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    for rendered in [*COBO_MANAGED, *TEMPLATE_OWNED]:
        assert (dest / rendered).is_file(), rendered
    git("init", "-q", "-b", "main", cwd=dest)
    git("add", "-A", cwd=dest)
    git("commit", "-q", "-m", "chore: render", cwd=dest)

    for rendered in COBO_MANAGED:
        (dest / rendered).write_text("# cobo-managed\n")
    git("commit", "-q", "-am", "chore: manage boilerplate with cobo", cwd=dest)

    for source in [*COBO_MANAGED.values(), *TEMPLATE_OWNED.values()]:
        path = versioned_template / "template" / source
        path.write_text(path.read_text() + "# added in v0.0.1\n")
    git("commit", "-q", "-am", "feat: extend the boilerplate", cwd=versioned_template)
    git("tag", "v0.0.1", cwd=versioned_template)

    result = copier("update", "--defaults", "--skip-answered", cwd=dest)
    assert result.returncode == 0, result.stderr
    for rendered in COBO_MANAGED:
        assert (dest / rendered).read_text() == "# cobo-managed\n", rendered
    for rendered in TEMPLATE_OWNED:
        assert "# added in v0.0.1" in (dest / rendered).read_text(), rendered
