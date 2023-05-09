from __future__ import annotations

from setuptools import setup  # type: ignore
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
__version__ = "0.0.1"

setup(long_description=long_description, version=__version__)
