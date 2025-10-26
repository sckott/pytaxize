# API Overview

The pytaxize library provides a comprehensive set of functions and classes for working with taxonomic data from multiple sources. This page provides an overview of the main API components.

## Main Components

### Core Functions (`tax` module)

The `tax` module contains the core functionality for working with taxonomic names and data:

- `names_list()` - Generate random taxonomic names for testing
- `vascan_search()` - Search the CANADENSYS Vascan API
- `scrapenames()` - Extract taxonomic names from text, URLs, or files

### Taxonomic IDs (`Ids` class)

The `Ids` class provides a unified interface for getting taxonomic IDs from names across multiple databases:

```python
from pytaxize import Ids

# Create an Ids object
ids_obj = Ids(['Helianthus annuus', 'Pinus contorta'])

# Get IDs from different databases
ids_obj.itis()    # ITIS database
ids_obj.ncbi()    # NCBI database  
ids_obj.gbif()    # GBIF database
ids_obj.eol()     # Encyclopedia of Life

print(ids_obj.ids)  # Access the results
```

### Scientific/Common Names (`scicomm` module)

Convert between scientific and common names:

```python
from pytaxize import scicomm

# Get common names from scientific names
common = scicomm.sci2comm('Helianthus annuus')
common = scicomm.sci2comm(['Helianthus annuus', 'Poa annua'])
```

### Taxonomic Hierarchy (`Classification` class)

Retrieve complete taxonomic classifications:

```python
from pytaxize import Classification

# Get classification for ITIS ID
classification = Classification(99208)
classification.itis()
```

### Taxonomic Children (`Children` class)

Get direct taxonomic children for a given taxon:

```python
from pytaxize import Children

# Get children for ITIS ID
children = Children(179913)
children.itis()
```

## Database-Specific Modules

### ITIS (Integrated Taxonomic Information System)

Access to ITIS-specific functions:

```python
from pytaxize import itis

# Various ITIS functions
itis.accepted_names(tsn=12345)
itis.common_names(tsn=12345)
itis.hierarchy_full(tsn=12345)
```

### Catalogue of Life

Search and retrieve data from Catalogue of Life:

```python
from pytaxize import col

# Search COL
results = col.search(name="Puma concolor")

# Get children
children = col.children(name="Felidae")
```

### Global Names Services

Access Global Names Index and Resolver:

```python
from pytaxize import gn

# Global Names Index
gn.gni.search(search_term="Helianthus*")
gn.gni.parse(names=['Cyanistes caeruleus'])

# Global Names Resolver  
gn.gnr.resolve(names="Homo sapiens")
gn.gnr.datasources()
```

### NCBI

NCBI-specific functionality integrated with other modules.

## Common Patterns

### Error Handling

Most functions will raise exceptions for invalid inputs or API failures:

```python
from pytaxize.gn.gni import NoResultError

try:
    result = some_function()
except NoResultError:
    print("No results found")
```

### Data Formats

Many functions support different return formats:

```python
# Return as list (default)
result = tax.names_list(size=5)

# Return as DataFrame
result = tax.names_list(size=5, as_dataframe=True)
```

### Multiple Inputs

Most functions accept both single values and lists:

```python
# Single name
result = some_function("Helianthus annuus")

# Multiple names
result = some_function(["Helianthus annuus", "Poa annua"])
```

## Configuration

### Environment Variables

Some functions require API keys set as environment variables:

- `ENTREZ_KEY` - Required for NCBI functions

```python
import os
os.environ['ENTREZ_KEY'] = 'your_api_key_here'
```

## Best Practices

1. **Handle exceptions**: Always wrap API calls in try-except blocks
2. **Use appropriate databases**: Different databases have different strengths
3. **Batch requests**: When possible, request multiple names at once
4. **Cache results**: API calls can be slow, consider caching results
5. **Respect rate limits**: Don't overwhelm APIs with too many rapid requests

## Next Steps

- See individual module documentation for detailed function references
- Check out the [Examples](../examples/getting-started.md) for common usage patterns
- Review specific database documentation for specialized use cases