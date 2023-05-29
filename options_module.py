import yaml

def options():
    with open("config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)

    print("1. Show word after loss")
    option = int(input("Enter your option: "))

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
                    

    with open("config.yaml", "w") as config_file:
        yaml.dump(config, config_file)
        return config

