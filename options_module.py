import main

def options():

    print("1. Show word after loss")

    option = int(input("Enter your option: "))

    match option:

        case 1:
            show_word_input = input("Enter On or Off: ")

            match show_word_input:

                case "On":
                    yaml_config = """options:
                    -show_word_after_loss: true"""
                
                case "Off":
                    yaml_config = """options:
                    -show_word_after_loss: false"""
    
    return yaml_config

def write_changes():

    with open("configw.yaml", "w") as config_file:
        config_file.write(options)