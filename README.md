# python-wordle
This is a repository for my Cert III Introduction to Programming project, which is making Worlde the NYT owned web game.

The following file will contain documentation about this project.

---

# Main Points

##  [Dependencies](#dependencies)
##  [Usage](./Instructions.md) 
##  [Developer Info](#developer-info)

---

# Dependencies

### This script was made in python@3.11, and should work with python@3.10 and above.
### Now you are going to want to install (insert packages here).

### Shell Commands (use pip@3.11 to avoid installation of default PATH)
```zsh
pip3.11 install colorama pyyaml
```
---

# Developer Info

### Packages used:

### All currently used packages come inbuilt with python (latest release).

    random (to get random strings)
    os (to check wether files are present)
    pathlib (had better experiences with this appose to a string path)
    debug_module (file containing debug functions)
    options_module (file that handled options)
    client (file the uploads users scores)

    pyyaml (used to manage options)
    colorama (makes the terminal look nicer, may have issues if user has a custom terminal or something like OHMYZSH etc)
### Functions / Methods

Choose a random word from `target_words.txt`

```python
import os
import pathlib
import random

TARGET_WORDS = pathlib.Path('./word-bank/target_words.txt')
VALID_WORDS = pathlib.Path('./word-bank/all_words.txt')

def files():
    if os.path.exists(TARGET_WORDS):
        with open(TARGET_WORDS, "r") as words:
            target_words_contents = words.read().splitlines()


    if os.path.exists(VALID_WORDS):
        with open(VALID_WORDS, "r") as valid_words:
            valid_words_contents = valid_words.read().splitlines()

    return(target_words_contents, valid_words_contents)
def selectword():

    word = str(random.choice(files()[0]))
    print(word)
selectword()

```
