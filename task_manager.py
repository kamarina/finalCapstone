from datetime import datetime, date
import os
# bold formatting

DATETIME_STRING_FORMAT = "%Y-%m-%d"  # Format used for datetime string representation


class TaskManager:
    """TaskManager class is used to manage tasks (adding, viewing and editing)
    as well as user authentication and registration"""
    def __init__(self):

        self.username_password = {}  # Empty dictionary to store user credentials
        self.task_list = []  # Empty list that will store task info
        self.logged_in_user = None  # Tracks the currently logged-in user
        self.load_data()  # Load user task data from files

    def load_data(self):
        """Loads user data and task data from respective files."""
        self.load_user_data()
        self.load_task_data()

    def load_user_data(self):
        """ Loads user data from 'user.txt', creating the file if it doesn't exist,
        and stores it in the username_password dictionary."""
        if not os.path.exists("user.txt"):
            with open("user.txt", "w") as default_file:
                default_file.write("admin;password")

        with open("user.txt", 'r') as user_file:
            user_data = user_file.read().split("\n")

        for user in user_data:
            try:
                username, stored_password = user.split(';')
                self.username_password[username] = stored_password
            except ValueError:
                print(f"Invalid user data format: {user}")

    def check_password(self, entered_password, stored_password):
        """Checks if the entered password matches the stored password."""
        return entered_password == stored_password

    def login_user(self, username, entered_password):
        """Attempts to log in a user with the provided username and password.
        Returns True on successful login, False when failed."""
        if username not in self.username_password:
            print("User does not exist")
            return False
        elif not self.check_password(entered_password, self.username_password[username]):
            print("Wrong password!\n")
            return False
        else:
            self.logged_in_user = username
            print("Login Successful!")
            return True

    def load_task_data(self):
        """Loads task data from 'tasks.txt', creating the file if it doesn't exist,
        and stores it in the task_list."""
        if not os.path.exists("tasks.txt"):
            with open("tasks.txt", "w"):
                pass

        with open("tasks.txt", 'r') as task_file:
            task_data = task_file.read().split("\n")
            task_data = [t for t in task_data if t != ""]

        for t_str in task_data:
            task_components = t_str.split(";")
            self.task_list.append({
                'username': task_components[0],
                'title': task_components[1],
                'description': task_components[2],
                'due_date': datetime.strptime(task_components[3], DATETIME_STRING_FORMAT),
                'assigned_date': datetime.strptime(task_components[4], DATETIME_STRING_FORMAT),
                'completed': True if task_components[5] == "Yes" else False
            })

    def save_data(self):
        """Saves task data and user data to their destination files."""
        self.save_task_data()
        self.save_user_data()

    def save_user_data(self):
        """Saves the current user data from the username_password dictionary to 'user.txt'."""
        with open("user.txt", "w") as user_file:
            user_list_to_write = [f"{user};{self.username_password[user]}" for user in self.username_password]
            user_file.write("\n".join(user_list_to_write))

    def save_task_data(self):
        """Saves the current task data from the task_list list to 'tasks.txt'."""
        with open("tasks.txt", "w") as task_file:
            task_list_to_write = [
                f"{t['username']};{t['title']};{t['description']};"
                f"{t['due_date'].strftime(DATETIME_STRING_FORMAT)};"
                f"{t['assigned_date'].strftime(DATETIME_STRING_FORMAT)};"
                f"{'Yes' if t['completed'] else 'No'}"
                for t in self.task_list
            ]
            task_file.write("\n".join(task_list_to_write))

    def reg_user(self):
        """Registers a new user with a username and password after confirming the password.
        Username must be unique."""
        new_username = input("New Username: ")
        if new_username in self.username_password:
            print("Username already exists. Please choose a different username.")
            return

        new_password = input("New Password: ")
        confirm_password = input("Confirm Password: ")
        if new_password == confirm_password:
            self.username_password[new_username] = new_password
            print("User registration successful.")
            self.save_user_data()
        else:
            print("Passwords don't match. User registration failed.")

    def add_task(self):
        """Adds a new task with a title, description, due date, and sets the assigned date to today.
        Available to logged-in users only."""
        task_username = input("Name of person assigned to task: ")
        if task_username not in self.username_password:
            print("User does not exist. Please enter a valid username.")
            return

        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")

        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break
            except ValueError:
                print("Invalid datetime format. Please use the format specified (YYYY-MM-DD)")

        curr_date = date.today()
        new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False
        }
        self.task_list.append(new_task)
        self.save_task_data()
        print("Task successfully added.")

    def view_all(self):
        """Displays all tasks assigned to registered users."""
        print("Viewing all tasks:")
        for i, task in enumerate(self.task_list, start=1):
            self.display_task(task, i)

    def view_mine(self):
        """Displays all tasks assigned to the logged-in user, including their completion status."""
        print("Viewing your tasks:")
        user_tasks = [t for t in self.task_list if t['username'] == self.logged_in_user]
        if user_tasks:
            for i, task in enumerate(user_tasks, start=1):
                print(f"{i}. Task: {task['title']}\n")
                print(f"Due Date: {task['due_date'].strftime(DATETIME_STRING_FORMAT)}")
                print(f"Task Description: {task['description']}")
                print(f"Completed: {'Yes' if task['completed'] else 'No'}\n")
        else:
            print("You have no tasks assigned.")

        task_option = input("Enter the task number to edit or mark as complete, or '-1' to return to the main menu: ")
        if task_option.isdigit() and 1 <= int(task_option) <= len(user_tasks):
            task_index = int(task_option) - 1
            selected_task = user_tasks[task_index]
            if selected_task['completed']:
                print("This task is already completed.")
                return
            action = input("Enter 'complete' to mark the task as complete or 'edit' to edit the task: ")
            if action == 'complete':
                selected_task['completed'] = True
                print("Task marked as completed.")
            elif action == 'edit':
                new_username = input("Enter the new username for the task (leave blank to keep current): ")
                if new_username:
                    if new_username in self.username_password:
                        selected_task['username'] = new_username
                    else:
                        print("Username does not exist. Task not updated.")
                        return
                new_due_date = input(
                    "Enter the new due date for the task (YYYY-MM-DD) or leave blank to keep current: ")
                if new_due_date:
                    try:
                        selected_task['due_date'] = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                    except ValueError:
                        print("Invalid datetime format. Task not updated.")
                        return
                print("Task updated successfully.")
            else:
                print("Invalid option.")
        elif task_option != '-1':
            print("Invalid task number.")
        self.save_task_data()

    def display_stats(self):
        """If the user is an admin, they can display statistics about the number of users and tasks."""
        # Check if reports exist and generate them if needed
        if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
            task_manager.generate_reports()
            print("Reports generated successfully!")

        curr_user = self.logged_in_user
        if curr_user == 'admin':
            try:
                with open("task_overview.txt", "r") as task_overview_file:
                    task_overview_content = task_overview_file.read()
                print("Task Overview:")
                print(task_overview_content)
            except FileNotFoundError:
                print("Task overview file not found.")

            try:
                with open("user_overview.txt", "r") as user_overview_file:
                    user_overview_content = user_overview_file.read()
                print("\nUser Overview:")
                print(user_overview_content)
            except FileNotFoundError:
                print("User overview file not found.")
        else:
            print("You do not have permission to view statistics. Only 'admin' can perform this action.")


    def display_task(self, task, task_number):
        """Display task in a unified way."""
        task_number_str = f"Task {task_number}: " if task_number is not None else ""
        disp_str = f"{task_number_str}{task['title']}\n"
        disp_str += f"\nAssigned to: {task['username']}\n"
        disp_str += f"Date Assigned: {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: {task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: {task['description']}\n"
        disp_str += f"Completed: {'Yes' if task['completed'] else 'No'}\n"
        print(disp_str + "-" * 50)

    def generate_reports(self):
        """Generate reports, only available to 'admin' user."""
        total_users = len(self.username_password)
        total_tasks = len(self.task_list)
        completed_tasks = sum(1 for task in self.task_list if task['completed'])
        uncompleted_tasks = total_tasks - completed_tasks

        today_datetime = datetime.combine(date.today(), datetime.min.time())

        with open("task_overview.txt", "w") as task_overview_file:
            task_overview_file.write(f"Total tasks: {total_tasks}\n")
            task_overview_file.write(f"Completed tasks: {completed_tasks}\n")
            task_overview_file.write(f"Uncompleted tasks: {uncompleted_tasks}\n")

            if total_tasks > 0:
                overdue_tasks = sum(1 for task in self.task_list if not task['completed']
                                    and task['due_date'] < today_datetime)
                task_overview_file.write(f"Overdue tasks: {overdue_tasks}\n")
                task_overview_file.write(f"Percentage of incomplete tasks: "
                                         f"{uncompleted_tasks / total_tasks * 100:.2f}%\n")
                task_overview_file.write(f"Percentage of overdue tasks: {overdue_tasks / total_tasks * 100:.2f}%\n")

        with open("user_overview.txt", "w") as user_overview_file:
            user_overview_file.write(f"Total users: {total_users}\n")
            user_overview_file.write(f"Total tasks: {total_tasks}\n")

            for user in self.username_password:
                user_tasks = [task for task in self.task_list if task['username'] == user]
                total_user_tasks = len(user_tasks)
                completed_user_tasks = sum(1 for task in user_tasks if task['completed'])
                uncompleted_user_tasks = total_user_tasks - completed_user_tasks

                user_overview_file.write(f"\nUser: {user}\n")
                user_overview_file.write(f"Total tasks assigned: {total_user_tasks}\n")

                if total_user_tasks > 0:
                    user_overview_file.write(f"Percentage of tasks assigned: "
                                             f"{total_user_tasks / total_tasks * 100:.2f}%\n")
                    user_overview_file.write(
                        f"Percentage of completed tasks: {completed_user_tasks / total_user_tasks * 100:.2f}%\n")
                    user_overview_file.write(
                        f"Percentage of uncompleted tasks: {uncompleted_user_tasks / total_user_tasks * 100:.2f}%\n")

                    overdue_user_tasks = sum(
                        1 for task in user_tasks if not task['completed'] and task['due_date'] < today_datetime)
                    user_overview_file.write(
                        f"Percentage of overdue tasks: {overdue_user_tasks / total_user_tasks * 100:.2f}%\n")


def main():
    """Runs the main functionality of the Task Manager program"""
    task_manager = TaskManager()

    logged_in = False
    while not logged_in:
        print("LOGIN")
        username = input("Username: ")
        password = input("Password: ")
        logged_in = task_manager.login_user(username, password)

    while True:
        print()
        menu = input('''Select one of the following Options:
        r - Registering a user
        a - Adding a task
        va - View all tasks
        vm - View my task
        ds - Display statistics 
        gr - Generate Reports
        e - Exit
        Your choice: ''').lower()
        print(f"{'-' * 50}")

        if menu == 'r':
            task_manager.reg_user()

        elif menu == 'a':
            task_manager.add_task()

        elif menu == 'va':
            task_manager.view_all()

        elif menu == 'vm':
            task_manager.view_mine()

        elif menu == 'ds':
            task_manager.display_stats()

        elif menu == 'gr':
            task_manager.generate_reports()
            print("Reports generated successfully!")

        elif menu == 'e':
            print('Goodbye!!!')
            task_manager.save_data()
            break  # Exit the loop when 'e' is entered
        else:
            print("Invalid option selected. Please try again.")


if __name__ == "__main__":
    main()
