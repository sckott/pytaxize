# Contributing to pytaxize

Thank you for your interest in contributing to pytaxize! This guide will help you get started with contributing to the project.

## Ways to Contribute

### Reporting Bugs

If you find a bug, please open an issue on GitHub with:

- A clear description of the problem
- Steps to reproduce the issue
- Expected vs. actual behavior
- Your Python version and pytaxize version
- Any error messages or stack traces

### Suggesting Features

We welcome feature suggestions! Please open an issue with:

- A clear description of the proposed feature
- The use case or problem it solves
- Any relevant examples or mockups

### Contributing Code

#### Setting Up the Development Environment

1. **Fork and clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/pytaxize.git
   cd pytaxize
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install in development mode**:
   ```bash
   pip install -e ".[dev]"
   ```

4. **Install pre-commit hooks** (recommended):
   ```bash
   pre-commit install
   ```

#### Development Workflow

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the coding standards below

3. **Run tests**:
   ```bash
   pytest
   ```

4. **Run linting**:
   ```bash
   ruff check .
   ruff format .
   ```

5. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add feature: your feature description"
   ```

6. **Push and create a pull request**:
   ```bash
   git push origin feature/your-feature-name
   ```

#### Coding Standards

- **Python Style**: Follow PEP 8. We use `ruff` for linting and formatting
- **Docstrings**: Use Google-style docstrings for all public functions and classes
- **Type Hints**: Add type hints where appropriate
- **Error Handling**: Include appropriate error handling and informative error messages

#### Example Function with Good Documentation

```python
def search_species(name: str, database: str = "itis") -> dict:
    """Search for species information in taxonomic databases.
    
    Args:
        name: Scientific name of the species to search for
        database: Database to search in (default: "itis")
        
    Returns:
        Dictionary containing species information including:
        - id: Taxonomic identifier
        - name: Matched scientific name
        - rank: Taxonomic rank
        
    Raises:
        ValueError: If database is not supported
        NoResultError: If no results are found
        
    Example:
        >>> result = search_species("Quercus alba")
        >>> print(result['name'])
        'Quercus alba'
    """
    if database not in SUPPORTED_DATABASES:
        raise ValueError(f"Database {database} not supported")
    
    # Implementation here
    pass
```

### Testing

#### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pytaxize

# Run specific test file
pytest test/test_tax.py

# Run specific test
pytest test/test_tax.py::test_names_list
```

#### Writing Tests

- Write tests for all new functions and classes
- Use descriptive test names
- Include both positive and negative test cases
- Mock external API calls when appropriate

#### Example Test

```python
import pytest
from pytaxize import tax
from unittest.mock import patch, Mock

def test_names_list_returns_correct_number():
    """Test that names_list returns the requested number of names."""
    result = tax.names_list(size=5)
    assert len(result) == 5

def test_names_list_invalid_rank():
    """Test that names_list handles invalid rank gracefully."""
    result = tax.names_list(rank='invalid')
    assert isinstance(result, str)
    assert 'must be one of' in result

@patch('pytaxize.tax.requests.get')
def test_api_call_error_handling(mock_get):
    """Test that API errors are handled properly."""
    mock_get.side_effect = requests.RequestException("API Error")
    
    with pytest.raises(requests.RequestException):
        tax.some_function_that_calls_api()
```

### Documentation

#### Updating Documentation

- Documentation is built with MkDocs and uses docstrings from the code
- Update docstrings when you modify function signatures or behavior
- Add examples to docstrings when helpful
- Update the changelog for user-facing changes

#### Building Documentation Locally

```bash
# Install docs dependencies
pip install -e ".[docs]"

# Serve docs locally
mkdocs serve

# Build static docs
mkdocs build
```

#### Documentation Structure

```
docs/
├── index.md                 # Main documentation page
├── api/                     # API reference
│   ├── overview.md
│   ├── tax.md
│   ├── ids.md
│   └── ...
├── examples/                # Usage examples
│   ├── getting-started.md
│   └── common-use-cases.md
├── contributing.md          # This file
└── changelog.md
```

## API Design Guidelines

### Function Design

- **Consistent naming**: Use clear, descriptive function names
- **Reasonable defaults**: Provide sensible default parameters
- **Return types**: Be consistent with return types across similar functions
- **Error handling**: Fail gracefully with informative error messages

### Database Integration

- **Consistent interface**: New database integrations should follow existing patterns
- **Error handling**: Handle API failures, rate limits, and network issues
- **Caching**: Consider caching for expensive operations
- **Documentation**: Document API limits, requirements, and quirks

### Example Database Integration

```python
def new_database_search(name: str, **kwargs) -> dict:
    """Search the New Database for taxonomic information.
    
    Args:
        name: Scientific name to search for
        **kwargs: Additional parameters passed to the API
        
    Returns:
        Dictionary with search results
        
    Raises:
        NoResultError: If no results found
        APIError: If API request fails
    """
    try:
        response = make_api_request(name, **kwargs)
        if not response.get('results'):
            raise NoResultError(f"No results found for {name}")
        return format_response(response)
    except requests.RequestException as e:
        raise APIError(f"API request failed: {e}")
```

## Release Process

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality in a backwards compatible manner
- **PATCH**: Backwards compatible bug fixes

### Changelog

Update `CHANGELOG.md` with:

- New features
- Bug fixes
- Breaking changes
- Deprecations

### Release Checklist

1. Update version in `pytaxize/__init__.py`
2. Update `CHANGELOG.md`
3. Run full test suite
4. Update documentation
5. Create release on GitHub
6. Publish to PyPI (maintainers only)

## Getting Help

- **Documentation**: Check the [API documentation](api/overview.md) and [examples](examples/getting-started.md)
- **Issues**: Search existing issues on GitHub
- **Discussions**: Use GitHub Discussions for questions and ideas
- **Contact**: Reach out to maintainers for complex questions

## Code of Conduct

This project follows a code of conduct based on respect and inclusivity:

- Be respectful and constructive in discussions
- Welcome newcomers and help them learn
- Focus on what is best for the community
- Show empathy towards other community members

## Recognition

Contributors are recognized in:

- GitHub contributor statistics
- Release notes for significant contributions
- Documentation acknowledgments

Thank you for contributing to pytaxize!