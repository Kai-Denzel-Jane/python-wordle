import yaml
from colorama import Fore, Back, Style

def options():
    with open("config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)

    
    tuple_options = (config["show_word_after_loss"], config["upload_score"], config["difficulty"])

    if config["show_word_after_loss"] == True:
        show_state = Fore.LIGHTGREEN_EX + "True"
    else:
        show_state = Fore.LIGHTRED_EX + "False"

    if config["upload_score"] == True:
        upload_state = Fore.LIGHTGREEN_EX + "True"
    else:
        upload_state = Fore.LIGHTRED_EX + "False"

    if config["difficulty"] == 0:
        difficulty_level = Fore.LIGHTGREEN_EX + "Easy, (Default)"
    elif config["difficulty"] == 1:
        difficulty_level = Fore.LIGHTRED_EX + "Hard"

    print(Fore.YELLOW + "1. Show Word After Loss:", show_state, Style.RESET_ALL)
    print(Fore.YELLOW + "2. Upload Score After Game:", upload_state, Style.RESET_ALL)
    print(Fore.YELLOW + "3. Difficulty:", difficulty_level, Style.RESET_ALL)
    option = int(input("Enter the option you would like to modify: "))

    match option:
        case 1:
            show_word_input = input("Enter true or false: ")
            match show_word_input.lower():
                case "true":
                    config["show_word_after_loss"] = True
                case "false":
                    config["show_word_after_loss"] = False
                case _:
                    print("Invalid input. Option not changed.")
                    
        case 2:
            upload_input = input("Enter true or false: ")
            match upload_input.lower():
                case "true":
                    config["upload_score"] = True
                case "false":
                    config["upload_score"] = False
                case _:
                    print("Invalid input. Option not changed.")
        case 3:
            difficulty_input = int(input("Enter the difficulty you would like to play at (0 Easy, 1 Hard): "))
            match difficulty_input:
                case 0:
                    config["difficulty"] == 0
                case 1:
                    config["difficulty"] == 1
                case _:
                    print("Invalid input. Option not changed.")
    with open("config.yaml", "w") as config_file:
        yaml.dump(config, config_file)
        return config

