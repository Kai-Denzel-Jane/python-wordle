"""NMTAFE ICTPRG302:
Guess-My-Word Project Application"""
# See the assignment worksheet and journal for further details.
# Begin by completing the TODO items below in the order you specified in the journal

import random
import os
import pathlib


TARGET_WORDS = pathlib.Path('./word-bank/target_words.txt')
VALID_WORDS = pathlib.Path('./word-bank/all_words.txt')

MAX_TRIES = 6


if os.path.exists(TARGET_WORDS):
    with open(TARGET_WORDS, "r") as words:
        contents = words.read().splitlines()

    word = str(random.choice(contents))
    print(word)

if os.path.exists(VALID_WORDS):
    with open(VALID_WORDS, "r") as valid_words:
        valid_words_contents = valid_words.read().splitlines()

def algorithm():

    for i, letter in user_input:
        if user_input[i] == word[i]:
            print("X")


def userinput(user_input, word):
    
    guessed = []
    

    if user_input in valid_words_contents:
    
        if len(user_input) == 5:

            algorithm()

            return(user_input)
    
user_input = str(input("Enter a word: "))
userinput()

def attempts():
    while MAX_TRIES > 0:
        userinput()

# TODO: ensure guess in VALID_WORDS

# TODO: provide clues for each character in the guess using your scoring algorithm

# (end loop)
print("Game Over")


# NOTES:
# ======
# - Add your own flair to the project
# - You will be required to add and refine features based on changing requirements
# - Ensure your code passes any tests you have defined for it.

# SNIPPETS
# ========
# A set of helpful snippets that may help you meet the project requirements.

def pick_target_word(words=None):
    """returns a random item from the list"""
    words = ['a', 'b', 'c']
    return random.choice(words)


def display_matching_characters(guess='hello', target_word='world'):
    """Get characters in guess that correspond to characters in the target_word"""
    i = 0
    for char in guess:
        print(char, target_word[i])
        i += 1

# Uncomment to run:
# display_matching_characters()
# print(pick_target_word())

