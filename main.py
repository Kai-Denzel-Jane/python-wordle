import random
import pathlib
import debug_module
import instructions
import base64
from colorama import Fore, Back, Style

instructions.dependencies()

def welcome():
    # Display the welcome menu and prompt for user input
    print(Fore.CYAN + "Enter a number to start:")
    print("1. Play the game")
    print("2. Instructions")
    print("3. Debug")
    print("4. Credits / Information")
    print("5. Exit")
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

def algorithm(user_word, word):
    # Perform the comparison and print the results with font colors
    tries = MAX_TRIES

    for letter in user_word:
        if letter not in word:
            print(Fore.RED + letter, "-")
        elif letter in word and user_word.index(letter) != word.index(letter):
            print(Fore.YELLOW + letter, "*")
        elif user_word.index(letter) == word.index(letter):
            print(Fore.GREEN + letter, "X")

    if user_word == word:
        print(Fore.GREEN + "You win")
    else:
        if tries > 0:
            print(Fore.YELLOW + "Try again")
            tries -= 1
            print(tries, "Tries remaining")
            user_input(word)
        else:
            print(Fore.RED + "You lose")

def user_input(word):
    # Prompt the user to enter a word and validate it
    if cheat:
        print(word, "What's the fun in this")

    user_word = input(Fore.CYAN + "Enter a 5-letter word: " + Style.RESET_ALL)
    user_word = user_word.lower()  # Convert to lowercase

    if len(user_word) != 5:
        print(Fore.RED + "Must be 5 letters. Try again.")
        user_input(word)

    valid_words_contents = load_files()[1]
    if user_word in valid_words_contents:
        algorithm(user_word, word)
    else:
        print(Fore.RED + "That word does not exist. Try again.")
        user_input(word)

def end():
    # Prompt the user to end the program
    end = input(Fore.CYAN + "End [y/n]" + Style.RESET_ALL)
    if end.lower() == "yes" or end.lower() == "y":
        exit()

def main():
    # Main game loop
    word = select_word()
    user_input(word)
    return word

credits = """
    Main Developer: Kai Jane (kaijanedev@icloud.com)
    Source code: https://github.com/Kai-Denzel-Jane/python-wordle/
    Current Release: 1.0.0
    Packages used: colorama
"""

continue_debug = True  # Variable to track if the game should continue

konami_code = b'VVAgVVAgRE9XTiBET1dOIExFRlQgUklHSFQgTEVGVCBSSUdIVCBCIEE='
secret = base64.b64decode(konami_code)

def check_konami_code(input_sequence):
    encoded_input = base64.b64encode(input_sequence.encode())
    return encoded_input == konami_code

cheat = False

while True:
    # Main program loop
    choice = welcome()

    match choice:
        case 1:
            main()
        case 2:
            instructions.show_instructions()
        case 3:
            continue_debug = debug_module.debug(welcome)
        case 4:
            print(Fore.YELLOW, credits)
            credit_input = 'UP UP DOWN DOWN LEFT RIGHT LEFT RIGHT B A'
            if check_konami_code(credit_input):
                cheat = True
                print("Cheat Mode enabled. You're really cheating!")
                welcome()
        case 5:
            SystemExit()
            cheat = False

    end()

    if KeyboardInterrupt:
        cheat = False
