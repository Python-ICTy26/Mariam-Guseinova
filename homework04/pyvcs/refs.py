import pathlib
import typing as tp


def update_ref(gitdir: pathlib.Path, ref: tp.Union[str, pathlib.Path], new_value: str) -> None:
    with open(gitdir / pathlib.Path(ref), "w") as file:
        file.write(new_value)


def symbolic_ref(gitdir: pathlib.Path, name: str, ref: str) -> None:
    if ref_resolve(gitdir, ref):
        with open(gitdir / name, "w") as file:
            file.write(f"ref: {ref}")


def ref_resolve(gitdir: pathlib.Path, refname: str) -> str:
    if refname == "HEAD":
        refname = get_ref(gitdir)
    path = gitdir / refname
    if path.exists():
        with open(path, "r") as file:
            return file.read()
    else:
        return refname


def resolve_head(gitdir: pathlib.Path) -> tp.Optional[str]:
    if gitdir / get_ref(gitdir).exists():
        return ref_resolve(gitdir, "HEAD")
    else:
        return None


def is_detached(gitdir: pathlib.Path) -> bool:
    with open(gitdir / "HEAD", "r") as file:
        content = str(file.read())
    return "ref" not in content


def get_ref(gitdir: pathlib.Path) -> str:
    with open(gitdir / "HEAD", "r") as file:
        return file.read()[file.read().find(" ") + 1 :]
