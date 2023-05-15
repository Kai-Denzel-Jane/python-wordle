import random
import os
import pathlib

TARGET_WORDS = pathlib.Path('./word-bank/target_words.txt')
VALID_WORDS = pathlib.Path('./word-bank/all_words.txt')

MAX_TRIES = 6

guessed = []
present_letters = []


if os.path.exists(TARGET_WORDS):
    with open(TARGET_WORDS, "r") as words:
        contents = words.read().splitlines()

    word = str(random.choice(contents))
    print(word)

if os.path.exists(VALID_WORDS):
    with open(VALID_WORDS, "r") as valid_words:
        valid_words_contents = valid_words.read().splitlines()

def algorithm():

    guessed.append(user_input)
    
    user_input_list = list(user_input)
    word_list = list(word)
 
def userinput():
    
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