
#!/bin/bash

echo "Setting up TeleRipper..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed. Please install pip first."
    exit 1
fi

# Check if virtual environment module is available
python3 -m venv --help &> /dev/null
if [ $? -ne 0 ]; then
    echo "Error: Python venv module is not available. Please install it first."
    echo "On Ubuntu/Debian: sudo apt-get install python3-venv"
    echo "On CentOS/RHEL: sudo yum install python3-venv"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install the package in development mode
echo "Installing TeleRipper and dependencies..."
pip install -e .

echo ""
echo "Setup complete! To use TeleRipper:"
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Run TeleRipper:"
echo "   teleripper --help"
echo ""
echo "3. First time usage:"
echo "   teleripper --lc           # List available channels"
echo "   teleripper --d CHANNEL_ID # Download media from a channel"
