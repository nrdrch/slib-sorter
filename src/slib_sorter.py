import os, shutil, stat, argparse
import time
import json
from termcolor import colored
import os, shutil, stat, tempfile, json, ctypes, importlib



def join_corrected_paths(settings):
    # Load the settings from the file
    with open(settings, "r") as file:
        settings = json.load(file)

    paths = settings.get('Paths', {})
    joined_paths = {}

    for key, path in paths.items():
        corrected_path = path.replace("/", "\\")
        more_corrected_path = corrected_path.replace("~", os.environ['USERPROFILE'])
        joined_paths[key] = more_corrected_path
        check_dir(more_corrected_path)
    return joined_paths 
def clr_get(settings):
    settings_folder = os.path.join(os.environ['USERPROFILE'], 'Documents', 'WindowsPowerShell', 'Scripts', 'slib_sorter')
    settings = os.path.join(settings_folder, "settings.json")
    with open(settings, "r") as file:
        settings = json.load(file)
    Colors = settings.get('Colors', {})
    Parsed_Colors = {}
    for key, value in Colors.items():
        Parsed_Colors[key] = value
    return Parsed_Colors

def path_finder(levels_up=0):
    current_dir = os.path.abspath(os.path.dirname(__file__))
    if levels_up > 0:
        for _ in range(levels_up):
            current_dir = os.path.dirname(current_dir)
    return current_dir
#settings = os.path.join(path_finder(0), 'settings.json')
def check_dir(*paths):
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            pass
settings_folder = os.path.join(os.environ['USERPROFILE'], 'Documents', 'WindowsPowerShell', 'Scripts', 'slib_sorter')
settings = os.path.join(settings_folder, "settings.json")
j_clrs = clr_get(settings)
j_paths = join_corrected_paths(settings)
with open(settings, 'r') as file:
    settings = json.load(file)
def log_message(message, color, centered=False, newline=True):
    if centered:
        message = message.center(119)
    end = "\n" if newline else ""
    print(colored(message, color), end=end)

def log_console(file_name, seperator, dest_path, color):
    if settings.get("Show More Console Logs", True):
        log_message(f'{file_name}', f'{color}', False, False)
        log_message(f'{seperator}', f'{j_clrs.get("Foreground Color 2")}', False, False)
        log_message(f' {dest_path}', f'{j_clrs.get("Foreground Color 1")}', False, True)
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

file_path = path1 = j_paths.get('To Be Processed Directory')


path2 = j_paths.get('Name Of Top Library Directory')


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
current_location = path_finder(0)
source_file = os.path.join(current_location, 'slib_sorter.py')
settings_f = os.path.join(os.environ['USERPROFILE'], 'Documents', 'WindowsPowerShell', 'Scripts', 'slib_sorter', 'settings.json')
temp_content = "\nSorted Library Location:        "+ f"{j_paths.get('Name Of Top Library Directory')}"+ "\nSettings Location:     "+ f"{settings_f}"+ "\nPyhton Script Location:    " f"{os.path.join(current_location, 'slib_sorter.py')}"+ "\nTo Be Sorted Location:    " f"{j_paths.get('To Be Processed Directory')}"+ "\nRejected Files Location:     " f"{j_paths.get('Rejected Files Directory')}"


start_time = time.time()



#settings = os.path.join(path_finder(0), 'settings.json')
folder_path = path2
check_dir(path1, path2)
if settings.get("Run Shell Command On Startup", True):
    CmdOnStartup = settings.get("Command On Startup")
    os.system(CmdOnStartup)
else:
    pass
pattern_lists = {
    "Bass": ['bass', 'BS', 'BASS', 'Bass', 'sub', 'contrabass', 'BA', 'BS', 'Growl', 'GROWL', 'growl'],
    "BassLoops": ['bass_loop', 'bass_loops', 'Bass loops', 'D&B_Bass_Loop', 'Bass_Loop'],
    "DrumLoops": ['DnB_Drum_Loop', 'DRMLP', 'drum_loop', 'PRCLP', '_DnB_Drum_Loop_', 'MBeatbox', 'Drum_Loop', 'Top Drum Loop', 'Full Drum Loop' ,'Drum Loops', 'Drum Loop', 'Drum_Beat', 'drum_beat', 'drum_beats', 'fill', 'rundown', 'break', 'breaks', 'breakbeat', 'BREAK', 'Break', 'fills', 'Fills', 'FILLS', 'FILL', 'Fill', 'top loop', 'TOP loop', 'Top Loop'],
    "BassHits": ['Bass_Hit', 'Bass_Hits', 'bass_hit', 'bass_hits'], 
    "Melodic": ['KEY', 'Melodics', 'KEYS', 'Lead', 'Organ', 'organ', 'ORGAN', 'melodic', 'Melodic', 'MELODIC', 'Melody', 'Arp', 'arp', 'melodic_one_shot', 'Arpeggio', 'arpeggio', 'ARP', 'Melody', 'melody', 'Melody', 'SEQ', 'seq', 'Bells', 'BELLS', 'Bell', 'bell', 'bells', 'Piano', 'piano', 'PIANO', 'Vibraphone', 'vibraphone'],
    "MelodicLoops": ['melodic_loop', 'String Loop', 'cj_170_melodic_loop', 'MELODIC', 'Chord Loop', 'Melody','Melody Loop', 'Arp', 'arp', 'melodic_loop', 'Arpeggio', 'String Loops', 'string loops' ],
    "Lead": ['lead', 'LD', 'LEAD', 'LD', 'LEAD', 'Lead'],
    "Synth": ['Saw Loop', 'ARP', 'arp', 'Synth Loop', 'Synth', 'synth', 'SYNTH', 'SAW', 'saw', 'SY', 'SQ', 'SEQ', 'SAW', 'saw', 'SY', 'SQ', 'STAB', 'Stab', 'Synth_Loops', 'Synth_Loop'],
    "Pad": ['PAD', 'CHORD', 'CH', 'chords', 'Chords', 'CHORDS', 'CHORD', 'chord', 'Soft Chord', 'PD','PAD', 'PD', 'pad', 'Pad', 'Pad_Loop', 'Pad_Loop', 'Pad Loop'],
    "Keys": ['KEY', 'KEYS', 'keys',  'Brass', 'Organ', 'organ', 'ORGAN', 'Melody', 'melody', 'Melody', 'Piano', 'piano', 'PIANO', 'ELS' 'Vibraphone', 'vibraphone'],
    "Wind": ['flute', 'FLUTE', 'flutes', 'Flutes', 'Brass', 'tuba', 'Woodwind', 'Tuba', 'SAX', 'sax', 'Sax', 'Saxophone', 'saxophone', 'SAXOPHONE', 'taiko', 'Taiko', 'TAIKO', 'horns', 'HORNS', 'horn', 'HORN'],
    "String": [ 'Guitar', 'guitar', 'Violine'],
    "Plucks": ['PL', 'pluck', 'plucks', 'PLUCK', 'pl'],
    "DrumSnare": ['SNR', 'snare', 'Snare', 'SNARE', 'snares', 'Snares', 'SNARES', 'snr', 'RIM', 'Rim', 'rim', 'snap', 'SNAP', 'Snap', 'Snare', 'Snares'],
    "DrumClap": ['CLAP', 'clap', 'Clap', 'CLAPS', 'claps', 'Claps'],
    "DrumShakers": ['Shakers',],
    "DrumTom": ['tom', 'TOM'],
    "808": ['808'],
    "DrumPresets": ['KICK', 'SNARE', 'Break', 'BREAK', 'CLAP', 'PERC', 'Kick', 'DRUM', 'Drum', 'drum', 'DRUMS', 'Drums', 'Drum', 'drums', 'KICKS', 'SNARES', 'CLAPS', 'PERCS', 'kick', 'snare', 'clap', 'perc', 'PR'],
    "DrumKick": ['Kick', 'kick', 'KICK', 'Kicks', 'kicks'],
    "DrumHats": ['Cymbal', 'HiHat', 'HH','Ride','ride', 'RIDE', 'CRASH', 'crash', 'Crash', 'Crashes', 'cymbal', 'CYMBAL', 'Hat', 'hat', 'HATS', 'HAT', 'hats', 'Hats'],
    "DrumHatsClosed": ['closed', 'Closed', 'CLOSED', 'closed_hihat'],
    "DrumHatsOpen": ['Open', 'open', 'OPEN', 'OHat', 'open_hihat'],
    "DrumPercs": ['PERCUSSION', 'Bongo', 'BONGO', 'Conga', 'CONGA', 'bongo', 'conga', 'perc', 'PERC', 'percussion', 'Percussion', 'Perc'],
    "DrumShakers": ['shaker', 'Shaker', 'SHAKER', 'shakers', 'Shakers', 'SHAKERS'],
    "FX": ['fx', 'SFX', 'sfx', 'Drop Loop', 'FX', 'FF', 'beep', 'effect', 'Rise', 'Acid', 'Riser', 'riser', 'rise', 'Buildup', 'texture', 'textures', 'Texture', 'Textures', 'TEXTURE', 'TEXTURES', 'noise', 'NOISE', 'sfx', 'SFX', 'Gun', 'gun', 'Hits', 'hits', 'HITS', 'Birds', 'birds', 'nature', 'NATURE', 'Nature'],
    "Riser": ['Riser', 'riser', 'Buildup', 'Build up', 'build up', 'Rise', 'Rises','Buildup Loop', 'Buildup Drums'],
    "Vinyl": ['vinyl', 'Vinyl', 'Tape', 'taoe', 'crackle', 'Crackle'],
    "Noise": ['Noise', 'White Noise'],
    "Impact": ['Impact', 'IMPACT', 'impacts'],
    "Siren": ['siren', 'Siren', 'dubsiren', 'Dubsiren', 'DubSiren'],
    "Atmos": ['atmos', 'Air Can', 'Crickets', 'Walking', 'Footsteps','Ocean', 'ocean', 'Shells', 'Pots and Pans', 'Home Depot', 'Target Foley', 'Atmos', 'Billiards Foley', 'atmosphere', 'Walmart', 'atmospheres', 'Atmospheres', 'AT', 'ATMOSPHERE', 'ATMO', 'atmo'],
    "Voice": ['Voice', 'Talk', 'Rudeboy', 'vocal', 'Vocal', 'VV', 'Dialogue', 'VOCAL'],
    "VocalLoops": ['Vocal Loop', "vocal loops", 'Vocal_Loop', "vocal_loops",],
    "Vocal Chop": ['Vocal Chop', 'vocal chop'],
    "Vocal Arp": ['Vocal Arp', 'vocal arp', 'VOCAL ARP', 'VOCAL ARP'],
    "Chants": ['Chant', 'chant', 'Chants', 'chants'],
    "Phrases": ['Phrase', 'Phrases','PHRASE','PHRASES'],
    "Hooks": ['hook', 'Hook','Hooks'],
    "Vox": ['vox', 'VOX', 'Vox', 'Vocode', 'Vocoder', 'vocoder'],
    "Screams": ['Scream', 'Screamer', 'shout', 'SREAM', 'SCREAMER'],
    "Templates": ['temp', 'Temp', 'Template']
}
def sort_files(file_path, pattern_lists):
    total = 0
    num_failed = 0
    num_failed2 = 0
    num_succeeded = 0
    rejected_unsorted_path = j_paths.get('Rejected Files Directory')
    check_dir(rejected_unsorted_path)
    audio_exts = ["wav", "mp3", "aif", "aiff", "flac", "ogg", "WAV", "m4a"]
    plugin_exts = ["vst", "aax", "dll", "vst3"]
    seperator = settings.get("Console Log Seperator")
    for root, dirs, files in os.walk(file_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_name, file_extension = os.path.splitext(filename)
            file_extension = file_extension[1:]
            if file_extension in audio_exts:
                if any(pattern in file_name for pattern in pattern_lists.get("DrumPercs", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'Drum', 'Percussion')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumLoops", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'Drum', 'Loops')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("VocalLoops", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'Voice', 'Loops')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("MelodicLoops", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'Melodic', 'Loops')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("BassLoops", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'Melodic', 'Bass', 'Loops')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumKick", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'Drum', 'Kicks')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumSnare", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'Drum', 'Snares')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumShakers", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'Drum', 'Shakers')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Synth", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'Melodic', 'Synths')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Plucks", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'Melodic', 'Plucks')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Bass", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'Melodic', 'Bass')
                    if settings.get("Show More Console Logs", "True"):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Keys", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'Melodic', 'Keys')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Lead", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'Melodic', 'Lead')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Pad", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'Melodic', 'Pad')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Synth", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'Melodic', 'Synth')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Wind", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'Melodic', 'Wind')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("String", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'Melodic', 'String')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("BassHits", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'Melodic', 'Bass', 'Hits')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Riser", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'FX', 'Riser')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Noise", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'FX', 'Noise')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Siren", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'FX', 'Siren')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Vinyl", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'FX', 'Vinyl')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Impact", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'FX', 'Impact')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("FX", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'FX')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumClap", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'Drum', 'Claps')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumHats", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'Drum', 'Hats')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumTom", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'Drum', 'Toms')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("808", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'Drum', '808')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumPercs", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'Drum', 'Percussion')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Percs", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'Drum', 'Percussion')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumHats", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'Drum', 'Hats')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumHatsOpen", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'Drum', 'Hats', 'Open')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumHatsClosed", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'Drum', 'Hats', 'Closed')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Vox", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'Voice', 'Vox')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Vocal Chop", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'Voice', 'Vocal Chop')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Vocal Arp", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'Voice', 'Vocal Arp')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Hooks", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'Voice', 'Hooks')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Screams", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'Voice', 'Scream')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Chants", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'Voice', 'Chant')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Phrases", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'Voice', 'Phrases')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Voice", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'Voice')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Atmos", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'Atmos')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                else:
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Samples', 'Unsorted')
                    total += 1
                    num_failed += 1
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Unsorted File Color'))
                    else:
                        pass   
            elif file_extension in ["fxp"]:
                if any(pattern in file_name for pattern in pattern_lists.get("Bass", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Presets', 'Serum Presets', 'Bass')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Keys", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Presets', 'Serum Presets', 'Keys')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Plucks", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Presets', 'Serum Presets', 'Plucks')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Lead", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Presets', 'Serum Presets' ,'Lead')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Synth", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Presets', 'Serum Presets' ,'Synth')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Pad", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Presets', 'Serum Presets' ,'Pad')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("FX", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Presets', 'Serum Presets', 'FX')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Atmos", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Presets', 'Serum Presets', 'Atmos')
                    if settings.get("Show More Console Logs"):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                elif any(pattern in file_name for pattern in pattern_lists.get("Voice", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Presets', 'Serum Presets', 'Voice')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("808", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Presets', 'Serum Presets', '808')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumPresets", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Presets', 'Serum Presets', 'DrumPresets')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                else:
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Presets', 'Serum Presets', 'Unsorted')
                    total += 1
                    num_failed += 1
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
            elif file_extension in ["nki"]:
                total += 1
                num_succeeded += 1
                dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Presets', 'Native Instruments')
                if settings.get("Show More Console Logs", True):
                    log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                else:
                    pass
            elif file_extension in ["mid"]:
                if any(pattern in file_name for pattern in pattern_lists.get("DrumSnare", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Midi', 'Drum', 'Snares')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumClap", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Midi', 'Drum', 'Claps')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Melodic", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Midi', 'Melodic')
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumTom", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Midi', 'Drum', 'Toms')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("808", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Midi', 'Drum', '808')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumKick", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Midi', 'Drum', 'Kicks')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumPercs", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Midi', 'Drum', 'Percussion')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumShakers", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Midi', 'Drum', 'Shakers')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("FX", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Midi', 'FX')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumLoops", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Midi', 'Drum', 'Loops')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumHats", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Midi', 'Drum', 'Hats')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumHatsOpen", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Midi', 'Drum', 'Hats', 'Open')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumHatsClosed", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Midi', 'Drum', 'Hats', 'Closed')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Voice", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Midi', 'Voice')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Bass", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Midi', 'Bass')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Atmos", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Midi', 'Atmos')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                else:
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Midi', 'Unsorted')
                    total += 1
                    num_failed += 1
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
            elif file_extension in ["nmsv"]:
                if any(pattern in file_name for pattern in pattern_lists.get("Bass", [])):
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Presets', 'Massive Presets', 'Bass')
                    total += 1
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass  
                elif any(pattern in file_name for pattern in pattern_lists.get("Plucks", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Presets', 'Massive Presets', 'Plucks')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Keys", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Presets', 'Massive Presets', 'Keys')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Pad", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Presets', 'Massive Presets', 'Pad')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Lead", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Presets', 'Massive Presets', 'Lead')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Synth", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Presets', 'Massive Presets', 'Synth')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("FX", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Presets', 'Massive Presets', 'FX')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Atmos", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Presets', 'Massive Presets', 'Atmos')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Voice", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Presets', 'Massive Presets', 'Voice')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("808", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Presets', 'Massive Presets', '808')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumPresets", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Presets', 'Massive Presets', 'DrumPresets')
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                else:
                    dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Presets', 'Massive Presets', 'Unsorted')
                    total += 1
                    num_succeeded += 1
                    if settings.get("Show More Console Logs", True):
                        log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                    else:
                        pass
                        num_failed += 1
            elif file_extension in ["flp", "abl"] and any(pattern in file_name for pattern in pattern_lists.get("Templates")):
                total += 1
                num_succeeded += 1
                dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Projects', 'Templates')
                if settings.get("Show More Console Logs", True):
                    log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                else:
                    pass
            elif file_extension in ["flp", "abl"]:
                total += 1
                num_succeeded += 1
                dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Projects')
                if settings.get("Show More Console Logs", True):
                    log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                else:
                    pass
            elif file_extension in plugin_exts:
                total += 1
                num_succeeded += 1
                dest_path = os.path.join(j_paths.get('Name Of Top Library Directory'), 'Plugins')
                if settings.get("Show More Console Logs", True):
                    log_console(f'{file_name}', f'{seperator}', f'{dest_path}', j_clrs.get('Successfully Sorted File Color'))
                else:
                    pass
            else:
                dest_path = rejected_unsorted_path
                total += 1
                num_failed2 += 1
                if settings.get("Show More Console Logs", True):
                    log_console(f'{file_name}', f'{seperator}', f'{rejected_unsorted_path}', j_clrs.get('Rejected Filetype Color'))
                else:
                    pass
            organize_files_by_extension(rejected_unsorted_path)
            if not os.path.exists(os.path.join(dest_path, filename)):
                os.makedirs(dest_path, exist_ok="green")
                shutil.move(file_path, dest_path)
            else:
                pass
    elapsed_time = time.time() - start_time
    prompt1 = settings.get("Prompt")
    def remove_readonly(func, path, _):
        os.chmod(path, stat.S_IWRITE)
        func(path)
    shutil.rmtree(path1, onerror=remove_readonly)
    check_dir(path1)
    if settings.get("Show Top Title Bar", True):
        bar = settings.get("Top Title Bar")
        log_message(bar, f'{j_clrs.get("Top Title Bar Color")}', True, True)
    else:
        pass
    
    if settings.get("Show Statistics", True):
        log_message(prompt1, f'{j_clrs.get("Prompt Color")}', False, False)
        log_message(f'sorted by name & file type:   ', f'{j_clrs.get("Foregroud Color 1")}', False, False)
        log_message(f' {num_succeeded}', f'{j_clrs.get("Successfully Sorted File Color")}', False, False)
        log_message(prompt1, f'{j_clrs.get("Prompt Color")}', False, False)
        log_message(f'sorted only by file type: ', f'{j_clrs.get("Foregroud Color 1")}', False, False)
        log_message(f' {num_failed}', f'{j_clrs.get("Unsorted File Color")}', False, False)
        log_message(prompt1, f'{j_clrs.get("Prompt Color")}', False, False)
        log_message(f'rejected file types: ', f'{j_clrs.get("Foregroud Color 1")}', False, False)
        log_message(f' {num_failed2}', f'{j_clrs.get("Rejected Filetype Color")}', False, False)
        log_message(f'      {total}', f'{j_clrs.get("Statistics Value Color")}', False, False)
        log_message(f' files processed in ', f'{j_clrs.get("Foreground Color 2")}', False, False)
        log_message(f'{elapsed_time:.2f}', f'{j_clrs.get("Statistics Value Color")}', False, False)
        log_message(f' seconds', f'{j_clrs.get("Foreground Color 1")}', False, True)
        maxfile = settings.get('Max files per Dir')
        split_files_in_subdirectories(path2, max_files_per_dir=maxfile)
        file_count, dir_count, total_size_mb, total_size_gb = count_files_in_directory(f'{path2}')
        log_message(f'          in ', f'{j_clrs.get("Foreground Color 2")}', False, False)
        log_message(f'{settings.get("Name Of Top Library Directory")}', f'{j_clrs.get("Statistics Value Color")}', False, True)
        log_message(f'              files', f'{j_clrs.get("Foreground Color 2")}', False, False)
        log_message(f' {file_count}', f'{j_clrs.get("Statistics Value Color")}', False, True)
        log_message(f'                  subdirectories', f'{j_clrs.get("Foreground Color 2")}', False, False)
        log_message(f' {dir_count}', f'{j_clrs.get("Statistics Value Color")}', False, True)
        log_message(f'                      size', f'{j_clrs.get("Foreground Color 2")}', False, False)
        log_message(f' {total_size_mb:.2f}', f'{j_clrs.get("Statistics Value Color")}', False, False)
        log_message(f' mb ', f'{j_clrs.get("Foreground Color 1")}', False, False)
        log_message(f'or ', f'{j_clrs.get("Foreground Color 2")}', False, False)
        log_message(f'{total_size_gb:.2f}', f'{j_clrs.get("Statistics Value Color")}', False, False)
        log_message(f' gb', f'{j_clrs.get("Foreground Color 1")}', False, False)
        log_message(f'', f'{j_clrs.get("Foreground Color 1")}', False, True)
    else:
        pass
    def remove_readonly(func, path, _):
        os.chmod(path, stat.S_IWRITE)
        func(path)
    shutil.rmtree(path1, onerror=remove_readonly)
    check_dir(path1)
def print_help_message():
    parser = argparse.ArgumentParser()
    parser.add_argument("-paths", action="store_true")
    parser.add_argument("-help", action="store_true")
    parser.add_argument("-colors", action="store_true")
    parser.add_argument("-config", action="store_true")
    temp_file_path = temp_path_file(temp_content)
    args = parser.parse_args()
    spacer = "              "
    if args.paths:
        with open(temp_file_path, 'r') as file:
            temp_file_path = file.read()
        if settings.get("Run Shell Command On Startup", True):
            os.system(CmdOnStartup)
        else:
            pass
        bar = settings.get("Top Title Bar")
        log_message(bar, f'{j_clrs.get("Top Title Bar Color")}', True, True)
        log_message(temp_content, f'{j_clrs.get("Foregroud Color 1")}', False, True)
    elif args.colors:
        if settings.get("Run Shell Command On Startup", True):
            os.system(CmdOnStartup)
        else:
            pass
        bar = settings.get("Top Title Bar")
        log_message(bar, f'{j_clrs.get("Top Title Bar Color")}', True, True)
        clist = {
            "Colors": ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white', 'light_grey', 'dark_grey', 'light_red', 'light_green', 'light_yellow', 'light_blue', 'light_magenta', 'light_cyan']
        }
        colors = clist["Colors"]
        log_message("Possible Color Settings", f'{j_clrs.get("Statistics Value Color")}', False, False)
        log_message(':', f'{j_clrs.get("Foregroud Color 1")}', False, True)
        for color in colors:
            log_message(spacer+ color, f'{color}', False, True)
    elif args.help:
        if settings.get("Run Shell Command On Startup", True):
            os.system(CmdOnStartup)
        else:
            pass
        bar = settings.get("Top Title Bar")
        log_message(bar, f'{j_clrs.get("Top Title Bar Color")}', True, True)
        log_message('Help', f'{j_clrs.get("Statistics Value Color")}', False, False)
        log_message(':', f'{j_clrs.get("Foregroud Color 1")}', False, True)
        log_message('           -paths '+ f'{spacer}', f'{j_clrs.get("Foregroud Color 1")}', False, False)
        log_message('Displays Paths', f'{j_clrs.get("Statistics Value Color")}', False, True)
        log_message('           -colors'+ f'{spacer}', f'{j_clrs.get("Foregroud Color 1")}', False, False)
        log_message('Displays Possible Color Settings', f'{j_clrs.get("Statistics Value Color")}', False, True)
        log_message('           -config'+ f'{spacer}', f'{j_clrs.get("Foregroud Color 1")}', False, False)
        log_message('Launch Config File', f'{j_clrs.get("Statistics Value Color")}', False, True)
        log_message('           -help  '+ f'{spacer}', f'{j_clrs.get("Foregroud Color 1")}', False, False)
        log_message('Displays Help', f'{j_clrs.get("Statistics Value Color")}', False, True)
    elif args.config:
        settingsfile = settings_f
        cmd = "Start "+ f'{settingsfile}'
        os.system(cmd)
    else:
        sort_files(path1, pattern_lists) 
def __main__():
    print_help_message()