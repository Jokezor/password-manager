# Password Manager

A simple, secure command-line password manager built with Python.

## Features

- Secure password storage using encryption
- CRUD operations for password management
- Simple command-line interface

## Requirements

- Docker (optional, for running in a container)

## Installation

### Using Installer Script
1. Download the installer script `install.sh`.
2. Download the pre-built binary from the [releases page](https://github.com/Jokezor/password-manager/releases).
3. Make the script executable:
  ```bash
  chmod +x install.sh
  ```
4. Run the installer:
  ```bash
  sudo ./install.sh
  ```

### Using Pre-built Binary

1. Download the pre-built binary from the [releases page](https://github.com/Jokezor/password-manager/releases).
2. Make the binary executable:
  ```bash
  chmod +x main
  ```
3. Move the binary to a directory in your PATH, e.g., /usr/local/bin:
  ```bash
  sudo mv main /usr/local/bin/password-manager
  ```
4. Verify the installation:
  ```bash
  password-manager
  ```

## Usage
To start the password manager, run:
```bash
password-manager
```
Follow the on-screen prompts to manage your passwords securely.

## Running with Docker

Build the Docker image:
```bash
docker build -t password-manager .
```

To run it with a persistent volume
```bash
docker run -it --rm -v password_manager_data:/app/data -e PASSWORD_MANAGER_D
B_PATH=/app/data/passwords.db -e PASSWORD_MANAGER_KEY_PATH=/app/data/secret.key password_manager
```
