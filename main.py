import random
import pathlib
import debug_module
import base64
import options_module
import client
import yaml
from colorama import Fore, Style, init
import subprocess

# Initialize colorama
init()

# Load the configuration file
with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

# Main menu
def welcome(cheat):
    print(Fore.CYAN + "1. Play the game")                       # Loads the game itself
    print("2. Instructions")                                    # Opens Instructions.md with default set app
    print("3. Debug")                                           # Allows users to see debug information
    print("4. Options")                                         # Where users can change options
    print("5. Credits / Information")                           # "Just" Credits ;)
    print("6. Exit")                                            # Exits the script
    print(Style.RESET_ALL)

    choice = int(input("Input number: "))
    return choice

TARGET_WORDS = pathlib.Path('./word-bank/target_words.txt')     # Words that can possibly be chosen as the word you are guessing
VALID_WORDS = pathlib.Path('./word-bank/all_words.txt')         # Words that can be guessed

MAX_TRIES = 6                                                   # Amount of lives user has (doesn't really need to be a constant)

# Load necessary files
def load_files():
    target_words_contents = []
    valid_words_contents = []

    if TARGET_WORDS.exists():
        with open(TARGET_WORDS, "r") as words:
            target_words_contents = words.read().splitlines()

    if VALID_WORDS.exists():
        with open(VALID_WORDS, "r") as valid_words:
            valid_words_contents = valid_words.read().splitlines()

    return target_words_contents, valid_words_contents

# Select a random word from the target words
def select_word():
    target_words_contents = load_files()[0]
    word = random.choice(target_words_contents)
    return word

# Main logic, implements the scoring
def algorithm(user_word, word, tries, config, cheat):
    user_word = list(user_word)
    word = list(word)
    output = [" "] * 5

    for position in range(len(word)):
        if user_word[position] == word[position]:
            output[position] = "X"
        elif user_word[position] in word and word.index(user_word[position]) != position:
            output[position] = "*"
        else:
            output[position] = "-"

    # Display the output with appropriate colors
    for position in range(len(output)):
        if output[position] == "X":
            print(Fore.GREEN + output[position], end=" ")
        elif output[position] == "*":
            print(Fore.YELLOW + output[position], end=" ")
        else:
            print(Fore.RED + output[position], end=" ")

    print(Style.RESET_ALL)

    # Determine if the user won or lost
    if user_word == word:
        if tries == 1:
            print(Fore.GREEN + "You won with one try remaining. That was close!")
            tries = 1

        if cheat:
            print(Fore.GREEN + "You win, but you cheated so you don't deserve it" + Style.RESET_ALL)
            tries = 0
        else:
            print(Fore.GREEN + "You win" + Style.RESET_ALL)

        if config.get("upload_score", False) and tries != 0:
            client.info_input(tries_remaining=tries)
    else:
        tries -= 1
        if tries > 0:
            print(Fore.MAGENTA + "Try again. " + str(tries) + " tries remaining.")
        else:
            print(Fore.RED + "You lost. Better luck next time!")
            if config.get("show_word_after_loss", False):
                print("The word was:", " ".join(word))

    return tries

# User input
def user_input(word, cheat, config, tries):
    if cheat:
        print("Word:", word)
        print("What's the fun in this")                            # Shows user is cheating

    user_word = input(Fore.CYAN + "Enter a 5-letter word: " + Style.RESET_ALL)    # Asks for user input
    user_word = user_word.lower()                               # Makes users input lowercase

    valid_words_contents = load_files()[1]                       # Calls the valid words from the returned tuple from the load_files function

    if len(user_word) == 5:                                      # Checks if the user inputted a 5-letter word as asked
        if user_word in valid_words_contents:
            return algorithm(user_word, word, tries, config, cheat)
        else:
            print(Fore.RED + "Invalid word")
            user_input(word, cheat, config, tries)
    else:
        print(Fore.RED + "Must be a 5-letter word. Try again.")
        user_input(word, cheat, config, tries)

def end():
    # Prompt the user to end the program
    end = input(Fore.CYAN + "End [y/n] ?" + Style.RESET_ALL)
    if end.lower() == "yes" or end.lower() == "y":
        exit()

def main(cheat):
    # Main game loop
    word = select_word()
    tries = MAX_TRIES

    user_input(word, cheat, config, tries)

def show_instructions():
    file_path = 'Instructions.md'
    try:
        subprocess.run(['open', file_path])                       # For macOS
    except FileNotFoundError:
        try:
            subprocess.run(['xdg-open', file_path])               # For Linux
        except FileNotFoundError:
            try:
                subprocess.run(['start', file_path], shell=True)  # For Windows
            except FileNotFoundError:
                print("Unable to open the instructions file. Please refer to the README for instructions.")

credits = """
    Main Developer: Kai Jane (kaijanedev@icloud.com)
    Source code: https://github.com/Kai-Denzel-Jane/python-wordle/
    Current Release: 0.0.1
    Packages used: colorama, pyyaml, plistlib
"""

konami_code = b'VVAgVVAgRE9XTiBET1dOIExFRlQgUklHSFQgTEVGVCBSSUdIVCBCIEE='
secret = base64.b64decode(konami_code)

def check_konami_code(input_sequence):
    encoded_input = base64.b64encode(input_sequence.encode())
    return encoded_input == konami_code

cheat = False

while True:
    # Main program loop
    choice = welcome(cheat)

    match choice:
        case 1:
            main(cheat)
        case 2:
            show_instructions()
        case 3:
            continue_debug = debug_module.debug(welcome)
        case 4:
            config = options_module.options()
        case 5:
            print(Fore.YELLOW + credits)
            credit_input = input("Enter to continue: ")
            if check_konami_code(credit_input):
                cheat = True
                print("Cheat Mode enabled. You're really cheating!")
                continue
        case 6:
            exit()

    end()

    if KeyboardInterrupt:
        cheat = False
        continue
