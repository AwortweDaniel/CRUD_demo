import mysql.connector
from mysql.connector import errorcode

config ={'user':'root',
         'port': 3306,
         'password':'root',
         'host':'localhost',
         'database':'students_register'}

try:
    connection = mysql.connector.connect(**config)
    if connection.is_connected():
        print("connection is established...")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Check your username and password.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database doesn't exist.")
    else:
        print(err)



def dataCreation(name, contact, email, course, department):
    cursor = connection.cursor()
    query = "INSERT INTO student_detail (student_name, contact,email, course, department) VALUES (%s,%s,%s,%s,%s)"
    values= (name, contact, email, course, department)

    cursor.execute(query, values)
    connection.commit()
    print("Student data created successfully")

    cursor.close()



def dataReading():
    cursor = connection.cursor()
    query = "SELECT * FROM student_detail"

    cursor.execute(query)
    rows = cursor.fetchall()

    student_details = [{"Id":row[0], "Name":row[1],"Contact":row[2],"Email":row[3], "Course":row[4],
                        "Department":row[5]}  for row in rows]
    print(student_details)

    cursor.close()




def dataUpdating(name):
    cursor = connection.cursor()
    updateWhat= input("Enter what to update(contact/email/course/department):\n")
    if updateWhat.lower() == 'contact':
        new_contact = input("Enter new contact: ")
        query = "UPDATE student_detail SET contact = %s WHERE student_name = %s"
        values = (new_contact, name)
    elif updateWhat.lower() == 'email':
        new_email = input("Enter new email: ")
        query = "UPDATE student_detail SET email = %s WHERE student_name = %s"
        values = (new_email, name)
    elif updateWhat.lower() == 'course':
        new_course = input("Enter new course: ")
        query = "UPDATE student_detail SET course = %s WHERE student_name = %s"
        values = (new_course, name)
    elif updateWhat.lower() == 'department':
        new_department = input("Enter new department: ")
        query = "UPDATE student_detail SET department = %s WHERE student_name = %s"
        values = (new_department, name)
    else:
        print("Invalid input or missing update value.")
        return

    cursor.execute(query, values)
    connection.commit()

    print(f"Updated {updateWhat} successfully for {name}")


def dataDeletion(name):
    cursor = connection.cursor()

    query = "DELETE FROM student_detail WHERE student_name = %s"
    values = (name,)

    cursor.execute(query, values)
    connection.commit()

    print("Data deleted successfully.")

    cursor.close()



print("Hello! Welcome to Student data Management System,\nIt supports Data Creation, Data Reading, Data Update, and Data Deletion.\n\n")
print("1. Create Student Data\n"
      "2. Read Student Data\n"
      "3. Update Student Data\n"
      "4. Delete Student Data\n")

while True:
    activity = input("\nEnter CRUD activity to perform [(1 OR create), (2 OR read), (3 OR update), (4 OR delete), (q to quit)]:\n")

    if activity.lower() == "read" or activity == "2":
        dataReading()

    elif activity.lower() == "update" or activity == "3":
        updateStudent = input("Enter the name of the student to update:\n")
        dataUpdating(updateStudent)

    elif activity.lower() == "delete" or activity == "4":
        deleteStudent = input("Enter the name of the student to be deleted:\n")
        dataDeletion(deleteStudent)

    elif activity.lower() == "create" or activity == "1":
        Name = input("Enter student's name: ")
        Contact = input("Enter student's contact: ")
        Email = input("Enter student's email: ")
        Course = input("Enter student's course: ")
        Department = input("Enter student's department: ")
        dataCreation(Name, Contact, Email, Course, Department)

    elif activity.lower() in ["q", "quit", "exit"]:
        print("Exiting the program.")
        break

    else:
        print("Invalid input. Please choose a valid option.")



connection.close()
print("Database connection closed.")
