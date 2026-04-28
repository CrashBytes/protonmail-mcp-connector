"""
Test script for ProtonMail MCP Connector (IMAP Version)

This script tests the IMAP/SMTP connection via ProtonMail Bridge.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
from protonmail_client_imap import ProtonMailClientIMAP


def print_section(title):
    """Print a section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def test_environment():
    """Test environment configuration."""
    print_section("Testing Environment Configuration")
    
    # Load .env file
    load_dotenv()
    
    username = os.getenv("BRIDGE_USERNAME")
    password = os.getenv("BRIDGE_PASSWORD")
    
    if not username:
        print("❌ BRIDGE_USERNAME not set in .env file")
        return False
    else:
        print(f"✓ BRIDGE_USERNAME: {username}")
    
    if not password:
        print("❌ BRIDGE_PASSWORD not set in .env file")
        return False
    else:
        print("✓ BRIDGE_PASSWORD: [hidden]")
    
    print("\n✅ Environment configuration OK")
    return True


def test_bridge_running():
    """Check if ProtonMail Bridge is running."""
    print_section("Checking ProtonMail Bridge")
    
    import socket
    
    imap_server = os.getenv("PROTON_IMAP_SERVER", "127.0.0.1")
    imap_port = int(os.getenv("PROTON_IMAP_PORT", "1143"))
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((imap_server, imap_port))
        sock.close()
        
        if result == 0:
            print(f"✓ ProtonMail Bridge is running on {imap_server}:{imap_port}")
            return True
        else:
            print(f"❌ Cannot connect to ProtonMail Bridge at {imap_server}:{imap_port}")
            print("\nMake sure:")
            print("  1. ProtonMail Bridge application is running")
            print("  2. Bridge is configured and logged in")
            print("  3. IMAP/SMTP ports are correct in .env")
            return False
    except Exception as e:
        print(f"❌ Error checking Bridge: {e}")
        return False


def test_authentication():
    """Test IMAP authentication."""
    print_section("Testing IMAP Authentication")
    
    load_dotenv()
    username = os.getenv("BRIDGE_USERNAME")
    password = os.getenv("BRIDGE_PASSWORD")
    
    if not username or not password:
        print("❌ Missing credentials in .env file")
        return False
    
    print(f"Authenticating as: {username}")
    print("This may take a moment...\n")
    
    client = ProtonMailClientIMAP()
    success = client.authenticate(username, password)
    
    if success:
        print("\n✅ Authentication successful!")
        client.close()
        return True
    else:
        print("\n❌ Authentication failed")
        print("\nPossible issues:")
        print("  - Incorrect Bridge username or password")
        print("  - ProtonMail Bridge not running")
        print("  - Bridge not properly configured")
        print("  - Network connectivity issues")
        return False


def test_basic_operations():
    """Test basic email operations."""
    print_section("Testing Basic Operations")
    
    load_dotenv()
    username = os.getenv("BRIDGE_USERNAME")
    password = os.getenv("BRIDGE_PASSWORD")
    
    client = ProtonMailClientIMAP()
    
    if not client.authenticate(username, password):
        print("❌ Cannot test operations - authentication failed")
        return False
    
    # Test: List messages
    try:
        print("\nTesting: list_messages...")
        messages = client.get_messages(limit=5)
        print(f"✓ Retrieved {len(messages)} messages")
        
        if messages:
            print(f"  Sample: '{messages[0].get('subject', 'No subject')}'")
    except Exception as e:
        print(f"❌ list_messages failed: {e}")
        client.close()
        return False
    
    # Test: Search messages
    try:
        print("\nTesting: search_messages...")
        results = client.search_messages("test", limit=5)
        print(f"✓ Search returned {len(results)} results")
    except Exception as e:
        print(f"❌ search_messages failed: {e}")
        client.close()
        return False
    
    # Test: Get folders
    try:
        print("\nTesting: get_folders...")
        folders = client.get_folders()
        print(f"✓ Retrieved {len(folders)} folders")
        if folders:
            print(f"  Folders: {', '.join([f['name'] for f in folders[:5]])}")
    except Exception as e:
        print(f"❌ get_folders failed: {e}")
        client.close()
        return False
    
    client.close()
    print("\n✅ All basic operations working")
    return True


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("  ProtonMail MCP Connector - IMAP Test Suite")
    print("=" * 60)
    
    all_passed = True
    
    # Run tests
    if not test_environment():
        all_passed = False
        print("\n⚠️  Create .env file and add Bridge credentials")
    else:
        # Only test Bridge if environment is configured
        if not test_bridge_running():
            all_passed = False
            print("\n⚠️  Start ProtonMail Bridge application")
        else:
            # Only test authentication if Bridge is running
            if not test_authentication():
                all_passed = False
            else:
                # Only test operations if authentication succeeded
                if not test_basic_operations():
                    all_passed = False
    
    # Final summary
    print_section("Test Summary")
    if all_passed:
        print("✅ All tests passed!")
        print("\nYou're ready to use the ProtonMail MCP Connector (IMAP)!")
        print("\nNext steps:")
        print("  1. Configure Claude Desktop (see BRIDGE_SETUP.md)")
        print("  2. Use: protonmail_server_imap.py")
        print("  3. Restart Claude Desktop")
        print("  4. Try: 'List my last 5 emails'")
    else:
        print("❌ Some tests failed")
        print("\nPlease review the errors above and:")
        print("  1. Make sure ProtonMail Bridge is installed and running")
        print("  2. Check Bridge credentials in .env")
        print("  3. Verify Bridge is logged in to your account")
        print("  4. See BRIDGE_SETUP.md for detailed setup instructions")
    
    print("\n" + "=" * 60 + "\n")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
