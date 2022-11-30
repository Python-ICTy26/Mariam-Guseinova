import os
import pathlib
import typing as tp


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    gitdir = os.getenv("GIT_DIR", ".git")
    current = pathlib.Path(workdir)
    path = current / gitdir
    if path.exists():
        return path
    for dirr in path.parents:
        if dirr.name == gitdir:
            return dirr
    raise Exception("Not a git repository")


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    current = pathlib.Path(workdir)
    if not current.is_dir():
        raise Exception(f"{current.name} is not a directory")
    gitdir = os.getenv("GIT_DIR", ".git")
    os.makedirs(current / gitdir / "refs" / "heads")
    os.makedirs(current / gitdir / "refs" / "tags")
    os.makedirs(current / gitdir / "objects")

    (current / gitdir / "HEAD").write_text("ref: refs/heads/master\n")
    (current / gitdir / "config").write_text(
        "[core]\n\trepositoryformatversion = 0\n\tfilemode = true"
        "\n\tbare = false\n\tlogallrefupdates = false\n"
    )
    (current / gitdir / "description").write_text("Unnamed pyvcs repository.\n")
    return current / gitdir
