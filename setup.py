from importlib.metadata import entry_points
from setuptools import find_packages, setup

setup(
    name="receipt",
    version="0.1.0",
    description="An application for generating receipt details of shopping baskets",
    url="https://github.com/marcelhohn/receipt.git",
    author="Marcel Hohn",
    author_email="marcel.hohn@web.de",
    packages=find_packages(),
    extras_require={"dev": ["black"]},
    entry_points={"console_scripts": ["receipt=receipt.main:main"]},
)
