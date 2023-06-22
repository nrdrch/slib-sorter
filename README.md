# Sample Library Sorter


### Dependecies
#### 
[Python](https://www.python.org/downloads/), [termcolor 2.3.0 ](https://pypi.org/project/termcolor/)
```
python3 -m pip install --upgrade termcolor
```
### Installation 
```
git clone https://github.com/nrdrch/slib-sorter.git $HOME\Documents\slib-sorter
```

### Usage 
1. Run
```
python3 $home\Documents\slib-sorter\src\slib-sorter.py
```
> If its the first time running this, it will now have created two directories on your desktop.

<picture>
    <img src="https://raw.githubusercontent.com/nrdrch/slib-sorter/main/examples/direxample.png?token=GHSAT0AAAAAACCUPKWOJF3EUJNKTAR7NJSSZEUEOLA">
</picture>

#### Note: Among other things, the names of these two directories & the name of the finished library can be changed in the settings file. 
```
$home\Documents\slib-sorter\settings.json
```

<picture>
    <img src="[https://raw.githubusercontent.com/nrdrch/slib-sorter/main/examples/settings.png?token=GHSAT0AAAAAACCUPKWP6PAP5GP6BWXX4ZJ6ZEUECZA](https://raw.githubusercontent.com/nrdrch/slib-sorter/main/examples/settings.png?token=GHSAT0AAAAAACCUPKWOI2DEHVEBXZM4Y23EZEUEP5A)">
</picture>

2. Move all your files into the 'To Be Sorted' directory
3. Run the same command again and wait for the process to be completed 
4. Inspect the newly created Sample Library located under 'Documents\Sample Library' folder.


### Suggestions
- Create a function in - or imported into your $PSPROFILE for easier Execution.

```
# example function 
# Change the name to your prefered alias for easier execution.
function libsort {
    python3 C:\Users\nrdrch\Documents\slib-sorter\src\slib-sorter.py
}
```
