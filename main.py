import random
import pathlib

import debug_module

def welcome():
    print("Eneter a number to start:")
    print("1. Play the game")
    print("2. Instructions")
    print("3. Debug")
    print("4. Exit")

    choice = int(input("Input number: "))

    return choice


TARGET_WORDS = pathlib.Path('./word-bank/target_words.txt')
VALID_WORDS = pathlib.Path('./word-bank/all_words.txt')

MAX_TRIES = 6

def instructions():
    print("Instructions:")

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

def select_word():
    target_words_contents = load_files()[0]
    word = random.choice(target_words_contents)
    print(word)
    
    return word

def algorithm(user_word):
    # Add your implementation of the algorithm here

    user_word = list(user_word)
    
    

def user_input():
    user_word = input("Enter a 5-letter word: ")

    if len(user_word) != 5:
        print("Must be 5 letters. Try again.")
        user_input()

    valid_words_contents = load_files()[1]
    if user_word in valid_words_contents:
        algorithm(user_word)
        
    else:
        print("That word does not exist. Try again.")
        user_input()

def end():

    end = input("End [y/n]")
    if end == "yes" or end == "y":
        exit()

def main():
    WORD = select_word()   # Call select_word() function to print a random word
    user_input()

while True:

    choice = welcome()

    match choice:

        case 1:
            main()
        case 2:
            instructions()
        case 3:
            debug_module.debug()
        case 4:
            exit()

    end()   

