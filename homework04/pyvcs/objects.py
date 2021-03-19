import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

from pyvcs import repo
from pyvcs.refs import update_ref
from pyvcs.repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    # PUT YOUR CODE HERE
    header = f"{fmt} {len(data)}\0"
    store = header.encode()+data
    result=hashlib.sha1(store).hexdigest()
    workdir = pathlib.Path(".")
    workdir = workdir.absolute()
    gitdir = repo.repo_find(workdir)
    (gitdir / "objects"/result[0:2]).mkdir(parents=True, exist_ok=True)
    text_to_write=zlib.compress(store)
    (gitdir / "objects" / result[0:2]/result[2:]).write_bytes(text_to_write)
    return result


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    final_list=[]
    if len(obj_name)>40 or len(obj_name)<4:
        raise Exception(f"Not a valid object name {obj_name}")
    path_hash=gitdir/ "objects"/obj_name[0:2]
    for file in path_hash.iterdir():
        if obj_name[2:] in str(file.parts[-1]):
            final_list.append(str(file.parts[-2])+str(file.parts[-1]))
    if not final_list:
        raise Exception(f"Not a valid object name {obj_name}")
    return final_list


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    # PUT YOUR CODE HERE
    ...


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    path_all=gitdir / "objects" / sha[0:2]/sha[2:]
    with path_all.open(mode="rb") as f:
        content = zlib.decompress(f.read())
        return ((content[:4].decode("utf-8"),content[8:]))

def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    # PUT YOUR CODE HERE
    ...


def cat_file(obj_name: str, pretty: bool = True) -> None:
    # PUT YOUR CODE HERE
    print("that's what she said")
    #path=repo.repo_find(pathlib.Path("."))/
    #return "GUSARY MOLCHAT'"


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    # PUT YOUR CODE HERE
    ...


def commit_parse(raw: bytes, start: int = 0, dct=None):
    # PUT YOUR CODE HERE
    ...
