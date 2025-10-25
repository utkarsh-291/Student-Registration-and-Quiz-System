# Student-Registration-and-Quiz-System

A comprehensive, command-line (CLI) application built with Python and SQLite. This project allows students to register, manage their profiles, and take quizzes. A separate, password-protected admin panel provides full control over users, questions, and results.

---

##  Features

# 1. Student Portal
* **Secure Authentication:** Users can register for a new account and log in.
* **Profile Management:** View and update personal details (phone, email, address, etc.).
* **Password Security:** Securely change a current password or use the "forgot password" flow to reset it.
* **Account Deletion:** Ability to permanently delete one's own account.

# 2. Quiz System
* **Dynamic Quizzes:** Take multiple-choice quizzes pulled directly from the database.
* **Instant Scoring:** Receive your score immediately upon completing the quiz.
* **Persistent Results:** All quiz attempts, scores, and start/end times are saved to the student's profile.

# 3. Admin Panel
* **Secure Login:** A separate, hard-coded password (`admin123`) protects admin-only functions.
* **Question Management:** Add new quiz questions, view all questions, and delete questions by ID.
* **User Management:** View a complete list of all registered student users.
* **View All Results:** See a detailed log of all quiz results from all users, sorted by time.

---

## Technologies Used

* **Language:** Python 3
* **Database:** SQLite 3 (for all persistent data storage)
* **Standard Modules:** `sqlite3`, `json` (for storing quiz options), `datetime`

---

## How to Run

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/utkarsh-291/Student-Registration-and-Quiz-System.git
    ```
2.  **Navigate to the directory:**
    ```bash
    cd Student-Registration-and-Quiz-System
    ```
3.  **Run the application:**
    (No external libraries are required)
    ```bash
    python main.py
    ```
4.  **Log in as Admin:**
    * From the main menu, choose "Admin".
    * The password is: `admin123`
