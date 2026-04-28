@echo off
REM ProtonMail MCP Connector Setup Script for Windows

echo ==================================================
echo ProtonMail MCP Connector - Setup Script (Windows)
echo ==================================================
echo.

REM Check if uv is installed
where uv >nul 2>nul
if %errorlevel% neq 0 (
    echo Installing uv package manager...
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    
    echo.
    echo uv installed successfully
    echo.
    echo IMPORTANT: Please restart your terminal and run this script again.
    pause
    exit /b 0
)

echo uv is already installed
echo.

REM Create virtual environment
echo Creating virtual environment...
uv venv
if %errorlevel% neq 0 (
    echo Failed to create virtual environment
    pause
    exit /b 1
)
echo Virtual environment created
echo.

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat
echo Virtual environment activated
echo.

REM Install dependencies
echo Installing dependencies...
uv pip install -e .
if %errorlevel% neq 0 (
    echo Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed
echo.

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo .env file created
    echo.
    echo IMPORTANT: Edit .env and add your ProtonMail credentials!
    echo    PROTON_USERNAME=your-email@protonmail.com
    echo    PROTON_PASSWORD=your-password
    echo.
) else (
    echo .env file already exists
    echo.
)

REM Test installation
echo Testing installation...
python -c "import mcp; from protonmail_client import ProtonMailClient" 2>nul
if %errorlevel% neq 0 (
    echo Import test failed. Please check the error messages above.
    pause
    exit /b 1
)
echo All imports successful
echo.

echo ==================================================
echo Setup Complete!
echo ==================================================
echo.
echo Next steps:
echo 1. Edit .env and add your ProtonMail credentials
echo 2. Test the server: uv run mcp dev protonmail_server.py
echo 3. Configure Claude Desktop (see QUICKSTART.md)
echo.
echo For detailed instructions, see:
echo   - QUICKSTART.md for quick setup
echo   - README.md for full documentation
echo.
pause
