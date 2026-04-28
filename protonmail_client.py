"""
ProtonMail client wrapper for MCP server.

This module provides a simplified interface to the ProtonMail API
for use in the MCP server.
"""

import os
import pickle
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime


class ProtonMailClient:
    """
    Wrapper class for ProtonMail API interactions.
    
    Handles authentication, session management, and provides
    simplified methods for common email operations.
    """
    
    def __init__(self, session_file: str = "proton_session.pickle"):
        """
        Initialize the ProtonMail client.
        
        Args:
            session_file: Path to store the session pickle file
        """
        self.session_file = Path(session_file)
        self.client: Optional[Any] = None
        self._authenticated = False
        
    def authenticate(
        self,
        username: str,
        password: str,
        pgp_password: Optional[str] = None
    ) -> bool:
        """
        Authenticate with ProtonMail.
        
        Attempts to load an existing session first. If that fails,
        performs a fresh login.
        
        Args:
            username: ProtonMail username/email
            password: ProtonMail password
            pgp_password: Optional PGP key passphrase
            
        Returns:
            True if authentication successful, False otherwise
        """
        try:
            # Import here to avoid issues if package not installed
            from protonmail import ProtonMail
            
            self.client = ProtonMail()
            
            # Try to load existing session first
            if self.session_file.exists():
                try:
                    self.client.load_session(str(self.session_file))
                    self._authenticated = True
                    print("✓ Loaded existing ProtonMail session")
                    return True
                except Exception as e:
                    print(f"⚠ Could not load session: {e}")
                    print("Attempting fresh login...")
            
            # Fresh login
            print("Logging into ProtonMail...")
            self.client.login(username, password)
            
            # Import and unlock PGP key if password provided
            if pgp_password:
                # Note: This may need to be customized based on your PGP key setup
                # For now, we'll skip this as it requires the private key file
                pass
            
            # Save session for future use
            self.client.save_session(str(self.session_file))
            self._authenticated = True
            print("✓ ProtonMail authentication successful!")
            return True
            
        except ImportError:
            print("❌ Error: protonmail-api-client not installed")
            print("Run: uv pip install protonmail-api-client")
            return False
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            self._authenticated = False
            return False
    
    def _ensure_authenticated(self):
        """Raise exception if not authenticated."""
        if not self._authenticated or not self.client:
            raise Exception("Not authenticated. Please call authenticate() first.")
    
    def get_messages(
        self,
        limit: int = 50,
        label: str = "inbox"
    ) -> List[Dict[str, Any]]:
        """
        Get messages from a folder.
        
        Args:
            limit: Maximum number of messages to retrieve
            label: Folder label (inbox, sent, drafts, etc.)
            
        Returns:
            List of message dictionaries
        """
        self._ensure_authenticated()
        
        try:
            # Get messages (API may vary based on library version)
            messages = self.client.get_messages(limit=limit)
            
            result = []
            for msg in messages:
                result.append({
                    "id": msg.get("ID", ""),
                    "subject": msg.get("Subject", "(No Subject)"),
                    "sender": msg.get("Sender", {}).get("Address", "Unknown"),
                    "sender_name": msg.get("Sender", {}).get("Name", ""),
                    "time": msg.get("Time", 0),
                    "unread": msg.get("Unread", 0) == 1,
                    "snippet": msg.get("Body", "")[:200]  # First 200 chars
                })
            
            return result
            
        except Exception as e:
            raise Exception(f"Failed to get messages: {e}")
    
    def read_message(self, message_id: str) -> Dict[str, Any]:
        """
        Read the full content of a specific message.
        
        Args:
            message_id: The ID of the message to read
            
        Returns:
            Dictionary with full message details
        """
        self._ensure_authenticated()
        
        try:
            msg = self.client.get_message(message_id)
            
            # Parse recipients
            to_list = msg.get("ToList", [])
            recipients = [r.get("Address", "") for r in to_list]
            
            cc_list = msg.get("CCList", [])
            cc_recipients = [r.get("Address", "") for r in cc_list]
            
            return {
                "id": msg.get("ID", ""),
                "subject": msg.get("Subject", "(No Subject)"),
                "sender": msg.get("Sender", {}).get("Address", "Unknown"),
                "sender_name": msg.get("Sender", {}).get("Name", ""),
                "recipients": recipients,
                "cc": cc_recipients,
                "time": msg.get("Time", 0),
                "body": msg.get("Body", ""),
                "attachments": len(msg.get("Attachments", [])),
                "attachment_names": [
                    att.get("Name", "") 
                    for att in msg.get("Attachments", [])
                ]
            }
            
        except Exception as e:
            raise Exception(f"Failed to read message: {e}")
    
    def send_message(
        self,
        to: List[str],
        subject: str,
        body: str,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        is_html: bool = False
    ) -> Dict[str, Any]:
        """
        Send an email via ProtonMail.
        
        Args:
            to: List of recipient email addresses
            subject: Email subject
            body: Email body (plain text or HTML)
            cc: Optional list of CC recipients
            bcc: Optional list of BCC recipients
            is_html: Whether the body is HTML
            
        Returns:
            Dictionary with send status and message ID
        """
        self._ensure_authenticated()
        
        try:
            # Create the message
            new_message = self.client.create_message(
                recipients=to,
                cc=cc or [],
                bcc=bcc or [],
                subject=subject,
                body=body
            )
            
            # Send the message
            result = self.client.send_message(new_message)
            
            return {
                "success": True,
                "message_id": result.get("ID") if result else None,
                "status": "sent",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            raise Exception(f"Failed to send message: {e}")
    
    def search_messages(
        self,
        query: str,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Search messages for a query string.
        
        Note: This is a client-side search implementation.
        For better results, ProtonMail's server-side search API
        would be needed (if available).
        
        Args:
            query: Search query string
            limit: Maximum number of messages to search through
            
        Returns:
            List of matching messages
        """
        self._ensure_authenticated()
        
        try:
            # Get recent messages to search through
            messages = self.client.get_messages(limit=limit * 2)
            
            # Simple text-based search
            results = []
            query_lower = query.lower()
            
            for msg in messages:
                # Search in subject, body, and sender
                subject = msg.get("Subject", "").lower()
                body = msg.get("Body", "").lower()
                sender = msg.get("Sender", {}).get("Address", "").lower()
                sender_name = msg.get("Sender", {}).get("Name", "").lower()
                
                if (query_lower in subject or 
                    query_lower in body or 
                    query_lower in sender or
                    query_lower in sender_name):
                    
                    results.append({
                        "id": msg.get("ID", ""),
                        "subject": msg.get("Subject", "(No Subject)"),
                        "sender": msg.get("Sender", {}).get("Address", "Unknown"),
                        "sender_name": msg.get("Sender", {}).get("Name", ""),
                        "time": msg.get("Time", 0),
                        "snippet": msg.get("Body", "")[:200]
                    })
                    
                    if len(results) >= limit:
                        break
            
            return results
            
        except Exception as e:
            raise Exception(f"Search failed: {e}")
    
    def delete_message(self, message_id: str) -> bool:
        """
        Delete a message.
        
        Args:
            message_id: ID of the message to delete
            
        Returns:
            True if successful
        """
        self._ensure_authenticated()
        
        try:
            self.client.delete_messages([message_id])
            return True
        except Exception as e:
            raise Exception(f"Failed to delete message: {e}")
    
    def get_folders(self) -> List[Dict[str, Any]]:
        """
        Get list of folders/labels.
        
        Returns:
            List of folder information
        """
        self._ensure_authenticated()
        
        try:
            # This may vary based on the API client version
            # Placeholder implementation
            return [
                {"name": "Inbox", "id": "0"},
                {"name": "Sent", "id": "1"},
                {"name": "Drafts", "id": "2"},
                {"name": "Trash", "id": "3"},
                {"name": "Spam", "id": "4"},
            ]
        except Exception as e:
            raise Exception(f"Failed to get folders: {e}")
