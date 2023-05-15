import random
import os
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

    if user_word == WORD:

        print("You Win!!!")
    

def user_input():
    user_word = input("Enter a 5-letter word: ")

    if len(user_word) != 5:
        print("Maximum of 5 letters. Try again.")
        user_input()

    valid_words_contents = load_files()[1]
    if user_word in valid_words_contents:
        algorithm(user_word)
        
    else:
        print("-1")
WORD = select_word()   # Call select_word() function to print a random word
user_input()