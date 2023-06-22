import os, shutil, stat
from termcolor import colored
import json
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
settings = os.path.join(os.environ['USERPROFILE'], 'Documents', 'Sorter', 'settings.json')

with open(settings, 'r') as file:
    settings = json.load(file)
file_path = path1 = os.path.join(os.environ['USERPROFILE'], 'Desktop', settings.get('To Be Processed Directory'))
path2 = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"))
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
                os.makedirs(new_dir_path)
            for i, file_name in enumerate(files):
                old_file_path = os.path.join(root, file_name)
                new_dir_index = i // max_files_per_dir
                start_index = new_dir_index * max_files_per_dir
                end_index = min((new_dir_index + 1) * max_files_per_dir, num_files)
                new_dir_name = f"{start_index}-{end_index-1}"
                new_dir_path = os.path.join(root, new_dir_name)
                new_file_path = os.path.join(new_dir_path, file_name)
                shutil.move(old_file_path, new_file_path)
