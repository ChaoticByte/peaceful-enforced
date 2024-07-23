#!/usr/bin/env python3

from json import load
from os import chdir
from pathlib import Path
from shutil import copy
from shutil import copytree
from shutil import make_archive
from shutil import rmtree


project_dir = Path(".").resolve()
build_root_dir = project_dir / "_build"

fabric_mod_json_path = project_dir / "fabric.mod.json"
source_files = [
    fabric_mod_json_path,
    project_dir / "pack.mcmeta",
    project_dir / "data"
]


def get_build_name(mod_info: dict) -> str:
    return f"{mod_info['id'].replace('_', '-')}-{mod_info['version']}-mc{mod_info['depends']['minecraft']}"


if __name__ == "__main__":
    # load mod info
    with fabric_mod_json_path.open("r") as f:
        mod_info = load(f)
    # get build name
    build_name = get_build_name(mod_info)
    # clear/create required directories
    build_tmp_dir = build_root_dir / build_name
    if build_tmp_dir.exists():
        rmtree(build_tmp_dir)
    build_tmp_dir.mkdir(parents=True)
    # copy source files
    for s in source_files:
        if s.is_dir():
            copytree(s, build_tmp_dir / s.name)
        else:
            copy(s, build_tmp_dir / s.name)
    # create jar archive
    chdir(build_root_dir)
    make_archive(build_name, "zip", build_tmp_dir.name)
    output_file = Path(build_name + ".zip").rename(build_name + ".jar").resolve()
    chdir(project_dir)
    # cleanup
    rmtree(build_tmp_dir)
    # done
    print("Done. The resulting jar file is at", output_file)
