import pandas as pd
import mysql.connector as mysql
from mysql.connector import Error

data = pd.read_csv(r'C:\Users\Josep\Downloads\Students.csv')
df = pd.DataFrame(data)


# Connecting to database and creating database school
try:
    db = mysql.connect(host='localhost', user='root', password="N83ngmyun46$^")

    if db.is_connected():
        cursor = db.cursor()
        cursor.execute("CREATE DATABASE school")
        print("Databased is created")

except Error as e:
    print("Error while connecting to MySQL")
    print(e)



# Creating TABLE Student and parsing data from CSV file
try:
    db = mysql.connect(host='localhost', user='root', password='N83ngmyun46$^', database='school')
    if db.is_connected():
        cursor = db.cursor()
        cursor.execute("SELECT DATABASE();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.execute("DROP TABLE IF EXISTS Student")
        print("Creating table....")
        # Creating table
        cursor.execute("CREATE TABLE Student(ID int NOT NULL AUTO_INCREMENT, Username varchar(255), Password varchar(255), PRIMARY KEY(ID))")
        print("Table is created....")
        # Loop through the data frame
        for i,row in data.iterrows():
            sql = "INSERT INTO school.student VALUES (%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            db.commit()
            print("Record inserted")
          
except Error as e:
            print("Error while connecting to MySQL")
            print(e)

# Creating Table Teacher, Attendance and Grade
try:
    db = mysql.connect(host='localhost', user='root', password='N83ngmyun46$^', database='school')
    if db.is_connected():
        print("Creating table....")
        cursor = db.cursor()
        cursor.execute("DROP TABLE IF EXISTS Teacher")
        cursor.execute("CREATE TABLE Teacher(Subject varchar(255) NOT NULL, Username varchar(255), Password varchar(255), PRIMARY KEY(Subject))")
        cursor.execute("DROP TABLE IF EXISTS Attendance")
        cursor.execute("CREATE TABLE Attendance(AttendanceID int NOT NULL AUTO_INCREMENT, Username varchar(255), Date varchar(255), Status varchar(255), ID int, PRIMARY KEY(AttendanceID), FOREIGN KEY(ID) REFERENCES Student(ID))")
        cursor.execute("DROP TABLE IF EXISTS Grade")
        cursor.execute("CREATE TABLE Grade(GradeID int NOT NULL AUTO_INCREMENT, Username varchar(255), Subject varchar(255), Grade varchar(255), ID int, PRIMARY KEY(GradeID), FOREIGN KEY(ID) REFERENCES Student(ID), FOREIGN KEY(Subject) REFERENCES Teacher(Subject))")
        print("Table created successfully")
except Error as e:
    print("Table could not be created")
    print(e)





#connecting to the database
db = mysql.connect(host='localhost',user='root',password='N83ngmyun46$^',database='school')
cursor = db.cursor(buffered=True)


#Main page
def main():
    while True:
        print("\nWelcome to the SCHOOL SYSTEM\n")
        print("*"*29)
        print("\n[1] STUDENT LOGIN")
        print("\n[2] TEACHER LOGIN")
        print("\n[3] ADMIN LOGIN")
        print("\n[4] EXIT\n")

        user_choice = input(str("Select: "))
        if user_choice == "1":
            auth_student()
        elif user_choice == "2":
            auth_teacher()
        elif user_choice == "3":
            auth_admin() 
        elif user_choice == "4":
            print("\nEnjoy Your Day")
            quit()
        else:
            print("\nInvalid Option Selected")

#Creating function for student authentication
def auth_student():
    print("\nStudent Login")
    print("-"*13)
    s_username = input(str("Username: "))
    password = input(str("Password: "))
    query_vals = (s_username, password,)
    #cursor = db.cursor()
    cursor.execute("SELECT Username FROM Student WHERE Username = %s AND Password = %s", query_vals)
    if cursor.rowcount <= 0:
        print("Invalid Username/Password")
    else:
        student_session(s_username)

#Creaating function for teacher authentication
def auth_teacher():
    print("\nTeacher Login")
    print("-"*13)
    t_username = input(str("Username: "))
    password = input(str("Password: "))
    query_vals = (t_username, password)
    cursor.execute("SELECT * FROM Teacher WHERE Username = %s AND Password = %s", query_vals)
    if cursor.rowcount <= 0:
        print("Invalid Username/Password")
    else:
        teacher_session()

#Creating function for admin authentication
def auth_admin():
    print("\nAdmin Login")
    print("-"*11)
    username = input(str("Username: "))
    password = input(str("Password: "))
    if username == "admin":
        if password == "password":
            admin_session()
        else:
            print("Invalid Password")
    else:
        print("Invalid Username/Password")

#Creating functions the student can accomplish in student page
def student_session(s_username):
    while True:
        print("\nSTUDENT PAGE")
        print("-"*12)
        print("\n[1] Attendance View")
        print("\n[2] Grade View")
        print("\n[3] Change Password")
        print("\n[4] Logout\n")

        user_choice = input(str("Select: "))

        #Students can view their attendance record
        if user_choice == "1":
            print("Displaying info")
            s_username = (str(s_username),)
            cursor = db.cursor()
            cursor.execute("SELECT Date, Username, Status FROM Attendance WHERE Username = %s", s_username)
            records = cursor.fetchall()
            for record in records:
                print(record)

        #students can view their grades
        elif user_choice == "2":
            print("Displaying info")
            s_username = (str(s_username),)
            cursor = db.cursor()
            cursor.execute("SELECT Username, Subject, Grade FROM Grade WHERE Username = %s", s_username)
            records = cursor.fetchall()
            for record in records:
                print(record)

        #Students can change their password 
        elif user_choice == "3":
            print("\nPassword change requested")
            s_username = (str(s_username),)
            password = (str(input("Enter OLD Password: ")))
            new_password = (str(input("Enter NEW Password: ")))
            cursor = db.cursor()
            query_vals = (new_password, password)
            cursor.execute("UPDATE Student SET Password = %s WHERE Password = %s", query_vals)
            db.commit()
            print("Password Changed Successfully")

        elif user_choice == "4":
            break

        else:
            print("Invalid Option Selected")

#Creating function the teacher can accomplish in teacher page
def teacher_session():
    while True:
        print("\nTEACHER PAGE")
        print("-"*12)
        print("\n[1] Mark Student Attendance")
        print("\n[2] View Attendance")
        print("\n[3] Enter Student Grades")
        print("\n[4] View Student Grades")
        print("\n[5] Logout\n")

        user_choice = input(str("Select: "))

        #Teacher can mark student attendance 
        if user_choice == "1":
            print("\nMark Student Attendance")
            cursor = db.cursor()
            cursor.execute("SELECT Username FROM Student")
            records = cursor.fetchall()
            date = input(str("Date (YYYY/MM/DD): "))
            for record in records:
                record = str(record).replace("'","")
                record = str(record).replace(",","")
                record = str(record).replace("(","")
                record = str(record).replace(")","")
                status = input(str("Status for " + str(record) + " (P)resent/(A)bsent/(L)ate: "))
                query_vals = (str(record),date,status)
                cursor.execute("INSERT INTO Attendance (Username, Date, Status) VALUES (%s, %s, %s)", query_vals)
                db.commit()
                print(record + " marked as " + status)

        #Teacher can view student attendance record
        elif user_choice == "2":
            print("\nViewing all student registers")
            cursor=db.cursor()
            cursor.execute("SELECT Username, Date, Status FROM Attendance")
            records = cursor.fetchall()
            print("Displaying all attendance record")
            for record in records:
                print(record)

        #Teacher can enter student grade
        elif user_choice == "3":
            print("Enter Student Grade")
            cursor=db.cursor()
            cursor.execute("SELECT Username FROM Student")
            records = cursor.fetchall()
            subject = input(str("Enter The Subject: "))
            for record in records:
                record = str(record).replace("'","")
                record = str(record).replace(",","")
                record = str(record).replace("(","")
                record = str(record).replace(")","")
                grade = input(str("Grade for " + str(record) + " A/B/C/D/F: "))
                query_vals = (str(record),subject,grade)
                cursor.execute("INSERT INTO Grade (Username, Subject, Grade) VALUES (%s, %s, %s)", query_vals)
                db.commit()
                print(record + " has received " + grade)
        
        #Teacher can view student grade
        elif user_choice == "4":
            print("\nViewing all student grades")
            cursor.execute("SELECT Username, Subject, Grade FROM Grade")
            records = cursor.fetchall()
            print("Displaying all grades")
            for record in records:
                print(record)

        elif user_choice == "5":
            break

        else:
            print("Invalid Option Selected")

#Creating function admin can accomplish in admin page
def admin_session():
    while True: 
        print("\nADMIN PAGE")
        print("-" * 10)
        print("\n[1] Register New Student")
        print("\n[2] Register New Teacher")
        print("\n[3] Delete Existing Student")
        print("\n[4] Delete Existing Teacher")
        print("\n[5] Logout\n")

        user_choice = input(str("Select: "))
        
        #Admin can register new student
        if user_choice == "1":
            print("\nRegister New Student")
            s_username = input(str("Student username: "))
            password = input(str("Student password: "))
            query_vals = (s_username,password)
            cursor.execute("INSERT INTO Student (Username, Password) VALUES (%s, %s)", query_vals)
            db.commit()
            print(s_username + " has been registered as a student")
        
        #Admin can register new teacher
        elif user_choice == "2":
            print("\nRegister New Teacher")
            t_username = input(str("Teacher username: "))
            password = input(str("Teacher password: "))
            t_subject = input(str("Teaching Subject: "))
            query_vals = (t_username, password, t_subject)
            cursor.execute("INSERT INTO Teacher (Username, Password, Subject) VALUES (%s, %s, %s)", query_vals)
            db.commit()
            print(t_username + " has been registered as a teacher")

        #Admin can delete student record
        elif user_choice == "3":
            print("\nDelete Existing Student Account")
            s_username = input(str("Student username: "),)
            query_vals = (s_username,)
            cursor.execute("DELETE FROM Student WHERE Username = %s", query_vals)
            db.commit()
            if cursor.rowcount < 1:
                print("User Not Found")
            else:
                print(s_username + " Has Been DELETED")

        #Admin can delete teacher record
        elif user_choice == "4":
            print("\nDelete Existing Teacher Account")
            t_username = input(str("Teacher Username: "),)
            query_vals = (t_username,)
            cursor.execute("DELETE FROM Teacher WHERE Username = %s", query_vals)
            db.commit()
            if cursor.rowcount < 1:
                print("User Not Found")
            else:
                print(t_username + " Has Been DELETED")

        elif user_choice == "5":
            break
        else:
            print("Invalid Option Selected")



main()