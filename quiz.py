import data
import datetime
import json

def start_quiz():
    if not data.session["is_logged_in"]:
        print("\nPlease log in to take the quiz.")
        return

    print("\n--- Welcome to the Quiz! ---")
    
    conn = data.get_db_connection()
    questions_rows = conn.execute("SELECT * FROM questions").fetchall()
    
    if not questions_rows:
        print("No questions are available at the moment.")
        conn.close()
        return
    
    questions = []
    for row in questions_rows:
        q = dict(row)
        q['options'] = json.loads(row['options'])
        questions.append(q)

    print(f"You will be asked {len(questions)} multiple-choice questions. Good luck!")

    start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    score = 0
    for i, q in enumerate(questions):
        print(f"\nQ{i+1} (ID: {q['id']}): {q['question']}")
        for option in q['options']:
            print(option)
        
        user_answer = input("Your answer (A, B, C, or D): ").strip().upper()
        
        if user_answer == q['answer']:
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! The correct answer was {q['answer']}.")

    print("\n--- Quiz Finished ---")
    print(f"Your final score is: {score}/{len(questions)}")

    enrollment = data.session["enrollment"]
    name = data.session["name"]
    
    end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        conn.execute(
            "INSERT INTO results (enrollment, name, score, total, start_time, end_time) VALUES (?, ?, ?, ?, ?, ?)",
            (enrollment, name, score, len(questions), start_time, end_time)
        )
        conn.commit()
        print("Your score has been saved.")
    except Exception as e:
        print(f"An error occurred while saving your score: {e}")
    
    conn.close()