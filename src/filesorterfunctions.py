import os, shutil, stat, tempfile
from termcolor import colored
import json
import ctypes
def path_finder(levels_up=0):
    current_dir = os.path.abspath(os.path.dirname(__file__))
    if levels_up > 0:
        for _ in range(levels_up):
            current_dir = os.path.dirname(current_dir)
    return current_dir
settings = os.path.join(path_finder(1), 'settings.json')
def check_dir(*paths):
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)
def log_message(message, color, centered=False, newline=True):
    if centered:
        message = message.center(119)
    end = "\n" if newline else ""
    print(colored(message, color), end=end)
def log_console(file_name, seperator, dest_path, color):
    if settings.get("Show More Console Logs", True):
        log_message(f'{file_name}', f'{color}', False, False)
        log_message(f'{seperator}', "dark_grey", False, False)
        log_message(f' {dest_path}', "white", False, True)
    else:
        pass
def check_if(*paths):
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)
def ps_script(source_file):
    winpro = os.path.join(os.environ['USERPROFILE'],'Documents', 'WindowsPowerShell')
    powershell_scripts_folder = os.path.join(winpro, 'Scripts')
    if not os.path.exists(powershell_scripts_folder):
        os.makedirs(powershell_scripts_folder)
    powershell_script_file = os.path.join(powershell_scripts_folder, 'slib-sorter' + ".psm1")
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
    with open(powershell_script_file, 'w') as f:
        f.write(script_content)
    profile_path = os.path.expanduser("~/Documents/WindowsPowerShell/Microsoft.PowerShell_profile.ps1")
    with open(profile_path, 'r') as f:
        profile_content = f.read()
        if f"Import-Module -DisableNameChecking \"{powershell_script_file}\"" in profile_content:
            pass
        else:
            with open(profile_path, 'a') as f:
                f.write(f"\nImport-Module -DisableNameChecking \"{powershell_script_file}\"")
def change_folder_icon(folder_path, icon_path):
    if not os.path.exists(folder_path):
        print("Folder does not exist.")
        return
    folder_path = os.path.abspath(folder_path)
    try:
        ini_path = os.path.join(folder_path, "desktop.ini")
        with open(ini_path, "w") as ini_file:
            ini_file.write("[.ShellClassInfo]\n")
            ini_file.write(f"IconFile={icon_path}\n")
            ini_file.write("IconIndex=0\n")
        ctypes.windll.kernel32.SetFileAttributesW(ini_path, 0x2 | 0x4)
        ctypes.windll.shell32.SHChangeNotify(0x08000000, 0x0000, None, None)
        print("Folder icon changed successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
with open(settings, 'r') as file:
    settings = json.load(file)
file_path = path1 = os.path.join(os.environ['USERPROFILE'], settings.get('TBPDPath'), settings.get('To Be Processed Directory'))
path2 = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"))
if settings.get("Run Shell Command On Startup", True):
    CmdOnStartup = settings.get("Command On Startup")
    os.system(CmdOnStartup)
else:
    pass
def organize_files_by_extension(path):
    if not os.path.isdir(path):
        raise Exception("The path provided is not a directory.")
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    for file in files:
        file_name, file_extension = os.path.splitext(file)
        if file_extension:
            subfolder_name = file_extension.lstrip(".")
        else:
            subfolder_name = "typeless"
        subfolder_path = os.path.join(path, subfolder_name)
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)
        file_path = os.path.join(path, file)
        shutil.move(file_path, os.path.join(subfolder_path, file))
def remove_empty_lines(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    lines = [line for line in lines if line.strip() != '']
    with open(file_path, 'w') as file:
        file.writelines(lines)
    return len(lines)
def count_files_in_directory(path):
    file_count = 0
    dir_count = 0
    total_size = 0
    for root, dirs, files in os.walk(path):
        file_count += len(files)
        dir_count += len(dirs)
        for file in files:
            file_path = os.path.join(root, file)
            total_size += os.path.getsize(file_path)
    total_size_mb = total_size / (1024 * 1024)
    total_size_gb = total_size_mb / 1024
    return file_count, dir_count, total_size_mb, total_size_gb
def remove_directory_tree(path):
    if os.path.isdir(path):
        for child_path in os.listdir(path):
            child_path = os.path.join(path, child_path)
            remove_directory_tree(child_path)
    try:
        os.remove(path)
    except OSError as error:
        os.chmod(path, stat.S_IWRITE)
        os.remove(path)
def split_files_in_subdirectories(path2, max_files_per_dir=50):
    for root, dirs, files in os.walk(path2):
        if root == path2:
            continue
        num_files = len(files)
        dir_count = len(dirs)
        if num_files > max_files_per_dir:
            dir_count = num_files // max_files_per_dir
            if num_files % max_files_per_dir != 0:
                dir_count += 1
            for i in range(dir_count):
                start_index = i * max_files_per_dir
                end_index = min((i + 1) * max_files_per_dir, num_files)
                new_dir_name = f"{start_index}-{end_index-1}"
                new_dir_path = os.path.join(root, new_dir_name)
                try:
                    os.mkdir(new_dir_path)
                except FileExistsError:
                    print()
            for i, file_name in enumerate(files):
                old_file_path = os.path.join(root, file_name)
                new_dir_index = i // max_files_per_dir
                start_index = new_dir_index * max_files_per_dir
                end_index = min((new_dir_index + 1) * max_files_per_dir, num_files)
                new_dir_name = f"{start_index}-{end_index-1}"
                new_dir_path = os.path.join(root, new_dir_name)
                new_file_path = os.path.join(new_dir_path, file_name)
                shutil.move(old_file_path, new_file_path)
def temp_path_file(temp_content):
    temp_dir = tempfile.gettempdir()
    file_path = tempfile.mktemp(dir=temp_dir)
    with open(file_path, 'a') as file:
        if isinstance(temp_content, dict):
            json.dump(temp_content, file)
        else:
            file.write(temp_content)
    return file_path
