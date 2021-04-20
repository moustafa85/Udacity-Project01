from os import system, name


def clear_screen():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


screen_options = {'PURPLE': '\033[95m',
                 'CYAN': '\033[96m',
                 'DARKCYAN': '\033[36m',
                 'BLUE': '\033[94m',
                 'GREEN': '\033[92m',
                 'YELLOW': '\033[93m',
                 'RED ': '\033[91m',
                 'BOLD': '\033[1m',
                 'UNDERLINE': '\033[4m',
                 'END': '\033[0m'}


def checkScreen():
    clear_screen()
    for key, value in screen_options.items():
        print(value+ ' Hello! Let\'s explore some US bike share data!')


checkScreen()
