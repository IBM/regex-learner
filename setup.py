from __future__ import annotations

from setuptools import setup  # type: ignore
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(long_description=long_description)
