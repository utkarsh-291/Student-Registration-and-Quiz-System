import authentication
import profile_1
import quiz
import data
import admin

def show_user_menu():
    print()
    print("*" * 30)
    print("      STUDENT MENU")
    print("*" * 30)
    
    if data.session["is_logged_in"]:
        name = data.session.get("name", "User")
        enrollment = data.session.get("enrollment", "N/A")
        print(f"Logged in as: {name} ({enrollment})")
        print("=" * 30)
        print("1. Show My Profile")
        print("2. Update My Profile")
        print("3. Change My Password")
        print("4. Take a Quiz")
        print("5. Logout")
        print("6. Delete My Account")
    else:
        print("1. Register New Student")
        print("2. Login")
        print("3. Forgot Password")
        print("4. Back to Main Menu")
        
    print("=" * 30)
    return input("Please choose an option: ")

def user_menu_loop():
    while True:
        choice = show_user_menu()
        
        if data.session["is_logged_in"]:
            if choice == '1':
                profile_1.show_profile()
            elif choice == '2':
                profile_1.update_profile()
            elif choice == '3':
                authentication.change_password()
            elif choice == '4':
                quiz.start_quiz()
            elif choice == '5':
                authentication.logout()
            elif choice == '6':
                authentication.delete_account()
            else:
                print()
                print("Invalid choice. Please select a valid option.")
        else:
            if choice == '1':
                authentication.register()
            elif choice == '2':
                authentication.login()
            elif choice == '3':
                authentication.forgot_password()
            elif choice == '4':
                print()
                print("Returning to main menu...")
                break 
            else:
                print("\nInvalid choice. Please select a valid option.")

def show_admin_menu():
    print()
    print("*" * 30)
    print("        ADMIN MENU")
    print("*" * 30)
    print("1. Add Question")
    print("2. View All Questions")
    print("3. Delete Question")
    print("4. View All Users")
    print("5. View All Results")
    print("6. Logout (Back to Main Menu)")
    print("=" * 30)
    return input("Please choose an option: ")

def admin_menu_loop():
    if not admin.admin_login():
        return 
    while True:
        choice = show_admin_menu()
        if choice == '1':
            admin.add_question()
        elif choice == '2':
            admin.view_questions()
        elif choice == '3':
            admin.delete_question()
        elif choice == '4':
            admin.view_all_users()
        elif choice == '5':
            admin.view_all_results()
        elif choice == '6':
            print("\nAdmin logged out. Returning to main menu...")
            break 
        else:
            print("\nInvalid choice. Please select a valid option.")

def main():
    data.load_data()
    
    while True:
        print("\n" + "=" * 30)
        print("      Welcome to LNCT")
        print("        MAIN MENU")
        print("=" * 30)
        print("1. User")
        print("2. Admin")
        print("3. Exit")
        print("=" * 30)
        main_choice = input("Are you a User or an Admin? (1-3): ")

        if main_choice == '1':
            user_menu_loop()
        elif main_choice == '2':
            admin_menu_loop()
        elif main_choice == '3':
            print("Goodbye!")
            break
        else:
            print()
            print("Invalid choice. Please select 1, 2, or 3.")

main()