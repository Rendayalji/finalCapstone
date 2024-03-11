"""This Task Manager application is designed for a small business
to help it manage tasks assigned to each member of a team by Admin.
The Task Manager Program is written in the Python and lists,
dictionaries and functions are used to extend the functionality
of this simple task management system.

Admin is given additional functionality to 
register users, display statistics and generate reports.
The generate reports function provides:
- the Task Overview Report for all assigned tasks,
- the User Overview Report which shows statistics about the
percentage of tasks completed, incomplete and overdue for each user.

The users can log in, view their tasks and assign tasks to themselves,
edit tasks so that their task can be assigned to another user, edit
the task due date and mark tasks as complete.
"""


#================== Notes ======================
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise
# the program will look in your root directory for the text files.


#============ Importing libraries ==============
import os
from datetime import datetime,date
DATETIME_STRING_FORMAT = "%Y-%m-%d"


#============= Opening text files ==============

# Create task_overview.txt if it doesn't exist.
if not os.path.exists("task_overview.txt"):
    with open("task_overview.txt", "w") as default_file:
        pass
     
# Create user_overview.txt if it doesn't exist.        
if not os.path.exists("user_overview.txt"):
    with open("user_overview.txt", "w") as default_file:
        pass

#=============== Login Section ================
'''This code reads usernames and passwords from the user.txt file to 
allow a user to login.
'''

# If no user.txt file, write one with a default account.
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file: 
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n") 
   
# Converting user_data list to a dictionary
username_password = {}
username = ""
password = ""
for user in user_data:
    if ";" in user:
        username, password = user.split(";") 
        username_password[username] = password

logged_in = False
while not logged_in:

    print("\n------------------  Welcome to Task Manager  -----------------")
    print("\n--------------------------------------------------------------")
    print("LOGIN\n")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist. Please enter your details again ensuring \
correct upper and lower case letters.")
        continue 
    elif username_password[curr_user] != curr_pass:
        print("Wrong password. Please try logging in again.\n")
        continue
    else:
        print("\nYou are now logged in.\n")
        print("---------------------------------------------------------------\n")
        logged_in = True
        
              
#====== Creating task dictionaries =============

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")  # Reads entire file and returns as a string. Separates at newline. 
    task_data = [t for t in task_data if t != ""]  # Creates a list removing empty strings. 
       
task_list = []
for t_str in task_data:  # Looping through task data and creating current_task dict.
    current_task = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    current_task['username'] = task_components[0]
    current_task['title'] = task_components[1]
    current_task['description'] = task_components[2]
    current_task['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    current_task['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    current_task['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(current_task)
    
#==================== Functions ===================

def reg_user():
    '''Admin can select this option in the Main Menu to register a new
    user.  The user will be added to the user.txt file, storing their
    username and password in the dictionary username_password.'''
    
    if curr_user == "admin":
        while True:
            # Request input of a new username
            print()
            print("\n--------------------------------------------------------------")
            print("REGISTERING A NEW USER")
            new_username = input("New username:  ")
            
            # If username entered already exists in user.txt. 
            # Allow user to enter a new username.
            if new_username in username_password.keys():
                print("This username already exists. Please register with \
a different username.")
                continue
            else:
                # Request input of a new password
                new_password = input("New Password:  ")

                # Request input of password confirmation.
                confirm_password = input("Confirm Password:  ")

                # Check if the new password and confirmed password are the same.
                if new_password == confirm_password:
                    # If they are the same, add them to the user.txt file.
                    username_password[new_username] = new_password
                    with open("user.txt", "w") as out_file:    
                        user_data = []
                        for k in username_password:
                            user_data.append(f"{k};{username_password[k]}")
                        out_file.write("\n".join(user_data))
                        out_file.write("\n")
                    
                    # Printing the user name and password that has just been registered.       
                    new_user_index = user_data[-1]
                    new_user_added = new_user_index.replace( ";", "  PASSWORD:")
                    print(f"\nUSERNAME:{new_user_added} registered on Task Manager.\n")
                    break                      
                else:
                    print("Passwords do not match. Please re-enter the \
username and password.")
                    continue
                
    # If non-admin users type 'r' in the Main menu selection, the message below will be output.                
    else:
        print("\nThis option is not available to you.")
    
    
def add_task():
    '''This function allows a user to add a new task.
    The user will be asked for details which will be collected in the
    form of a dictionary.
    The task dictionary will be added task.txt file where all task
    dictionaries will be stored in a list.
    '''
    # Prompting the user for task details.
    while True:
        task_username = input("\nName of person assigned to task:  ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            continue
        
        task_title = input("Title of Task:  ")
        task_description = input("Description of Task: ")
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD):  ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break
            except ValueError:
                print("Invalid datetime format. Please use the format\
specified")
                
        # The current date.
        curr_date = datetime.now()
        
        '''Adding the data to the file task.txt and
        including 'No' to indicate if the task is incomplete.
        '''
        new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False
        }
            
        task_list.append(new_task)
        with open("tasks.txt", "w+") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))
        print("\nThis task has been added.")
        print(f"\nTask titled:\t{task_title}\nUsername:\t{task_username}\n")
        break


def view_all():
    '''Ths function reads the tasks from task.txt file and prints to the
    console.
    '''
    print("\n---------------------------------------------------------------")
    print("\tASSIGNED TASKS")
    for t in task_list:
        disp_str = f"\nTask: \t\t\t {t['title']}\n"
        disp_str += f"Assigned to: \t\t {t['username']}\n"
        disp_str += f"Date Assigned: \t\t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t\t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \t {t['description']}\n"
        if t['completed'] == True:
            disp_str += f"Task complete ?: \t Yes"
        else:
            disp_str += f"Task complete ?: \t No"
        print(disp_str)
    
            
def view_mine():
    '''This functions enables the user to view their own tasks which
    are read from task.txt file. The tasks can be identified by their
    Task number.
    For incomplete task(s), the task(s) can be marked as completed
    and edited for a new due date and assigned to another user.
    '''
    
    # Displaying the current user's tasks.
    while True: 
        print("\n---------------------------------------------------------------")
        print("YOUR TASKS")   
        for index, t in enumerate(task_list):  # Numbering the tasks for identification.
            if t['username'] == curr_user: 
                disp_str = f"\nTask {index+1}: \t\t {t['title']}\n"   
                disp_str += f"Assigned to: \t\t {t['username']}\n"
                disp_str += f"Date Assigned: \t\t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Due Date: \t\t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Task Description: \t {t['description']}\n"
                if t['completed'] == True:
                    disp_str += f"Task complete ?: \t Yes"
                else:
                    disp_str += f"Task complete ?: \t No"
                print(disp_str)
        
        print("\nTasks can be marked as completed and edited \
\n(for new due date and reassigning to another user) if incomplete.")
        
        
        # The user can choose to either edit a task or return to the Main menu.
        while True:
            try:
                task_edit_choice = int(input("\nFrom your task(s) above, \
please type the \nTask number (for marking and editing the task) \
or -1 for the Main menu:  "))  
                  
            
                # If '-1' is selected the Main menu will appear.
                if task_edit_choice == -1:
                    break
                
                # To handle user input that is out of task_list range (ie. task not in tasks.txt).
                elif task_edit_choice < 1 or task_edit_choice > len(task_list): 
                    print("\nInvalid entry. Please select a task number \
from your displayed tasks.")
                    continue
                
                # A task number choosen to mark the task as complete or edit. 
                else: 
                    task_index = task_list[task_edit_choice-1]
            
            # To handle user entering a non-integer.      
            except ValueError: 
                print("\nThis is an invalid entry.  Choose a valid task \
number or -1.")  
                continue
            
            # If user enters a task number that is not in tasks.txt.
            except IndexError:                      
                print("\nThis is an invalid entry.  Select a task of yours \
that is incomplete.") 
                continue
            
            
            """ The user is asked to select marking complete their
            chosen task or editting it.
            """ 
            while True:  
                    mark_or_edit = input("\nWould you like to mark the task as \
complete (m) or edit the task (e)? (Enter m or e):  ").lower()
                    
                    if mark_or_edit == "m" or mark_or_edit == "e":
                        break
                    else:
                        print("This is an invalid entry.") 
                        continue
            
            
            """If option is 'm', the task must be incomplete and
            current user can only mark their own task as complete.
            """  
            if mark_or_edit == "m" and not task_index["completed"] and task_index["username"] == curr_user:  
                task_index["completed"] = True                    
                with open("tasks.txt", "w") as task_file:
                    task_list_to_write = []
                    for t in task_list:
                        str_attrs = [
                            t['username'],
                            t['title'],
                            t['description'],
                            t['due_date'].strftime(DATETIME_STRING_FORMAT),
                            t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                            "Yes" if t['completed'] else "No"
                        ]
                        task_list_to_write.append(";".join(str_attrs))
                    task_file.write("\n".join(task_list_to_write))
                    
                    print(f"\nThe task: {task_index["title"]} - marked as completed.\n")   
                                   
                
                """If option is 'e', the task must be incomplete and
                current user can only edit their own task.
                """
            elif mark_or_edit == "e" and not task_index['completed'] and task_index["username"] == curr_user:  
                
                # User asked to select edit username or edit due date.
                while True:
                    edit_task = input("\nWould you like to edit the \
task username (u) or due date (d)? (Enter u or d):  ").lower() 
                    
                     
                    if edit_task == "u" or edit_task == "d":
                        break
                    else:
                        print("This is an invalid entry.")
                        continue
                    
                # User's chosen task is assigned to another registered user
                # and this info is written to tasks.txt.
                if edit_task == "u" and not task_index["completed"]:
                    edit_username = input("\nPlease enter a new username for the task: ")
                    if edit_username in username_password.keys():
                        task_index["username"] = edit_username
                    
                        with open("tasks.txt", "w") as task_file:  
                            task_list_to_write = []
                            for t in task_list: 
                                str_attrs = [
                                    t['username'],
                                    t['title'],
                                    t['description'],
                                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                                    "Yes" if t['completed'] else "No"
                                ]
                                task_list_to_write.append(";".join(str_attrs))
                            task_file.write("\n".join(task_list_to_write))
                        
                        # Output to user confirming re-assigning of task.
                        print("\nTask has been re-assigned.")
                        print(f"\nTask:\t\t\t{task_index["title"]}\n\
Now assigned to:\t{edit_username}") 
                        print("\n") 
                    
                    # If new username entered is not registered ie. in username_password dictionary.
                    else:
                        print(f"{edit_username} is not a valid username so \
cannot be assigned to this task.")   
                        
                        
                    """User's chosen task is updated with a new due date
                    and this info is written to tasks.txt. 
                    """  
                elif edit_task == "d" and not task_index["completed"]:
                    
                    while True:
                        try:
                            edit_due_date = input("\nNew due date of task \
(YYYY-MM-DD):  ")
                            edit_due_date = datetime.strptime(edit_due_date, DATETIME_STRING_FORMAT)
                            break
                        except ValueError:
                            print("Invalid datetime format. Please use the \
format specified")
            
                    task_index['due_date'] = edit_due_date         
                    with open("tasks.txt", "w") as task_file:
                        task_list_to_write = []
                        for t in task_list:  
                            str_attrs = [
                                t['username'],
                                t['title'],
                                t['description'],
                                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                                "Yes" if t['completed'] else "No"
                            ]
                            task_list_to_write.append(";".join(str_attrs))
                        task_file.write("\n".join(task_list_to_write))
                        
                    print(f"\nThe task titled:\t{task_index["title"]}\
\nUpdated due date is:\t{edit_due_date}.") 
                    print("\n") 
                    
                # User inputs something other than 'u' or 'd'.
                else:
                    print("This is an invalid entry.")  
            
                """User enters a task number for a completed task or
                task number that belongs to someone else.
                """               
            else:  
                print("\nUnable to edit this task.  The task has already been \
completed or has been assigned to someone else. \n")  
        break    


def generate_user_report():
    """This function generates the User Overview Report in
    user_overview.txt which can be viewed only by admin. 
    This function gathers task data for each registered user.
     
    This generate_user_reports function is called to from the
    generate_reports function.
    """
     
    current_date = datetime.today()
    
    # This string will be written to user_overview.txt.
    user_overview = f"\n---------------------------- User Overview Report --------------------------------\n"
    user_overview += f"\nDate and time of User Overview Report: {current_date}\n"
    user_overview += f"\nTotal number of users registered with task_manager.py:\t\t\t\t {str(len(username_password.keys()))}"
    user_overview += f"\nTotal number of tasks generated and tracked by task_manager.py:\t\t {str(len(task_list))}\n" 
    
    # Loop through users in dictionary to seperate tasks by their assigned user.
    for username in username_password.keys(): 
        print("\n")
        user_tasks = 0
        user_tasks_complete = 0  
        user_tasks_incomplete = 0  
        user_tasks_overdue = 0  

        """Looping through tasks and counting total tasks, completed tasks,
        incomplete tasks and overdue tasks for each username.
        """
        for t in task_list:
            
            if t["username"] == username: 
                user_tasks += 1 # Counts user's tasks.
                
                if t["completed"] is True:
                    user_tasks_complete += 1  # Counts user's complete tasks.
                    
                else:
                    user_tasks_incomplete += 1  # Counts user's incomplete tasks.
                    if current_date > t["due_date"]:
                        user_tasks_overdue += 1   # Counts user's overdue tasks.
    
      
        user_overview += f"\n\n{username}"    
        user_overview += f"\nTotal number of tasks assigned:\t\t\t\t\t\t\t\t\t\t {str(user_tasks)}"
        # If user has assigned tasks.
        if user_tasks > 0:
            user_overview += f"\nPercentage of the total number of tasks assigned:\t\t\t\t\t {str(round(user_tasks / len(task_list) * 100, 2))}%" 
            user_overview += f"\nPercentage of tasks assigned that have been completed:\t\t\t\t {str(round(user_tasks_complete / (user_tasks) * 100, 2))}%"  
            user_overview += f"\nPercentage of tasks still to be completed:\t\t\t\t\t\t\t {str(round((user_tasks_incomplete) / (user_tasks) * 100, 2))}%" 
            user_overview += f"\nPercentage of incomplete and overdue tasks:\t\t\t\t\t\t\t {str(round((user_tasks_overdue / (user_tasks)) * 100, 2))}%\n" 
             
        # If user does not have any assigned tasks.
        else:
            user_overview += f"\nNo further statistics for this user as no tasks have been assigned to them." 
                
    with open("user_overview.txt", "w") as users_file:
        users_file.write(user_overview)


def generate_reports():
    """ This function is used to gather information about all tasks.
    The task information once gathered will be written to
    task_overview.txt. This function will generate the text file
    'task_overview.txt'.
    
    The generate_user_report function is called to when the user
    selects gr (generate reports).
    This will generate the 'user_overview.txt' 
    (See generate_user_report function in the functions section
    for the code).
    """

    current_date = datetime.today()
    
    # Setting counters to 0.
    complete_tasks = 0  
    incomplete_tasks = 0 
    overdue_tasks = 0 

    if curr_user == "admin":
        
        generate_user_report()  # If admin is the current user: Calling this function will generate a User Overview Report.
        
        # Message output to admin only.
        print("The Task Overview Report and User Overview Report\nhave \
now been generated in the text files for you to view.\n\nThese reports \
can be viewed on the screen by selecting the 'ds' option from the \
Main Menu.")
        
        for t in task_list:
            
            # Counting completed tasks.
            if t["completed"] is True:
                complete_tasks  += 1  
               
            else:
                incomplete_tasks += 1 
                
                # Counter increases by 1 for each incompleted and overdue task.    
                if current_date > t["due_date"]: 
                    overdue_tasks += 1   
                    
        """String created using counter variables from looping through task_list.
        The string task_overview will be written to task_view.txt.
        """
        task_overview = f"\n---------------------------- Task Overview Report -----------------------------------\n"
        task_overview += f"\nDate and time of report: {current_date}\n"
        task_overview += f"\nTotal number of tasks generated and tracked by task_manager.py:\t\t {str(len(task_list))}"
        task_overview  += f"\nTotal number of completed tasks:\t\t\t\t\t\t\t\t\t {str(complete_tasks)}" 
        task_overview  += f"\nTotal number of incomplete tasks:\t\t\t\t\t\t\t\t\t {str(incomplete_tasks)}"
        task_overview  += f"\nTotal number of incomplete and overdue tasks:\t\t\t\t\t\t {str(overdue_tasks)}"  
        task_overview  += f"\nPercentage of incomplete tasks:\t\t\t\t\t\t\t\t\t\t {str(round((incomplete_tasks / len(task_list)) * 100, 2))}%"
        task_overview  += f"\nPercentage of tasks that are overdue:\t\t\t\t\t\t\t\t {str(round((overdue_tasks / len(task_list)) * 100, 2))}%"  
        
        with open("task_overview.txt", "w") as tasks_file:
           tasks_file.write(task_overview)
    
    # Message output if non-admin users type 'gr'.   
    else:
        print("\nThis option is not available to you.")
            
   
def display_statistics():  
    '''This function will display on screen, general statistics (User Overview), \
Task Oveview Report and User Overview Report for admin only.'''
   
   # Printing User Overview on screen.
   
    current_date = date.today()
    
    num_users = len(username_password.keys())
    num_tasks = len(task_list)

    if curr_user == "admin":
        
        """Calling to generate_reports function.  If admin is the current user, 
Task Overview Report and User Overview Report will be generated if 
they have not already been generated."""
        generate_reports() 
        
        print("\n\n------------------------------------- User Overview --------------------------------\n")
        print(f"Date and time of User Overview: {current_date}\n")
        print(f"\nNumber of users: \t {num_users}")
        print(f"Number of tasks: \t {num_tasks}")
        print("\n------------------------------------------------------------------------------------\n\n\n")   
    
    
    # Printing Task Over Report on screen by reading from task.txt (task_list).
         
    current_date = datetime.today()
    
    # Setting counters to 0.
    complete_tasks = 0  
    incomplete_tasks = 0 
    overdue_tasks = 0 

    if curr_user == "admin":
        for t in task_list:
            
            if t["completed"] is True:
                complete_tasks  += 1  
                
            else:
                incomplete_tasks += 1  
                    
                if current_date > t["due_date"]: 
                    overdue_tasks += 1     
                    
        #  task_overview created using counter variables from looping through task_list.  
        task_overview = f"\n---------------------------- Task Overview Report -----------------------------------\n\n"
        task_overview += f"Date and time of report: {current_date}\n"
        task_overview += f"\nTotal number of tasks generated and tracked by task_manager.py:\t\t {str(len(task_list))}"
        task_overview  += f"\nTotal number of completed tasks:\t\t\t\t\t {str(complete_tasks)}" 
        task_overview  += f"\nTotal number of incomplete tasks:\t\t\t\t\t {str(incomplete_tasks)}"
        task_overview  += f"\nTotal number of incomplete and overdue tasks:\t\t\t\t {str(overdue_tasks)}"  
        task_overview  += f"\nPercentage of incomplete tasks:\t\t\t\t\t\t {str(round((incomplete_tasks / len(task_list)) * 100, 2))}%"
        task_overview  += f"\nPercentage of tasks that are overdue:\t\t\t\t\t {str(round((overdue_tasks / len(task_list)) * 100, 2))}%"  
        print(task_overview)
        print("\n---------------------------------------------------------------------------------------\n\n")
        
        # Printing User Over Report on screen by reading from task.txt (task_list) 
        # and user.txt (username_password dict).
        
        user_overview = f"\n---------------------------- User Overview Report -----------------------------------\n\n"
        user_overview += f"Date and time of report: {current_date}\n"
        user_overview += f"\nTotal number of users registered with task_manager.py:\t\t\t {str(len(username_password.keys()))}"
        user_overview += f"\nTotal number of tasks generated and tracked by task_manager.py:\t\t {str(len(task_list))}\n" 
        
        for username in username_password.keys(): # Loop through users in dict to seperate tasks by their assigned user.
            print("\n")
            user_tasks = 0
            user_tasks_complete = 0
            user_tasks_incomplete = 0
            user_tasks_overdue = 0

            for t in task_list:
                
                if t["username"] == username: 
                    user_tasks += 1
                    
                    if t["completed"] is True:
                        user_tasks_complete += 1
                    else:
                        user_tasks_incomplete += 1
                        if current_date > t["due_date"]:
                            user_tasks_overdue += 1
        
        
            user_overview += f"\n\n{username}"    
            user_overview += f"\nTotal number of tasks assigned:\t\t\t\t\t\t {str(user_tasks)}"
            
            if user_tasks > 0:
                user_overview += f"\nPercentage of the total number of tasks assigned:\t\t\t {str(round(user_tasks / len(task_list) * 100, 2))}%" 
                user_overview += f"\nPercentage of tasks assigned that have been completed:\t\t\t {str(round(user_tasks_complete / (user_tasks) * 100, 2))}%"  
                user_overview += f"\nPercentage of tasks still to be completed:\t\t\t\t {str(round((user_tasks_incomplete) / (user_tasks) * 100, 2))}%" 
                user_overview += f"\nPercentage of incomplete and overdue tasks:\t\t\t\t {str(round((user_tasks_overdue / (user_tasks)) * 100, 2))}%\n"  
            else:
                user_overview += f"\nNo further statistics for this user as no tasks have been assigned to them."
        
        print(user_overview)
        print("\n---------------------------------------------------------------------------------------\n\n")
    
    # If non-admin users enter 'ds' from the Main menu.    
    else: 
        print("\nThis option is not available for you.")  
            
                     
#=============================== MAIN CODE ===============================

while True:
    # Presenting the Main menu to admin.
    if curr_user == "admin" and curr_pass == "password":
        print("\n------------------------------------------------------------")
        print("MAIN MENU\n")
        menu = input('''Select one of the following options:\n
r  -\t Registering a user
a  -\t Adding a task
va -\t View all tasks
vm -\t View my tasks
gr -\t Generate reports
ds -\t Display statistics
e  -\t Exit
:\n  ''').lower()  # Making sure that the user input is converted to lower case.

    
    # Main menu will be presented to all registered users.
    else:
        print("\n------------------------------------------------------------")
        print("MAIN MENU\n")
        menu = input('''Select one of the following options:\n
a  -\t Adding a task
va -\t View all tasks
vm -\t View my tasks
e  -\t Exit
:  ''').lower()


    if menu == 'r':
        reg_user()
        
    elif menu == 'a':
        add_task()
        
    elif menu == 'va':
        view_all()
        
    elif menu == 'vm':
        view_mine()
    
    elif menu == "gr":
        generate_reports()
    
    elif menu == "ds":
        display_statistics()
        
    elif menu == 'e':
        print('\nGoodbye!!!\n')
        break
     
    else:
        print("\nYou have made a wrong choice. Please select an option \
from the MAIN MENU.")
  
