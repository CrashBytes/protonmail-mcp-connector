# ProtonMail MCP Connector

A Model Context Protocol (MCP) server that enables Claude and other AI assistants to interact with ProtonMail.

## Features

- 📧 **List Messages** - View recent emails from your inbox
- 📖 **Read Messages** - Read full message content
- ✉️ **Send Emails** - Compose and send emails
- 🔍 **Search** - Search through your emails
- 🔐 **Secure** - Uses session persistence to minimize authentication

## Prerequisites

- Python 3.10 or higher
- A ProtonMail account
- [uv](https://github.com/astral-sh/uv) package manager (recommended)
- Claude Desktop (for MCP integration)

## Installation

### 1. Install uv (if not already installed)

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Set up the project

```bash
cd protonmail-mcp-connector

# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# OR
.venv\Scripts\activate  # Windows

# Install dependencies
uv pip install -e .
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```bash
PROTON_USERNAME=your-email@protonmail.com
PROTON_PASSWORD=your-password
PROTON_PGP_PASSWORD=your-pgp-passphrase-if-needed
```

**⚠️ Important:** Never commit your `.env` file to version control!

### 4. Test the server

```bash
# Run with MCP inspector for testing
uv run mcp dev protonmail_server.py

# Or test directly
uv run python protonmail_server.py
```

## Usage with Claude Desktop

### Configure Claude Desktop

Add the following to your Claude Desktop configuration file:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "protonmail": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/protonmail-mcp-connector",
        "run",
        "protonmail_server.py"
      ]
    }
  }
}
```

Replace `/absolute/path/to/protonmail-mcp-connector` with the actual path to this directory.

### Restart Claude Desktop

After updating the configuration, restart Claude Desktop to load the ProtonMail connector.

## Available Tools

### `list_messages`
List recent messages from your inbox.

**Example:**
```
List my last 10 emails
```

### `read_message`
Read the full content of a specific message.

**Example:**
```
Read message ID abc123
```

### `send_email`
Send an email via ProtonMail.

**Example:**
```
Send an email to john@example.com with subject "Meeting Tomorrow" 
and body "Hi John, let's meet at 2pm tomorrow."
```

### `search_email`
Search for emails matching a query.

**Example:**
```
Search for emails about "project update"
```

## Troubleshooting

### Authentication Issues

If you're experiencing authentication issues:

1. **CAPTCHA Protection**: ProtonMail may require CAPTCHA verification. To bypass:
   - Log into your account via web browser 10+ times
   - Complete any CAPTCHAs that appear
   - Your account will be allowlisted for API access

2. **Two-Factor Authentication**: If you have 2FA enabled, you may need to use an app-specific password

3. **Session Expired**: Delete the `proton_session.pickle` file and re-authenticate

### Connection Errors

- Ensure your credentials in `.env` are correct
- Check your internet connection
- Verify ProtonMail service status

### Claude Desktop Not Detecting the Server

1. Verify the path in `claude_desktop_config.json` is absolute (not relative)
2. Ensure the virtual environment is created (`uv venv`)
3. Check Claude Desktop logs for error messages
4. Restart Claude Desktop after configuration changes

## Project Structure

```
protonmail-mcp-connector/
├── .env                    # Environment variables (create this)
├── .gitignore             # Git ignore file
├── README.md              # This file
├── pyproject.toml         # Python project configuration
├── protonmail_client.py   # ProtonMail API wrapper
├── protonmail_server.py   # MCP server implementation
└── requirements.txt       # Python dependencies
```

## Development

### Running Tests

```bash
# Run the MCP inspector
uv run mcp dev protonmail_server.py
```

### Adding New Features

To add new tools:

1. Add methods to `ProtonMailClient` class in `protonmail_client.py`
2. Create corresponding `@mcp.tool()` decorated functions in `protonmail_server.py`
3. Document the new tool in this README

## Security Considerations

- **Never commit** your `.env` file or `proton_session.pickle` to version control
- Store credentials securely
- The session file contains authentication tokens - protect it like a password
- Use app-specific passwords if available
- Consider using a dedicated ProtonMail account for API access

## Limitations

- This is an **unofficial** ProtonMail client using reverse-engineered APIs
- ProtonMail may rate-limit or block API access
- Some ProtonMail features may not be available
- Attachments support is limited in the current version
- No official support from ProtonMail

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Built with [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- Uses [protonmail-api-client](https://pypi.org/project/protonmail-api-client/)
- Inspired by the Model Context Protocol community

## Disclaimer

This project is not affiliated with, endorsed by, or sponsored by Proton AG. Use at your own risk.
