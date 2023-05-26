import random
import pathlib
import debug_module
import base64
import options_module
import yaml
import requests
from colorama import Fore, Back, Style

with open("config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

    #_options_ = requests.get(config["show_word_after_loss"])
print(config)



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

def algorithm(user_word, word, tries, _options_):

    user_word = list(user_word)
    word = list(word)
    postion = 0
    output = list()

    for position in range(len(word)):
    
        if user_word[postion] == word[position]:
            output.append(user_word[postion])
            user_word[postion] = "_"
            postion += 1





    #for letter in user_word:
        #if letter not in word:
            #print(Fore.RED + letter, "-")
        #elif letter in word and user_word.index(letter) != word.index(letter):
            #print(Fore.YELLOW + letter, "*")
        #elif user_word.index(letter) == word.index(letter):
            #print(Fore.GREEN + letter, "X")

    if user_word == word:
        print(Fore.GREEN + "You win")
    elif user_word == word and tries == 1:
        print("You won with one try remainding that was close")
    else:
        tries -= 1  # Decrease the tries counter
        if tries > 0:
            print(Fore.YELLOW + "Try again")
            print(tries, "Tries remaining")
            user_input(word, cheat, tries)  # Pass the updated tries value
        else:
            print(Fore.RED + "You lose")
            if _options_ == "true":
                print("The word was: " + word)


def user_input(word, cheat, tries=MAX_TRIES):
    if cheat:
        print("Word:", word)
        print("What's the fun in this")

    user_word = input(Fore.CYAN + "Enter a 5-letter word: " + Style.RESET_ALL)
    user_word = user_word.lower()

    valid_words_contents = load_files()[1]

    if len(user_word) == 5:
        if user_word in valid_words_contents:
            algorithm(user_word, word, tries,)
        else:
            print(Fore.RED + "Invalid word")
            user_input(word, cheat, tries)
    else:
        print(Fore.RED + "Must be a 5 letter word. Try again.")
        user_input(word, cheat, tries)


def end():
    # Prompt the user to end the program
    end = input(Fore.CYAN + "End [y/n]" + Style.RESET_ALL)
    if end.lower() == "yes" or end.lower() == "y":
        exit()

def main():
    # Main game loop
    word = select_word()
    user_input(word, cheat)
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

cheat = False

while True:
    # Main program loop
    choice = welcome(cheat)

    match choice:
        case 1:
            main()
        case 2:
            show_instructions()
        case 3:
            continue_debug = debug_module.debug(welcome)
        case 4:
            options = options_module.options()
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

