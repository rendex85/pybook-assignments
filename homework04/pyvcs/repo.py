import os
import pathlib
import typing as tp
import os


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    # PUT YOUR CODE HERE
    try:
        git_dir_pointer = os.environ['GIT_DIR'] if os.environ['GIT_DIR'] else ".git"
    except:
        git_dir_pointer=".git"
    git_dir = None
    workdir=pathlib.Path(workdir)
    try:
        workdir.parents
    except:
        raise Exception("Not a git repository")
    if len(workdir.parents) == 0:
        return pathlib.Path("/" + git_dir_pointer)
    else:
        for path in workdir.parents:
            if git_dir_pointer in str(path):
                git_dir = path
    if not git_dir:
        raise Exception("Not a git repository")
    return git_dir


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    # PUT YOUR CODE HERE
    try:
        if workdir.is_file():
            raise Exception(f"{str(workdir)} is not a directory")
    except AttributeError:
        workdir=pathlib.Path(workdir)
    try:
        git_dir = os.environ['GIT_DIR'] if os.environ['GIT_DIR'] else ".git"
    except:
        git_dir=".git"
    gitdit = workdir / git_dir
    gitdit.mkdir(parents=True, exist_ok=True)
    (gitdit / ("HEAD")).write_text("ref: refs/heads/master\n", encoding="utf-8")
    (gitdit / ("config")).write_text(
        "[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n",
        encoding="utf-8")
    (gitdit / ("description")).write_text("Unnamed pyvcs repository.\n", encoding="utf-8")
    (gitdit / "objects").mkdir(parents=True, exist_ok=True)
    (gitdit / "refs").mkdir(parents=True, exist_ok=True)
    (gitdit / "refs/heads").mkdir(parents=True, exist_ok=True)
    (gitdit / "refs/tags").mkdir(parents=True, exist_ok=True)

    return gitdit
