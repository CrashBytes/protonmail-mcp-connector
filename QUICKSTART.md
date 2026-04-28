# Quick Start Guide

Get your ProtonMail MCP connector running in 5 minutes!

## Prerequisites

- Python 3.10+
- A ProtonMail account
- Claude Desktop installed

## Installation Steps

### 1. Install uv (Python package manager)

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Restart your terminal after installation.

### 2. Set up the project

```bash
cd ~/github/protonmail-mcp-connector

# Create virtual environment
uv venv

# Activate it
source .venv/bin/activate  # macOS/Linux
# OR
.venv\Scripts\activate     # Windows

# Install dependencies
uv pip install -e .
```

### 3. Configure credentials

Create a `.env` file in the project directory:

```bash
cp .env.example .env
```

Edit `.env` and add your ProtonMail credentials:

```bash
PROTON_USERNAME=your-email@protonmail.com
PROTON_PASSWORD=your-password-here
```

**🔒 Important:** Never commit this file to Git!

### 4. Test the server

```bash
# Test with MCP inspector
uv run mcp dev protonmail_server.py
```

This should open a browser window where you can test the tools.

### 5. Configure Claude Desktop

Find your Claude config file:
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Add this configuration (replace the path with your actual path):

```json
{
  "mcpServers": {
    "protonmail": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/YOUR_USERNAME/github/protonmail-mcp-connector",
        "run",
        "protonmail_server.py"
      ]
    }
  }
}
```

**macOS users:** Full example path:
```json
"/Users/blackholesoftware/github/protonmail-mcp-connector"
```

**Windows users:** Full example path:
```json
"C:\\Users\\YourName\\github\\protonmail-mcp-connector"
```

### 6. Restart Claude Desktop

Quit Claude Desktop completely and restart it.

## Testing

Open Claude Desktop and try these commands:

1. **List emails:**
   ```
   List my last 10 emails
   ```

2. **Read an email:**
   ```
   Read the first email in my inbox
   ```

3. **Search:**
   ```
   Search for emails about "project update"
   ```

4. **Send email:**
   ```
   Send a test email to myself with subject "Test" and body "Hello from MCP!"
   ```

## Troubleshooting

### "Not authenticated" error

1. Check your `.env` file has correct credentials
2. Delete `proton_session.pickle` if it exists
3. Try running the server manually to see authentication errors:
   ```bash
   uv run python protonmail_server.py
   ```

### CAPTCHA issues

ProtonMail may show CAPTCHAs for new API access:

1. Log into ProtonMail web interface 10+ times
2. Complete any CAPTCHAs
3. Your account will be allowlisted for API access

### Claude Desktop not detecting the server

1. Verify the path in config is absolute (not relative)
2. Check the path actually exists
3. Look at Claude Desktop logs for errors
4. Restart Claude Desktop after changing config

### Import errors

Make sure you've installed dependencies:
```bash
uv pip install -e .
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check out available tools and prompts
- Customize the server for your needs

## Need Help?

Open an issue on GitHub with:
- Your operating system
- Python version (`python --version`)
- Error messages
- Steps you've tried
