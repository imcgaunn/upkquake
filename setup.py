from setuptools import setup, find_packages


PROJECT_URL = "github.com/imcgaunn/upkquake"

setup(
    name="upkquake",
    version="0.1",
    description="tool to download and extract quake ii archive",
    author="ian mcgaunn",
    packages=find_packages(),
    entry_points={"console_scripts": ["upkquake=upkquake.upkquake:main"]},
    install_requires=open("requirements.txt").readlines(),
)
