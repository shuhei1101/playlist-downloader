from setuptools import setup, find_packages

setup(
    name="playlist-downloader",
    version="0.1",
    packages=find_packages(exclude=["tests"]),
    test_suite="tests",
)
