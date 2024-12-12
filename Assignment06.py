# ------------------------------------------------------------------------------------------ #
# Title: Assignment06
# Desc: This assignment demonstrates using classes, functions, and structured errors.
# Change Log: (Who, When, What)
#   Jason Coult, 12/11/2024, Created script
# ------------------------------------------------------------------------------------------ #

# Import statements section----------------------------------------------------------------- #

import json

# Data layer ------------------------------------------------------------------------------- #

# Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"  # Name of data file

# Variables
students: list = []  # a table of student data
menu_choice: str = ''  # Hold the choice made by the user.

# Processing layer -------------------------------------------------------------------------- #

class FileProcessor:
    """
    Functions that handle use of json data files.

    Changelog:
    Jason Coult, 12/10/2024, Create script for Lab03
    Jason Coult, 12/11/2024, Modify script for Assignment06
    """

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """
        This function reads data from file.

        Changelog:
        Jason Coult, 12/11/2024, Create function

        :param file_name: string for file name
        :param student_data: list of students
        :return: list
        """

        try:
            file = open(file_name, "r")  # Open in read mode
            student_data = json.load(file)  # Use json package function to open json file
            file.close()  # Close after read-in
        except FileNotFoundError as e:  # Specific error case for missing file. Show file name to user.
            IO.output_error_messages("The JSON file " + file_name + " does not exist!\n",e)  # Call error output message
        except Exception as e:  # General error
            IO.output_error_messages("There was a general error!\n",e)  # Catch-all error statement
        finally:
            if file.closed == False:  # Closes file in case the close statement wasn't reached due to error
                file.close()
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """ This function writes data to file

        Changelog:
        Jason Coult, 12/11/2024, Create function

        :param file_name: string for file name
        :param student_data: list of student data
        :return: none
        """

        try:
            file = open(file_name, "w")  # Open file in write mode
            json.dump(student_data, file, indent=4)  # Save data & format it nicely within the file
            file.close()
            print("The following roster was saved to file:")
            IO.output_student_courses(student_data)  # Display what was just written to file
        except TypeError as e:
            IO.output_error_messages("Please check that data is valid JSON format", e)
        except Exception as e:
            IO.output_error_messages("A general error has occurred!", e)
        finally:
            if file.closed == False:
                file.close()

# Presentation & I/O layer ------------------------------------------------------------------- #

class IO:
    """
    Functions that handle the user I/O.

    Changelog:
    Jason Coult, 12/10/2024, Create script for Mod06-Lab03
    Jason Coult, 12/11/2024, Modify script for assignment6
    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """
        This function displays a custom error message to the user.

        Changelog:
        Jason Coult, 12/10/2024, Create function

        :param message: string for message
        :param error: exception for error
        :return: None
        """

        print("\n !!! Error Warning !!! \n")
        print(message, end="\n")  # Print the error message
        print()
        if error is not None:  # Print more details
            print("-- Technical Details of Error --")
            print(error.__doc__, type(error), sep='\n')
        print()

    @staticmethod
    def output_menu(menu: str):
        """
        This function displays the menu of choices to the user.

        ChangeLog:
        Jason Coult, 12/10/2024, Created script for lab03
        Jason Coult, 12/11/2024, Modify script for Assignment6

        :param menu: string
        :return: None
        """

        print(menu)  # Print the menu

    @staticmethod
    def input_menu_choice():
        """
        This function collects user input for menu choice.

        ChangeLog:
        Jason Coult, 12/10/2024, Created script for lab03
        Jason Coult, 12/11/2024, Modify script for Assignment6

        :return: string
        """

        try:
            choice = input("Enter your menu choice number: ")  # User input prompt
            if len(choice) == 0:  # Error case for no input
                raise Exception("No choice made. Please enter a choice!")
            elif choice not in ("1", "2", "3", "4"):  # Error case for invalid selection
                raise Exception("Please only chose 1,2,3,4")
        except Exception as e:
            IO.output_error_messages(e.__str__(), e)  # Display the particular error message
        return choice  # Return the user's choice

    @staticmethod
    def output_student_courses(student_data: list):
        """
        This function displays the list of students and their courses.

        ChangeLog:
        Jason Coult, 12/11/2024, Create script

        :param student_data: list of student data
        :return: None
        """

        print("-" * 50)
        print("   -    Student Roster    -   ")
        for student in student_data:  # Loop through list and print each student/course
            print(f'{student["FirstName"]} {student["LastName"]} is enrolled in {student["CourseName"]}')
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list):
        """
        This function gets the student data input from the user.

        Changelog:
        Jason Coult, 12/11/2024, Create script

        :param student_data: list of student data
        :return: list
        """

        try:
            # Enter first name and check value for errors
            student_first_name = input("Enter the student's first name: ")  # Individual name entry
            if len(student_first_name) == 0:  # Check for an empty name first
                raise ValueError("The student's first name should not be empty.")
            elif not student_first_name.isalpha():  # Then check if it contains numbers
                raise ValueError("The student's first name should not contain a number.")

            # Enter last name and check value for errors
            student_last_name = input("Enter the student's last name: ")
            if len(student_last_name) == 0:  # Check for an empty entry first again
                raise ValueError("The student's last name should not be empty.")
            elif not student_last_name.isalpha():  # Then check if it contains numbers
                raise ValueError("The student's last name should not contain a number.")

            # Enter course name and check for errors
            course_name = input("Please enter the name of the course: ")
            if len(course_name) == 0:  # Check for empty course name entry
                raise ValueError("The course name should not be empty.")

            # Now combine the inputs together into the entry
            student = {"FirstName": student_first_name,
                            "LastName": student_last_name,
                            "CourseName": course_name}
            student_data.append(student)  # Append the new student to the roster
            print(f"You have registered {student_first_name} {student_last_name} for {course_name}.")
        except ValueError as e:
            IO.output_error_messages(e.__str__(), e)  # Display the specific string message for particular error
        except Exception as e:
            IO.output_error_messages("There was a general error with your input data!",e)
        return student_data


# Main body of program ------------------------------------------------------------------- #

# First, load data file
students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

# Loop continuously through options
while True:

    # Present choices and get user input
    IO.output_menu(menu=MENU)  # Display menu text
    menu_choice = IO.input_menu_choice()  # Prompt user input

    # Input user data
    if menu_choice == "1":
        students = IO.input_student_data(student_data=students)  # Input a new student and add to roster of students
        IO.output_student_courses(student_data=students)  # Show the updated roster
        continue

    # Present the current data
    elif menu_choice == "2":

        IO.output_student_courses(student_data=students)  # Display the current roster
        continue

    # Save the data to a file
    elif menu_choice == "3":

        FileProcessor.write_data_to_file(file_name=FILE_NAME,student_data=students)  # Write students roster to file
        continue

    # Exit by stopping the loop
    elif menu_choice == "4":
        break  # Quit out of the loop

    #
    else:
        print("Please select a valid menu choice!")

print("Program Ended")
