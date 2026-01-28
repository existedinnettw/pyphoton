from setuptools import setup, find_packages
from pathlib import Path

setup(
    name='pyphoton',
    version='1.0.0',
    url='https://github.com/astagi/pyphoton',
    install_requires=["httpx>=0.23.0"],
    description="Photon Python client",
    long_description=Path('README.rst').read_text(encoding='utf-8'),
    license="MIT",
    author="Andrea Stagi",
    author_email="stagi.andrea@gmail.com",
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'
    ]
)
