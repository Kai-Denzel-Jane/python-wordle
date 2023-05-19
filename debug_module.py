# Debugging

import platform


def debug():

    debug_info = list()
    debug_info_available = list()

    debug_info.append(f"Platform: {platform.platform()}"); debug_info_available.append(f"Platform")
    debug_info.append(f"Python_Version: {platform.python_version()}"); debug_info_available.append(f"Python_Version")
    debug_info.append(f"Python_Build: {platform.python_build()}"); debug_info_available.append(f"Python_Build")
    debug_info.append(f"Python_Implementation: {platform.python_implementation()}"); debug_info_available.append(f"Python_Implementation")
    debug_info.append(f"Python_Executable: {platform.python_compiler()}"); debug_info_available.append(f"Python_Executable")
    debug_info.append(f"Architecture: {platform.architecture()}"); debug_info_available.append(f"Architecture")
    debug_info.append(f"Processor: {platform.processor()}"); debug_info_available.append(f"Processor")

    get_platform = debug_info[0]
    get_python_version = debug_info[1]
    get_python_build = debug_info[2]
    get_python_implementation = debug_info[3]
    get_python_compiler = debug_info[4]
    get_architecture = debug_info[5]
    get_processor = debug_info[6]


    debug_info_input = str(input("What information you want to see (? for list, BACK to go back): "))

    match debug_info_input:
        case "?":
            print(debug_info_available)
            debug()
        case "Platform":
            print(get_platform)
        case "Python_Version":
            print(get_python_version)
        case "Python_Build":
            print(get_python_build)
        case "Python_Implementation":
            print(get_python_implementation)
        case "Python_Executable":
            print(get_python_compiler)
        case "Architecture":
            print(get_architecture)
        case "Processor":
            print(get_processor)
        case "BACK":
            import main
            main.welcome()
    
    input_choice = str(input("Do you want to continue? (y/n): "))

    match input_choice:
        case "y":
            debug()
        case "n":
            import main
            main.welcome()