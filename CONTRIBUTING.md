# Contributing to PhantomTrace

Thank you for your interest in contributing to PhantomTrace! This project aims to advance anti-forensics research and privacy protection.

## Code of Conduct

- Use this software ethically and legally
- Respect privacy and security
- Contribute high-quality, well-tested code
- Document your work thoroughly

## How to Contribute

### Reporting Bugs

- Check if the issue already exists
- Provide detailed reproduction steps
- Include system information (OS, Python version)
- Attach relevant logs or error messages

### Suggesting Features

- Describe the anti-forensics technique clearly
- Explain the novel aspects
- Provide research references if available
- Discuss implementation approach

### Contributing Code

1. **Fork the repository**

2. **Create a feature branch**
   ```bash
   git checkout -b feature/new-technique
   ```

3. **Write your code**
   - Follow Python PEP 8 style guide
   - Add docstrings to all functions/classes
   - Include type hints where appropriate
   - Keep functions focused and modular

4. **Add tests**
   - Write unit tests for new functionality
   - Ensure tests pass: `pytest`
   - Aim for >80% code coverage

5. **Update documentation**
   - Add docstrings
   - Update README if needed
   - Create example usage in `examples/`

6. **Run linters**
   ```bash
   black phantomtrace/
   flake8 phantomtrace/
   ```

7. **Commit your changes**
   ```bash
   git commit -m "Add feature: [brief description]"
   ```

8. **Push and create pull request**
   ```bash
   git push origin feature/new-technique
   ```

## Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/phantomtrace.git
cd phantomtrace

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
pip install -r requirements.txt
pip install pytest black flake8

# Run tests
pytest
```

## Module Structure

When adding a new anti-forensics module:

```python
"""
Module Name

Brief description of the technique.

Novel Concepts:
- Concept 1
- Concept 2
"""

class YourModule:
    """
    Detailed class description.
    
    Features:
    - Feature 1
    - Feature 2
    """
    
    def __init__(self):
        """Initialize module."""
        pass
    
    def main_function(self, arg1: str, arg2: int = 10) -> bool:
        """
        Function description.
        
        Args:
            arg1: Description
            arg2: Description with default
        
        Returns:
            Description of return value
        """
        pass
```

## Research Contributions

If you're implementing a technique from a research paper:

1. Cite the paper in the module docstring
2. Explain how your implementation differs/improves
3. Add the paper to `docs/research.md`
4. Include performance benchmarks if relevant

## Security

- Never commit sensitive data
- Review code for security vulnerabilities
- Test with sanitized data only
- Report security issues privately

## Questions?

Open an issue or start a discussion on GitHub.

Thank you for contributing to privacy and security research!
