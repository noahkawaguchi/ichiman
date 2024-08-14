from print_only import welcome, main_menu
import menu_options as menu

def main():
    WIDTH = 30
    welcome(WIDTH)
    show_menu = True
    while True:
        if show_menu:
            main_menu(WIDTH)
        user_choice = input('Enter the number of your choice: ')
        print()
        show_menu = True
        if user_choice == '1':
            menu.new_habit()
        elif user_choice == '2':
            menu.track_habit()
        elif user_choice == '3':
            menu.calculate_avg()
        elif user_choice == '4':
            menu.goal_progress()
        elif user_choice == '5':
            menu.create_graph()
        elif user_choice == '0':
            print('See you tomorrow!')
            print()
            break
        else:
            print('Invalid input. Please enter one of the above numbers.')
            print()
            show_menu = False

if __name__ == "__main__":
    main()
