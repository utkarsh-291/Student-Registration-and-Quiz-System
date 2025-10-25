import data
import json

def admin_login(): # returns bool
    print("\n--- Admin Login ---")
    password = input("Enter admin password: ")
    
    if password == "admin123":
        print("Admin login successful.")
        return True
    else:
        print("Incorrect password.")
        return False

def add_question(): #null ret.
    print()
    print("--- Add New Question ---")
    
    question_text = input("Enter the question: ")
    
    options = []
    options.append("A. " + input("Enter option A: "))
    options.append("B. " + input("Enter option B: "))
    options.append("C. " + input("Enter option C: "))
    options.append("D. " + input("Enter option D: "))
    
    # Convert list of options to a JSON string for storage
    options_json = json.dumps(options)
    
    answer = input("Enter the correct answer (A, B, C, or D): ").strip().upper()
    while answer not in ['A', 'B', 'C', 'D']:
        answer = input("Invalid. Please enter A, B, C, or D: ").strip().upper()
        
    try:
        conn = data.get_db_connection()
        conn.execute(
            "INSERT INTO questions (question, options, answer) VALUES (?, ?, ?)",
            (question_text, options_json, answer)
        )
        conn.commit()
        conn.close()
        print("Question added successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

def view_questions():
    print()
    print("--- All Quiz Questions ---")
    conn = data.get_db_connection()
    questions = conn.execute("SELECT * FROM questions").fetchall()
    conn.close()

    if not questions:
        print("No questions found.")
        return

    for q in questions:
        print()
        print(f"Q{q['id']}: {q['question']}")
        options_list = json.loads(q['options'])
        for opt in options_list:
            print(f"  {opt}")
        print(f"  Answer: {q['answer']}")
    print("-" * 20)

def delete_question():
    print()
    print("--- Delete Question ---")
    
    conn = data.get_db_connection()
    questions = conn.execute("SELECT id, question FROM questions ORDER BY id").fetchall()
    
    if not questions:
        print("No questions to delete.")
        conn.close()
        return

    for q in questions:
        print(f"  ID {q['id']}: {q['question']}")

    print()
    
    try:
        choice_id = int(input("Enter the question ID to delete (0 to cancel): "))
        
        if choice_id == 0:
            print("Delete cancelled.")
            conn.close()
            return
            
        conn.execute("DELETE FROM questions WHERE id = ?", (choice_id,))
        conn.commit()
        
        if conn.total_changes > 0:
            print(f"Successfully deleted question ID {choice_id}.")
        else:
            print("Invalid ID. No question deleted.")
            
    except ValueError:
        print("Invalid input. Please enter a number.")
    
    conn.close()

def view_all_users():
    print()
    print("--- All Registered Users ---")
    
    conn = data.get_db_connection()
    students = conn.execute("SELECT enrollment, name, branch, phone FROM students").fetchall()
    conn.close()
    
    if not students:
        print("No users found.")
        return
    
    print(f"{'Enrollment':<15} {'Name':<20} {'Branch':<10} {'Phone':<12}")
    print("-" * 57)
    
    for student in students:
        print(f"{student['enrollment']:<15} {student['name']:<20} {student['branch']:<10} {student['phone']:<12}")

def view_all_results():
    print()
    print("--- All Quiz Results ---")
    
    conn = data.get_db_connection()
    results = conn.execute("SELECT * FROM results ORDER BY start_time DESC").fetchall()
    conn.close()
    
    if not results:
        print("No results found.")
        return
        
    print(f"{'Enrollment':<15} {'Name':<20} {'Score':<7} {'Total':<7} {'Start Time':<20} {'End Time':<20}")
    print("-" * 89)
    
    for result in results:

        start_ts = result['start_time'] if result['start_time'] else 'N/A'
        end_ts = result['end_time'] if result['end_time'] else 'N/A'

        print(f"{result['enrollment']:<15} {result['name']:<20} {result['score']:<7} {result['total']:<7} {start_ts:<20} {end_ts:<20}")