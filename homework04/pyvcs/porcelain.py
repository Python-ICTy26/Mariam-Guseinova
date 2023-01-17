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
    index = read_index(gitdir)
    return commit_tree(gitdir, write_tree(gitdir, index), message, author=author)


def checkout(gitdir: pathlib.Path, obj_name: str) -> None:
    update_ref(gitdir, "HEAD", obj_name)

    hash = commit_parse(read_object(obj_name, gitdir)[1])
    files = find_tree_files(hash, gitdir)

    names = []
    for i in read_index(gitdir):
        names.append(i.name)

    update_index(gitdir, [pathlib.Path(i[1]) for i in files], write=True)

    for j in names:
        first = j.split("/")[0]
        if pathlib.Path(first).is_dir():
            shutil.rmtree(first)
        else:
            if pathlib.Path(first).exists():
                os.remove(first)

    for z in files:
        if "/" in z[1]:
            el = os.path.split(z[1])[0]
            if not pathlib.Path(el).exists():
                os.makedirs(el)
        f = open(z[1], "wb")
        f.write(read_object(z[0], gitdir)[1])

