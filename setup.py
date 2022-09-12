from os import path
from setuptools import setup
from setuptools import find_namespace_packages

setup(
    name="league_account_manager",
    version="0.0.1",
    description="This is a League of Legends account manager",
    long_description=open(
        path.join(path.abspath(path.dirname(__file__)), "README.md")
    ).read(),
    long_description_content_type="text/markdown",
    author="CasperDoesCoding",
    packages=find_namespace_packages(where="src"),
    install_requires=["setuptools"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # entry_points={"console_scripts": ["my-command=riot-api.src:main"]},
)
