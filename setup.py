import setuptools
import shutil
import os
import json, importlib
import src.filesorterfunctions as fsf
current_location = os.path.abspath(os.path.dirname(__file__))

def install():
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

    setuptools.setup(
        name="slib_sorter",
        version="1.1.0",
        author="Lukas Hübinger",
        author_email="fettkindasindauchoke@gmail.com",
        description="A Python library for sorting Sample Libraries",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/nrdrch/slib-sorter",
        packages=setuptools.find_packages(), 
        entry_points={
            "console_scripts": [
                "slib-sorter = src.slib_sorter:__main__"
            ]
        },
        install_requires=[
            "termcolor==2.3.0"
        ],
        classifiers=[
            "Programming Language :: Python :: 3.7",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: Microsoft :: Windows :: Windows 10"
        ],
    )
    fsf.ps_script(os.path.join(current_location, "src", "slib_sorter.py"))
    
def reload():
    importlib.reload(current_location)
    install()
def __main__():
    try:
        install()
    except:
        reload()
__main__()