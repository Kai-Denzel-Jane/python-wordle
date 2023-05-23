import subprocess

def show_instructions():
    file_path = 'Instructions.md'
    try:
        subprocess.run(['open', file_path])  # For macOS
    except FileNotFoundError:
        try:
            subprocess.run(['xdg-open', file_path])  # For Linux
        except FileNotFoundError:
            try:
                subprocess.run(['start', file_path], shell=True)  # For Windows
            except FileNotFoundError:
                print("Unable to open the instructions file. Please refer to the README for instructions.")

def dependencies():

    import  platform

    # Check if Colorama is installed
    try:
        import colorama
        from colorama import Fore, Back, Style
    except ImportError:
        print("Colorama is not installed.")
        print("Please install Colorama to run this program.")

        # Check the user's operating system and provide installation instructions accordingly
        system = platform.system()
        if system == "Windows":
            print("To install Colorama on Windows, run the following command in your command prompt or terminal:")
            print("pip install colorama")
        elif system == "Darwin":
            print("To install Colorama on macOS, run the following command in your terminal:")
            print("pip install colorama")
        elif system == "Linux":
            print("To install Colorama on Linux, run the following command in your terminal:")
            print("pip install colorama")
        else:
            print("Please install Colorama manually to run this program on your operating system.")
        exit()


    