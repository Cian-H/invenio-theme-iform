#!/usr/bin/env python
"""A Script for checking that the version number has been incremented between pushes."""

from pathlib import Path
import re
import shutil
import subprocess
import sys
import tomllib

ALLOWED_EXECUTABLES: list[str] = [
    "git",
    "uv",
]


def validate_command(command: str) -> list[str]:
    """Validate and guard command calls.

    Args:
        command (str): the command to be validated.

    Returns:
        str: the validated command

    Raises:
        FileNotFoundError: if the command was not found

    """
    cmd: list[str] = command.split().copy()
    if cmd[0] not in ALLOWED_EXECUTABLES:
        msg = f"Command {cmd} is not allowed!"
        raise PermissionError(msg)
    call = shutil.which(cmd[0])
    if not call:
        msg = f"Command {call} not found!"
        raise FileNotFoundError(msg)
    cmd[0] = call
    if cmd[0] == "uv" and cmd[1] == "run":
        cmd = [cmd[0], cmd[1], *validate_command("".join(cmd[2:]))]
    return cmd


def run_command(command: str) -> str:
    """Run a command and get its output as a string.

    Args:
        command (str): The command to run.

    Returns:
        The output returned on stdout.

    """
    cmd = validate_command(command)
    return subprocess.run(  # noqa: S603
        cmd,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


def get_version_file_from_pyproject() -> str:
    """Get the path to the version file from the pyproject file.

    Returns:
        str: the path to the project version file

    Raises:
        FileNotFoundError: the pyproject file is not found
        KeyError: the pyproject file does not reference a version file

    """
    try:
        with Path("pyproject.toml").open("rb") as f:
            return tomllib.load(f)["tool"]["hatch"]["version"]["path"]
    except FileNotFoundError as e:
        msg = "Project has no pyproject.toml file!"
        raise FileNotFoundError(msg) from e
    except KeyError as e:
        msg = "Attribute `tool.hatch.version.path` not found in pyproject.toml"
        raise KeyError(msg) from e


def get_remote_version(remote: str, branch: str, version_file: str) -> str:
    """Get the version from the repository remote.

    Args:
        remote (str): The remote to fetch the version string from.
        branch (str): The branch to fetch the version string from.
        version_file (str): The file to fetch the version string from.

    Returns:
        str: The version string.

    Raises:
        AttributeError: NO `__version__` attribute was found in `version_file`.

    """
    remote_file = f"{remote}/{branch}:{version_file}"
    match = re.search(
        r"__version__\s*=\s*['\"]([^'\"]+)['\"]",
        run_command(f"git show {remote_file}"),
    )
    if match:
        return match.group(1)
    msg = f"No `__version__` attribute found in {remote_file}"
    raise AttributeError(msg)


def main() -> None:
    """Entrypoint for this script."""
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
