import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

from pyvcs.refs import update_ref
from pyvcs.repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    store = f"{fmt} {len(data)}\0".encode() + data
    hashh = hashlib.sha1(store).hexdigest()
    if write:
        path = repo_find() / "objects" / hashh[:2]
        if not path.exists():
            path.mkdir(parents=True)
        file = path / hashh[2:]
        if not file.exists():
            file.write_bytes(zlib.compress(store))
    return hashh


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    if len(obj_name) < 4 or len(obj_name) > 40:
        raise Exception(f"Not a valid object name {obj_name}")
    objects = []
    paths = gitdir / "objects" / obj_name[:2]
    for path in paths.iterdir():
        if not path.name.find(obj_name[2:]):
            objects.append(obj_name[:2] + path.name)
    if len(objects):
        return objects
    else:
        raise Exception(f"Not a valid object name {obj_name}")


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    if obj_name[2:] in str(gitdir.name):
        return f"{obj_name[:2]}{gitdir.name}"
    else:
        return "Not find"


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    path = gitdir / "objects" / sha[:2] / sha[2:]
    with open(path, "rb") as f:
        content = zlib.decompress(f.read())
    part = content.find(b"\x00")
    head = content[:part]
    form = head[: head.find(b" ")]
    data = content[(part + 1) :]
    return form.decode(), data


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    result = []
    while len(data) != 0:
        mode = int(data[: data.find(b" ")].decode())
        data = data[data.find(b" ") + 1 :]
        name = data[: data.find(b"\x00")].decode()
        data = data[data.find(b"\x00") + 1 :]
        sha = bytes.hex(data[:20])
        data = data[20:]
        result.append((mode, name, sha))
    return result


def cat_file(obj_name: str, pretty: bool = True) -> None:
    path = repo_find()
    for obj in resolve_object(obj_name, path):
        header, data = read_object(obj, path)
        if header == "tree":
            result = ""
            for j in read_tree(data):
                result += (
                    f"{str(j[0]).zfill(6)} {read_object(j[2], repo_find())[0]} {j[2]}\t{j[1]}\n"
                )
            print(result)
        else:
            print(data.decode())


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    result = []
    header, data = read_object(tree_sha, gitdir)
    for i in read_tree(data):
        if read_object(i[2], gitdir)[0] == "tree":
            tree = find_tree_files(i[2], gitdir)
            for j in tree:
                name = i[1] + "/" + j[0]
                result.append((name, j[1]))
        else:
            result.append((i[1], i[2]))
    return result


def commit_parse(raw: bytes, start: int = 0, dct=None):
    data = zlib.decompress(raw)
    ind = data.find(b"tree")
    return data[ind + 5 : ind + 45]
