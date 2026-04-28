"""
ProtonMail MCP Server (IMAP/SMTP Version)

A Model Context Protocol server that enables AI assistants like Claude
to interact with ProtonMail via IMAP/SMTP using ProtonMail Bridge.

This version is more reliable than the API-based version.
"""

import os
import sys
from typing import List, Optional
from datetime import datetime
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from protonmail_client_imap import ProtonMailClientIMAP

# Load environment variables
load_dotenv()

# Initialize MCP server
mcp = FastMCP("ProtonMail-IMAP", dependencies=["python-dotenv"])

# Initialize ProtonMail IMAP client
pm_client = ProtonMailClientIMAP(
    imap_server=os.getenv("PROTON_IMAP_SERVER", "127.0.0.1"),
    imap_port=int(os.getenv("PROTON_IMAP_PORT", "1143")),
    smtp_server=os.getenv("PROTON_SMTP_SERVER", "127.0.0.1"),
    smtp_port=int(os.getenv("PROTON_SMTP_PORT", "1025"))
)

# Get Bridge credentials from environment
BRIDGE_USERNAME = os.getenv("BRIDGE_USERNAME")
BRIDGE_PASSWORD = os.getenv("BRIDGE_PASSWORD")

# Authenticate on server startup
print("=" * 60)
print("ProtonMail MCP Server (IMAP) Starting...")
print("=" * 60)

if BRIDGE_USERNAME and BRIDGE_PASSWORD:
    print(f"Authenticating via Bridge as: {BRIDGE_USERNAME}")
    success = pm_client.authenticate(BRIDGE_USERNAME, BRIDGE_PASSWORD)
    if not success:
        print("⚠ Warning: Initial authentication failed")
        print("Make sure ProtonMail Bridge is running!")
else:
    print("⚠ Warning: No Bridge credentials found in .env file")
    print("Please set BRIDGE_USERNAME and BRIDGE_PASSWORD")

print("=" * 60)


# ============================================================================
# TOOLS - Functions that Claude can call to perform actions
# ============================================================================

@mcp.tool()
def list_messages(limit: int = 20, folder: str = "INBOX") -> str:
    """
    List recent messages from ProtonMail.
    
    Args:
        limit: Maximum number of messages to return (default: 20, max: 100)
        folder: Folder to list from (default: INBOX)
    
    Returns:
        Formatted list of messages with ID, sender, subject, and preview
    """
    try:
        # Validate limit
        limit = min(max(1, limit), 100)
        
        messages = pm_client.get_messages(limit=limit, folder=folder)
        
        if not messages:
            return f"No messages found in {folder}"
        
        result = [f"Found {len(messages)} message(s) in {folder}:\n"]
        
        for i, msg in enumerate(messages, 1):
            # Format timestamp
            timestamp = msg.get('time', 0)
            if timestamp:
                dt = datetime.fromtimestamp(timestamp)
                time_str = dt.strftime("%Y-%m-%d %H:%M")
            else:
                time_str = "Unknown"
            
            # Format sender
            sender_name = msg.get('sender_name', '')
            sender_addr = msg.get('sender', 'Unknown')
            sender = f"{sender_name} <{sender_addr}>" if sender_name else sender_addr
            
            # Unread indicator
            unread = "🔵 " if msg.get('unread') else ""
            
            result.append(
                f"\n{i}. {unread}{msg['subject']}\n"
                f"   ID: {msg['id']}\n"
                f"   From: {sender}\n"
                f"   Time: {time_str}\n"
            )
        
        return "\n".join(result)
        
    except Exception as e:
        return f"❌ Error listing messages: {str(e)}"


@mcp.tool()
def read_message(message_id: str) -> str:
    """
    Read the full content of a specific message.
    
    Args:
        message_id: The IMAP message ID
    
    Returns:
        Full message content including headers and body
    """
    try:
        msg = pm_client.read_message(message_id)
        
        # Format timestamp
        timestamp = msg.get('time', 0)
        if timestamp:
            dt = datetime.fromtimestamp(timestamp)
            time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
        else:
            time_str = "Unknown"
        
        # Format sender
        sender_name = msg.get('sender_name', '')
        sender_addr = msg.get('sender', 'Unknown')
        sender = f"{sender_name} <{sender_addr}>" if sender_name else sender_addr
        
        # Format recipients
        recipients = ", ".join(msg.get('recipients', []))
        cc = ", ".join(msg.get('cc', []))
        
        # Build message
        parts = [
            "=" * 70,
            f"Subject: {msg['subject']}",
            f"From: {sender}",
            f"To: {recipients}",
        ]
        
        if cc:
            parts.append(f"CC: {cc}")
        
        parts.extend([
            f"Date: {time_str}",
            f"Attachments: {msg['attachments']}",
        ])
        
        if msg.get('attachment_names'):
            parts.append(f"Files: {', '.join(msg['attachment_names'])}")
        
        parts.extend([
            "=" * 70,
            "",
            msg['body'],
            "",
            "=" * 70
        ])
        
        return "\n".join(parts)
        
    except Exception as e:
        return f"❌ Error reading message: {str(e)}"


@mcp.tool()
def send_email(
    to: List[str],
    subject: str,
    body: str,
    cc: Optional[List[str]] = None,
    bcc: Optional[List[str]] = None,
    is_html: bool = False
) -> str:
    """
    Send an email via ProtonMail Bridge.
    
    Args:
        to: List of recipient email addresses
        subject: Email subject line
        body: Email body content (plain text or HTML)
        cc: Optional list of CC recipients
        bcc: Optional list of BCC recipients
        is_html: Set to True if body contains HTML (default: False)
    
    Returns:
        Status message with send confirmation
    """
    try:
        # Validate recipients
        if not to or len(to) == 0:
            return "❌ Error: At least one recipient is required"
        
        result = pm_client.send_message(
            to=to,
            subject=subject,
            body=body,
            cc=cc,
            bcc=bcc,
            is_html=is_html
        )
        
        if result.get("success"):
            recipients_str = ", ".join(to)
            msg_id = result.get("message_id", "unknown")
            
            return (
                f"✅ Email sent successfully!\n"
                f"To: {recipients_str}\n"
                f"Subject: {subject}\n"
                f"Sent at: {result.get('timestamp', 'unknown')}"
            )
        else:
            return "❌ Email sending failed - no success confirmation received"
            
    except Exception as e:
        return f"❌ Error sending email: {str(e)}"


@mcp.tool()
def search_email(query: str, limit: int = 10) -> str:
    """
    Search for emails matching a query string.
    
    Uses IMAP SEARCH to find messages containing the query in
    subject or body.
    
    Args:
        query: Search terms to look for
        limit: Maximum number of results to return (default: 10)
    
    Returns:
        Formatted list of matching messages
    """
    try:
        messages = pm_client.search_messages(query, limit=limit)
        
        if not messages:
            return f"No messages found matching '{query}'"
        
        result = [f"Found {len(messages)} message(s) matching '{query}':\n"]
        
        for i, msg in enumerate(messages, 1):
            # Format timestamp
            timestamp = msg.get('time', 0)
            if timestamp:
                dt = datetime.fromtimestamp(timestamp)
                time_str = dt.strftime("%Y-%m-%d %H:%M")
            else:
                time_str = "Unknown"
            
            # Format sender
            sender_name = msg.get('sender_name', '')
            sender_addr = msg.get('sender', 'Unknown')
            sender = f"{sender_name} <{sender_addr}>" if sender_name else sender_addr
            
            result.append(
                f"\n{i}. {msg['subject']}\n"
                f"   ID: {msg['id']}\n"
                f"   From: {sender}\n"
                f"   Time: {time_str}\n"
            )
        
        return "\n".join(result)
        
    except Exception as e:
        return f"❌ Error searching: {str(e)}"


@mcp.tool()
def delete_message(message_id: str) -> str:
    """
    Delete a message (move to trash).
    
    Args:
        message_id: IMAP message ID
    
    Returns:
        Confirmation message
    """
    try:
        success = pm_client.delete_message(message_id)
        
        if success:
            return f"✅ Message {message_id} deleted successfully"
        else:
            return f"❌ Failed to delete message {message_id}"
            
    except Exception as e:
        return f"❌ Error deleting message: {str(e)}"


@mcp.tool()
def get_folders() -> str:
    """
    Get list of available IMAP folders.
    
    Returns:
        List of folder names
    """
    try:
        folders = pm_client.get_folders()
        
        result = ["Available folders:\n"]
        for folder in folders:
            result.append(f"- {folder['name']}")
        
        return "\n".join(result)
        
    except Exception as e:
        return f"❌ Error getting folders: {str(e)}"


# ============================================================================
# RESOURCES - Read-only data that can be accessed by Claude
# ============================================================================

@mcp.resource("protonmail://status")
def get_status() -> str:
    """Get ProtonMail Bridge connection status."""
    if pm_client._authenticated:
        return f"✅ Connected to ProtonMail Bridge as {BRIDGE_USERNAME}"
    else:
        return "❌ Not connected to ProtonMail Bridge. Make sure Bridge is running!"


@mcp.resource("protonmail://account")
def get_account_info() -> str:
    """Get account information."""
    if not pm_client._authenticated:
        return "Not authenticated"
    
    return f"""ProtonMail Account Information:
Username: {BRIDGE_USERNAME}
Status: Active via Bridge
Connection: IMAP/SMTP
IMAP: {pm_client.imap_server}:{pm_client.imap_port}
SMTP: {pm_client.smtp_server}:{pm_client.smtp_port}
"""


# ============================================================================
# PROMPTS - Pre-written templates to help with common tasks
# ============================================================================

@mcp.prompt()
def draft_email_prompt(recipient: str, topic: str) -> str:
    """
    Create a prompt template for drafting an email.
    
    Args:
        recipient: Who the email is for
        topic: What the email is about
    
    Returns:
        A formatted prompt to help draft the email
    """
    return f"""Please help me draft a professional email with the following details:

**To:** {recipient}
**Topic:** {topic}

Please create a well-structured email that includes:

1. **Subject Line:** A clear, concise subject that summarizes the purpose
2. **Greeting:** An appropriate salutation
3. **Body:** 
   - Clear introduction stating the purpose
   - Well-organized main points
   - Specific action items or next steps if applicable
4. **Closing:** Professional sign-off

Keep the tone professional but friendly. Make it clear and concise.

Once you've drafted the email, I can send it using:
```
send_email(
    to=["{recipient}"],
    subject="Your Subject Here",
    body="Your email body here"
)
```
"""


@mcp.prompt()
def email_summary_prompt(message_id: str) -> str:
    """
    Create a prompt for summarizing an email.
    
    Args:
        message_id: IMAP ID of the message to summarize
    
    Returns:
        A formatted prompt for email summarization
    """
    return f"""Please read and summarize the following email:

First, retrieve the email:
```
read_message("{message_id}")
```

Then provide:
1. **Key Points:** Main topics or requests in the email
2. **Action Items:** Any tasks or actions requested
3. **Urgency:** Whether this requires immediate attention
4. **Suggested Response:** If a reply is needed, suggest key points to address
"""


# ============================================================================
# MAIN - Server entry point
# ============================================================================

if __name__ == "__main__":
    print("\n🚀 Starting ProtonMail MCP Server (IMAP)...")
    print("📧 Ready to process email requests from Claude via Bridge!\n")
    
    # Run the MCP server
    mcp.run()
