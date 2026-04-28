# ProtonMail Bridge Setup Guide

This guide explains how to set up and use the IMAP-based ProtonMail MCP Connector with ProtonMail Bridge.

## Why Use Bridge?

✅ **Official** - Supported by ProtonMail  
✅ **Stable** - Won't break with ProtonMail updates  
✅ **Reliable** - Uses standard IMAP/SMTP protocols  
✅ **No 2FA issues** - Bridge handles authentication  

## Prerequisites

- ProtonMail account (any plan)
- macOS, Windows, or Linux computer
- Claude Desktop installed

## Step 1: Install ProtonMail Bridge

### Download Bridge

Visit: https://proton.me/mail/bridge

Download the version for your operating system:
- macOS: .dmg file
- Windows: .exe installer
- Linux: .deb or .rpm package

### Install Bridge

**macOS:**
1. Open the .dmg file
2. Drag Bridge to Applications folder
3. Open Bridge from Applications

**Windows:**
1. Run the .exe installer
2. Follow the installation wizard
3. Launch Bridge from Start menu

**Linux:**
```bash
# Debian/Ubuntu
sudo dpkg -i protonmail-bridge_*.deb

# Fedora/RHEL
sudo rpm -i protonmail-bridge_*.rpm
```

## Step 2: Configure ProtonMail Bridge

### Initial Setup

1. **Launch ProtonMail Bridge**
   - Look for the Bridge icon in your system tray/menu bar

2. **Sign In**
   - Click "Sign in" or "Add account"
   - Enter your ProtonMail email
   - Enter your ProtonMail password
   - Complete any 2FA if enabled

3. **Wait for Sync**
   - Bridge will sync your emails
   - This may take a few minutes for large mailboxes

### Get Bridge Credentials

Once signed in, Bridge generates IMAP/SMTP credentials:

1. **Click on your account** in Bridge
2. **Look for "Mailbox configuration"** or **"IMAP/SMTP Settings"**
3. You'll see:
   - **Username:** Usually your ProtonMail email
   - **Password:** A Bridge-generated password (NOT your ProtonMail password)
   - **IMAP Server:** 127.0.0.1
   - **IMAP Port:** 1143
   - **SMTP Server:** 127.0.0.1
   - **SMTP Port:** 1025

4. **Copy the Bridge password** - you'll need this for the connector

## Step 3: Update Your .env File

Edit your `.env` file with the Bridge credentials:

```bash
# ProtonMail Bridge Credentials
BRIDGE_USERNAME=your-email@protonmail.com
BRIDGE_PASSWORD=your-bridge-generated-password

# Optional: Only change if Bridge uses different ports
PROTON_IMAP_SERVER=127.0.0.1
PROTON_IMAP_PORT=1143
PROTON_SMTP_SERVER=127.0.0.1
PROTON_SMTP_PORT=1025
```

**Important:**
- Use your **ProtonMail email** as the username
- Use the **Bridge-generated password**, NOT your ProtonMail password
- Bridge password is shown in Bridge settings, usually a long random string

## Step 4: Test the Connection

Run the IMAP test script:

```bash
uv run python test_connection_imap.py
```

You should see:
```
✓ BRIDGE_USERNAME: your-email@protonmail.com
✓ BRIDGE_PASSWORD: [hidden]
✓ ProtonMail Bridge is running on 127.0.0.1:1143
✓ IMAP authentication successful!
✓ Retrieved 5 messages
✅ All tests passed!
```

If tests fail, check:
- Bridge application is running
- Bridge is signed in to your account
- Bridge password in .env is correct
- No firewall blocking localhost connections

## Step 5: Configure Claude Desktop

Edit Claude Desktop config file:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Add this configuration:

```json
{
  "mcpServers": {
    "protonmail": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/blackholesoftware/github/protonmail-mcp-connector",
        "run",
        "protonmail_server_imap.py"
      ]
    }
  }
}
```

**Important:** 
- Use **absolute path** to your project directory
- Use `protonmail_server_imap.py` (not `protonmail_server.py`)
- Replace `/Users/blackholesoftware/...` with your actual path

**Windows example:**
```json
{
  "mcpServers": {
    "protonmail": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\Users\\YourName\\github\\protonmail-mcp-connector",
        "run",
        "protonmail_server_imap.py"
      ]
    }
  }
}
```

## Step 6: Restart Claude Desktop

1. **Quit Claude Desktop completely**
   - macOS: Cmd+Q or Claude → Quit
   - Windows: Right-click taskbar icon → Exit

2. **Restart Claude Desktop**

3. **Verify connection**
   - Look for ProtonMail in available tools
   - Try: "List my last 5 emails"

## Using the IMAP Connector

### Available Commands

Once configured, try these with Claude:

```
List my last 10 emails
Read the first email
Search for emails about "meeting"
Send an email to john@example.com about the project
Show me my email folders
```

### Testing Without Claude

You can also test directly:

```bash
# Test with MCP inspector
uv run mcp dev protonmail_server_imap.py

# Run programmatic examples
uv run python examples_imap.py
```

## Troubleshooting

### "Bridge is not running"

**Solution:**
1. Open ProtonMail Bridge application
2. Make sure it's signed in
3. Check system tray/menu bar for Bridge icon

### "Authentication failed"

**Solutions:**
1. Verify Bridge password in .env (NOT your ProtonMail password)
2. Check Bridge is logged in to your account
3. Try signing out and back in to Bridge
4. Regenerate Bridge password in Bridge settings

### "Cannot connect to 127.0.0.1:1143"

**Solutions:**
1. Check Bridge is running
2. Verify ports in .env match Bridge settings
3. Check firewall isn't blocking localhost
4. Some Bridge versions use different ports - check Bridge settings

### "SSL/TLS errors"

Bridge uses unencrypted local connections (it's on localhost). This is normal and secure since it's not going over the network.

### Bridge won't start

**Solutions:**
1. Check system requirements
2. Try reinstalling Bridge
3. Check Bridge logs:
   - macOS: `~/Library/Logs/protonmail/bridge/`
   - Windows: `%LOCALAPPDATA%\ProtonMail\Bridge\logs\`
   - Linux: `~/.cache/protonmail/bridge/logs/`

## Bridge Tips

### Keep Bridge Running

- Bridge must be running for the connector to work
- Set Bridge to start automatically:
  - macOS: System Preferences → Users & Groups → Login Items
  - Windows: Task Manager → Startup

### Multiple Accounts

Bridge supports multiple ProtonMail accounts:
1. Add accounts in Bridge settings
2. Each account gets its own credentials
3. Use different .env files or switch as needed

### Bridge Updates

- Bridge updates automatically
- Updates won't break the connector (stable IMAP protocol)
- Check for updates in Bridge → Settings

## Performance Notes

- **First sync:** May be slow for large mailboxes
- **Subsequent use:** Fast - Bridge caches locally
- **Offline mode:** Bridge requires internet for sync
- **Resource usage:** Bridge uses ~100-200MB RAM

## Security

✅ **Local only** - Bridge runs on localhost  
✅ **Encrypted** - Bridge decrypts emails locally  
✅ **Private** - No data leaves your computer except to ProtonMail  
✅ **Zero-knowledge** - ProtonMail can't read your Bridge password  

## Next Steps

Once everything is working:

1. ✅ Test basic email operations
2. ✅ Try with Claude Desktop
3. 📚 Read the full [README.md](README.md) for all features
4. 🎯 Check out [examples_imap.py](examples_imap.py) for programmatic use

## Getting Help

- 📖 ProtonMail Bridge docs: https://proton.me/support/bridge
- 🐛 Bridge issues: Contact ProtonMail support
- 💬 Connector issues: Open GitHub issue

---

**That's it!** You now have a stable, officially-supported ProtonMail connector for Claude.
