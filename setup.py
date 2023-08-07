# !/usr/bin/env python

import os
from setuptools import setup
from typing import List

DESCRIPTION = 'CrowdStrike Foundry Function Software Developer Kit for Python'
PACKAGE_NAME = 'crowdstrike.foundry.function'
PACKAGE_DIR = {
    'crowdstrike.foundry.function': './src/crowdstrike/foundry/function',
}
PACKAGES = [
    'crowdstrike.foundry.function',
]
PYTHON_VERSION = '>=3.9.0,<3.10.0'
SETUP_REQUIRES = [
    'setuptools',
]


def main():
    setup(
        description=DESCRIPTION,
        install_requires=find_dependencies(os.path.join(os.path.dirname(__file__), "requirements.txt")),
        name=PACKAGE_NAME,
        package_dir=PACKAGE_DIR,
        packages=PACKAGES,
        python_requires=PYTHON_VERSION,
        setup_requires=SETUP_REQUIRES,
    )


def find_dependencies(requirements) -> List[str]:
    with open(requirements, 'r') as reqs:
        return [line for line in sanitized_lines(reqs.readlines())]


def sanitized_lines(lines: List[str]):
    for line in lines:
        line = line.strip()
        if line != '' and line[0] != '#':
            yield line


if __name__ == "__main__":
    main()
