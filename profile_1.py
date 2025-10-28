import data 

def show_profile():
    if not data.session["is_logged_in"]:
        print()
        print("Please log in first to view your profile.")
        return

    print()
    print("--- Student Profile ---")
    enrollment = data.session["enrollment"]
    
    conn = data.get_db_connection()
    student = conn.execute("SELECT * FROM students WHERE enrollment = ?", (enrollment,)).fetchone()
    conn.close()
    
    if not student:
        print("Error: Could not find your profile.")
        return

    for key in student.keys():
        if key != "password":
            print(f"{key.replace('_', ' ').capitalize()}: {student[key]}")
    print()
    input("press any key to continue... ")

def update_profile():
    if not data.session["is_logged_in"]:
        print()
        print("Please log in first to update your profile.")
        return
    
    print()
    print("--- Update Profile ---")
    print("Leave a field blank and press Enter if you don't want to change it.")
    
    enrollment = data.session["enrollment"]
    conn = data.get_db_connection()
    student = conn.execute("SELECT * FROM students WHERE enrollment = ?", (enrollment,)).fetchone()
    
    if not student:
        print("Error: Could not find your profile.")
        conn.close()
        return

    fields_to_update = {}
    
    for key in student.keys():
        if key in ["enrollment", "password", "name", "roll_no"]:
            continue

        current_value = student[key]
        new_value = input(f"Update {key.replace('_', ' ')} ({current_value}): ").strip()

        if new_value != "":
            fields_to_update[key] = new_value

    if not fields_to_update:
        print()
        print("No changes were made.")
        conn.close()
        return

    set_clause = ", ".join([f"{key} = ?" for key in fields_to_update.keys()])
    params = list(fields_to_update.values())
    params.append(enrollment)
    
    query = f"UPDATE students SET {set_clause} WHERE enrollment = ?"
    
    try:
        conn.execute(query, params)
        conn.commit()
        print("\nProfile updated successfully!")
    except Exception as e:
        print()
        print(f"An error occurred while updating: {e}")
    
    conn.close()