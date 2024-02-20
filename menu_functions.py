from data_report_functions import*
from datetime import datetime, date



# Prints the menu to the user and takes input for there menu choice
def menu_input(menu_list, color):
    """
    The function `menu_input` takes a list of menu options as input and prompts the user to choose an
    option, ensuring that the input is a valid alphabetic choice.

    :param menu_list: The menu_list parameter is a list of options that will be displayed to the user as
    a menu
    :return: the user's input as a lowercase string if it consists only of alphabetic characters.
    """
    while True:
        print(color(menu_list, BLUE))
        user_input = input(": ").lower()
        # Input valdation to check input is in the alphabet
        if user_input.isalpha():
            return user_input
        else:
            print(color("Your choice cannot be a number", RED))
            continue


# Created the reg_user function to store all code related to this operation
def reg_user(color, username_password):
    """
    The `reg_user()` function allows a user to register a new username and password, checks if the
    username already exists, and stores the new user information in a file.
    :return: after adding the new user to the `username_password` dictionary and writing the updated
    user data to the "user.txt" file.
    """
    while True:
        # - Request input of a new username
        new_username = input("New Username: ")
        #  An input check to see if the entered username alrady exists
        # and continues a loop until valid input has been entered
        if new_username in username_password:
            print(color("Username already exists, please enter another", RED))
            continue
        # - Request input of a new password
        new_password = input("New Password: ")

        # - Request input of password confirmation.
        confirm_password = input("Confirm Password: ")

        # - Check if the new password and confirmed password are the same.
        if new_password == confirm_password:
            # - If they are the same, add them to the user.txt file,
            print(color("New user added", GREEN))
            username_password[new_username] = new_password

            with open("user.txt", "w") as out_file:
                user_data = []
                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")
                out_file.write("\n".join(user_data))
            return


#  Created the add task function, storing previous code
def add_task(task_file: list, color, username_password) -> list:
    """
    The `add_task()` function allows a user to add a new task to a task.txt file by prompting for the
    username, title, description, and due date of the task.
    """
    while True:
        curr_date = date.today()
        task_username = input("Name of person assigned to task: ")
        # Checks to see if the username is valid
        if task_username not in username_password.keys():
            print(color("User does not exist. Please enter a valid username", RED))
            continue
        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(
                    task_due_date, DATETIME_STRING_FORMAT)
                break

            except ValueError:
                print(
                    color("Invalid datetime format. Please use the format specified", RED))
        # Creates a new dictionary to store previous Inputs from user
        new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False
        }
        # Adds the new task dictionary to the task_file list
        task_file.append(new_task)
        return task_file


#  Displays all tasks currently availiable
def view_all(color, task_list):
    """
    The `view_all` function displays all the tasks in the `task_list` with their details.
    """
    # A counter variable to give all tasks a number
    i = 1
    # Loops through the task task_list, and prints out the
    # dictionary task data in a neat format.
    for t in task_list:
        disp_str = f"Task {i}: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t\t {t['username']}\n"
        disp_str += f"""Date Assigned: \t\t {
            t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"""
        disp_str += f"""Due Date: \t\t {
            t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"""
        disp_str += f"Task Description: \t {t['description']}\n"
        print(disp_str)
        i += 1
    # A screen holder to allow the user to continue when ready
    input(color("Press any key to continue", GREEN))


# Allows user to view only there assigned tasks
def view_mine(task_file, color, curr_user):
    """
    The `view_mine` function displays tasks assigned to the current user and returns a list of the
    indices of those tasks.

    :param task_file: The `task_file` parameter is a list of dictionaries. Each dictionary represents a
    task and contains the following keys:
    :return: a list of task indices that belong to the current user.
    """
    # A counter variable to assign all tasks a number
    i = 1
    # An empty list to recieve task index's for later use
    task_index = []
    print("\nYour Tasks:")

    for index, t in enumerate(task_file,):

        # Checks if the current user matches the task
        if t['username'] == curr_user:
            # Appends the index of that task to the task_index list
            task_index.append(index)

            disp_str = f"\nTask {i}: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t\t {t['username']}\n"
            disp_str += f"""Date Assigned: \t\t {
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"""
            disp_str += f"""Due Date: \t\t {
                t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"""
            disp_str += f"Task Description: \t {t['description']}\n"
            disp_str += "Complete:\t\t Yes" if t['completed'] else "Complete:\t\t No"
            print(color(disp_str, BLUE))
            i += 1
    return task_index


# Allows the user to choose a task from the list of tasks,
# And uses their input as an index to select that task.
def task_input(user_index, task_file, color):
    """
    The function `task_input` takes user input to select a task from a list and returns the index of the
    selected task.

    :param user_index: user_index is a list that contains the indices of tasks in the task_file. It is
    used to map the user's input to the corresponding task in the task_file
    :param task_file: The `task_file` parameter is a list of dictionaries that represents a collection
    of tasks. Each dictionary in the list represents a single task
    :return: the index of the selected task from the task_file.
    """
    while True:
        user_input = input(
            "Please choose a Task from the list or enter -1 to return: ")
        if user_input.isnumeric():
            user_input = int(user_input)

            # Creating the user selected index variable for later use
            find_index = user_index[user_input-1]
            # Input validation and a print out for the user to see
            # Which task has been selected
            if user_input > 0 <= (len(user_index)) - 1:
                print(color(f"""\nYou have selected the task: {
                    task_file[find_index]["title"]}""", GREEN))

            else:
                print(color("Not a valid option, try again: ", RED))
                continue

        # Returns -1 to break out of the while loop in the main code
        elif user_input == "-1":
            return user_input

        else:
            print(color("Not a valid option"))
            continue
        return find_index


# Allows the user to edit the selected task in different ways.
def edit_task(task_index, task_file, color, username_password):
    """
    The function `edit_task` allows the user to mark a task as complete, edit a task by assigning it to
    a different user or changing the due date.

    :param task_index: The task_index parameter is the index of the task in the task_file list that you
    want to edit
    :param task_file: The `task_file` parameter is a list of dictionaries that represents a collection
    of tasks. Each dictionary in the list represents a single task and contains the following key-value
    pairs:
    :return: the updated task_file.
    """
    while True:
        print(
            "\nWould you like to:\n1. Mark the Task to complete\n2. Edit this Task\n3. Exit")
        sub_menu = input(": ")

        # Set Task to complete
        if sub_menu == "1":
            task_complete = input(color(
                "Enter 'y' to complete Task, 'n' to return: ", GREEN))
            if task_complete == "y":
                task_file[task_index]["completed"] = True
                return task_file
            elif task_complete == "n":
                break
            else:
                print(color("Invalid option, try again: ", RED))
                continue

        # Edit a task
        elif sub_menu == "2":
            complete = task_file[task_index]["completed"]
            if complete == True:
                print(color("\nYou cannot edit an already completed task", RED))
                print("Please choose another task")
                break

            else:
                print("\nPlease choose which option you would like to edit ")
                print("1. Assign to different user\n2. Edit Due Date")
                edit_option = input(": ")

                # Assgin a new user to the selected task
                if edit_option == "1":
                    print("\nAssign Task to Different User")
                    change_user = input(
                        "Please enter the new user to assign this task to:  ")

                    # Checks new user is in the username_password dictionary
                    # before changing
                    if change_user.isalnum() and change_user in username_password:
                        task_file[task_index]["username"] = change_user
                        print(f"Task assgined to {change_user}")
                        input(color("Press Any Key to continue", GREEN))
                        break
                    else:
                        print(color("Please enter a valid user", RED))
                        continue
                # Allows user to change the due date of the task
                elif edit_option == "2":
                    print("\nEdit Tasks Due date")
                    while True:
                        curr_date = date.today()
                        try:
                            new_due_date = input(
                                "Enter new due date of task (YYYY-MM-DD): ")
                            due_date_time = datetime.strptime(
                                new_due_date, DATETIME_STRING_FORMAT)

                            # Changes the due date to the previous input
                            task_file[task_index]["due_date"] = due_date_time

                            # Updates the assigned date to the day the task was edited
                            task_file[task_index]["assigned_date"] = curr_date

                            print(color(f"""{task_file[task_index]["title"]}'s Due date is now: {
                                  new_due_date}""", GREEN))
                            break
                        except ValueError:
                            print(color(
                                "Invalid datetime format. Please use the format specified", RED))

        elif sub_menu == "3":
            break
    return task_file
