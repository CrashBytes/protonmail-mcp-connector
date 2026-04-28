# Contributing to ProtonMail MCP Connector

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on what's best for the community
- Show empathy towards others

## How Can I Contribute?

### Reporting Bugs

Before creating a bug report:
1. Check existing issues to avoid duplicates
2. Collect relevant information (OS, Python version, error logs)
3. Try to reproduce the issue with minimal steps

When creating a bug report, include:
- **Clear title** describing the issue
- **Steps to reproduce** the bug
- **Expected behavior** vs. **actual behavior**
- **Environment details** (OS, Python version, etc.)
- **Error messages** and logs
- **Screenshots** if applicable

### Suggesting Features

Feature suggestions are welcome! Please:
1. Check if the feature has already been suggested
2. Clearly describe the use case
3. Explain why this would be useful
4. Consider implementation complexity

### Pull Requests

1. **Fork** the repository
2. **Create a branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** with clear, descriptive commits
4. **Test thoroughly** - make sure nothing breaks
5. **Update documentation** if needed
6. **Submit a pull request** with a clear description

#### Pull Request Guidelines

- Keep changes focused and atomic
- Follow existing code style
- Add comments for complex logic
- Update CHANGELOG.md
- Test on multiple platforms if possible

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/protonmail-mcp-connector.git
cd protonmail-mcp-connector

# Set up development environment
uv venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
uv pip install -e .

# Create .env file
cp .env.example .env
# Add your test credentials
```

## Code Style

- Follow PEP 8 for Python code
- Use type hints where appropriate
- Write descriptive variable and function names
- Keep functions focused and single-purpose
- Add docstrings to all functions and classes

Example:
```python
def send_email(
    to: List[str],
    subject: str,
    body: str
) -> Dict[str, Any]:
    """
    Send an email via ProtonMail.
    
    Args:
        to: List of recipient email addresses
        subject: Email subject line
        body: Email body content
        
    Returns:
        Dictionary with send status and message ID
    """
    # Implementation here
```

## Testing

Before submitting a PR:

1. **Manual testing:**
   ```bash
   uv run mcp dev protonmail_server.py
   ```

2. **Test with Claude Desktop:**
   - Install your local version
   - Test all modified functionality
   - Verify error handling

3. **Check for common issues:**
   - Authentication works
   - Error messages are clear
   - No credentials in code
   - Documentation is updated

## Documentation

Good documentation is crucial. Please:
- Update README.md for new features
- Add examples for new tools
- Update QUICKSTART.md if setup changes
- Document any new configuration options
- Keep code comments clear and helpful

## Areas for Contribution

Looking for ideas? Here are some areas that need help:

### High Priority
- [ ] Attachment support (upload/download)
- [ ] Better error handling and retry logic
- [ ] Server-side search implementation
- [ ] Mark messages as read/unread
- [ ] Move messages between folders

### Medium Priority
- [ ] Draft management
- [ ] Folder/label management
- [ ] Message filtering options
- [ ] Better test coverage
- [ ] Performance optimizations

### Nice to Have
- [ ] Calendar integration
- [ ] Contact management
- [ ] Multi-account support
- [ ] Message templates
- [ ] Automated testing suite

## Questions?

- Open an issue with the "question" label
- Start a discussion in GitHub Discussions
- Check existing issues for similar questions

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Thanked in the community

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to ProtonMail MCP Connector! 🚀
