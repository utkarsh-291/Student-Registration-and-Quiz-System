import data 
import sqlite3
import json

def register():
    print("\n--- Student Registration ---")

    enrollment = input("Enter enrollment number: ")
    
    password = input("Create a new password (min 8 characters): ")
    while len(password) < 8:
        password = input("Password is too short. Please choose a stronger password (min 8 characters): ")

    name = input("Enter full name: ")
    roll_no = input("Enter roll number: ")
    branch = input("Enter branch: ")
    section = input("Enter section: ")
    year = input("Enter year of study: ")
    age = input("Enter age: ")
    gender = input("Enter gender: ")
    email = input("Enter email: ")
    
    phone = input("Enter 10-digit phone number: ")
    while not phone.isdigit() or len(phone) != 10:
        phone = input("Invalid input. Please enter a valid 10-digit phone number: ")

    address = input("Enter address: ")

    try:
        conn = data.get_db_connection()
        conn.execute(
            """
            INSERT INTO students (enrollment, password, name, roll_no, branch, section, year, age, gender, email, phone, address)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (enrollment, password, name, roll_no, branch, section, year, age, gender, email, phone, address)
        )
        conn.commit()
        conn.close()
        print()
        print(f"Registration successful for {name}!")
    except sqlite3.IntegrityError:
        print("\nThis enrollment number already exists. Please try a different one.")
    except Exception as e:
        print()
        print(f"An error occurred during registration: {e}")


def login():
    print()
    print("--- Student Login ---")
    enrollment = input("Enter your enrollment number: ")
    password = input("Enter your password: ")

    conn = data.get_db_connection()
    student = conn.execute("SELECT * FROM students WHERE enrollment = ?", (enrollment,)).fetchone()
    conn.close()

    if student and student["password"] == password:
        data.session["is_logged_in"] = True
        data.session["enrollment"] = student["enrollment"]
        data.session["name"] = student["name"]
        print()
        print(f"Welcome back, {student['name']}!")
    else:
        print()
        print("Invalid enrollment number or password. Please try again.")

def logout():
    if data.session["is_logged_in"]:
        student_name = data.session.get("name", "User") 
        print()
        print(f"{student_name} has been logged out successfully.")
        # Reset the session
        data.session["is_logged_in"] = False
        data.session["enrollment"] = None
        data.session["name"] = None
    else:
        print()
        print("No user is currently logged in.")

def forgot_password():
    print()
    print("--- Forgot Password ---")
    enrollment = input("Enter your enrollment number: ")
    
    conn = data.get_db_connection()
    student = conn.execute("SELECT * FROM students WHERE enrollment = ?", (enrollment,)).fetchone()
    
    if not student:
        conn.close()
        print("No account found for that enrollment number.")
        return

    # two creden. of information for now to reset
    phone = input("For verification, please enter your 10-digit phone number: ")
    roll_no = input("For verification, please enter your roll number: ")
    
    if student["phone"] == phone and student["roll_no"] == roll_no:
        print("Verification successful!")
        new_password = input("Enter your new password (min 8 characters): ")
        
        while len(new_password) < 8:
            new_password = input("Password is too short. Enter a new password (min 8 characters): ")
        
        conn.execute("UPDATE students SET password = ? WHERE enrollment = ?", (new_password, enrollment))
        conn.commit()
        print("Password updated successfully. Please log in.")
    else:
        print("Verification failed. The phone number or roll number did not match.")
    
    conn.close()

def change_password():
    if not data.session["is_logged_in"]:
        print()
        print("You must be logged in to change your password.")
        return

    print()
    print("--- Change Password ---")
    enrollment = data.session["enrollment"]
    
    conn = data.get_db_connection()
    student = conn.execute("SELECT password FROM students WHERE enrollment = ?", (enrollment,)).fetchone()
    
    # verifyin old one
    old_password = input("Enter your CURRENT password: ")
    
    if student["password"] != old_password:
        print("Incorrect password. Your password has not been changed.")
        conn.close()
        return
        
    new_password = input("Enter your NEW password (min 8 characters): ")
    while len(new_password) < 8:
        new_password = input("Password is too short. Enter a NEW password (min 8 characters): ")
        
    confirm_password = input("Confirm your NEW password: ")
    
    if new_password == confirm_password:
        conn.execute("UPDATE students SET password = ? WHERE enrollment = ?", (new_password, enrollment))
        conn.commit()
        print("Password changed successfully!")
    else:
        print("Passwords do not match. Your password has not been changed.")
        
    conn.close()

def delete_account():
    if not data.session["is_logged_in"]:
        print()
        print("You must be logged in to delete your account.")
        return

    print()
    print("--- Delete Account ---")
    print("WARNING: This action is permanent and cannot be undone.")
    enrollment = data.session["enrollment"]
    student_name = data.session.get("name", "User")

    confirm = input(f"Are you sure you want to delete the account for {student_name}? (y/n): ").strip().lower()

    if confirm != 'y':
        print("Account deletion cancelled.")
        return

    conn = data.get_db_connection()
    student = conn.execute("SELECT password FROM students WHERE enrollment = ?", (enrollment,)).fetchone()
    password = input("To confirm, please enter your password: ")
    
    if student["password"] == password:
        conn.execute("DELETE FROM students WHERE enrollment = ?", (enrollment,))
        conn.commit()
        conn.close()
        print()
        print("Account successfully deleted.")
        
        data.session["is_logged_in"] = False
        data.session["enrollment"] = None
        data.session["name"] = None
    else:
        print("Incorrect password. Account deletion cancelled.")
        conn.close()