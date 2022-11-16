import os
import pathlib
import stat
import time
import typing as tp

from pyvcs.index import GitIndexEntry, read_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    tree = b""
    for f in index:
        files = oct(f.mode)[2:].encode()
        if "/" in f.name:
            num = f.name.find("/")
            dirname = (f.name[: num])
            new_f = files + b" " + f.name[num + 1 :].encode() + b"\0" + f.sha1
            hashh = bytes.fromhex(hash_object(new_f, fmt="tree", write=True))
            tree += b"40000 " + dirname.encode() + b"\0" + hashh
        else:
            tree += files + b" " + f.name.encode() + b"\0" + f.sha1
    return hash_object(tree, fmt="tree", write=True)


def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:
    if not author:
        author = f"{os.getenv('GIT_AUTHOR_NAME')} <{os.getenv('GIT_AUTHOR_EMAIL')}>"
    timestamp = int(time.mktime(time.localtime()))
    timezone = time.timezone
    sign = "+" if timezone < 0 else "-"
    hours = str(abs(timezone // 3600))
    hours_ = hours if int(hours) > 10 else "0" + hours
    secs = str(abs((timezone // 60) % 60))
    secs_ = secs if int(secs) > 0 else "0" + secs
    author_t = f"{timestamp} {sign}{hours_}{secs_}"
    result = f"tree {tree}\n"
    if parent:
        result += f"parent {parent}\n"
    result += f"author {author_t}\ncommitter {author} {author_t}\n\n{message}\n"
    return hash_object(result.encode(), "commit", True)
