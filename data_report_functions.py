from datetime import date
import copy

DATETIME_STRING_FORMAT = "%Y-%m-%d"

#  Color constants used in the add_color() function
GREEN = '\033[1;32m'
RED = '\033[1;31m'
BLUE = '\033[0;34m'


# Allows changes to the task_file to be updated and written to the
# Tasks.txt file
def write_to_file(task_file, prompt, color):
    """
    The function `write_to_file` takes a list of task dictionaries and writes their attributes to a file
    in a specific format, and then prints a prompt.

    :param task_file: The `task_file` parameter is a list of dictionaries, where each dictionary
    represents a task. Each task dictionary should have the following keys:
    :param prompt: The `prompt` parameter is a string that represents a message or prompt that you want
    to print after writing to the file. It can be used to provide feedback or notify the user about the
    completion of the file writing process
    """
    with open("tasks.txt", "w") as task_write:
        return_list = []
        for t in task_file:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(
                    DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            return_list.append(";".join(str_attrs))
        task_write.write("\n".join(return_list))
    print(color(prompt, GREEN))


# Calculates the percentage of two integers
# returns 0 if ZeroDivisionError present
def percentage(x: int, y: int) -> int:
    try:
        return round((x/y) * 100, 1)
    except:
        ZeroDivisionError
        return 0


#  Creates an almost empty dictionary, which a for loop will populate
#  Depending on certain logic, this creates the task_overview data
def task_overview_data(task_file: list, calculation) -> int:
    """
    The function `task_overview_data` takes a task file as input and returns an overview dictionary
    containing information about the total number of tasks, completed tasks, incomplete tasks, overdue
    tasks, and the percentage of incomplete and overdue tasks.

    :param task_file: The parameter `task_file` is expected to be a list of dictionaries, where each
    dictionary represents a task. Each task dictionary should have the following keys:
    :return: a dictionary containing various statistics about the task file.
    """
    curr_date = date.today()
    overview_dict = {
        "total_task": len(task_file),
        "total_completed": 0,
        "total_incomplete": 0,
        "total_overdue": 0,
        "percent_incomplete": 0,
        "percent_overdue": 0,
    }

    for task in task_file:
        if task["completed"] == True:
            overview_dict["total_completed"] += 1

        elif task["completed"] == False:
            overview_dict["total_incomplete"] += 1
            # Checks if the task is overdue and adds one to
            # The counter
            if task['due_date'].date() < curr_date:
                overview_dict["total_overdue"] += 1

    # uses the percentage function to calculate the results
    overview_dict["percent_incomplete"] = calculation(
        overview_dict["total_incomplete"], len(task_file))
    overview_dict["percent_overdue"] = calculation(
        overview_dict["total_overdue"], len(task_file))
    return overview_dict


# Creates two dictionarys, from looping over the username_password
# List and the task_file list, to populate the dictionarys with relevant data
def user_overview_data(task_file: list, user_pass: dict, calculation, username_password: dict) -> dict:
    """
    The function `user_overview_data` calculates various statistics about user tasks and returns them in
    a dictionary format.

    :param task_file: The `task_file` parameter is a list of dictionaries that represents the tasks.
    Each dictionary in the list contains information about a specific task, such as the username of the
    user assigned to the task, whether the task is completed or not, and the due date of the task
    :param user_pass: A dictionary containing usernames as keys and passwords as values. This dictionary
    represents the usernames and passwords of the users in the system
    :param calculation: The "calculation" parameter is a function that takes two arguments and returns a
    calculated value. It is used to calculate the percentages in the "overview_dict" dictionary. The
    function should take the numerator and denominator as arguments and return the calculated value
    :return: an overview dictionary that contains information about the users and their tasks. The
    dictionary includes the total number of users and tasks, as well as information about each user's
    tasks, such as the percentage of total tasks, percentage of completed tasks, percentage of tasks
    due, and percentage of overdue tasks.
    """
    curr_date = date.today()
    # Local variables to be used in the percentage calculation
    total_completed = 0
    total_incomplete = 0
    total_overdue = 0

    overview_dict = [{
        "total_users": len(username_password),
        "total_tasks":  len(task_file),
    },
    ]

    dict_template = {
        "user": "",
        "user_tasks": 0,
        "percent_total": 0,
        "percent_complete": 0,
        "percent_due":  0,
        "percent_overdue": 0,
    }

    for user in user_pass.keys():
        for tasks in task_file:
            if tasks["username"] == user and dict_template["user"] == "":
                dict_template["user"] = user
                dict_template["user_tasks"] = 1

                if tasks["completed"] == True:
                    total_completed = 1
                else:
                    total_incomplete = 1
                    if tasks['due_date'].date() < curr_date:
                        total_overdue = 1

            elif tasks["username"] == user:
                dict_template["user_tasks"] += 1

                if tasks["completed"] == True:
                    total_completed += 1
                else:
                    total_incomplete += 1
                    if tasks['due_date'].date() < curr_date:
                        total_overdue += 1

            # Resets the dict_template for the next user in the loop
            elif tasks["username"] != user and dict_template["user"] == "":
                dict_template["user"] = user
                dict_template["user_tasks"] = 0
                total_completed = 0
                total_incomplete = 0
                total_overdue = 0

        # One the template has been populate, we copy this
        # for further calculations to be made.
        user_dict = copy.copy(dict_template)

        user_dict["percent_total"] = calculation(
            user_dict["user_tasks"], len(task_file))
        user_dict["percent_complete"] = calculation(
            total_completed, user_dict["user_tasks"])
        user_dict["percent_due"] = calculation(
            total_incomplete, user_dict["user_tasks"])
        user_dict["percent_overdue"] = calculation(
            total_overdue, user_dict["user_tasks"])

        # The copy is appended to the overview_dict to then be
        # returned
        overview_dict.append(user_dict)
        # Resets this "user" value in the template dictionary
        dict_template["user"] = ""

    return overview_dict

# Creates the task_overview txt file


def create_task_report(file, report_list: list) -> None:
    """
    The function `create_task_report` takes a file and a dictionary of task report values, and writes a
    formatted report to the file.

    :param file: The `file` parameter is the name or path of the file where the task report will be
    created
    :param report_list: The `report_list` parameter is a dictionary that contains the following keys and
    values:
    """
    # Opens the file in the argument as read
    with open(file, "w") as report:
        value_list = []
        #  Loops through the report_list and appends all values
        # To the value_list variable
        for values in report_list.values():
            value_list.append(values)

        # Writes the f string in the desired format to the txt file,
        # Indexing the data in value_list
        report.write(f"""Total number of tasks: {value_list[0]}\nNumber of Complete tasks: {
            value_list[1]}\nNumber of Incomplete tasks: {value_list[2]}\nNumber of Overdue tasks: {
            value_list[3]}\nIncomplete Tasks {value_list[4]}%\nOverdue Tasks {value_list[5]}%""")


#  Creates the user_overview txt file
def create_user_report(file: __file__, report_list: list) -> None:
    """
    The function `create_user_report` takes a file and a list of dictionaries as input, and writes a
    report containing user information to the file.

    :param file: The `file` parameter is the name or path of the file where the report will be written
    :param report_list: The `report_list` parameter is a list of dictionaries. Each dictionary
    represents a user and contains the following keys:
    """
    with open(file, "w") as report:
        value_list = []

        # Loops through overview data, and appends dictionary values to value_list
        for values in report_list:
            value_list.append(list(values.values()))
        counter = 1

        # While the counter is <= the number of tasks
        while counter <= value_list[0][0]:
            # Writes total number of users and tasks only the first time
            if counter == 1:
                report.write(f"""\nTotal number of users: {
                    value_list[0][0]}\nTotal number of Tasks: {
                    value_list[0][1]}\n\nUsername: {
                    value_list[counter][0]}\nNumber of assigned tasks: {
                    value_list[counter][1]}\nUsers percentage of Total tasks: {
                    value_list[counter][2]}%\nUsers completed task percentage: {
                    value_list[counter][3]}%\nUsers due Tasks: {
                    value_list[counter][4]}%\nUsers overdue Tasks {value_list[counter][5]}%""")
            else:
                report.write(f"""\n\nUsername: {value_list[counter][0]}\nNumber of assigned tasks: {
                    value_list[counter][1]}\nUsers percentage of Total tasks: {
                    value_list[counter][2]}%\nUsers completed task percentage: {
                    value_list[counter][3]}%\nUsers due Tasks: {
                    value_list[counter][4]}%\nUsers overdue Tasks {value_list[counter][5]}%""")

            counter += 1

# Reads through overview file entered in the argument
# And displays them to the user


def display_stats(file, prompt, color):
    """
    The function `display_stats` reads a file and prints its contents line by line, with an optional
    prompt.

    :param file: The file parameter is the name or path of the file that contains the statistics data
    :param prompt: The prompt is a string that will be displayed before printing the contents of the
    file. It is used to provide context or information to the user before displaying the statistics
    """
    with open(file, "r") as tasks:
        stats = tasks.readlines()
        print("-" * 26)
        print(f"{prompt}")
        print("-" * 26)

        for line in stats:
            print(line.strip("\n"))

    print("-" * 26)
    # Screen holder so the user can continue when ready
    input(color("Press any key to continue", GREEN))


def add_color(string, color):
    """
    The function `add_color` takes a string and a color as input and returns the string with the
    specified color applied.

    :param string: The `string` parameter is a string that you want to add color to
    :param color: The `color` parameter is a string that represents the color you want to apply to the
    `string`
    :return: a new string with the input string wrapped in the specified color.
    """
    off = '\033[0m'
    new_string = f"{color} {string} {off}"
    return new_string
