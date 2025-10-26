# Scientific and Common Names (scicomm)

The `scicomm` module provides functions to convert between scientific names and common names using various taxonomic databases.

::: pytaxize.scicomm

## Functions

### sci2comm

::: pytaxize.scicomm.sci2comm

Convert scientific names to common names.

**Parameters:**

- `x` (str, list, or Ids): Scientific name(s) or an Ids object
- `db` (str): Database to use - 'ncbi' or 'itis'. Default: 'ncbi'

**Returns:**

- Dictionary with scientific names as keys and common names as values

**Examples:**

```python
from pytaxize import scicomm

# Single scientific name
common = scicomm.sci2comm('Helianthus annuus')
print(common)  # {'Helianthus annuus': ['common sunflower']}

# Multiple names
names = ['Helianthus annuus', 'Poa annua']
common = scicomm.sci2comm(names)
print(common)

# Using ITIS database
common = scicomm.sci2comm('Puma concolor', db="itis")

# Using an Ids object
from pytaxize import Ids
ids_obj = Ids('Helianthus annuus')
ids_obj.ncbi()
common = scicomm.sci2comm(ids_obj)
```

## Classes

### CommonNames

::: pytaxize.scicomm.CommonNames

Internal class for handling common name lookups. Not typically used directly.

**Methods:**

- `call()`: Execute the common name lookup
- `ncbi(x)`: Get common names from NCBI
- `itis(x)`: Get common names from ITIS

## Usage Examples

### Basic Usage

```python
from pytaxize import scicomm

# Get common names for well-known species
animals = ['Homo sapiens', 'Canis lupus', 'Felis catus']
common_names = scicomm.sci2comm(animals)

for scientific, common in common_names.items():
    if common:
        print(f"{scientific}: {', '.join(common)}")
    else:
        print(f"{scientific}: No common names found")
```

### Using Different Databases

```python
from pytaxize import scicomm

species = 'Loxodonta africana'

# Try NCBI first
ncbi_names = scicomm.sci2comm(species, db='ncbi')
print(f"NCBI: {ncbi_names}")

# Try ITIS
itis_names = scicomm.sci2comm(species, db='itis')
print(f"ITIS: {itis_names}")
```

### Working with Ids Objects

```python
from pytaxize import scicomm, Ids

# Create Ids object with multiple names
species_list = ['Gadus morhua', 'Pomatomus saltatrix']
ids_obj = Ids(species_list)

# Get IDs from ITIS
ids_obj.itis()
print("ITIS IDs:", ids_obj.ids)

# Get common names using the Ids object
common = scicomm.sci2comm(ids_obj)
print("Common names:", common)
```

### Error Handling

```python
from pytaxize import scicomm

try:
    # This might fail if ENTREZ_KEY is not set for NCBI
    result = scicomm.sci2comm('Helianthus annuus', db='ncbi')
    print(result)
except Exception as e:
    print(f"Error: {e}")
    
# Try with a non-existent species
result = scicomm.sci2comm('Nonexistent species')
print(result)  # Will likely return empty list
```

## Database Information

### NCBI (National Center for Biotechnology Information)

- **API**: NCBI E-utilities
- **Requirements**: ENTREZ_KEY environment variable must be set
- **Coverage**: Comprehensive for animals, plants, and microorganisms
- **Common name types**: Genbank common names

```python
import os
os.environ['ENTREZ_KEY'] = 'your_ncbi_api_key'
```

### ITIS (Integrated Taxonomic Information System)

- **API**: ITIS Web Services
- **Requirements**: No API key needed
- **Coverage**: North American species focus
- **Common name types**: Vernacular names from ITIS database

## Configuration

### Environment Variables

For NCBI access, you must set your ENTREZ API key:

```bash
export ENTREZ_KEY="your_api_key_here"
```

Or in Python:

```python
import os
os.environ['ENTREZ_KEY'] = 'your_api_key_here'
```

You can get a free NCBI API key by:
1. Creating an NCBI account
2. Going to your account settings
3. Creating an API key

### Rate Limits

- **NCBI**: 3 requests/second without API key, 10 requests/second with API key
- **ITIS**: No explicit rate limits, but please be respectful

## Return Format

The `sci2comm` function returns a dictionary where:

- **Keys**: Original scientific names (input)
- **Values**: Lists of common names (may be empty if no common names found)

```python
{
    'Helianthus annuus': ['common sunflower', 'sunflower'],
    'Unknown species': []  # No common names found
}
```

## Notes and Limitations

1. **Database Coverage**: Not all species have common names in databases
2. **Multiple Names**: Some species may have multiple common names
3. **Language**: Common names are primarily in English
4. **Spelling Variations**: Scientific name spelling must be exact
5. **Synonyms**: Only current accepted names may return results

## Best Practices

1. **Always handle empty results**: Not all species have common names
2. **Use appropriate database**: NCBI for broad coverage, ITIS for North American focus
3. **Set API keys**: Required for NCBI, improves rate limits
4. **Batch requests**: Process multiple names at once when possible
5. **Cache results**: API calls can be slow, consider caching for repeated use

## Related Functions

- [`Ids`](ids.md): Get taxonomic IDs from names
- [`tax.names_list`](tax.md#names_list): Generate test species names
- [`itis`](itis.md): Direct ITIS database access