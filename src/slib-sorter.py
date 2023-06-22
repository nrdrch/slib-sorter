import os, shutil, stat
import filesorterfunctions as fsf
import time
import json

settings = os.path.join(os.environ['USERPROFILE'], 'Documents', 'slib-sorter', 'settings.json')

with open(settings, 'r') as file:
    settings = json.load(file)
file_path = path1 = os.path.join(os.environ['USERPROFILE'], 'Desktop', settings.get('To Be Processed Directory'))
path2 = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"))
fsf.check_dir(path1, path2)
if settings.get("Run Shell Command On Startup", True):
    CmdOnStartup = settings.get("Command On Startup")
    os.system(CmdOnStartup)
else:
    pass
pattern_lists = {
    "Bass": ['bass', 'BS', 'BASS', 'Bass', 'sub', 'contrabass', 'BA', 'BS', 'Growl', 'GROWL', 'growl'],
    "BassLoops": ['bass_loop', 'bass_loops', 'Bass loops', 'D&B_Bass_Loop', 'Bass_Loop'],
    "DrumLoops": ['DnB_Drum_Loop', '_DnB_Drum_Loop_', 'Drum_Loop', 'Drum Loops', 'Drum_Beat', 'drum_beat', 'drum_beats', 'fill', 'rundown', 'break', 'breaks', 'breakbeat', 'BREAK', 'Break', 'fills', 'Fills', 'FILLS', 'FILL', 'Fill', 'top', 'TOP', 'Top'],
    "BassHits": ['Bass_Hit', 'Bass_Hits', 'bass_hit', 'bass_hits'], 
    "Melodic": ['KEY', 'KEYS', 'Lead', 'Organ', 'organ', 'ORGAN', 'melodic', 'Melodic', 'MELODIC', 'Melody', 'Arp', 'arp', 'Arpeggio', 'arpeggio', 'ARP', 'Melody', 'melody', 'Melody', 'SEQ', 'seq', 'Bells', 'BELLS', 'Bell', 'bell', 'bells', 'Piano', 'piano', 'PIANO', 'Vibraphone', 'vibraphone'],
    "MelodicLoops": ['melodic_loop','cj_170_melodic_loop', 'MELODIC', 'Melody','Melody Loop', 'Arp', 'arp', 'melodic_loop', 'Arpeggio', 'String Loops', 'string loops' ],
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
    "FX": ['fx', 'SFX', 'sfx', 'FX', 'FF', 'beep', 'effect', 'Rise', 'Riser', 'riser', 'rise', 'Buildup', 'texture', 'textures', 'Texture', 'Textures', 'TEXTURE', 'TEXTURES', 'noise', 'NOISE', 'sfx', 'SFX', 'Gun', 'gun', 'Hits', 'hits', 'HITS', 'Birds', 'birds', 'nature', 'NATURE', 'Nature'],
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
    "Screams": ['Scream', 'Screamer', 'shout', 'SREAM', 'SCREAMER']
}
def sort_files(file_path, pattern_lists):
    start_time = time.time()
    total = 0
    num_failed = 0
    num_failed2 = 0
    num_succeeded = 0
    rejected_unsorted_path = os.path.join(os.environ['USERPROFILE'], "Desktop", settings.get("Rejected Files"))
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
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'Drum', 'Percussion')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumLoops", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'Drum', 'Loops')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("VocalLoops", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'Voice', 'Loops')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("MelodicLoops", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'Melodic', 'Loops')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("BassLoops", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'Melodic', 'Bass', 'Loops')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumKick", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'Drum', 'Kicks')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumSnare", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'Drum', 'Snares')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumShakers", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'Drum', 'Shakers')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Synth", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'Melodic', 'Synths')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass

                elif any(pattern in file_name for pattern in pattern_lists.get("Plucks", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'Melodic', 'Plucks')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Bass", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'Melodic', 'Bass')
                    if settings.get("Show More Console Logs", "True"):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Keys", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'Melodic', 'Keys')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Lead", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'Melodic', 'Lead')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Pad", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'Melodic', 'Pad')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Synth", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'Melodic', 'Synth')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Wind", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'Melodic', 'Wind')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("String", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'Melodic', 'String')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("BassHits", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'Melodic', 'Bass', 'Hits')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass


                elif any(pattern in file_name for pattern in pattern_lists.get("Riser", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'FX', 'Riser')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Noise", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'FX', 'Noise')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Siren", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'FX', 'Siren')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Vinyl", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'FX', 'Vinyl')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Impact", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'FX', 'Impact')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("FX", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'FX')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumClap", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'Drum', 'Claps')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumHats", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'Drum', 'Hats')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumTom", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'Drum', 'Toms')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("808", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'Drum', '808')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumPercs", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'Drum', 'Percussion')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Percs", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'Drum', 'Percussion')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumHats", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'Drum', 'Hats')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumHatsOpen", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'Drum', 'Hats', 'Open')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumHatsClosed", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'Drum', 'Hats', 'Closed')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass

                elif any(pattern in file_name for pattern in pattern_lists.get("Vox", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'Voice', 'Vox')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Vocal Chop", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'Voice', 'Vocal Chop')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Vocal Arp", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'Voice', 'Vocal Arp')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Hooks", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'Voice', 'Hooks')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Screams", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'Voice', 'Scream')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Chants", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'Voice', 'Chant')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Phrases", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'Voice', 'Phrases')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Voice", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'Voice')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Atmos", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'Atmos')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                else:
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Samples', 'Unsorted')
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
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Serum Presets', 'Bass')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Keys", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Serum Presets', 'Keys')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Plucks", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Serum Presets', 'Plucks')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Lead", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Serum Presets' ,'Lead')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Synth", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Serum Presets' ,'Synth')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Pad", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Serum Presets' ,'Pad')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("FX", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Serum Presets', 'FX')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Atmos", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Serum Presets', 'Atmos')
                    if settings.get("Show More Console Logs"):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                elif any(pattern in file_name for pattern in pattern_lists.get("Voice", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Serum Presets', 'Voice')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("808", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Serum Presets', '808')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumPresets", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Serum Presets', 'DrumPresets')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                else:
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Serum Presets', 'Unsorted')
                    total += 1
                    num_failed += 1
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
            elif file_extension in ["nki"]:
                total += 1
                num_succeeded += 1
                dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Native Instruments')
                if settings.get("Show More Console Logs", True):
                    fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                else:
                    pass
            elif file_extension in ["mid"]:
                if any(pattern in file_name for pattern in pattern_lists.get("DrumSnare", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Midi', 'Drum', 'Snares')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumClap", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Midi', 'Drum', 'Claps')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Melodic", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Midi', 'Melodic')
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumTom", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Midi', 'Drum', 'Toms')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("808", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Midi', 'Drum', '808')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumKick", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Midi', 'Drum', 'Kicks')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumPercs", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Midi', 'Drum', 'Percussion')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumShakers", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Midi', 'Drum', 'Shakers')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("FX", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Midi', 'FX')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumLoops", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Midi', 'Drum', 'Loops')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumHats", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Midi', 'Drum', 'Hats')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumHatsOpen", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Midi', 'Drum', 'Hats', 'Open')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumHatsClosed", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Midi', 'Drum', 'Hats', 'Closed')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Voice", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Midi', 'Voice')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Bass", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Midi', 'Bass')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Atmos", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Midi', 'Atmos')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                else:
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Midi', 'Unsorted')
                    total += 1
                    num_failed += 1
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
            elif file_extension in ["nmsv"]:
                if any(pattern in file_name for pattern in pattern_lists.get("Bass", [])):
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Massive Presets', 'Bass')
                    total += 1
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass  
                elif any(pattern in file_name for pattern in pattern_lists.get("Plucks", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Massive Presets', 'Plucks')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Keys", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Massive Presets', 'Keys')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Pad", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Massive Presets', 'Pad')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Lead", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Massive Presets', 'Lead')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Synth", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Massive Presets', 'Synth')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("FX", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Massive Presets', 'FX')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Atmos", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Massive Presets', 'Atmos')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("Voice", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Massive Presets', 'Voice')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("808", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Massive Presets', '808')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                elif any(pattern in file_name for pattern in pattern_lists.get("DrumPresets", [])):
                    total += 1
                    num_succeeded += 1
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Massive Presets', 'DrumPresets')
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                else:
                    dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Massive Presets', 'Unsorted')
                    total += 1
                    num_succeeded += 1
                    if settings.get("Show More Console Logs", True):
                        fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                    else:
                        pass
                        num_failed += 1
            elif file_extension in plugin_exts:
                total += 1
                num_succeeded += 1
                dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Plugins')
                if settings.get("Show More Console Logs", True):
                    fsf.log_console(f'{file_name}', f'{seperator}', f'{dest_path}', "green")
                else:
                    pass
            elif file_extension in ["flp", "abl"]:
                total += 1
                num_succeeded += 1
                dest_path = os.path.join(os.environ['USERPROFILE'], 'Documents', settings.get("Name Of Top Library Directory"), 'Projects')
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
                total += 1
            else:
                pass
    elapsed_time = time.time() - start_time
    prompt1 = settings.get("Prompt")
    def remove_readonly(func, path, _):
        os.chmod(path, stat.S_IWRITE)
        func(path)
    shutil.rmtree(path1, onerror=remove_readonly)
    fsf.check_if(path1)
    fsf.split_files_in_subdirectories(path2, max_files_per_dir=50)
    def remove_readonly(func, path, _):
        os.chmod(path, stat.S_IWRITE)
        func(path)
    shutil.rmtree(path1, onerror=remove_readonly)
    fsf.check_if(path1)
    if settings.get("Show Top Bar", True):
        bar = settings.get("Top Bar")
        fsf.log_message(bar, "dark_grey", True, True)
    else:
        pass
    if settings.get("Show Statistics", True):
        fsf.log_message(prompt1, "dark_grey", False, False)
        fsf.log_message(f'sorted by name & file type:   ', "white", False, False)
        fsf.log_message(f' {num_succeeded}', "green")
        fsf.log_message(prompt1, "dark_grey", False, False)
        fsf.log_message(f'sorted only by file type: ', "white", False, False)
        fsf.log_message(f' {num_failed}', "yellow")
        fsf.log_message(prompt1, "dark_grey", False, False)
        fsf.log_message(f'rejected file types: ', "white", False, False)
        fsf.log_message(f' {num_failed2}', "red")
        fsf.log_message(f'      {total}', "blue", False, False)
        fsf.log_message(f' files processed in ', "dark_grey", False, False)
        fsf.log_message(f'{elapsed_time:.2f}', "blue", False, False)
        fsf.log_message(f' seconds', "dark_grey", False, True)
        fsf.split_files_in_subdirectories(path2, max_files_per_dir=50)
        file_count, dir_count, total_size_mb, total_size_gb = fsf.count_files_in_directory(f'{path2}')
        fsf.log_message(f'          in ', "dark_grey", False, False)
        fsf.log_message(f'{settings.get("Name Of Top Library Directory")}', "light_grey", False, True)
        fsf.log_message(f'              files', "dark_grey", False, False)
        fsf.log_message(f' {file_count}', "blue", False, True)
        fsf.log_message(f'                  subdirectories', "dark_grey", False, False)
        fsf.log_message(f' {dir_count}', "blue", False, True)
        fsf.log_message(f'                      size', "dark_grey", False, False)
        fsf.log_message(f' {total_size_mb:.2f}', "blue", False, False)
        fsf.log_message(f' mb ', "light_grey", False, False)
        fsf.log_message(f'or ', "dark_grey", False, False)
        fsf.log_message(f'{total_size_gb:.2f}', "blue", False, False)
        fsf.log_message(f' gb', "light_grey", False, False)
    else:
        pass
    def remove_readonly(func, path, _):
        os.chmod(path, stat.S_IWRITE)
        func(path)
    shutil.rmtree(path1, onerror=remove_readonly)
    fsf.check_dir(path1)
sort_files(path1, pattern_lists)
