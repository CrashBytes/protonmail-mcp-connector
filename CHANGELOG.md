# Changelog

All notable changes to the ProtonMail MCP Connector will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Attachment support (upload and download)
- Mark messages as read/unread
- Move messages between folders
- Draft management
- Calendar integration
- Contact management
- Better error handling and retry logic
- Server-side search (if API supports it)
- Multi-account support

## [0.1.0] - 2024-11-29

### Added
- Initial release
- ProtonMail authentication with session persistence
- List messages from inbox
- Read full message content
- Send emails with CC and BCC support
- Search messages (client-side)
- Delete messages
- MCP tools for all email operations
- MCP resources for status and account info
- MCP prompts for email drafting and summarization
- Comprehensive documentation
- Quick start guide
- MIT License

### Security
- Environment variable support for credentials
- Session file for persistent authentication
- .gitignore configured to prevent credential leaks

## [0.0.1] - 2024-11-29

### Added
- Project structure
- Basic documentation
- Development environment setup
