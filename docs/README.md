# pytaxize Documentation

This directory contains the complete documentation for the pytaxize package, built with MkDocs and the Material theme.

## Overview

The documentation includes:

- **API Reference**: Complete documentation of all classes and functions
- **Getting Started Guide**: Tutorial for new users
- **Common Use Cases**: Real-world examples and workflows
- **Contributing Guide**: Information for developers
- **Changelog**: Version history and changes

## Building the Documentation

### Prerequisites

Make sure you have the documentation dependencies installed:

```bash
uv sync --group docs
```

### Building Static Documentation

To build the documentation as static HTML files:

```bash
uv run mkdocs build
```

The built documentation will be available in the `site/` directory.

### Serving Documentation Locally

To serve the documentation locally with live reload:

```bash
uv run mkdocs serve
```

This will start a development server at `http://localhost:8000` where you can view the documentation. The server will automatically reload when you make changes to the documentation files.

### Opening Documentation

To build and immediately open the documentation in your browser:

```bash
uv run mkdocs serve --open
```

## Documentation Structure

```
docs/
├── README.md                    # This file
├── index.md                     # Main documentation page
├── api/                         # API reference documentation
│   ├── overview.md             # API overview and patterns
│   ├── tax.md                  # Core tax module functions
│   ├── scicomm.md              # Scientific/common name conversion
│   ├── ids.md                  # Taxonomic ID retrieval
│   ├── itis.md                 # ITIS database functions
│   ├── ncbi.md                 # NCBI database integration
│   ├── col.md                  # Catalogue of Life functions
│   ├── gn.md                   # Global Names services
│   ├── children.md             # Taxonomic children retrieval
│   ├── classification.md       # Taxonomic hierarchy retrieval
│   └── utils.md                # Utility functions
├── examples/                    # Usage examples and tutorials
│   ├── getting-started.md      # Basic usage tutorial
│   └── common-use-cases.md     # Advanced workflows
├── contributing.md              # Developer contribution guide
└── changelog.md                 # Version history and changes
```

## Writing Documentation

### Markdown Guidelines

- Use clear, descriptive headings
- Include code examples for all functions
- Add usage examples that users can copy and run
- Use consistent formatting for parameters, returns, and examples
- Include error handling examples where appropriate

### Code Examples

All code examples should be:
- Runnable (when dependencies are available)
- Well-commented
- Include expected output when helpful
- Show error handling where appropriate

Example format:
```python
from pytaxize import Ids

# Get taxonomic IDs for species
ids_obj = Ids(['Homo sapiens', 'Quercus alba'])
ids_obj.itis()

# Print results
for species, results in ids_obj.ids.items():
    print(f"{species}: {len(results)} matches")
```

### API Documentation

Each API page should include:
- Overview of the module/class
- Complete function/method signatures
- Parameter descriptions
- Return value descriptions
- Usage examples
- Error handling examples
- Integration examples with other modules
- Notes and limitations

## Configuration

The documentation is configured in `mkdocs.yml` with:

- **Material theme** with dark/light mode toggle
- **Navigation** organized by topic
- **Search** functionality
- **Code highlighting** with copy buttons
- **Responsive design** for mobile and desktop

## Deployment

The documentation can be deployed to:

- **GitHub Pages**: Using `mkdocs gh-deploy`
- **Read the Docs**: Automatically builds from the repository
- **Custom hosting**: Deploy the `site/` directory contents

## Contributing to Documentation

1. **Fork and clone** the repository
2. **Make changes** to the relevant `.md` files
3. **Test locally** with `uv run mkdocs serve`
4. **Build documentation** with `uv run mkdocs build`
5. **Submit pull request** with your improvements

### Common Documentation Tasks

**Adding a new API function:**
1. Document it in the appropriate `api/*.md` file
2. Include usage examples and error handling
3. Add cross-references to related functions

**Adding a new example:**
1. Add to `examples/common-use-cases.md`
2. Include complete, runnable code
3. Explain the use case and benefits

**Updating existing documentation:**
1. Ensure examples still work with current API
2. Update parameter descriptions if changed
3. Add new features and deprecation notices

## Troubleshooting

### Build Errors

If `mkdocs build` fails:
1. Check that all referenced files exist
2. Verify markdown syntax is correct
3. Ensure all internal links are valid
4. Check that code examples use correct API

### Dependency Issues

If documentation dependencies are missing:
```bash
uv sync --group docs
```

### Live Reload Not Working

If `mkdocs serve` doesn't auto-reload:
1. Check file permissions
2. Restart the development server
3. Use `mkdocs serve --clean` for a fresh build

## Links

- [MkDocs Documentation](https://www.mkdocs.org/)
- [Material Theme](https://squidfunk.github.io/mkdocs-material/)
- [Markdown Guide](https://www.markdownguide.org/)
- [pytaxize Repository](https://github.com/sckott/pytaxize)