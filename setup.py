# !/usr/bin/env python
"""Package setup for crowdstrike-foundry-function."""

import os
from setuptools import setup

DESCRIPTION = 'CrowdStrike Foundry Function Software Developer Kit for Python'
PACKAGE_NAME = 'crowdstrike.foundry.function'
PACKAGE_DIR = {
    'crowdstrike.foundry.function': './src/crowdstrike/foundry/function',
}
PACKAGES = [
    'crowdstrike.foundry.function',
]
PYTHON_VERSION = '>=3.9.0'
SETUP_REQUIRES = [
    'setuptools',
]
VERSION = '1.1.4'


def main():
    """Build crowdstrike-foundry-function package."""
    setup(
        description=DESCRIPTION,
        install_requires=find_dependencies(os.path.join(os.path.dirname(__file__), "requirements.txt")),
        name=PACKAGE_NAME,
        package_dir=PACKAGE_DIR,
        packages=PACKAGES,
        python_requires=PYTHON_VERSION,
        setup_requires=SETUP_REQUIRES,
        version=VERSION,
        long_description=long_description(),
        long_description_content_type="text/markdown",
    )


def find_dependencies(requirements) -> list[str]:
    """Parse the package dependencies from requirements file."""
    with open(requirements, 'r') as reqs:
        return [line for line in sanitized_lines(reqs.readlines())]


def long_description() -> str:
    """Generate package long description."""
    with open("README.md", "r", encoding="utf-8") as fh:
        descript = fh.read()

    # Remove GitHub's emoji
    emojis = [
        ":speech_balloon: ", ":bulb: ", ":pray: ", ":raised_hands: ", " :fire:", ":fire: ",
        "<small>", "</small>", " :mag_right:", " :dizzy:", " :memo:", " :coffee:", " :book:"
    ]
    for emoji in emojis:
        descript = descript.replace(emoji, "")
    return descript


def sanitized_lines(lines: list[str]):
    """Sanitize the lines read from requirements file."""
    for line in lines:
        line = line.strip()
        if line != '' and line[0] != '#':
            yield line


if __name__ == "__main__":
    main()
