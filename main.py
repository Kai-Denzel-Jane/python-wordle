import random
import pathlib
import debug_module
import base64
import options_module
import client
import yaml
from colorama import Fore, Back, Style


def welcome(cheat):
    # Display the welcome menu and prompt for user input
    print(Fore.CYAN + "Enter a number to start:")
    print("1. Play the game")
    print("2. Instructions")
    print("3. Debug")
    print("4. Options")
    print("5. Credits / Information")
    print("6. Exit")
    print(Style.RESET_ALL)

    choice = int(input("Input number: "))
    return choice

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

def algorithm(user_word, word, tries, config, cheat):
    user_word = list(user_word)
    word = list(word)
    position = 0
    output = [" "] * 5

    for position in range(len(word)):
        if user_word[position] == word[position]:
            output[position] = "X"
        elif user_word[position] in word and word.index(user_word[position]) != position:
            output[position] = "*"
        else:
            output[position] = "-"

    for position in range(len(output)):
        if output[position] == "X":
            print(Fore.GREEN, output[position])
        elif output[position] == "*":
            print(Fore.YELLOW, output[position])
        else:
            print(Fore.RED, output[position])

    if user_word == word:
        print(Fore.GREEN + "You win")
        tries_remaining = tries
    elif user_word == word and cheat:
        print(Fore.GREEN + "You win, but you cheated so you don't deserve it")
        tries_remaining = 0  # Makes score 0 because of cheating
    elif user_word == word and tries == 1:
        print("You won with one try remaining. That was close!")
        tries_remaining = 1
    else:
        tries -= 1  # Decrease the tries counter
        if tries > 0:
            print(Fore.MAGENTA + "Try again")
            print(tries, "Tries remaining")
            return False  # Indicate the need for another input
        else:
            print(Fore.RED + "You lose")
            if config.get("show_word_after_loss", False):
                print("The word was:", " ".join(word))
    return True  # Indicate the end of the game

def user_input(word, cheat, config, tries=MAX_TRIES):
    if cheat:
        print("Word:", word)
        print("What's the fun in this")

    user_word = input(Fore.CYAN + "Enter a 5-letter word: " + Style.RESET_ALL)
    user_word = user_word.lower()

    valid_words_contents = load_files()[1]

    if len(user_word) == 5:
        if user_word in valid_words_contents:
            return algorithm(user_word, word, tries, config, cheat)
        else:
            print(Fore.RED + "Invalid word")
    else:
        print(Fore.RED + "Must be a 5 letter word. Try again.")
    return False  # Indicate the need for another input

def end():
    # Prompt the user to end the program
    end = input(Fore.CYAN + "End [y/n]" + Style.RESET_ALL)
    if end.lower() == "yes" or end.lower() == "y":
        exit()

def main(cheat):
    # Main game loop
    word = select_word()
    while True:
        if user_input(word, cheat, config):
            break
    return word

import subprocess

def show_instructions():
    file_path = 'Instructions.md'
    try:
        subprocess.run(['open', file_path])  # For macOS
    except FileNotFoundError:
        try:
            subprocess.run(['xdg-open', file_path])  # For Linux
        except FileNotFoundError:
            try:
                subprocess.run(['start', file_path], shell=True)  # For Windows
            except FileNotFoundError:
                print("Unable to open the instructions file. Please refer to the README for instructions.")

credits = """
    Main Developer: Kai Jane (kaijanedev@icloud.com)
    Source code: https://github.com/Kai-Denzel-Jane/python-wordle/
    Current Release: 1.0.0
    Packages used: colorama
"""

konami_code = b'VVAgVVAgRE9XTiBET1dOIExFRlQgUklHSFQgTEVGVCBSSUdIVCBCIEE='
secret = base64.b64decode(konami_code)

def check_konami_code(input_sequence):
    encoded_input = base64.b64encode(input_sequence.encode())
    return encoded_input == konami_code

config = {}
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
            print(Fore.YELLOW, credits)
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
