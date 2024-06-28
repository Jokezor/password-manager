from cryptography.fernet import Fernet
import sqlite3
import os
import getpass

DB_PATH = os.getenv("PASSWORD_MANAGER_DB_PATH", "passwords.db")
KEY_PATH = os.getenv("PASSWORD_MANAGER_KEY_PATH", "secret.key")


# Generate a key for encryption/decryption
def generate_key():
    key = Fernet.generate_key()
    with open(KEY_PATH, "wb") as key_file:
        key_file.write(key)
    return key


# Load the previously generated key
def load_key():
    return open(KEY_PATH, "rb").read()


# Initialize database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS passwords (service TEXT, password TEXT)""")
    conn.commit()
    conn.close()


# Encrypt password
def encrypt_password(password, key):
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    return encrypted_password


# Decrypt password
def decrypt_password(encrypted_password, key):
    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password).decode()
    return decrypted_password


# Add a password
def add_password(service, password):
    key = load_key()
    encrypted_password = encrypt_password(password, key)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO passwords (service, password) VALUES (?, ?)",
        (service, encrypted_password),
    )
    conn.commit()
    conn.close()


# Retrieve a password
def get_password(service):
    key = load_key()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT password FROM passwords WHERE service=?", (service,))
    encrypted_password = c.fetchone()
    conn.close()
    if encrypted_password:
        return decrypt_password(encrypted_password[0], key)
    else:
        return None


# Main function
if __name__ == "__main__":
    if not os.path.exists(KEY_PATH):
        generate_key()
    init_db()
    print("Password Manager")
    while True:
        choice = input("Choose an option: (1) Add password (2) Get password (3) Exit: ")
        if choice == "1":
            service = input("Enter the service: ")
            password = getpass.getpass("Enter the password: ")
            add_password(service, password)
        elif choice == "2":
            service = input("Enter the service: ")
            password = get_password(service)
            if password:
                print(f"Password for {service}: {password}")
            else:
                print("No password found for this service.")
        elif choice == "3":
            break
        else:
            print("Invalid choice.")
