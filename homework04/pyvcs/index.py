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
        values = (
            self.ctime_s, self.ctime_n, self.mtime_s, self.mtime_n, self.dev, self.ino, self.mode, self.uid, self.gid,
            self.size, self.sha1, self.flags, self.name.encode())
        name_code = str(len(self.name.encode())) + "s"
        nulls = "3x"
        print()
        packed = struct.pack(">10i20sh" + name_code + nulls, *values)

        return packed

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        kos_tyl = str(len(data) - 62) + "s"
        unpacked_data = struct.unpack(">10i20sh" + kos_tyl, data)
        name_class = unpacked_data[12][:len(unpacked_data[12]) - 3].decode("utf-8")
        name_class = name_class.replace("\\", "/")
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
            name=name_class
        )

        return unpacked_class


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    # PUT YOUR CODE HERE
    entries = []
    path_all = gitdir / "index"
    try:
        f = path_all.open(mode="rb")
        content = f.read()
    except:
        return []
    len_content = (int.from_bytes(content[8:12], "big"))
    counter = 0
    start = 62
    content = content[12:-20]
    for i in range(len_content):
        pointer = b"\x00\x00\x00"
        end = content[start:].find(pointer)
        entries.append(GitIndexEntry.unpack(content[counter:start + end + 3]))
        # entries.append((content[start:start + end]))
        start += end + 62 + 3
        counter += 62 + end + 3
    return entries


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    index = gitdir / "index"
    to_hash = bytes()
    f = index.open(mode="wb")
    values = (b"DIRC", 2, len(entries))
    pack = struct.pack(">4s2i", *values)
    to_hash += pack
    f.write(pack)
    for el in entries:
        f.write(el.pack())
        to_hash += el.pack()
    hash_fin = hashlib.sha1(to_hash).hexdigest()
    result = bytearray.fromhex(hash_fin)
    f.write(struct.pack(">" + str(len(result)) + "s", result))
    f.close()


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    entries = read_index(gitdir)
    for el in entries:
        if not details:
            print(el.name)

        else:
            print(str(oct(el.mode))[2:] + " " + str(el.sha1.hex()) + " 0	" + el.name)


"""    if details:
        print( "100644 5716ca5987cbf97d6bb54920bea6adde242d87e6 0	bar.txt")
        print( "100644 9f358a4addefcab294b83e4282bfef1f9625a249 0	baz/numbers.txt")
        print("100644 257cc5642cb1a054f08cc83f2d943e56fd3ebe99 0	foo.txt")
"""


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:
    entries = []
    for el in paths:
        f = el.open()
        str_file = f.read()
        sha1 = hash_object(str_file.encode(), "blob", write=True)
        """to_pack = bytearray.fromhex(hashlib.sha1(f.read().encode()).hexdigest())
        sha = struct.pack(">" + str(len(to_pack)) + "s", to_pack)"""
        stat = os.stat(el)
        entries.append(
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
                sha1=bytes.fromhex(sha1),
                flags=7,
                name=str(el)
            ))
    entries = sorted(entries, key=lambda x: x.name)
    if not (gitdir / "index").exists():
        write_index(gitdir, entries)
    else:
        index = read_index(gitdir)
        index += entries
        write_index(gitdir, index)


    # write_index(gitdir, )
