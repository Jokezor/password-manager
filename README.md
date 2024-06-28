# Password Manager

A simple, secure command-line password manager built with Python.

## Features

- Secure password storage using encryption
- CRUD operations for password management
- Simple command-line interface

## Requirements

- Docker (optional, for running in a container)

## Running with Docker

Build the Docker image:
```bash
docker build -t password-manager .

To run it with a persistent volume
```bash
docker run -it --rm -v password_manager_data:/app/data -e PASSWORD_MANAGER_D
B_PATH=/app/data/passwords.db -e PASSWORD_MANAGER_KEY_PATH=/app/data/secret.key password_manager
