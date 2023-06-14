# python-Wordle

## Version: 1.0

**Description:** This is a word guessing game where the player needs to guess a random 5-letter word.

**Instructions:**

1. Select 'Play the game' from the main menu to start the game.
2. Enter a 5-letter word and press Enter to make a guess.
3. The program will provide feedback on your guess:
   - 'X' indicates a correct letter in the correct position.
   - '*' indicates a correct letter in the wrong position.
   - '-' indicates an incorrect letter.
4. Keep guessing until you correctly guess the word or run out of tries.
5. If you win, the program will display a victory message. If you lose, it will display a loss message.
6. You can access instructions by selecting 'Instructions' from the main menu.
7. You can access debug information by selecting 'Debug' from the main menu.
8. In the Options Menu you have access to two options (curently) show_word_loss print the target word after the user looses and upload score after game attempts to connect to server after the user wins
9. To exit the program, select 'Exit' from the main menu.


Server Setup is quite simple make sure server folder is on the machine and start the python server.[y file and it should work correctly, Default PORT: 8080

Serever also works fine locally just keep it in your desired location and start the python file and on the client side when uploading scores use the IP: 127.0.0.1

Have fun playing the Wordle in python!
