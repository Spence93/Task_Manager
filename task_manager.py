# =====importing libraries===========
import os
from datetime import datetime, date
from data_report_functions import *
from menu_functions import *

DATETIME_STRING_FORMAT = "%Y-%m-%d"

main_menu = '''\nSelect one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr = Generate reports
ds - Display statistics
e - Exit
'''


def main():
    # Create tasks.txt if it doesn't exist
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w") as default_file:
            pass

    # Reads and stores the data from tasks.txt as a list in the
    # Task data variable
    with open("tasks.txt", 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]

    task_list = []
    for t_str in task_data:
        curr_t = {}

        # Split by semicolon and manually add each component
        task_components = t_str.split(";")
        curr_t['username'] = task_components[0]
        curr_t['title'] = task_components[1]
        curr_t['description'] = task_components[2]
        curr_t['due_date'] = datetime.strptime(
            task_components[3], DATETIME_STRING_FORMAT)
        curr_t['assigned_date'] = datetime.strptime(
            task_components[4], DATETIME_STRING_FORMAT)
        curr_t['completed'] = True if task_components[5] == "Yes" else False

        task_list.append(curr_t)

    # ==========================Login Section==========================#
    '''This code reads usernames and password from the user.txt file to 
        allow a user to login.
    '''
    # If no user.txt file, write one with a default account
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as default_file:
            default_file.write("admin;password")

    # Read in user_data
    with open("user.txt", 'r') as user_file:
        user_data = user_file.read().split("\n")

    # Convert to a dictionary
    username_password = {}
    for user in user_data:
        username, password = user.split(';')
        username_password[username] = password

    logged_in = False
    while not logged_in:
        # Login screen, prompting for input from the user
        print(add_color("\nLOGIN", GREEN))
        curr_user = input("Username: ")
        curr_pass = input("Password: ")
        if curr_user not in username_password.keys():
            print(add_color("User does not exist", RED))
            continue
        elif username_password[curr_user] != curr_pass:
            print(add_color("Wrong password", RED))
            continue
        else:
            print(add_color("\nLogin Successful!", GREEN))
            logged_in = True

    while True:
        # Presenting the menu to the user and
        menu = menu_input(main_menu, add_color)

        # Register user option
        if menu == 'r':
            reg_user(add_color, username_password)

        # Add task option
        elif menu == 'a':
            add_task(task_list, add_color, username_password)
            write_to_file(task_list, "\nTask successfully added.")

        # View all tasks
        elif menu == 'va':
            view_all(add_color, task_list)

        # View 'my' Tasks
        elif menu == 'vm':
            while True:
                # Prints out and numbers all the users tasks,
                # And returns index in relation to overall task list
                users_index_list = view_mine(task_list, add_color, curr_user)

                # Takes input from user
                # And returns index of the selected task
                task_select = task_input(
                    users_index_list, task_list, add_color)

                # Allows user to return to previous menu
                if task_select == "-1":
                    break

                # Allows the user to edit the selected task
                # And returns the edited task
                edited_task = edit_task(
                    task_select, task_list, add_color, username_password)

                # Updates the task file by writing the edited task
                # To the task.txt file
                write_to_file(
                    edited_task, "\nTask has been updated", add_color)

        # Generates user reports
        elif menu == "gr":
            # Stores both task and user overview data in seperate variables
            task_overview = task_overview_data(task_list, percentage)
            user_overview = user_overview_data(
                task_list, username_password, percentage, username_password)
            # Writes and creates the two txt files with the data created above
            create_task_report("task_overview.txt", task_overview)
            create_user_report("user_overview.txt", user_overview)
            print(add_color("\nReports have been successfully generated", GREEN))

        # Display stats from Task_overview and User_overview
        elif menu == 'ds' and curr_user == 'admin':
            # Generating the correct reports to be displayed
            task_overview = task_overview_data(task_list, percentage)
            user_overview = user_overview_data(
                task_list, username_password, percentage, username_password)
            create_task_report("task_overview.txt", task_overview)
            create_user_report("user_overview.txt", user_overview)

            # Reading the report files, to display the data to the user
            display_stats("task_overview.txt", "Task Overview: ", add_color)
            display_stats("user_overview.txt", "User Overview: ", add_color)

        # Final option to exit the program
        elif menu == 'e':
            print('Goodbye!!!')
            exit()

        else:
            print(add_color("\nYou have made a wrong choice, Please Try again", RED))


if __name__ == "__main__":
    main()
