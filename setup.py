import setuptools
import shutil
import os
import json

def ps_script(source_file):
    winpro = os.path.join(os.environ['USERPROFILE'], 'Documents', 'WindowsPowerShell')
    powershell_scripts_folder = os.path.join(winpro, 'Scripts', 'slib_sorter')
    settings_file = os.path.join(powershell_scripts_folder, 'settings.json')
    
    if not os.path.exists(powershell_scripts_folder):
        os.makedirs(powershell_scripts_folder)
    
    powershell_script_file = os.path.join(powershell_scripts_folder, 'slib_sorter.psm1')
    
    return settings_file

settings_folder = os.path.join(os.environ['USERPROFILE'], 'Documents', 'WindowsPowerShell', 'Scripts', 'slib_sorter')
settings = os.path.join(settings_folder, "settings.json")

default_config = '''
{
    "Paths": {
        "To Be Processed Directory": "~/Desktop/To Be Processed",
        "Name Of Top Library Directory": "~/Desktop/Sample Library",
        "Rejected Filetype Directory": "~/Desktop/Rejected Files"
    },
    "Colors": {
        "Foreground Color 1": "white",
        "Foreground Color 2": "dark_grey",
        "Top Title Bar Color": "dark_grey",
        "Prompt Color": "dark_grey",
        "Statistics Value Color": "light_red",
        "Successfully Sorted File Color": "light_green",
        "Unsorted File Color": "light_yellow",
        "Rejected Filetype Color": "red"
    },
    "Show More Console Logs": true,
    "Console Log Seperator": "  >>>--<>  ",
    "Top Title Bar": "<   Sample Library Sorter   >",
    "Prompt": "$ ",
    "Max files per Dir": 50,
    "Command On Startup": "cls",
    "Run Shell Command On Startup": false,
    "Show Top Title Bar": true,
    "Show Statistics": true,
    "Show Seperator": true
}
'''

def install():
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
    
    if not os.path.exists(settings_folder):
        os.makedirs(settings_folder)
    
    if not os.path.exists(settings):
        with open(settings, 'w') as f:
            f.write(default_config)
    
    setuptools.setup(
        name="slib-sorter",
        version="1.6.5",
        author="Lukas H",
        author_email="fettkindasindauchoke@gmail.com",
        description="A Python package for sorting Sample Libraries",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/nrdrch/slib-sorter",
        packages=setuptools.find_packages(), 
        entry_points={
            "console_scripts": [
                "Slib-Sorter = src.slib_sorter:__main__"
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

def __setup__():
    install()

__setup__()
