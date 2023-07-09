# Sample Library Sorter
###### *for now only meant to run on Windows10
> This script allows you to quickly sort a massive amount of files, any kind you might find in your Sample Library as a Music Producer. For now, it will match after file name & type to the best of its abilitys. If you're curious about what it is matching the files against:  
<details>
<summary>
Look at this son of a book
</summary>

```
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
```
</details>

##### Audio, Project Files & Plugin Presets (for now just Serum and Massive)
### Dependecies 
#### [Python](https://www.python.org/downloads/), [termcolor 2.3.0 ](https://pypi.org/project/termcolor/)
### Installation 
> from [PyPI](https://pypi.org/)
```
py -m pip install --upgrade slib-sorter
```
> from [GitHub ](https://github.com/nrdrch/slib-sorter.git)
```
git clone https://github.com/nrdrch/slib-sorter.git; python3 \slib-sorter\src\slib-sorter.py
```

### Usage 

> If its the first time running or if the directories don't exist, it will create these on your desktop.

<img src="examples/direxample.png">

1. Copy all your files into the 'To Be Sorted' directory
2. Run the command again and wait for the process to be completed 
```
Slib-Sorter
```
3. Inspect the newly created Sample Library

<img src="examples/outputstatistics.png">


> for other options look at:
```
Slib-Sorter -help
```
##### Note: Among other things, the names of these two directories & the name of the finished library can be changed in the settings file. 
```
$home\Documents\slib-sorter\settings.json
```
<details>
<summary>
config preview
</summary>
<img src ="examples/settings.png"> 
</details>

> or run this and it will open the settings file for you
```
Slib-Sorter -config
```


### Future additions and improvements :bulb:  
- [x] Make any used path easier configurable by the user.
- [x] Fix minor issues regarding time.
- [ ] Add further support for other Plugins and theird presets.
- [ ] Add support for other Linux.
- [ ] Further improve pattern matching
- [ ] Apply somewhat simple AI to further boost accuracy, including sorting not based on sound.




