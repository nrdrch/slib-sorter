# Sample Library Sorter
###### *for now only meant to run on Windows10
> This script allows you to quickly sort a massive amount of files, any kind you might find in your Sample Library as a Music Producer. For now, it will match after file name & type to the best of its abilitys. If you're curious about what it is matching the files against. [Look at this son of a book](src/slib-sorter.py#L161-204)
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




