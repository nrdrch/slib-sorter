import os, shutil, stat, argparse
import filesorterfunctions as fsf

import time
import json
start_time = time.time()
current_location = fsf.path_finder(0)
source_file = os.path.join(current_location, 'slib-sorter.py')
fsf.ps_script(source_file)


icon_path = os.path.join(fsf.path_finder(1), 'examples', 'icn.ico')

settings = os.path.join(fsf.path_finder(1), 'settings.json')
with open(settings, 'r') as file:
    settings = json.load(file)
file_path = path1 = os.path.join(os.environ['USERPROFILE'], settings.get('TBPDPath'), settings.get('To Be Processed Directory'))
path2 = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"))
folder_path = path2
#fsf.change_folder_icon(folder_path, icon_path)
fsf.check_dir(path1, path2)
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
    rejected_unsorted_path = os.path.join(os.environ['USERPROFILE'], settings.get('RFPath'), settings.get("Rejected Files"))
    fsf.check_if(rejected_unsorted_path)
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
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'Drum', 'Percussion')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumLoops", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'Drum', 'Loops')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("VocalLoops", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'Voice', 'Loops')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("MelodicLoops", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'Melodic', 'Loops')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("BassLoops", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'Melodic', 'Bass', 'Loops')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumKick", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'Drum', 'Kicks')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumSnare", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'Drum', 'Snares')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumShakers", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'Drum', 'Shakers')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Synth", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'Melodic', 'Synths')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass

                elif any(pattern in file_name for pattern in pattern_lists.get("Plucks", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'Melodic', 'Plucks')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Bass", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'Melodic', 'Bass')
                    if settings.get("Show More Console Logs", "True"):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Keys", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'Melodic', 'Keys')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Lead", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'Melodic', 'Lead')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Pad", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'Melodic', 'Pad')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Synth", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'Melodic', 'Synth')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Wind", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'Melodic', 'Wind')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("String", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'Melodic', 'String')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("BassHits", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'Melodic', 'Bass', 'Hits')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass


                elif any(pattern in file_name for pattern in pattern_lists.get("Riser", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'FX', 'Riser')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Noise", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'FX', 'Noise')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Siren", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'FX', 'Siren')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Vinyl", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'FX', 'Vinyl')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Impact", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'FX', 'Impact')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("FX", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'FX')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumClap", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'Drum', 'Claps')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumHats", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'Drum', 'Hats')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumTom", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'Drum', 'Toms')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("808", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'Drum', '808')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumPercs", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'Drum', 'Percussion')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Percs", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'Drum', 'Percussion')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumHats", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'Drum', 'Hats')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumHatsOpen", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'Drum', 'Hats', 'Open')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumHatsClosed", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'Drum', 'Hats', 'Closed')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass

                elif any(pattern in file_name for pattern in pattern_lists.get("Vox", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'Voice', 'Vox')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Vocal Chop", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'Voice', 'Vocal Chop')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Vocal Arp", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'Voice', 'Vocal Arp')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Hooks", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'Voice', 'Hooks')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Screams", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'Voice', 'Scream')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Chants", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'Voice', 'Chant')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Phrases", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'Voice', 'Phrases')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Voice", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'Voice')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Atmos", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'Atmos')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                else:
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Samples', 'Unsorted')
                    total += 1
                    num_failed += 1
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "yellow")
                    else:
                        pass   
            elif file_extension in ["fxp"]:
                if any(pattern in file_name for pattern in pattern_lists.get("Bass", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Presets', 'Serum Presets', 'Bass')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Keys", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Presets', 'Serum Presets', 'Keys')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Plucks", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Presets', 'Serum Presets', 'Plucks')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Lead", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Presets', 'Serum Presets' ,'Lead')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Synth", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Presets', 'Serum Presets' ,'Synth')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Pad", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Presets', 'Serum Presets' ,'Pad')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("FX", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Presets', 'Serum Presets', 'FX')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Atmos", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Presets', 'Serum Presets', 'Atmos')
                    if settings.get("Show More Console Logs"):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                elif any(pattern in file_name for pattern in pattern_lists.get("Voice", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Presets', 'Serum Presets', 'Voice')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("808", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Presets', 'Serum Presets', '808')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumPresets", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Presets', 'Serum Presets', 'DrumPresets')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                else:
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Presets', 'Serum Presets', 'Unsorted')
                    total += 1
                    num_failed += 1
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
            elif file_extension in ["nki"]:
                total += 1
                num_succeeded += 1
                dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Presets', 'Native Instruments')
                if settings.get("Show More Console Logs", True):
                    fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                else:
                    pass
            elif file_extension in ["mid"]:
                if any(pattern in file_name for pattern in pattern_lists.get("DrumSnare", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Midi', 'Drum', 'Snares')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumClap", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Midi', 'Drum', 'Claps')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Melodic", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Midi', 'Melodic')
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumTom", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Midi', 'Drum', 'Toms')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("808", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Midi', 'Drum', '808')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumKick", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Midi', 'Drum', 'Kicks')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumPercs", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Midi', 'Drum', 'Percussion')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumShakers", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Midi', 'Drum', 'Shakers')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("FX", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Midi', 'FX')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumLoops", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Midi', 'Drum', 'Loops')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumHats", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Midi', 'Drum', 'Hats')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumHatsOpen", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Midi', 'Drum', 'Hats', 'Open')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumHatsClosed", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Midi', 'Drum', 'Hats', 'Closed')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Voice", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Midi', 'Voice')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Bass", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Midi', 'Bass')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Atmos", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Midi', 'Atmos')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                else:
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Midi', 'Unsorted')
                    total += 1
                    num_failed += 1
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
            elif file_extension in ["nmsv"]:
                if any(pattern in file_name for pattern in pattern_lists.get("Bass", [])):
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Presets', 'Massive Presets', 'Bass')
                    total += 1
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass  
                elif any(pattern in file_name for pattern in pattern_lists.get("Plucks", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Presets', 'Massive Presets', 'Plucks')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Keys", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Presets', 'Massive Presets', 'Keys')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Pad", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Presets', 'Massive Presets', 'Pad')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Lead", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Presets', 'Massive Presets', 'Lead')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Synth", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Presets', 'Massive Presets', 'Synth')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("FX", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Presets', 'Massive Presets', 'FX')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Atmos", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Presets', 'Massive Presets', 'Atmos')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Voice", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Presets', 'Massive Presets', 'Voice')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("808", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Presets', 'Massive Presets', '808')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumPresets", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Presets', 'Massive Presets', 'DrumPresets')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                else:
                    dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Presets', 'Massive Presets', 'Unsorted')
                    total += 1
                    num_succeeded += 1
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                        num_failed += 1
            elif file_extension in ["flp", "abl"] and any(pattern in file_name for pattern in pattern_lists.get("Templates")):
                total += 1
                num_succeeded += 1
                dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Projects', 'Templates')
                if settings.get("Show More Console Logs", True):
                    fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                else:
                    pass
            elif file_extension in ["flp", "abl"]:
                total += 1
                num_succeeded += 1
                dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Projects')
                if settings.get("Show More Console Logs", True):
                    fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                else:
                    pass
            elif file_extension in plugin_exts:
                total += 1
                num_succeeded += 1
                dest_path = os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get("Name Of Top Library Directory"), 'Plugins')
                if settings.get("Show More Console Logs", True):
                    fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                else:
                    pass
            else:
                dest_path = rejected_unsorted_path
                total += 1
                num_failed2 += 1
                if settings.get("Show More Console Logs", True):
                    fsf.log_console(f'{file_name}', f'{seperator}', f'{rejected_unsorted_path}', "red")
                else:
                    pass
            fsf.organize_files_by_extension(rejected_unsorted_path)
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
    fsf.check_if(path1)
    #fsf.split_files_in_subdirectories(path2, max_files_per_dir=50)
    def remove_readonly(func, path, _):
        os.chmod(path, stat.S_IWRITE)
        func(path)
    shutil.rmtree(path1, onerror=remove_readonly)
    fsf.check_if(path1)
    if settings.get("Show Top Bar", True):
        bar = settings.get("Top Bar")
        fsf.log_message(bar, f'{settings.get("Top Bar Color")}', True, True)
        
    else:
        pass
    if settings.get("Show Statistics", True):
        fsf.log_message(prompt1, f'{settings.get("Prompt Color")}', False, False)
        fsf.log_message(f'sorted by name & file type:   ', f'{settings.get("Foregroud Color 1")}', False, False)
        fsf.log_message(f' {num_succeeded}', "green")
        fsf.log_message(prompt1, f'{settings.get("Prompt Color")}', False, False)
        fsf.log_message(f'sorted only by file type: ', f'{settings.get("Foregroud Color 1")}', False, False)
        fsf.log_message(f' {num_failed}', "yellow")
        fsf.log_message(prompt1, f'{settings.get("Prompt Color")}', False, False)
        fsf.log_message(f'rejected file types: ', f'{settings.get("Foregroud Color 1")}', False, False)
        fsf.log_message(f' {num_failed2}', "red")
        fsf.log_message(f'      {total}', f'{settings.get("Statistics Value Color")}', False, False)
        fsf.log_message(f' files processed in ', "dark_grey", False, False)
        fsf.log_message(f'{elapsed_time:.2f}', f'{settings.get("Statistics Value Color")}', False, False)
        fsf.log_message(f' seconds', "dark_grey", False, True)
        maxfile = settings.get('Max files per Dir')
        fsf.split_files_in_subdirectories(path2, max_files_per_dir=maxfile)
        file_count, dir_count, total_size_mb, total_size_gb = fsf.count_files_in_directory(f'{path2}')
        fsf.log_message(f'          in ', "dark_grey", False, False)
        fsf.log_message(f'{settings.get("Name Of Top Library Directory")}', f'{settings.get("Statistics Value Color")}', False, True)
        fsf.log_message(f'              files', "dark_grey", False, False)
        fsf.log_message(f' {file_count}', f'{settings.get("Statistics Value Color")}', False, True)
        fsf.log_message(f'                  subdirectories', "dark_grey", False, False)
        fsf.log_message(f' {dir_count}', f'{settings.get("Statistics Value Color")}', False, True)
        fsf.log_message(f'                      size', "dark_grey", False, False)
        fsf.log_message(f' {total_size_mb:.2f}', f'{settings.get("Statistics Value Color")}', False, False)
        fsf.log_message(f' mb ', "light_grey", False, False)
        fsf.log_message(f'or ', "dark_grey", False, False)
        fsf.log_message(f'{total_size_gb:.2f}', f'{settings.get("Statistics Value Color")}', False, False)
        fsf.log_message(f' gb', "light_grey", False, False)
        fsf.log_message(f'', "light_grey", False, False)
    else:
        pass
    def remove_readonly(func, path, _):
        os.chmod(path, stat.S_IWRITE)
        func(path)
    shutil.rmtree(path1, onerror=remove_readonly)
    fsf.check_dir(path1)
sort_files(path1, pattern_lists)
temp_content = "\nSorted Library Location:        " f"{os.path.join(os.environ['USERPROFILE'], settings.get('NOFLDPath'), settings.get('Name Of Top Library Directory'))}"+ "\nSettings Location:     "+ f"{os.path.join(fsf.path_finder(1), 'settings.json')}"+ "\nPyhton Script Location:    " f"{os.path.join(current_location, 'slib-sorter.py')}"+ "\nTo Be Sorted Location:    " f"{os.path.join(os.environ['USERPROFILE'], settings.get('TBPDPath'), settings.get('To Be Processed Directory'))}"+ "\nRejected Files Location:     " f"{os.path.join(os.environ['USERPROFILE'], settings.get('RFPath'), settings.get('Rejected Files'))}"
print('')
def print_help_message():
    parser = argparse.ArgumentParser()
    parser.add_argument("-Paths", action="store_true", help="Print the paths.")
    parser.add_argument("-Help", action="store_true", help="Print the manual.")
    parser.add_argument("-Colors", action="store_true", help="Print the possible color settings.")
    temp_file_path = fsf.temp_path_file(temp_content)
    args = parser.parse_args()
    if args.Paths:
        with open(temp_file_path, 'r') as file:
    # Read the contents of the file
            temp_file_path = file.read()
    
    # Print the contents
            os.system('cls')
            bar = settings.get("Top Bar")
            fsf.log_message(bar, f'{settings.get("Top Bar Color")}', True, True)
            print(temp_file_path)
    elif args.Colors:
        os.system('cls')
        bar = settings.get("Top Bar")
        fsf.log_message(bar, f'{settings.get("Top Bar Color")}', True, True)
        clist = {
            "Colors": ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white', 'light_grey', 'dark_grey', 'light_red', 'light_green', 'light_yellow', 'light_blue', 'light_magenta', 'light_cyan']
        }
        colors = clist["Colors"]
        for color in colors:
            fsf.log_message(color, f'{color}', True, True)
    elif args.Help:
        os.system('cls')
        bar = settings.get("Top Bar")
        fsf.log_message(bar, f'{settings.get("Top Bar Color")}', True, True)
        fsf.log_message('Help: ', f'{settings.get("Foregroud Color 1")}', False, True)
        fsf.log_message('           -Paths      = Displays Paths', f'{settings.get("Foregroud Color 1")}', False, True)
        fsf.log_message('           -Colors      = Displays Color Options', f'{settings.get("Foregroud Color 1")}', False, True)
        fsf.log_message('           -Help      = Displays Help', f'{settings.get("Foregroud Color 1")}', False, True)
    else:
        pass
    
print_help_message()

