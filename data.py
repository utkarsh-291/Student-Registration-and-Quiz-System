import sqlite3
import json
import os

DB_FILE = "student_quiz.db"

session = {
    "is_logged_in": False,
    "enrollment": None,
    "name": None 
}

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        enrollment TEXT PRIMARY KEY NOT NULL,
        password TEXT NOT NULL,
        name TEXT NOT NULL,
        roll_no TEXT,
        branch TEXT,
        section TEXT,
        year TEXT,
        age TEXT,
        gender TEXT,
        email TEXT,
        phone TEXT,
        address TEXT
    );
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        options TEXT NOT NULL, 
        answer TEXT NOT NULL
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        enrollment TEXT NOT NULL,
        name TEXT NOT NULL,
        score INTEGER NOT NULL,
        total INTEGER NOT NULL,
        start_time TEXT, 
        end_time TEXT,
        FOREIGN KEY (enrollment) REFERENCES students (enrollment)
    );
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database '{DB_FILE}' initialized successfully.")

def load_data():
    init_db()