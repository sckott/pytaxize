# pytaxize

A taxonomic toolbelt for Python providing access to multiple taxonomic databases and services.

## Overview

`pytaxize` is a Python library that provides a unified interface to query taxonomic databases and services. It allows you to:

- Get taxonomic IDs from taxonomic names and vice versa
- Retrieve taxonomic hierarchies and classifications
- Access common names for scientific names
- Search and resolve taxonomic names
- Get taxonomic children for given taxa
- Access data from multiple taxonomic databases

## Supported Data Sources

- **ITIS** (Integrated Taxonomic Information System)
- **NCBI** (National Center for Biotechnology Information)
- **Catalogue of Life**
- **Global Names Index**
- **Global Names Resolver**
- **CANADENSYS Vascan API**

## Installation

Install from PyPI:

```bash
pip install pytaxize
```

Or install the development version:

```bash
pip install git+https://github.com/sckott/pytaxize.git
```

## Quick Start

```python
from pytaxize import tax, Ids
from pytaxize import scicomm

# Get random taxonomic names
names = tax.names_list(rank='species', size=5)
print(names)

# Get taxonomic IDs
ids_obj = Ids(['Helianthus annuus', 'Pinus contorta'])
ids_obj.itis()
print(ids_obj.ids)

# Get common names from scientific names
common = scicomm.sci2comm('Helianthus annuus')
print(common)

# Search for names in text
results = tax.scrapenames(text='A spider named Pardosa moesta Banks, 1892')
print(results)
```

## Main Modules

- **`tax`** - Core taxonomic functions for name lists and text scraping
- **`Ids`** - Get taxonomic IDs from names across multiple databases
- **`scicomm`** - Convert between scientific and common names
- **`Children`** - Retrieve taxonomic children
- **`Classification`** - Get taxonomic hierarchies
- **`itis`** - ITIS-specific functions
- **`col`** - Catalogue of Life functions
- **`gn`** - Global Names services

## Features

- **Multiple data sources**: Access to major taxonomic databases
- **Flexible input**: Accept strings, lists, or specialized objects
- **Consistent interface**: Similar patterns across different data sources
- **Rich metadata**: Get detailed information about taxonomic records
- **Error handling**: Robust error handling for API failures
- **Data formats**: Support for both raw data and pandas DataFrames

## Use Cases

- **Biodiversity research**: Standardize and validate species names
- **Ecological studies**: Get taxonomic hierarchies for analysis
- **Museum collections**: Resolve and update taxonomic names
- **Literature mining**: Extract taxonomic names from text
- **Data cleaning**: Validate and standardize taxonomic data

## Getting Help

- Check the [API Reference](api/overview.md) for detailed documentation
- See [Examples](examples/getting-started.md) for common usage patterns
- Visit the [GitHub repository](https://github.com/sckott/pytaxize) for issues and discussions
- Read the [Contributing Guide](contributing.md) to help improve pytaxize

## License

MIT License. See the [LICENSE](https://github.com/sckott/pytaxize/blob/main/LICENSE) file for details.

## Citation

If you use pytaxize in your research, please cite:

```
Chamberlain, S. (2024). pytaxize: Taxonomic toolbelt for Python.
https://github.com/sckott/pytaxize
```
