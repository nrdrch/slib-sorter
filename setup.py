import setuptools
import shutil
import os
import json, importlib
settings_folder = os.path.join(os.environ['USERPROFILE'], 'Documents', 'WindowsPowerShell', 'Scripts', 'slib_sorter')
settings = os.path.join(settings_folder, "settings.json")
default_config = f'''
{{
    "Foregroud Color 1": "white",
    "Top Bar Color": "dark_grey",
    "Show Top Bar": true,
    "Top Bar": "<   Sample Library Sorter   >",
    "Prompt Color": "dark_grey",
    "Prompt": "$ ",
    "Console Log Seperator": "  >>>--<>  ",
    "Show More Console Logs": false,
    "Show Seperator": true,
    "Show Statistics": true,
    "Statistics Value Color": "light_red",
    "Max files per Dir": 50,
    "TBPDPath": "Desktop",
    "To Be Processed Directory": "To Be Sorted",
    "NOFLDPath": "Desktop",
    "Name Of Top Library Directory": "Sample Library",
    "RFPath": "Desktop",
    "Rejected Files": "Rejected Files",
    "Run Shell Command On Startup": false,
    "Command On Startup": "cls" 
}}
    '''
def ps_script(source_file):
    
    winpro = os.path.join(os.environ['USERPROFILE'],'Documents', 'WindowsPowerShell')
    powershell_scripts_folder = os.path.join(winpro, 'Scripts', 'slib_sorter')
    settings_file_ps = os.path.join(powershell_scripts_folder, 'settings.json')
    if not os.path.exists(powershell_scripts_folder):
        os.makedirs(powershell_scripts_folder)
    else:
        pass
    powershell_script_file = os.path.join(powershell_scripts_folder, 'slib_sorter' + ".psm1")
    settings_file = os.path.join(powershell_scripts_folder, 'settings.json')
    return settings_file_ps
settings_file = settings
settings_source = 'settings.json'

def install():
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
    if not os.path.exists(settings_file):
        with open(settings_file, 'w') as f:
            f.write(default_config)
    else:
        pass

    setuptools.setup(
        name="slib-sorter",
        version="1.2.6",
        author="Lukas Hübinger",
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

    if not os.path.exists(settings_file):
        ps_script(settings_source)
    else:
        pass
    

def __setup__():
    install()

__setup__()