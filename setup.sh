#!/bin/bash

# ProtonMail MCP Connector Setup Script
# This script automates the setup process for Unix-like systems (macOS, Linux)

set -e  # Exit on error

echo "=================================================="
echo "ProtonMail MCP Connector - Setup Script"
echo "=================================================="
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # Source the shell configuration to get uv in PATH
    if [ -f "$HOME/.cargo/env" ]; then
        source "$HOME/.cargo/env"
    fi
    
    echo "✓ uv installed successfully"
    echo ""
    echo "⚠️  Please restart your terminal and run this script again."
    exit 0
fi

echo "✓ uv is already installed"
echo ""

# Create virtual environment
echo "🔨 Creating virtual environment..."
uv venv
echo "✓ Virtual environment created"
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source .venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "📚 Installing dependencies..."
uv pip install -e .
echo "✓ Dependencies installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your ProtonMail credentials!"
    echo "   PROTON_USERNAME=your-email@protonmail.com"
    echo "   PROTON_PASSWORD=your-password"
    echo ""
else
    echo "✓ .env file already exists"
    echo ""
fi

# Test installation
echo "🧪 Testing installation..."
if python -c "import mcp; from protonmail_client import ProtonMailClient" 2>/dev/null; then
    echo "✓ All imports successful"
    echo ""
else
    echo "❌ Import test failed. Please check the error messages above."
    exit 1
fi

echo "=================================================="
echo "✅ Setup Complete!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "1. Edit .env and add your ProtonMail credentials"
echo "2. Test the server: uv run mcp dev protonmail_server.py"
echo "3. Configure Claude Desktop (see QUICKSTART.md)"
echo ""
echo "For detailed instructions, see:"
echo "  - QUICKSTART.md for quick setup"
echo "  - README.md for full documentation"
echo ""
