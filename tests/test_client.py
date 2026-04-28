"""Smoke tests for ProtonMailClient (no network required)."""

import pytest
from protonmail_client import ProtonMailClient


class TestProtonMailClientInit:
    """Test client instantiation and default state."""

    def test_default_session_file(self):
        client = ProtonMailClient()
        assert client.session_file.name == "proton_session.pickle"

    def test_custom_session_file(self):
        client = ProtonMailClient(session_file="/tmp/test_session.pickle")
        assert str(client.session_file) == "/tmp/test_session.pickle"

    def test_not_authenticated_by_default(self):
        client = ProtonMailClient()
        assert client._authenticated is False
        assert client.client is None


class TestUnauthenticatedGuard:
    """Verify that operations fail gracefully when not authenticated."""

    def test_get_messages_requires_auth(self):
        client = ProtonMailClient()
        with pytest.raises(Exception, match="Not authenticated"):
            client.get_messages()

    def test_read_message_requires_auth(self):
        client = ProtonMailClient()
        with pytest.raises(Exception, match="Not authenticated"):
            client.read_message("fake-id")

    def test_send_message_requires_auth(self):
        client = ProtonMailClient()
        with pytest.raises(Exception, match="Not authenticated"):
            client.send_message(to=["a@b.com"], subject="Hi", body="Hello")

    def test_search_messages_requires_auth(self):
        client = ProtonMailClient()
        with pytest.raises(Exception, match="Not authenticated"):
            client.search_messages("test")

    def test_delete_message_requires_auth(self):
        client = ProtonMailClient()
        with pytest.raises(Exception, match="Not authenticated"):
            client.delete_message("fake-id")

    def test_get_folders_requires_auth(self):
        client = ProtonMailClient()
        with pytest.raises(Exception, match="Not authenticated"):
            client.get_folders()
