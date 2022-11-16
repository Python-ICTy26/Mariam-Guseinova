import os
import pathlib
import shutil
import typing as tp

from pyvcs.index import read_index, update_index
from pyvcs.objects import commit_parse, find_object, find_tree_files, read_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref
from pyvcs.tree import commit_tree, write_tree


def add(gitdir: pathlib.Path, paths: tp.List[pathlib.Path]) -> None:
    update_index(gitdir, paths)


def commit(gitdir: pathlib.Path, message: str, author: tp.Optional[str] = None) -> str:
    return commit_tree(gitdir, write_tree(gitdir, read_index(gitdir)), message, author)


def checkout(gitdir: pathlib.Path, obj_name: str) -> None:
    file = gitdir / "refs" / "heads" / obj_name
    if file.exists():
        with open(head, "w") as f:
            obj_name = f.read()
    ind = read_index(gitdir)
    for i in ind:
        if pathlib.Path(i.name).is_file():
            if "/" in i.name:
                index = i.name.find("/")
                shutil.rmtree(i.name[:index])
            else:
                os.remove(i.name)
    path = gitdir / "objects" / obj_name[:2] / obj_name[2:]
    with open(path, "rb") as f1:
        sha = commit_parse(f1.read()).decode()
    for f2 in find_tree_files(sha, gitdir):
        if "/" in f2[0]:
            index = f2[0].find("/")
            dirname = f2[0][:index]
            pathlib.Path(dirname).absolute().mkdir()
        with open(f2[0], "w") as f3:
            f3.write(read_object(f2[1], gitdir)[1].decode())
