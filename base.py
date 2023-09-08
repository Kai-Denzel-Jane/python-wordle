import os
from flask import Flask, render_template, request, redirect, url_for, session, flash

from main import *

app = Flask(__name__, static_folder="static", static_url_path="/static")

app.secret_key = os.urandom(24)

@app.route('/')
def load_menu():

    return render_template('welcome.html')


@app.route('/main_menu', methods=['GET', 'POST'])
def process_option():

    selected_option = None

    if request.method == 'POST':
        selected_option = request.form.get('choice')


    if selected_option == "play":
        return redirect(url_for('flask_select_word'))
    
    if selected_option is None:
        return "Invalid option or method used."

@app.route('/play', methods=['GET', 'POST'])

def flask_select_word():
    word = session.get('word')

    if word is None:
        word = select_word()
        session['word'] = word

    # Check if there's a POST request
    if request.method == 'POST':
        return user_input(word)  # If it's a POST request, redirect to the user_input function

    return render_template('game_main.html', word=word)  # If it's a GET request, render the template

def user_input(word, cheat=False, config={}, tries):
    # if cheat:
    #     # ...

    if request.method == 'POST':
        user_word = request.form.get('user_word')
        user_word = user_word.lower()

        valid_words_contents = load_files()[1]

        if len(user_word) == 5:
            if user_word in valid_words_contents:
                print("Valid word")
                return flask_algorithm(user_word, word, tries, config, cheat)
            else:
                print("Invalid word (not in dictionary)")
                return render_template("game_main.html", word=session['word'], error_message="Invalid word (not in dictionary)", tries_remaining=tries)  # Pass updated tries value
        else:
            print("Invalid word (not 5 letters)")
            return render_template("game_main.html", word=session['word'], error_message="Invalid word (not 5 letters)", tries_remaining=tries)  # Pass updated tries value

def flask_algorithm(user_word, word, tries, config={}, cheat=False):
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
    word = list(map(str.upper, word))

    position = 0  # Could be removed
    output = [" "] * len(word)  # Output list to show hints

    selected_word_counts = {}  # Dictionary to store the counts of each letter in the selected word
    for letter in word:
        if letter in selected_word_counts:
            selected_word_counts[letter] += 1
        else:
            selected_word_counts[letter] = 1

    for position in range(len(word)):
        if user_word[position] == word[position]:
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
    if user_word == word:
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
            return user_input(word, cheat=False, config={}, tries=tries)  # Indicate the need for another input
        else:
            print(Fore.RED + f"You lose")
            if config.get(f"show_word_after_loss", False):
                print(f"The word was:", " ".join(word))  # If configuration set to true, show what the correct word was
    
if __name__ == '__main__':
    app.run(debug=True)
    



