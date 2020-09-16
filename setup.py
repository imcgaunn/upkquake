from setuptools import setup, find_packages


PROJECT_URL = "github.com/imcgaunn/upkquake"

setup(
    name="upkquake",
    version="0.1",
    description="tool to download and extract quake ii archive",
    author="ian mcgaunn",
    author_email="ianmcgaunn@pressmail.ch",
    packages=find_packages(exclude=("tests", "docs")),
    entry_points={"console_scripts": ["upkquake=upkquake.upkquake:main"]},
    install_requires=open("requirements-dev.txt").readlines(),
)
