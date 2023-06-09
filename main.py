# Import modules 
import random # Used to generate random word 
import pathlib # Used to define file paths because pythons default method can be weird
import debug_module # File with debug functions 
import base64 # Used to endcode / decode strings
import options_module # File with option functions to allow user to change 
import client # File which asks for information and attempts to upload scores to server
import yaml # Downloaded package allowing for configuration to be saved in yaml files
from colorama import Fore, Back, Style # Downloaded package allowing for prettier terminal 

# Loads the configuration file
with open("config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)

# Main Menu 
def welcome(cheat):
    # Display the welcome menu and prompt for user input

    print(Fore.CYAN + "1. Play the game") # Loads the game itself 
    print("2. Instructions") # Opens Instructions.md with default set app
    print("3. Debug") # Allows users to see debug information 
    print("4. Options") # Where users can change options 
    print("5. Credits / Information") # "Just" Credits ;)
    print("6. Exit") # Exits the script 
    print(Style.RESET_ALL)

    choice = int(input("Input number: "))
    return choice

TARGET_WORDS = pathlib.Path('./word-bank/target_words.txt') # Words that can possibly be chosen as the word yoh are guessing 
VALID_WORDS = pathlib.Path('./word-bank/all_words.txt') # Words that can be guessed 

MAX_TRIES = 6 # Amount of lives user has doesn't really need to be a constant 

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

# Select a random word from the target words
def select_word():
    target_words_contents = load_files()[0]
    word = random.choice(target_words_contents)
    return word

# Main logic, this is where the scoring is implemented 
def algorithm(user_word, word, tries, config, cheat):
    user_word = list(user_word) # Make the users guess a list
    word = list(word) # Make the selected word a list
    position = 0 # Could be removed 
    output = [" "] * 5 # Output list to show hints

    for position in range(len(word)):
        if user_word[position] == word[position]:
            output[position] = "X" # Updates the output list at the position where the letter was both in the word and correct position 
        elif user_word[position] in word and word.index(user_word[position]) != position:
            output[position] = "*" # Updates the output list at the position where the letter is in the word but not that position 
        else:
            output[position] = "-" # Updates the output list at the position indicating there's no occurrence of this letter in the selected word
    # Some nice colours
    for position in range(len(output)):
        if output[position] == "X":
            print(Fore.GREEN, output[position])
        elif output[position] == "*":
            print(Fore.YELLOW, output[position])
        else:
            print(Fore.RED, output[position])
    # Determines if the user one or lost
    if user_word == word:
        if tries == 1:
            print("You won with one try remaining. That was close!")
            tries = 1

        if cheat:
            print(Fore.GREEN + "You win, but you cheated so you don't deserve it", Style.RESET_ALL)
            tries = 0  # Makes score 0 because of cheating
        else:
            print(Fore.GREEN + "You win", Style.RESET_ALL)

        if config.get("upload_score", False):
            client.info_input(tries_remaining = tries) # If configuration is set to true attempt to upload scores
    else:
        tries -= 1  # Decrease the tries counter
        if tries > 0:
            print(Fore.MAGENTA + "Try again")
            print(tries, "Tries remaining")
            user_input(word, cheat, config, tries)  # Indicate the need for another input
        else:
            print(Fore.RED + "You lose")
            if config.get("show_word_after_loss", False):
                print("The word was:", " ".join(word)) # If configuration set to true show what the correct word was

# User Input
def user_input(word, cheat, config, tries):
    if cheat:
        print("Word:", word)
        print("What's the fun in this") # Shows user is cheating 

    user_word = input(Fore.CYAN + "Enter a 5-letter word: " + Style.RESET_ALL) # Asks for user input 
    user_word = user_word.lower() # Makes users input lowercase 

    valid_words_contents = load_files()[1] # Calls the valid words from the returned tuple from the load_files function

    if len(user_word) == 5: # Checks the user inputted a 5 letter word as asked
        if user_word in valid_words_contents:
            return algorithm(user_word, word, tries, config, cheat)
        else:
            print(Fore.RED + "Invalid word")
            user_input(word, cheat, config, tries)
    else:
        print(Fore.RED + "Must be a 5 letter word. Try again.")
        user_input(word, cheat, config, tries)

def end():
    # Prompt the user to end the program
    end = input(Fore.CYAN + "End [y/n]" + Style.RESET_ALL)
    if end.lower() == "yes" or end.lower() == "y":
        exit()

def main(cheat):
    # Main game loop
    word = select_word()
    tries = MAX_TRIES

    user_input(word, cheat, config, tries)

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
    Current Release: 0.0.1
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
        case 000:
            main(cheat=True)

    end()

    if KeyboardInterrupt:
        cheat = False
