#!/bin/bash

# Use the system Python we know exists
PYTHON_CMD="/usr/bin/python3"

echo "Using Python interpreter: $PYTHON_CMD"

# Check required packages
check_and_install_package() {
    local package=$1
    if ! $PYTHON_CMD -c "import $package" >/dev/null 2>&1; then
        echo "$package package not found. Installing..."
        $PYTHON_CMD -m pip install --user $package
    fi
}

check_and_install_package "telethon"
check_and_install_package "configparser"

echo "Checking for script updates..."
SCRIPT_VERSION="1.1.0"
echo "Current version: $SCRIPT_VERSION"
echo "All required packages installed."

# Run the script
$PYTHON_CMD "$(dirname "$0")/TeleRipper.py" "$@"
exit $?
