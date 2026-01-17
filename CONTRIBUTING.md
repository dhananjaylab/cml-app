# Contributing to Text2SQL

Thank you for considering contributing to Text2SQL! This document provides guidelines and instructions for contributing to the project.

## 🤝 Code of Conduct

Please be respectful, inclusive, and constructive in all interactions. We're building a welcoming community for developers of all skill levels.

## 📋 Getting Started

### Prerequisites

- Python 3.10 or higher
- Git
- GitHub account
- Familiarity with FastAPI and Streamlit (helpful but not required)

### Fork and Clone

```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/YOUR_USERNAME/cml-app.git
cd cml-app

# Add upstream remote
git remote add upstream https://github.com/dhananjaylab/cml-app.git

# Create a new branch
git checkout -b feature/your-feature-name
```

### Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies with dev tools
pip install -r 0_session-install-dependencies/requirements.txt
pip install pytest pytest-cov black isort flake8 mypy
```

## 🛠️ Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

Branch naming conventions:
- `feature/` - New features
- `bugfix/` - Bug fixes
- `docs/` - Documentation
- `refactor/` - Code refactoring
- `test/` - Test additions

### 2. Make Changes

Follow these guidelines:

**Code Style**
- Use 4 spaces for indentation
- Follow PEP 8 style guide
- Maximum line length: 88 characters (Black standard)
- Use meaningful variable names

**Comments and Docstrings**
- Add docstrings to all functions and classes
- Use Google-style docstrings:
```python
def convert_text_to_sql(question: str, database: str) -> str:
    """Convert natural language question to SQL query.
    
    Args:
        question: Natural language question from user
        database: Target database name (e.g., 'HR', 'Banking')
    
    Returns:
        Generated SQL query string
        
    Raises:
        ValueError: If question is empty or database not supported
    """
```

### 3. Format and Lint

```bash
# Format code with Black
black . --line-length 88

# Sort imports with isort
isort .

# Check code quality with flake8
flake8 . --max-line-length 88

# Type checking with mypy (optional)
mypy . --ignore-missing-imports
```

### 4. Write Tests

Add tests for new functionality:

```python
# tests/test_llm_handler.py
import pytest
from app.utils.llm_handler import convert_to_sql

def test_convert_simple_question():
    result = convert_to_sql("Show all employees")
    assert "SELECT" in result
    assert "EMPLOYEE" in result

def test_convert_with_filter():
    result = convert_to_sql("Show employees in sales department")
    assert "WHERE" in result
    assert "SALES" in result.upper()
```

Run tests:
```bash
pytest tests/ -v --cov=app
```

### 5. Update Documentation

- Update README.md if behavior changes
- Add docstrings to new functions
- Update ARCHITECTURE.md if structure changes
- Add examples for new features

### 6. Commit Changes

```bash
# Stage changes
git add .

# Commit with clear message
git commit -m "feat: add support for GROUP BY queries"

# Commit message format:
# feat: New feature
# fix: Bug fix
# docs: Documentation changes
# refactor: Code restructuring
# test: Test additions
# perf: Performance improvements
```

### 7. Push and Create Pull Request

```bash
# Push to your fork
git push origin feature/your-feature-name

# Go to GitHub and create a Pull Request
```

**PR Title Format**: `[Type] Short description`
Example: `[Feature] Add support for subqueries`

**PR Description Template**:
```markdown
## Description
Brief description of changes

## Related Issues
Fixes #123

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added
- [ ] Integration tests added
- [ ] Manual testing done

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-reviewed changes
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] Tests passing locally
```

## 📝 Types of Contributions

### Bug Reports

Found a bug? [Open an issue](https://github.com/dhananjaylab/cml-app/issues)

**Issue template**:
```markdown
**Describe the bug**
Clear description of what the bug is

**Steps to reproduce**
1. ...
2. ...
3. ...

**Expected behavior**
What should happen

**Actual behavior**
What happens instead

**Environment**
- OS: [Windows/Mac/Linux]
- Python version: 3.x
- Browser: [if applicable]

**Logs/Screenshots**
Any error messages or screenshots
```

### Feature Requests

Have an idea? [Open a feature request](https://github.com/dhananjaylab/cml-app/issues)

**Template**:
```markdown
**Problem statement**
Describe the problem or use case

**Proposed solution**
How should this be implemented

**Alternative solutions**
Other approaches considered

**Additional context**
Any other information
```

### Documentation

Improvements to documentation are always welcome:
- Fix typos
- Clarify complex sections
- Add examples
- Improve formatting
- Translate to other languages

### Code Quality

- Add tests for untested code
- Optimize performance
- Refactor complex functions
- Improve error messages
- Add type hints

## 🔍 Code Review Process

### What We Look For

1. **Functionality**: Does it work? Is it bug-free?
2. **Code Quality**: Is it clean, readable, and maintainable?
3. **Tests**: Are there adequate tests?
4. **Documentation**: Is it well-documented?
5. **Performance**: Does it impact performance negatively?
6. **Security**: Are there security concerns?
7. **Backwards Compatibility**: Does it break existing functionality?

### Review Timeline

- We aim to review PRs within 48 hours
- Feedback will be provided as comments
- You may be asked to make changes
- Once approved, maintainers will merge

## 🚀 Development Tips

### Running Locally

```bash
# Terminal 1: Start backend
cd 3_app-run-python-script
python app.py --reload

# Terminal 2: Start frontend
streamlit run app.py

# Terminal 3: Run tests
pytest tests/ -v --watch
```

### Debugging

```python
# Use print statements
print(f"Debug: {variable}")

# Or use Python debugger
import pdb; pdb.set_trace()

# Or use VS Code debugger with launch.json
```

### Common Issues

**Issue**: Virtual environment not activating
```bash
# Try this
python -m venv venv
source venv/bin/activate
```

**Issue**: Module not found
```bash
# Reinstall dependencies
pip install -r 0_session-install-dependencies/requirements.txt --upgrade
```

**Issue**: Tests failing
```bash
# Run with verbose output
pytest tests/ -vv --tb=short
```

## 📚 Resources

- [Git Guide](https://git-scm.com/doc)
- [GitHub Help](https://help.github.com/)
- [Python Style Guide (PEP 8)](https://pep8.org/)
- [FastAPI Best Practices](https://fastapi.tiangolo.com/deployment/)
- [Streamlit Best Practices](https://docs.streamlit.io/library/get-started)

## ❓ Questions?

- Check existing [issues](https://github.com/dhananjaylab/cml-app/issues)
- Ask in [discussions](https://github.com/dhananjaylab/cml-app/discussions)
- Email: [your-email@example.com]

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Text2SQL! 🎉
