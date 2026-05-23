from setuptools import setup

setup(
    name="zblock-core",
    version="2.0.0",
    author="vertudee",
    description="A secure geometric syntax interpreter handling hybrid file-folder contexts.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/vertudee/apps",
    packages=["zblock_core"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "z-core=zblock_core.interpreter:list_z_nodes",
        ],
    },
)
