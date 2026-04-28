# ProtonMail MCP Connector - Project Summary

## 📦 What We've Built

A complete Model Context Protocol (MCP) server that enables Claude and other AI assistants to interact with ProtonMail for:

- ✉️ Reading and listing emails
- 📤 Sending emails (with CC/BCC support)
- 🔍 Searching messages
- 🗑️ Deleting messages
- 📁 Managing folders
- 🎨 HTML email support

## 📁 Project Structure

```
protonmail-mcp-connector/
├── .env.example              # Template for environment variables
├── .git/                     # Git repository (already initialized)
├── .gitignore               # Prevents committing sensitive files
├── CHANGELOG.md             # Version history
├── CONTRIBUTING.md          # Contribution guidelines
├── CONTRIBUTORS.md          # List of contributors
├── LICENSE                  # MIT License
├── QUICKSTART.md           # Quick setup guide
├── README.md               # Main documentation
├── examples.py             # Usage examples
├── protonmail_client.py    # ProtonMail API wrapper
├── protonmail_server.py    # MCP server implementation
├── pyproject.toml          # Python project configuration
├── requirements.txt        # Python dependencies
├── setup.bat              # Windows setup script
├── setup.sh               # Unix/macOS setup script
└── test_connection.py     # Test script
```

## 🚀 Quick Start

### 1. Run the Setup Script

**macOS/Linux:**
```bash
cd ~/github/protonmail-mcp-connector
chmod +x setup.sh
./setup.sh
```

**Windows:**
```cmd
cd %USERPROFILE%\github\protonmail-mcp-connector
setup.bat
```

### 2. Configure Credentials

Edit `.env`:
```bash
PROTON_USERNAME=your-email@protonmail.com
PROTON_PASSWORD=your-password
```

### 3. Test the Connection

```bash
uv run python test_connection.py
```

### 4. Try the Examples

```bash
uv run python examples.py
```

### 5. Set Up Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "protonmail": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/blackholesoftware/github/protonmail-mcp-connector",
        "run",
        "protonmail_server.py"
      ]
    }
  }
}
```

## 🔧 Available MCP Tools

When using with Claude Desktop, you can:

1. **list_messages** - "List my last 10 emails"
2. **read_message** - "Read message ID abc123"
3. **send_email** - "Send an email to john@example.com"
4. **search_email** - "Search for emails about project updates"
5. **delete_message** - "Delete message ID abc123"
6. **get_folders** - "Show me my email folders"

## 🎯 MCP Prompts

Pre-built prompts for common tasks:

1. **draft_email_prompt** - Help drafting professional emails
2. **email_summary_prompt** - Summarize important emails

## 📚 Documentation Files

- **README.md** - Comprehensive documentation
- **QUICKSTART.md** - Fast setup guide
- **CONTRIBUTING.md** - How to contribute
- **CHANGELOG.md** - Version history

## 🧪 Testing Your Setup

### Test 1: Verify Installation
```bash
uv run python test_connection.py
```

### Test 2: Test with MCP Inspector
```bash
uv run mcp dev protonmail_server.py
```

### Test 3: Test Programmatically
```bash
uv run python examples.py
```

### Test 4: Test with Claude
Open Claude Desktop and try:
```
List my last 5 emails
```

## 🔐 Security Best Practices

✅ DO:
- Keep `.env` file secure and never commit it
- Use app-specific passwords if available
- Regularly rotate credentials
- Review the code before using

❌ DON'T:
- Commit credentials to Git
- Share your `.env` file
- Use your main password if 2FA is enabled
- Trust unverified code modifications

## 🐛 Troubleshooting

### Common Issues

1. **"Not authenticated" error**
   - Check credentials in `.env`
   - Delete `proton_session.pickle`
   - Run `test_connection.py`

2. **CAPTCHA challenges**
   - Log into ProtonMail web 10+ times
   - Complete any CAPTCHAs
   - Wait for allowlist

3. **Import errors**
   - Run: `uv pip install -e .`
   - Activate venv: `source .venv/bin/activate`

4. **Claude not detecting server**
   - Use absolute paths in config
   - Restart Claude Desktop
   - Check logs for errors

## 🔄 Next Steps

### Immediate
1. ✅ Test authentication
2. ✅ Verify MCP tools work
3. ✅ Configure Claude Desktop
4. ✅ Try sample queries

### Future Enhancements
- [ ] Add attachment support
- [ ] Implement mark as read/unread
- [ ] Add folder management
- [ ] Improve error handling
- [ ] Add more comprehensive tests
- [ ] Create CI/CD pipeline

## 📖 Learning Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [ProtonMail API Info](https://github.com/ProtonMail)

## 🤝 Contributing

Want to improve this project?

1. Check out [CONTRIBUTING.md](CONTRIBUTING.md)
2. Look at open issues
3. Submit a pull request
4. Join the discussion

## 📝 License

MIT License - see [LICENSE](LICENSE) file

## 🙏 Acknowledgments

- Built with [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- Uses [protonmail-api-client](https://pypi.org/project/protonmail-api-client/)
- Thanks to the MCP community

## 📞 Getting Help

- 📖 Read the [QUICKSTART.md](QUICKSTART.md)
- 🔍 Check [README.md](README.md)
- 🐛 Open an issue on GitHub
- 💬 Start a discussion

---

**Created by:** Michael Eakins / Blackhole Software LLC
**GitHub:** [@CrashBytes](https://github.com/CrashBytes)
**Date:** November 29, 2024

Happy emailing! 📧
