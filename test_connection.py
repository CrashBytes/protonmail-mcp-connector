"""
Test script for ProtonMail MCP Connector

This script performs basic tests to verify the installation
and ProtonMail connection.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
from protonmail_client import ProtonMailClient


def print_section(title):
    """Print a section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def test_imports():
    """Test that all required packages are installed."""
    print_section("Testing Imports")
    
    try:
        import mcp
        print("✓ mcp package installed")
    except ImportError:
        print("❌ mcp package not found")
        return False
    
    try:
        from protonmail import ProtonMail
        print("✓ protonmail-api-client package installed")
    except ImportError:
        print("❌ protonmail-api-client package not found")
        return False
    
    try:
        import dotenv
        print("✓ python-dotenv package installed")
    except ImportError:
        print("❌ python-dotenv package not found")
        return False
    
    print("\n✅ All required packages are installed")
    return True


def test_environment():
    """Test environment configuration."""
    print_section("Testing Environment Configuration")
    
    # Load .env file
    load_dotenv()
    
    username = os.getenv("PROTON_USERNAME")
    password = os.getenv("PROTON_PASSWORD")
    
    if not username:
        print("❌ PROTON_USERNAME not set in .env file")
        return False
    else:
        print(f"✓ PROTON_USERNAME: {username}")
    
    if not password:
        print("❌ PROTON_PASSWORD not set in .env file")
        return False
    else:
        print("✓ PROTON_PASSWORD: [hidden]")
    
    print("\n✅ Environment configuration OK")
    return True


def test_authentication():
    """Test ProtonMail authentication."""
    print_section("Testing ProtonMail Authentication")
    
    load_dotenv()
    username = os.getenv("PROTON_USERNAME")
    password = os.getenv("PROTON_PASSWORD")
    pgp_password = os.getenv("PROTON_PGP_PASSWORD")
    
    if not username or not password:
        print("❌ Missing credentials in .env file")
        return False
    
    print(f"Attempting to authenticate as: {username}")
    print("This may take a moment...\n")
    
    client = ProtonMailClient()
    success = client.authenticate(username, password, pgp_password)
    
    if success:
        print("\n✅ Authentication successful!")
        return True
    else:
        print("\n❌ Authentication failed")
        print("\nPossible issues:")
        print("  - Incorrect username or password")
        print("  - ProtonMail CAPTCHA protection (log in via web 10+ times)")
        print("  - Network connectivity issues")
        print("  - Two-factor authentication enabled (use app password)")
        return False


def test_basic_operations():
    """Test basic email operations."""
    print_section("Testing Basic Operations")
    
    load_dotenv()
    username = os.getenv("PROTON_USERNAME")
    password = os.getenv("PROTON_PASSWORD")
    pgp_password = os.getenv("PROTON_PGP_PASSWORD")
    
    client = ProtonMailClient()
    
    if not client.authenticate(username, password, pgp_password):
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
        return False
    
    # Test: Search messages
    try:
        print("\nTesting: search_messages...")
        results = client.search_messages("test", limit=5)
        print(f"✓ Search returned {len(results)} results")
    except Exception as e:
        print(f"❌ search_messages failed: {e}")
        return False
    
    # Test: Get folders
    try:
        print("\nTesting: get_folders...")
        folders = client.get_folders()
        print(f"✓ Retrieved {len(folders)} folders")
    except Exception as e:
        print(f"❌ get_folders failed: {e}")
        return False
    
    print("\n✅ All basic operations working")
    return True


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("  ProtonMail MCP Connector - Test Suite")
    print("=" * 60)
    
    all_passed = True
    
    # Run tests
    if not test_imports():
        all_passed = False
        print("\n⚠️  Install packages: uv pip install -e .")
    
    if not test_environment():
        all_passed = False
        print("\n⚠️  Create .env file from .env.example and add credentials")
    else:
        # Only test authentication if environment is configured
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
        print("\nYou're ready to use the ProtonMail MCP Connector!")
        print("\nNext steps:")
        print("  1. Configure Claude Desktop (see QUICKSTART.md)")
        print("  2. Restart Claude Desktop")
        print("  3. Try: 'List my last 5 emails'")
    else:
        print("❌ Some tests failed")
        print("\nPlease review the errors above and:")
        print("  1. Check the QUICKSTART.md guide")
        print("  2. Verify your .env configuration")
        print("  3. Ensure all packages are installed")
    
    print("\n" + "=" * 60 + "\n")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
