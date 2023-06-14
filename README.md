# python-wordle

This is a repository for my Cert III Introduction to Programming project, which is making Worlde the NYT owned web game.

The following file will contain documentation about this project.

> **WARNING: Make sure files are all present before running**

---

# Main Points

## [Dependencies](#dependencies)

## [Usage](./Instructions.md)

## [Developer Info](#developer-info)

---

# Dependencies

### This script was made in python@3.11, and should work with python@3.10 and above.

### Now you are going to want to install (insert packages here).

### Shell Commands (use pip3.11 to avoid installation of default PATH)

```zsh
pip3.11 install colorama pyyaml biplist
```

---

# Developer Info

### Modules used:

* random | pip-name (N/A)
* pathlib | pip-name (N/A)
* base64 | pip-name (N/A)
* subprocess | pip-name (N/A)
* debug_module | pip-name (N/A)
* options_module | pip-name (N/A)
* client | pip-name (N/A)
* yaml  | pip-name (pyyaml)
* colorama | pip-name (colorama)
* plistlib | pip-name (biplist)
* platform | pip-name (N/A)

Functions / Methods

Choose a random word from `target_words.txt`

```python
import random
import pathlib

TARGET_WORDS = pathlib.Path('./word-bank/target_words.txt')
VALID_WORDS = pathlib.Path('./word-bank/all_words.txt')

MAX_TRIES = 6

def load_files():
  
    target_words_contents = []
    valid_words_contents = []

    if TARGET_WORDS.exists():
        with open(TARGET_WORDS, "r") as words:
            target_words_contents = words.read().splitlines()
    else:
        print("The", TARGET_WORDS, "file required to run the game cant be found")
  

    if VALID_WORDS.exists():
        with open(VALID_WORDS, "r") as valid_words:
            valid_words_contents = valid_words.read().splitlines()
    else:
        print("The", VALID_WORDS, "file required to run the game cant be found")

    return target_words_contents, valid_words_contents

def select_word():
    target_words_contents = load_files()[0]
    selected_word = random.choice(target_words_contents)
    return selected_word

```

Ask User for input and compare requirements

```python
from colorama import Fore, Back, Style

def get_user_input(selected_word, cheat, config, tries):
    if cheat:
        print("Word:", selected_word)
        print("What's the fun in this") # Shows user is cheating 

    user_word = input(CYAN + "Enter a 5-letter word: " + Style.RESET_ALL) # Asks for user input 
    user_word = user_word.lower() # Makes users input lowercase 

    valid_words_contents = load_files()[1] # Calls the valid words from the returned tuple from the load_files function

    if len(user_word) == 5: # Checks the user inputted a 5 letter word as asked
        if user_word in valid_words_contents:
            return algorithm(user_word, selected_word, tries, config, cheat)
        else:
            print(Fore.RED + "Invalid word")
            get_user_input(selected_word, cheat, config, tries)
    else:
        print(Fore.RED + "Must be a 5 letter word. Try again.")
        get_user_input(selected_word, cheat, config, tries)
```
