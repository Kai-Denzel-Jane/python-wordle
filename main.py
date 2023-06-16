# Import modules 
import random                                       # Used to generate random word 
import pathlib                                      # Used to define file paths because pythons default method can be weird 
import base64                                       # Used to endcode / decode strings
import subprocess                                   # Used to open default applications for markdown files 
import debug_module                                 # File with debug functions
import options_module                               # File with option functions to allow user to change 
import client                                       # File which asks for information and attempts to upload scores to server
import yaml                                         # Downloaded package allowing for configuration to be saved in yaml files
from colorama import Fore, Back, Style              # Downloaded package allowing for prettier terminal 

ORANGE = '\033[38;5;208m'
CYAN = Fore.CYAN
RED = Fore.RED
LIGHT_RED = Fore.LIGHTRED_EX
GREEN = Fore.GREEN
LIGHT_GREEN = Fore.LIGHTGREEN_EX
YELLOW = Fore.YELLOW
WHITE = Fore.WHITE
MAGENTA = Fore.MAGENTA

# Loads the configuration file
with open("config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)

# Main Menu 
# Main Menu
def welcome(cheat):
    print(ORANGE + "1. " + CYAN + "Play the game")
    print(ORANGE + "2. " + CYAN + "Instructions")
    print(ORANGE + "3. " + CYAN + "Debug")
    print(ORANGE + "4. " + CYAN + "Options")
    print(ORANGE + "5. " + CYAN + "Credits / Information")
    print(ORANGE + "6. " + CYAN + "Exit")
    print(Style.RESET_ALL)

    choice = int(input("Input number: "))
    return choice

TARGET_WORDS = pathlib.Path('./word-bank/target_words.txt')         # Words that can possibly be chosen as the word yoh are guessing 
VALID_WORDS = pathlib.Path('./word-bank/all_words.txt')             # Words that can be guessed 

MAX_TRIES = 6                                                       # Amount of lives user has doesn't really need to be a constant 

# Loads necessary files
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

# Select a random word from the target words
def select_word():
    target_words_contents = load_files()[0]
    selected_word = random.choice(target_words_contents)
    return selected_word

# Main logic, this is where the scoring is implemented 
def algorithm(user_word, selected_word, tries, config, cheat):
    user_word = map(str.upper, user_word)
    selected_word = map(str.upper, selected_word)

    user_word = list(user_word)
    selected_word = list(selected_word)   
    position = 0                                
    output = [" "] * 5                              # Output list to show hints


    for position in range(len(selected_word)):
        if user_word[position] == selected_word[position]:
            output[position] = "X"                  # Updates the output list at the position where the letter was both in the word and correct position 
        elif user_word[position] in selected_word and selected_word.index(user_word[position]) != position:
            output[position] = "*"                  # Updates the output list at the position where the letter is in the word but not that position 
        else:
            output[position] = "-"                  # Updates the output list at the position indicating there's no occurrence of this letter in the selected word

    # Some nice colours and printing of the output
    for position in range(len(output)):
        if output[position] == "X":
            print(WHITE + user_word[position], LIGHT_GREEN, output[position])
        elif output[position] == "*":
            print(WHITE + user_word[position], YELLOW, output[position])
        else:
            print(WHITE + user_word[position], LIGHT_RED, output[position])
            
    # Determines if the user one or lost
    if user_word == selected_word:
        if tries == 1:
            print("You won with one try remaining. That was close!")
            tries = 1

        if cheat:
            print(LIGHT_GREEN + "You win, but you cheated so you don't deserve it", Style.RESET_ALL)
            tries = 0                               # Makes score 0 because of cheating
        else:
            print(LIGHT_GREEN + "You win", Style.RESET_ALL)

        if config.get("upload_score", False) and tries != 0:
            client.info_input(tries_remaining = tries) # If configuration is set to true attempt to upload scores
    else:
        tries -= 1  # Decrease the tries counter
        if tries > 0:
            print(RED + "Try again", Style.RESET_ALL)
            print(YELLOW, tries, "Tries remaining", Style.RESET_ALL)
            get_user_input(selected_word, cheat, config, tries)  # Indicate the need for another input
        else:
            print(LIGHT_RED + "You lose", Style.RESET_ALL)
            if config.get("show_word_after_loss", False):
                print("The word was:", " ".join(selected_word)) # If configuration set to true show what the correct word was

# User Input
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
            print(LIGHT_RED + "Invalid word", Style.RESET_ALL)
            get_user_input(selected_word, cheat, config, tries)
    else:
        print(LIGHT_RED + "Must be a 5 letter word. Try again.", Style.RESET_ALL)
        get_user_input(selected_word, cheat, config, tries)

def end():
    # Prompt the user to end the program
    stop = input(Style.BRIGHT + CYAN + "End " + CYAN + "[" + LIGHT_GREEN + "y" + CYAN + "/" + LIGHT_RED + "n" + CYAN + "]? " + Style.RESET_ALL)
    if stop.lower() == "yes" or stop.lower() == "y":
        exit()
    elif stop.lower() == "no" or stop.lower() == "n":
        return
    else:
        print(LIGHT_RED + "Invalid choice. Please enter 'y' or 'n'")
        end()


def main(cheat):
    # Main game loop
    word = select_word()
    if hardMode:
        tries = 3
    else:
        tries = MAX_TRIES

    get_user_input(word, cheat, config, tries)


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
                print(LIGHT_RED,"Unable to open the instructions file. Please refer to the README for instructions.")

credits = """
    Main Developer: Kai Jane (kaijanedev@icloud.com)
    Source code: https://github.com/Kai-Denzel-Jane/python-wordle/
    Current Release: v1.1
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
            print(YELLOW, credits)
            credit_input = input(WHITE + "Enter to continue: ")
            if check_konami_code(credit_input):
                cheat = True
                print(MAGENTA + "Cheat Mode enabled. You're really cheating!")
                continue
        case 6:
            exit()
        case 7:
            # VERY WORK IN PROGRESS
            hardMode = True
        case 0: # REMOVE THIS CASE IN MAIN BRANCH COMMITS
            print(YELLOW, "DEV MODE, this is a development mode, only to be used for testing purposes.")
            
            selected_word = input(CYAN + "Enter the word you want to be assigned as the target word: ")
            cheat = True #So we dont go uploading dev stuff to the scoreboard
            get_user_input(selected_word, cheat, config, MAX_TRIES)



    end()

    if KeyboardInterrupt:
        cheat = False
