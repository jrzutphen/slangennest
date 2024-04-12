"""
This module contains functions for compiling Python files
and moving the compiled files to a specified build path.

Functions:

    compile_projects(source_root: str, build_root: str, projects: list[str]) -> None:
        Compiles the projects in the specified source root directory
        and moves the compiled files to the build root directory.

    main() -> None:
        Provides a command line interface for compiling Python files.
"""

from argparse import ArgumentParser

import compileall
import shutil
import os

def _move_compiled_files(source_path: str, build_path: str):
    """
    Move compiled files from the source path to the build path.

    Args:
        source_path (str): The path where the compiled files are located.
        build_path (str): The path where the compiled files should be moved to.
    """
    for root, _, files in os.walk(source_path):
        for file in files:
            if file.endswith(".pyc"):
                source_file = os.path.join(root, file)
                build_file = os.path.join(build_path, os.path.relpath(source_file, source_path))

                if not os.path.exists(os.path.dirname(build_file)):
                    os.makedirs(os.path.dirname(build_file))

                shutil.move(source_file, build_file)

def compile_projects(source_root: str, build_root: str, projects: list[str]):
    """
    Compile the projects in the specified source root directory
    and move the compiled files to the build root directory.

    Args:
        source_root (str): The root directory where the source files are located.
        build_root (str): The root directory where the compiled files will be moved to.
        projects (list[str]): A list of project names to be compiled.

    Returns:
        None
    """
    for project in projects:
        source_path = os.path.join(source_root, project)
        build_path = os.path.join(build_root, project)

        if os.path.exists(build_path):
            shutil.rmtree(build_path)
        os.makedirs(build_path)

        compileall.compile_dir(source_path, stripdir=source_root, legacy=True)

        _move_compiled_files(source_path, build_path)


def main():
    """
    Compile python source code.

    This function parses command line arguments, including the source root directory,
    build root directory, and projects to compile. It then calls the `compile_projects`
    function with the provided arguments.

    Args:
        None

    Returns:
        None
    """
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
