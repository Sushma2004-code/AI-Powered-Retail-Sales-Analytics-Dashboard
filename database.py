import sqlite3
import hashlib
import os

DB = "users.db"

# ----------------------------
# CONNECT
# ----------------------------
def connect():
    return sqlite3.connect(DB, check_same_thread=False)

# ----------------------------
# CREATE TABLE + MIGRATION
# ----------------------------
def create_table():
    conn = connect()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        salt TEXT
    )
    """)

    # Migration
    c.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in c.fetchall()]

    if "salt" not in columns:
        c.execute("ALTER TABLE users ADD COLUMN salt TEXT")

    conn.commit()
    conn.close()

# ----------------------------
# STRONG HASH (PBKDF2 🔥)
# ----------------------------
def hash_password(password, salt):
    return hashlib.pbkdf2_hmac(
        'sha256',
        password.encode(),
        salt.encode(),
        100000
    ).hex()

# ----------------------------
# PASSWORD VALIDATION
# ----------------------------
def is_strong_password(password):
    return (
        len(password) >= 6 and
        any(c.isdigit() for c in password) and
        any(c.isalpha() for c in password)
    )

# ----------------------------
# ADD USER
# ----------------------------
def add_user(username, password):

    if not username or not password:
        return False

    if not is_strong_password(password):
        return False

    conn = connect()
    c = conn.cursor()

    try:
        c.execute("SELECT 1 FROM users WHERE username=?", (username,))
        if c.fetchone():
            return False

        salt = os.urandom(16).hex()
        hashed = hash_password(password, salt)

        c.execute(
            "INSERT INTO users (username, password, salt) VALUES (?, ?, ?)",
            (username, hashed, salt)
        )

        conn.commit()
        return True

    finally:
        conn.close()

# ----------------------------
# LOGIN USER
# ----------------------------
def login_user(username, password):
    conn = connect()
    c = conn.cursor()

    try:
        c.execute("SELECT password, salt FROM users WHERE username=?", (username,))
        data = c.fetchone()

        if not data:
            return False

        stored_password, salt = data

        # 🔥 handle old users (no salt)
        if not salt:
            # force reset instead of silent fail
            return False

        return stored_password == hash_password(password, salt)

    finally:
        conn.close()

# ----------------------------
# UPDATE PASSWORD
# ----------------------------
def update_password(username, new_password):

    if not is_strong_password(new_password):
        raise ValueError("Weak password")

    conn = connect()
    c = conn.cursor()

    try:
        c.execute("SELECT 1 FROM users WHERE username=?", (username,))
        if not c.fetchone():
            raise Exception("User not found")

        salt = os.urandom(16).hex()
        hashed = hash_password(new_password, salt)

        c.execute(
            "UPDATE users SET password=?, salt=? WHERE username=?",
            (hashed, salt, username)
        )

        conn.commit()

    finally:
        conn.close()