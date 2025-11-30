import sqlite3

conn = sqlite3.connect("users.db")
c = conn.cursor()
c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL,
        eye_power INTEGER NOT NULL,
        eye_problems TEXT NOT NULL,
        otp INTEGER NOT NULL,
        disease TEXT NOT NULL,
        password TEXT NOT NULL
        
    )
""")
conn.commit()
conn.close()

def add_user(name,email,age,gender,eye_power,eye_problems,otp,disease,password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO users (name,email,age,gender,eye_power,eye_problems,otp,disease,password) VALUES (?, ?, ?,?,?,?,?,?,?)", (name,email,age,gender,eye_power,eye_problems,otp,disease,password))
    conn.commit()
    conn.close()

def authenticate_user(email, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user = c.fetchone()
    conn.close()
    return user
def fetch_user(email):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = c.fetchone()
    conn.close()
    return user
def add_disease(email,disease):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("UPDATE users SET disease = ? WHERE email = ?", (disease,email))
    conn.commit()
    conn.close()

def add_otp(email,otp):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("UPDATE users SET otp = ? WHERE email = ?", (otp,email))
    conn.commit()
    conn.close()

def fetch_otp(email):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT otp FROM users WHERE email = ?", (email,))
    otp = c.fetchone()
    conn.close()
    return otp