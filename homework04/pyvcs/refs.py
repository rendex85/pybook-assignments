import pathlib
import typing as tp


def update_ref(gitdir: pathlib.Path, ref: tp.Union[str, pathlib.Path], new_value: str) -> None:
    ref = pathlib.Path(ref)
    path = gitdir / ref
    f = path.open("w")
    f.write(new_value)
    f.close()


def symbolic_ref(gitdir: pathlib.Path, name: str, ref: str) -> None:
    # PUT YOUR CODE HERE
    ...


def ref_resolve(gitdir: pathlib.Path, refname: str) -> str:
    if refname == "HEAD":
        ref_dir = gitdir / refname
        with ref_dir.open(mode="r") as f:
            content = f.read()
        refname = content[content.find(" ") + 1:].strip()

    path = gitdir / refname
    if path.exists() is False:
        return None
    with path.open(mode="r") as f:
        content = f.read()

    return content


def resolve_head(gitdir: pathlib.Path) -> tp.Optional[str]:
    return ref_resolve(gitdir, "HEAD")


def is_detached(gitdir: pathlib.Path) -> bool:
    refname = "HEAD"
    ref_dir = gitdir / refname
    with ref_dir.open(mode="r") as f:
        content = str(f.read())
    if content.find("ref") != -1:
        return False
    else:
        return True


def get_ref(gitdir: pathlib.Path) -> str:
    refname = "HEAD"
    ref_dir = gitdir / refname
    with ref_dir.open(mode="r") as f:
        content = f.read()
    refname = content[content.find(" ") + 1:].strip()
    return refname
