import random
import os
import pathlib

TARGET_WORDS = pathlib.Path('./word-bank/target_words.txt')
VALID_WORDS = pathlib.Path('./word-bank/all_words.txt')

MAX_TRIES = 6

def files():
    if os.path.exists(TARGET_WORDS):
        with open(TARGET_WORDS, "r") as words:
            target_words_contents = words.read().splitlines()


    if os.path.exists(VALID_WORDS):
        with open(VALID_WORDS, "r") as valid_words:
            valid_words_contents = valid_words.read().splitlines()

    return(target_words_contents, valid_words_contents)
def selectword():

    word = str(random.choice(files()[0]))
    print(word)
selectword()

def algorithm():

    print(comments)

def userinput():

    user_input = str(input("Enter a 5 letter word: "))

    if len(user_input) >> 5:
        print("Maxium of 5 letters try again.")
        userinput()
    elif user_input in files()[1]:
        algorithm()
        return(user_input)
    else:
        print("-1")
    
userinput()

