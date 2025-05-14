#!/usr/bin/env python

from pathlib import Path
import re
import subprocess
import sys
import tomllib


def run_command(command):
    return subprocess.run(
        command, shell=True, capture_output=True, text=True, check=True
    ).stdout.strip()


def get_version_file_from_pyproject():
    try:
        with Path("pyproject.toml").open("rb") as f:
            return tomllib.load(f)["tool"]["hatch"]["version"]["path"]
    except FileNotFoundError:
        raise FileNotFoundError("Project has no pyproject.toml file!")
    except KeyError:
        raise KeyError("Attribute `tool.hatch.version.path` not found in pyproject.toml")


def get_remote_version(remote, branch, version_file):
    remote_file = f"{remote}/{branch}:{version_file}"
    match = re.search(
        r"__version__\s*=\s*['\"]([^'\"]+)['\"]",
        run_command(f"git show {remote_file}"),
    )
    if match:
        return match.group(1)
    else:
        raise AttributeError(f"No `__version__` attribute found in {remote_file}")


def main():
    version_file = get_version_file_from_pyproject()
    branch = run_command("git rev-parse --abbrev-ref HEAD")
    remote = sys.argv[1] if len(sys.argv) > 1 else "origin"

    current_version = run_command("uv run hatch version")
    remote_version = get_remote_version(remote, branch, version_file)

    assert current_version != remote_version, (
        "Version has not been incremented! Please update the version before pushing."
    )


if __name__ == "__main__":
    main()
