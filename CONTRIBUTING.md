# Contributing to MoltSwarm

Thank you for your interest in contributing! MoltSwarm is an open collaborative project — everyone is welcome.

## 🤝 How to Contribute

### Report Bugs

Found a bug? Please open an issue with:

- Bug description
- Steps to reproduce
- Expected vs actual behavior
- Environment details

### Suggest Features

Have an idea? We'd love to hear it:

- Feature description
- Use case
- Possible implementation approach

### Submit Code

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 🛠️ Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/MoltSwarm.git
cd MoltSwarm

# Install in development mode
pip install -e . -r requirements-dev.txt

# Run tests
pytest

# Format code
black moltswarm/
isort moltswarm/
```

## 📋 Coding Standards

- Follow PEP 8
- Add docstrings to functions/classes
- Keep functions focused and small
- Add type hints where useful

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_node.py

# With coverage
pytest --cov=moltswarm
```

## 📖 Documentation

Keep docs in sync with code:

- Update README.md for user-facing changes
- Update ARCHITECTURE.md for design changes
- Update API.md for API changes

## 🎯 Good First Issues

Look for issues labeled `good first issue` to get started.

## 💬 Discussion

Join the discussion in Moltbook community!

---

Thank you for contributing! 🐝
