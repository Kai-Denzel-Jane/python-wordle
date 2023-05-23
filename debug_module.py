import platform
from colorama import Fore, Style


def get_release_version():
    system = platform.system()
    release = platform.release()

    if system == "Darwin":
        # macOS major release version
        return f"macOS {release}"
    elif system == "Linux":
        # Linux distribution and major release version
        with open("/etc/os-release", "r") as f:
            lines = f.readlines()
            distro = None
            for line in lines:
                if line.startswith("PRETTY_NAME="):
                    distro = line.split("=")[1].strip().strip('"')
                    break
            if distro:
                return f"{distro} {release}"
            else:
                return f"Linux {release}"
    elif system == "Windows":
        # Windows major release version
        return f"Windows {release}"
    else:
        return "Unknown"

def debug(welcome_func):
    # Get debug information about the system
    debug_info = [
        f"Platform: {platform.platform()}",
        f"Python_Version: {platform.python_version()}",
        f"Python_Build: {platform.python_build()}",
        f"Python_Implementation: {platform.python_implementation()}",
        f"Python_Executable: {platform.python_compiler()}",
        f"Release: {get_release_version()}",
        f"Architecture: {platform.architecture()}",
        f"Processor: {platform.processor()}",
        f"Machine: {platform.machine()}",
        f"System: {platform.system()}",
    ]

    # List of available debug information options
    debug_info_available = [
        "Platform",
        "Python_Version",
        "Python_Build",
        "Python_Implementation",
        "Python_Executable",
        "Release",
        "Architecture",
        "Processor",
        "Machine",
        "System",
    ]

    # Prompt the user for debug information input
    debug_info_input = input(Fore.CYAN + "What information do you want to see (? for list, BACK to go back): " + Style.RESET_ALL)

    if debug_info_input == "?":
        # Print the available debug information options
        print(debug_info_available)
        debug(welcome_func)
    elif debug_info_input in debug_info_available:
        # Display the selected debug information
        index = debug_info_available.index(debug_info_input)
        print(Fore.YELLOW + debug_info[index])
    elif debug_info_input == "BACK":
        # Go back to the welcome menu
        welcome_func()

    # Prompt the user to continue or exit
    input_choice = input(Fore.CYAN + "Do you want to continue? (y/n): " + Style.RESET_ALL)

    if input_choice == "y":
        return debug(welcome_func)
    elif input_choice == "n":
        return False
