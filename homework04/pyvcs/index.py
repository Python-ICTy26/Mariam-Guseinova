import hashlib
import operator
import os
import pathlib
import struct
import typing as tp

from pyvcs.objects import hash_object


class GitIndexEntry(tp.NamedTuple):
    # @see: https://github.com/git/git/blob/master/Documentation/technical/index-format.txt
    ctime_s: int
    ctime_n: int
    mtime_s: int
    mtime_n: int
    dev: int
    ino: int
    mode: int
    uid: int
    gid: int
    size: int
    sha1: bytes
    flags: int
    name: str

    def pack(self) -> bytes:
        return struct.pack(
            f"!4L6i20sh{len(self.name)}s3x",
            *[
                self.ctime_s,
                self.ctime_n,
                self.mtime_s,
                self.mtime_n,
                self.dev,
                self.ino,
                self.mode,
                self.uid,
                self.gid,
                self.size,
                self.sha1,
                self.flags,
                self.name.encode(),
            ],
        )

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        f = f"!4L6i20sh{len(data) - 62}s"
        unpacked = list(struct.unpack(f, data))
        unpacked[-1] = unpacked[-1][:-3].decode()
        return GitIndexEntry(*unpacked)


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    result: tp.List[GitIndexEntry] = []
    try:
        with open(gitdir / "index", "rb") as file:
            content = file.read()
    except:
        return result

    c = int.from_bytes(content[8:12], "big")
    inf = content[12:-20]
    count = 0
    for i in range(c):
        start = count + 62
        end = inf[start:].find(b"\x00\x00\x00") + start + 3
        result.append(GitIndexEntry.unpack(inf[count:end]))
        count = end
    return result


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    with open(gitdir / "index", "wb") as file:
        hashh = struct.pack("!4s2i", *(b"DIRC", 2, len(entries)))
        file.write(hashh)
        for entry in entries:
            file.write(entry.pack())
            hashh += entry.pack()
        hash2 = str(hashlib.sha1(hashh).hexdigest())
        file.write(struct.pack(f"!{len(bytes.fromhex(hash2))}s", bytes.fromhex(hash2)))


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    for f in read_index(gitdir):
        if details:
            print(f"{oct(f.mode)[2:]} {f.sha1.hex()} 0	{f.name}")
        else:
            print(f.name)


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:
    if (gitdir / "index").exists():
        result = read_index(gitdir)
    else:
        result = []
    for path in paths:
        file = open(path, "rb")
        sha = hash_object(file.read(), "blob", True)
        stat = os.stat(path)
        result.append(
            GitIndexEntry(
                ctime_s=int(stat.st_ctime),
                ctime_n=0,
                mtime_s=int(stat.st_mtime),
                mtime_n=0,
                dev=stat.st_dev,
                ino=stat.st_ino,
                mode=stat.st_mode,
                uid=stat.st_uid,
                gid=stat.st_gid,
                size=stat.st_size,
                sha1=bytes.fromhex(sha),
                flags=7,
                name=str(path).replace("\\", "/"),
            )
        )
    result = sorted(result, key=lambda x: x.name)
    write_index(gitdir, result)
