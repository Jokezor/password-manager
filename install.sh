#!/bin/bash

# Check if the user is root
if [ "$EUID" -ne 0 ]; then 
  echo "Please run as root"
  exit
fi

# Make the binary executable
chmod +x main

# Move the binary to /usr/local/bin
mv main /usr/local/bin/password-manager

echo "Installation complete. You can now run 'password-manager' from anywhere in your terminal."
