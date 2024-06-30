import os
from cryptography.fernet import Fernet, InvalidToken
import sqlite3
import getpass

DB_PATH = os.getenv("PASSWORD_MANAGER_DB_PATH", "passwords.db")
KEY_PATH = os.getenv("PASSWORD_MANAGER_KEY_PATH", "secret.key")


def generate_key():
    key = Fernet.generate_key()
    with open(KEY_PATH, "wb") as key_file:
        key_file.write(key)
    return key


def load_key():
    return open(KEY_PATH, "rb").read()


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS passwords (service TEXT, password TEXT)""")
    conn.commit()
    conn.close()


def encrypt_data(data, key):
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode())
    return encrypted_data


def decrypt_data(encrypted_data, key):
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data).decode()
    return decrypted_data


def add_password(service, password, key):
    encrypted_password = encrypt_data(password, key)
    encrypted_service = encrypt_data(service, key)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO passwords (service, password) VALUES (?, ?)",
        (encrypted_service, encrypted_password),
    )
    conn.commit()
    conn.close()


def get_password(service, key):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT service, password FROM passwords")
    encrypted_data = c.fetchall()
    conn.close()

    for encrypted_service, password in encrypted_data:
        try:
            decrypted_service = decrypt_data(encrypted_service, key)
            if decrypted_service == service:
                return decrypt_data(password, key)
        except InvalidToken:
            continue

    print("Service not found or invalid key.")
    return None


if __name__ == "__main__":
    if not os.path.exists(KEY_PATH):
        generate_key()

    secret_key = load_key()

    init_db()
    print("Password Manager")
    while True:
        choice = input("Choose an option: (1) Add password (2) Get password (3) Exit: ")
        if choice == "1":
            service = input("Enter the service: ")
            password = getpass.getpass("Enter the password: ")
            add_password(service, password, secret_key)
        elif choice == "2":
            service = input("Enter the service: ")
            password = get_password(service, secret_key)
            if password:
                print(f"Password for {service}: {password}")
            else:
                print("No password found for this service.")
        elif choice == "3":
            break
        else:
            print("Invalid choice.")
