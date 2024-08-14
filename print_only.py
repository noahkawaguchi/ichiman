def welcome(width: int) -> None:
    """Print the welcome message."""
    print()
    print('*' * width)
    print()
    print('Welcome to'.center(width))
    print('ICHIMAN'.center(width))
    print()
    print('a duration-based'.center(width))
    print('habit tracking program'.center(width))
    print()
    print('developed by'.center(width))
    print('Noah Kawaguchi'.center(width))
    print()
    print('*' * width)
    print()

def main_menu(width: int) -> None:
    """Print the main menu."""
    print('-' * width)
    print('MAIN MENU'.center(width))
    print('-' * width)
    print('1 - Start a New Habit')
    print('2 - Track an Existing Habit')
    print('3 - Calculate Averages')
    print('4 - Calculate Goal Progress')
    print('5 - Create Graphs')
    print('0 - Quit')
    print()
