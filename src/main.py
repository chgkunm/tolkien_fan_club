import sys
from os import listdir, mkdir, path
from shutil import copy, rmtree

from generate_page import generate_page

basepath = "./"
if len(sys.argv) > 1:
    basepath = sys.argv[1]
STATIC = "./static/"
CONTENT = "./content/"
DOCS = "./docs/"
TEMPLATE = "./template.html"


def copy_from_source_to_destination(base_path: str = STATIC):
    dest_path = base_path.replace("/static/", "/docs/")
    static_dir = listdir(base_path)
    for a_dir in static_dir:
        dir_path = path.join(base_path, a_dir)
        if path.isfile(dir_path):
            copy(dir_path, dest_path)
        else:
            dir_dest_path = f"{path.join(dest_path, a_dir)}/"
            mkdir(dir_dest_path)
            copy_from_source_to_destination(dir_path)


def main():
    print(basepath, STATIC, CONTENT, DOCS, TEMPLATE)
    if path.exists(STATIC):
        print("exists")
        if path.exists(DOCS):
            print("exists but deleted")
            rmtree(DOCS)
        mkdir(DOCS)
        copy_from_source_to_destination()
        generate_page(basepath, CONTENT, TEMPLATE, DOCS)


if __name__ == "__main__":
    main()
