"""
Example usage of ProtonMail MCP Connector

This file demonstrates how to use the ProtonMail client
programmatically (without Claude Desktop).
"""

import os
from dotenv import load_dotenv
from protonmail_client import ProtonMailClient


def example_list_and_read():
    """Example: List emails and read the first one."""
    print("\n=== Example: List and Read Emails ===\n")
    
    # Load credentials
    load_dotenv()
    client = ProtonMailClient()
    
    # Authenticate
    success = client.authenticate(
        os.getenv("PROTON_USERNAME"),
        os.getenv("PROTON_PASSWORD")
    )
    
    if not success:
        print("Authentication failed!")
        return
    
    # List recent emails
    print("Fetching your 5 most recent emails...\n")
    messages = client.get_messages(limit=5)
    
    for i, msg in enumerate(messages, 1):
        print(f"{i}. {msg['subject']}")
        print(f"   From: {msg['sender']}")
        print(f"   Preview: {msg['snippet']}...\n")
    
    # Read the first message in detail
    if messages:
        print("\nReading the first message in full:\n")
        first_msg = client.read_message(messages[0]['id'])
        print(f"Subject: {first_msg['subject']}")
        print(f"From: {first_msg['sender']}")
        print(f"Body:\n{first_msg['body'][:500]}...")


def example_search():
    """Example: Search for specific emails."""
    print("\n=== Example: Search Emails ===\n")
    
    load_dotenv()
    client = ProtonMailClient()
    
    client.authenticate(
        os.getenv("PROTON_USERNAME"),
        os.getenv("PROTON_PASSWORD")
    )
    
    # Search for emails containing "update"
    query = "update"
    print(f"Searching for emails containing '{query}'...\n")
    
    results = client.search_messages(query, limit=5)
    
    if results:
        print(f"Found {len(results)} matching emails:\n")
        for msg in results:
            print(f"- {msg['subject']}")
            print(f"  From: {msg['sender']}\n")
    else:
        print(f"No emails found matching '{query}'")


def example_send_email():
    """Example: Send an email."""
    print("\n=== Example: Send Email ===\n")
    
    load_dotenv()
    client = ProtonMailClient()
    
    client.authenticate(
        os.getenv("PROTON_USERNAME"),
        os.getenv("PROTON_PASSWORD")
    )
    
    # Send a test email to yourself
    your_email = os.getenv("PROTON_USERNAME")
    
    print(f"Sending a test email to {your_email}...\n")
    
    result = client.send_message(
        to=[your_email],
        subject="Test Email from ProtonMail MCP Connector",
        body="""Hello!

This is a test email sent via the ProtonMail MCP Connector.

If you're seeing this, it means the connector is working correctly!

Best regards,
Your ProtonMail MCP Connector
"""
    )
    
    if result['success']:
        print(f"✅ Email sent successfully!")
        print(f"Message ID: {result['message_id']}")
    else:
        print("❌ Failed to send email")


def example_with_html():
    """Example: Send an HTML email."""
    print("\n=== Example: Send HTML Email ===\n")
    
    load_dotenv()
    client = ProtonMailClient()
    
    client.authenticate(
        os.getenv("PROTON_USERNAME"),
        os.getenv("PROTON_PASSWORD")
    )
    
    your_email = os.getenv("PROTON_USERNAME")
    
    html_body = """
    <html>
    <body>
        <h1>Hello from ProtonMail MCP!</h1>
        <p>This is an <strong>HTML</strong> email with formatting:</p>
        <ul>
            <li>Bullet points</li>
            <li><em>Italic text</em></li>
            <li><strong>Bold text</strong></li>
        </ul>
        <p>Pretty cool, right?</p>
    </body>
    </html>
    """
    
    print(f"Sending an HTML email to {your_email}...\n")
    
    result = client.send_message(
        to=[your_email],
        subject="HTML Test from MCP Connector",
        body=html_body,
        is_html=True
    )
    
    if result['success']:
        print(f"✅ HTML email sent successfully!")
    else:
        print("❌ Failed to send HTML email")


def main():
    """Run all examples."""
    print("=" * 60)
    print("  ProtonMail MCP Connector - Usage Examples")
    print("=" * 60)
    
    # Check if credentials are configured
    load_dotenv()
    if not os.getenv("PROTON_USERNAME") or not os.getenv("PROTON_PASSWORD"):
        print("\n⚠️  Error: Credentials not configured!")
        print("Please create a .env file with your ProtonMail credentials.")
        print("\nSee .env.example for the required format.")
        return
    
    try:
        # Run examples
        example_list_and_read()
        example_search()
        
        # Ask before sending emails
        print("\n" + "=" * 60)
        response = input("\nWould you like to run the email sending examples? (y/n): ")
        if response.lower() == 'y':
            example_send_email()
            example_with_html()
        else:
            print("\nSkipping email sending examples.")
        
        print("\n" + "=" * 60)
        print("  Examples completed!")
        print("=" * 60)
        print("\nFor more information, see:")
        print("  - README.md for full documentation")
        print("  - protonmail_client.py for available methods")
        print("  - protonmail_server.py for MCP tools")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure:")
        print("  1. Your .env file has correct credentials")
        print("  2. You've run: uv pip install -e .")
        print("  3. Your ProtonMail account is accessible")


if __name__ == "__main__":
    main()
