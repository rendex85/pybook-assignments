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
        values = (self.ctime_s, self.ctime_n, self.mtime_s, self.mtime_n, self.dev, self.ino, self.mode, self.uid, self.gid,self.size, self.sha1, self.flags, self.name.encode())
        name_code=str(len(self.name.encode()))+"s"
        nulls="3x"
        print()
        packed = struct.pack(">10i20sh"+name_code+nulls, *values)

        return packed

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        kos_tyl=str(len(data)-62)+"s"
        unpacked_data=struct.unpack(">10i20sh1"+kos_tyl, data)
        unpacked_class = GitIndexEntry(
            ctime_s=unpacked_data[0],
            ctime_n=unpacked_data[1],
            mtime_s=unpacked_data[2],
            mtime_n=unpacked_data[3],
            dev=unpacked_data[4],
            ino=unpacked_data[5],
            mode=unpacked_data[6],
            uid=unpacked_data[7],
            gid=unpacked_data[8],
            size=unpacked_data[9],
            sha1=unpacked_data[10],
            flags=unpacked_data[11],
            name=unpacked_data[12][:len(unpacked_data[12])-3].decode("utf-8"),
        )
        return unpacked_class


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    # PUT YOUR CODE HERE
    path_all=gitdir/"index"
    with path_all.open(mode="rb") as f:
        content=f.read()
    len=(int.from_bytes(content[8:12], "big"))
    start=0
    finder=62
    content = content[12:-20]
    for i in range (0,3):
        pointer=b"\x00\x00\x00"
        end=content[finder:].find(pointer)
        print(content[62:62+end])
        #print(GitIndexEntry.unpack(content[start:end]).name)
        start=end
    print(content[12:-20])

    return []


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    # PUT YOUR CODE HERE
    ...


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    # PUT YOUR CODE HERE
    ...


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:
    # PUT YOUR CODE HERE
    ...
