from argparse import ArgumentParser

import compileall
import shutil
import os


def compile_projects(source_root: str, build_root: str, projects: list[str]):
    for project in projects:
        source_path = os.path.join(source_root, project)
        build_path = os.path.join(build_root, project)

        if os.path.exists(build_path):
            shutil.rmtree(build_path)
        os.makedirs(build_path)

        compileall.compile_dir(source_path, stripdir=source_root, legacy=True)

        for root, _, files in os.walk(source_path):
            for file in files:
                if file.endswith(".pyc"):
                    source_file = os.path.join(root, file)
                    build_file = os.path.join(build_path, os.path.relpath(source_file, source_path))

                    if not os.path.exists(os.path.dirname(build_file)):
                        os.makedirs(os.path.dirname(build_file))

                    shutil.move(source_file, build_file)


def main():
    parser = ArgumentParser(
        description="Compile python source code",
    )
    parser.add_argument(
        "--src",
        "-i",
        dest="source_root",
        default="src",
        help="Root directory of the source code (default: src)",
    )
    parser.add_argument(
        "--build",
        "-o",
        dest="build_root",
        default="build",
        help="Root directory of the compiled code (default: build)",
    )
    parser.add_argument("projects", nargs="+", help="Projects to compile")

    args = parser.parse_args()

    compile_projects(args.source_root, args.build_root, args.projects)


if __name__ == "__main__":
    main()
