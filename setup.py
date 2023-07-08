import setuptools
import shutil
import os
import json, importlib
settings_folder = os.path.join(os.environ['USERPROFILE'], 'Documents', 'WindowsPowerShell', 'Scripts', 'slib_sorter')
settings = os.path.join(settings_folder, "settings.json")
def ps_script(source_file):
    winpro = os.path.join(os.environ['USERPROFILE'],'Documents', 'WindowsPowerShell')
    powershell_scripts_folder = os.path.join(winpro, 'Scripts', 'slib_sorter')
    if not os.path.exists(powershell_scripts_folder):
        os.makedirs(powershell_scripts_folder)
    powershell_script_file = os.path.join(powershell_scripts_folder, 'slib_sorter' + ".psm1")
    settings_file = os.path.join(powershell_scripts_folder, 'settings.json')
    script_content = f'''
function Start-Sorter {{
    [CmdletBinding()]
    param(
        [Parameter(ValueFromRemainingArguments=$true)]
        [string]$CustomInput
    )
    $argsString = $CustomInput -join "' '"
    $pythonScript = '{source_file}'
    python3 $pythonScript $argsString
}}
    '''
    #with open(powershell_script_file, 'a') as f:
    #    f.write(script_content)
    
    if not os.path.exists(settings_folder):
        os.makedirs(settings_folder)
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
    if not os.path.exists(settings):
        with open(settings, 'w') as f:
            f.write(default_config)
    else:
        pass
    with open(settings, 'r') as file:
        settings = json.load(file)
    settings = settings_file
    #profile_path = os.path.expanduser("~/Documents/WindowsPowerShell/Microsoft.PowerShell_profile.ps1")
    #with open(profile_path, 'r') as f:
    #    profile_content = f.read()
    #    if f"Import-Module -DisableNameChecking \"{powershell_script_file}\"" in profile_content:
    #        pass
    #    else:
    #        with open(profile_path, 'a') as f:
    #            f.write(f"\nImport-Module -DisableNameChecking \"{powershell_script_file}\"")
    try:
        if settings.get("Run Shell Command On Startup", True):
            CmdOnStartup = settings.get("Command On Startup")
            os.system(CmdOnStartup)
        else:
            pass
    except:
        winpro = os.path.join(os.environ['USERPROFILE'],'Documents', 'WindowsPowerShell')
        powershell_scripts_folder = os.path.join(winpro, 'Scripts', 'slib_sorter')
        
        importlib.reload(settings)
        #setupfile = os.path.join(path_finder(0), 'setup.py')



current_location = os.path.abspath(os.path.dirname(__file__))
def install():
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

    setuptools.setup(
        name="slib-sorter",
        version="1.2.2",
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
    ps_script(os.path.join(current_location, "src", "slib_sorter.py"))
    
def reload():
    importlib.reload(settings)
def __main__():
    try:
        install()
    except:
        reload()
__main__()