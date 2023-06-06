# python-wordle

This is a repository for my Cert III Introduction to Programming project, which is making Worlde the NYT owned web game.

The following file will contain documentation about this project.

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
pip3.11 install colorama pyyaml plistlib
```

---

# Developer Info

### Packages used:

### Most are built into python

    random (built-in)
    pathlib (built-in)
    debug_module (file)
    base64  (built-in)
    options_module (file)
    client  (file)
    yaml (package)

### Functions / Methods

Choose a random word from `target_words.txt`

```python
import random
import pathlib

TARGET_WORDS = pathlib.Path('./word-bank/target_words.txt')
VALID_WORDS = pathlib.Path('./word-bank/all_words.txt')

MAX_TRIES = 6

def load_files():
    # Load the contents of the target words and valid words files
    target_words_contents = []
    valid_words_contents = []

    if TARGET_WORDS.exists():
        with open(TARGET_WORDS, "r") as words:
            target_words_contents = words.read().splitlines()
  

    if VALID_WORDS.exists():
        with open(VALID_WORDS, "r") as valid_words:
            valid_words_contents = valid_words.read().splitlines()

    return target_words_contents, valid_words_contents

def select_word():
    # Select a random word from the target words
    target_words_contents = load_files()[0]
    word = random.choice(target_words_contents)
    return word

```

Yes this is just the function definition and packages / paths
