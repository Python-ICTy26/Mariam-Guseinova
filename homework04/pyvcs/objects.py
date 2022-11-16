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
    hash_store = hashlib.sha1(store).hexdigest()
    if write:
        path = repo_find() / "objects" / hash_store[:2]
        if not path.exists():
            path.mkdir(parents=True)
        file_path = path / hash_store[2:]
        if not file_path.exists():
            file_path.write_bytes(zlib.compress(store))
    return hash_store


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    if len(obj_name) < 4 or len(obj_name) > 40:
        raise Exception(f"Not a valid object name {obj_name}")
    objects = []
    for i in (gitdir / "objects").iterdir():
        if i.is_dir() and i.name == obj_name[:2]:
            for j in i.iterdir():
                if obj_name[2:] in j.name:
                    objects.append(i.name + j.name)
    if len(objects) == 0:
        raise Exception(f"Not a valid object name {obj_name}")
    return objects


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    object_new = resolve_object(obj_name, gitdir)
    if len(object_new) == 1:
        return object_new[0]
    else:
        raise Exception(f"Ambiguous object name {obj_name}")


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
    for i in resolve_object(obj_name, path):
        fmt, data = read_object(i, path)
        if fmt == "tree":
            result = ""
            for j in read_tree(data):
                repo_find()
                result += (
                    f"{str(j[0]).zfill(6)} {read_object(j[2], repo_find())[0]} {j[2]}\t{j[1]}\n"
                )
            print(result)
        else:
            print(data.decode())


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    result = []
    header, data = read_object(tree_sha, gitdir)
    for f in read_tree(data):
        if read_object(f[2], gitdir)[0] == "tree":
            tree = find_tree_files(f[2], gitdir)
            for blob in tree:
                name = f[1] + "/" + blob[0]
                result.append((name, blob[1]))
        else:
            result.append((f[1], f[2]))
    return result


def commit_parse(raw: bytes, start: int = 0, dct=None):
    data = zlib.decompress(raw)
    i = data.find(b"tree")
    return data[i + 5 : i + 45]
