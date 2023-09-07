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

# Loads the configuration file
with open("config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)

# Main Menu
def welcome(cheat):
    """This function is the main menu of the game. It asks the user to choose what they want to do.
    
        Parameters:
            cheat (bool): Whether or not to load the game in cheat mode.

        Returns:
            choice (int): The number of the option chosen by the user.    
    """
    print(ORANGE + f"1. " + CYAN + f"Play the game")
    print(ORANGE + f"2. " + CYAN + f"Instructions")
    print(ORANGE + f"3. " + CYAN + f"Debug")
    print(ORANGE + f"4. " + CYAN + f"Options")
    print(ORANGE + f"5. " + CYAN + f"Credits / Information")
    print(ORANGE + f"6. " + CYAN + f"Exit")
    print(Style.RESET_ALL)

    choice = input("Input number: ")

    try:
        choice = int(choice)
        return choice
    except:
        print(RED + f"I clearly said number, and you didn't enter a number, try again.")
        welcome(cheat)

    

TARGET_WORDS = pathlib.Path('./word-bank/target_words.txt')         # Words that can possibly be chosen as the word you are guessing 
VALID_WORDS = pathlib.Path('./word-bank/all_words.txt')             # Words that can be guessed 

MAX_TRIES = 6                                                       # Amount of tries user has doesn't really need to be a constant 

# Loads necessary files
def load_files():
    """Loads necessary files to run the game

        Parameters:
            None
    
        Returns:
            target_words_contents (list): List of words that can possibly be chosen as the word you.
            valid_words_contents (list): List of words that can be guessed.
        """ 
    target_words_contents = []
    valid_words_contents = []

    if TARGET_WORDS.exists():
        with open(TARGET_WORDS, "r") as words:
            target_words_contents = words.read().splitlines()
    else:
        print(f"The", TARGET_WORDS, f"file required to run the game cant be found")
    

    if VALID_WORDS.exists():
        with open(VALID_WORDS, "r") as valid_words:
            valid_words_contents = valid_words.read().splitlines()
    else:
        print(f"The", VALID_WORDS, f"file required to run the game cant be found")

    return target_words_contents, valid_words_contents

# Select a random word from the target words
def select_word():
    """Select a random word from the target words
    
    
    Parameters:
        None
    
    Returns:
        selected_word (str): The selected word
    """
    target_words_contents = load_files()[0]
    selected_word = random.choice(target_words_contents)
    return selected_word

# Main logic, this is where the scoring is implemented 
def algorithm(user_word, selected_word, tries, config, cheat):
    """Main logic, this is where the scoring is implemented 
    
    
    Parameters:
        user_word (str): The word the user is guessing
        selected_word (str): The word that the user is guessing
        tries (int): The amount of tries the user has
        config (dict): The configuration file
        cheat (bool): Whether or not to load the game in cheat mode.
    
    Returns:
        None    
    """
    user_word = list(map(str.upper, user_word))
    selected_word = list(map(str.upper, selected_word))

    position = 0  # Could be removed
    output = [" "] * len(selected_word)  # Output list to show hints

    selected_word_counts = {}  # Dictionary to store the counts of each letter in the selected word
    for letter in selected_word:
        if letter in selected_word_counts:
            selected_word_counts[letter] += 1
        else:
            selected_word_counts[letter] = 1

    for position in range(len(selected_word)):
        if user_word[position] == selected_word[position]:
            output[position] = "X"  # Updates the output list at the position where the letter was both in the word and correct position
            selected_word_counts[user_word[position]] -= 1  # Decrease the count for correctly guessed letters
        elif user_word[position] in selected_word_counts and selected_word_counts[user_word[position]] > 0:
            output[position] = "*"  # Updates the output list at the position where the letter is in the word but not at that position
            selected_word_counts[user_word[position]] -= 1  # Decrease the count for partially correct letters
        else:
            output[position] = "-"  # Updates the output list at the position where the letter is not in the word


    # Some nice colors and printing of the output
    for position in range(len(output)):
        if output[position] == f"X":
            print(Fore.WHITE + user_word[position], Fore.GREEN, output[position])
        elif output[position] == f"*":
            print(Fore.WHITE + user_word[position], Fore.YELLOW, output[position])
        else:
            print(Fore.WHITE + user_word[position], Fore.RED, output[position])

    # Determines if the user won or lost
    if user_word == selected_word:
        if tries == 1:
            print(f"You won with one try remaining. That was close!")
            tries = 1

        if cheat:
            print(Fore.GREEN + f"You win, but you cheated so you don't deserve it", Style.RESET_ALL)
            tries = 0  # Makes score 0 because of cheating
        else:
            print(Fore.GREEN + f"You win", Style.RESET_ALL)

        if config.get(f"upload_score", False) and tries != 0:
            client.info_input(tries_remaining=tries)  # If configuration is set to true, attempt to upload scores
    else:
        tries -= 1  # Decrease the tries counter
        if tries > 0:
            print(Fore.MAGENTA + f"Try again")
            print(tries, f"Tries remaining")
            get_user_input(selected_word, cheat, config, tries)  # Indicate the need for another input
        else:
            print(Fore.RED + "fYou lose")
            if config.get(f"show_word_after_loss", False):
                print(f"The word was:", " ".join(selected_word))  # If configuration set to true, show what the correct word was


# User Input
def get_user_input(selected_word, cheat, config, tries):
    """User Input
    
        Parameters:
            selected_word (str): The word that the user is guessing
            cheat (bool): Whether or not to load the game in cheat mode.
            config (dict): The configuration file
            tries (int): The amount of tries the user has

        Returns:
            algorithm (function): The function that will be used to run the algorithm    
        """
    if cheat:
        print(f"Word:", selected_word)
        print(f"What's the fun in this") # Shows user is cheating 

    user_word = input(CYAN + f"Enter a 5-letter word: " + Style.RESET_ALL) # Asks for user input 
    user_word = user_word.lower() # Makes users input lowercase 

    valid_words_contents = load_files()[1] # Calls the valid words from the returned tuple from the load_files function

    if len(user_word) == 5: # Checks the user inputted a 5 letter word as asked
        if user_word in valid_words_contents:
            return algorithm(user_word, selected_word, tries, config, cheat)
        else:
            print(Fore.RED + f"Invalid word")
            get_user_input(selected_word, cheat, config, tries)
    else:
        print(Fore.RED + f"Must be a 5 letter word. Try again.")
        get_user_input(selected_word, cheat, config, tries)

def end():
    # Prompt the user to end the program
    stop = input(Style.BRIGHT + CYAN + f"End " + CYAN + f"[" + Fore.LIGHTGREEN_EX + f"y" + CYAN + f"/" + Fore.LIGHTRED_EX + f"n" + CYAN + f"]? " + Style.RESET_ALL)
    if stop.lower() == "yes" or stop.lower() == "y":
        exit()
    elif stop.lower() == "no" or stop.lower() == "n":
        return
    else:
        print(Fore.RED + f"Invalid choice. Please enter 'y' or 'n'")
        end()


def main(cheat):
    """Function to run the game
    
    Parameters:
        cheat (bool): Whether or not to load the game in cheat mode.

    Returns:
        None
    """
    # Main game loop
    word = select_word()
    tries = MAX_TRIES

    get_user_input(word, cheat, config, tries)


def show_instructions():
    """Function to show the instructions
    
    Parameters:
        None

    Returns:
        None
    """
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
                print(LIGHT_RED, f"Unable to open the instructions file. Please refer to the README for instructions.")


credits = """
    Main Developer: Kai Jane (kaijanedev@icloud.com)
    Source code: https://github.com/Kai-Denzel-Jane/python-wordle/
    Current Release: 0.0.1
    Packages used: colorama, pyyaml, plistlib
"""

konami_code = b'VVAgVVAgRE9XTiBET1dOIExFRlQgUklHSFQgTEVGVCBSSUdIVCBCIEE='
secret = base64.b64decode(konami_code)

def check_konami_code(input_sequence):
    """Check input sequence
    
    Parameters:
        input_sequence (str): The input sequence
    
    Returns:
        encoded_input (str): The encoded input sequence    
    """
    encoded_input = base64.b64encode(input_sequence.encode())
    return encoded_input == konami_code

cheat = False

if __name__ == "__main__":

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
                credit_input = input(WHITE + f"Enter to continue: ")
                if check_konami_code(credit_input):
                    cheat = True
                    print(f"Cheat Mode enabled. You're really cheating!")
                    continue
            case 6:
                exit()
            
        end()

        if KeyboardInterrupt:
            cheat = False
