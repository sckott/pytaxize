# Taxonomic IDs (Ids Class)

The `Ids` class provides a unified interface for retrieving taxonomic identifiers from taxonomic names across multiple databases.

## Overview

The `Ids` class is designed to take taxonomic names and retrieve corresponding identifiers from various taxonomic databases. It provides a consistent interface regardless of which database you're querying.

## Class Methods

### Constructor

```python
from pytaxize.ids import Ids

# Single name
ids_obj = Ids('Helianthus annuus')

# Multiple names
ids_obj = Ids(['Helianthus annuus', 'Pinus contorta'])

# From list
names = ['Homo sapiens', 'Canis lupus']
ids_obj = Ids(names)
```

### Database Methods

#### itis()

Get taxonomic IDs from ITIS (Integrated Taxonomic Information System).

**Parameters:**
- `type` (str): Type of search - "scientific" (default)

**Examples:**

```python
from pytaxize.ids import Ids

ids_obj = Ids(['Helianthus annuus', 'Pinus contorta'])
ids_obj.itis()
print(ids_obj.ids)

# With search type
ids_obj = Ids('Quercus alba')
ids_obj.itis(type='scientific')
print(ids_obj.ids)
```

#### ncbi()

Get taxonomic IDs from NCBI Taxonomy database.

**Examples:**

```python
from pytaxize.ids import Ids

ids_obj = Ids('Homo sapiens')
ids_obj.ncbi()
print(ids_obj.ids)
```

#### gbif()

Get taxonomic IDs from GBIF (Global Biodiversity Information Facility).

**Parameters:**
- `rank` (str): Taxonomic rank to search - "species" (default)

**Examples:**

```python
from pytaxize.ids import Ids

ids_obj = Ids('Quercus alba')
ids_obj.gbif()
print(ids_obj.ids)

# With specific rank
ids_obj.gbif(rank='genus')
```

#### db()

Generic method to query any supported database.

**Parameters:**
- `db` (str): Database name ('itis', 'ncbi')
- `**kwargs`: Additional parameters passed to specific database methods

**Examples:**

```python
from pytaxize.ids import Ids

ids_obj = Ids('Canis lupus')
ids_obj.db(db='itis')
ids_obj.db(db='ncbi')

# With parameters
ids_obj.db(db='itis', type='scientific')
```

## Properties

### ids

Access the retrieved taxonomic IDs.

**Returns:**
- Dictionary with species names as keys and lists of ID records as values

### name

Get the original input names.

**Returns:**
- List of taxonomic names that were queried

### db_ids

Get the database that was last queried.

**Returns:**
- String indicating the database ('itis', 'ncbi', 'gbif')

## Methods

### extract_ids()

Extract just the ID values from the results.

**Returns:**
- Dictionary with species names as keys and lists of ID strings as values

**Examples:**

```python
from pytaxize.ids import Ids

ids_obj = Ids(['Homo sapiens', 'Quercus alba'])
ids_obj.itis()

# Get full results
print(ids_obj.ids)

# Extract just the IDs
id_dict = ids_obj.extract_ids()
print(id_dict)
```

## Usage Examples

### Basic Usage

```python
from pytaxize.ids import Ids

# Single species
single_species = Ids('Helianthus annuus')
single_species.itis()
print(f"ITIS results: {single_species.ids}")

# Multiple species
multi_species = Ids(['Helianthus annuus', 'Pinus contorta', 'Quercus alba'])
multi_species.itis()
print(f"Multiple species results: {multi_species.ids}")
```

### Querying Multiple Databases

```python
from pytaxize.ids import Ids

species = Ids('Homo sapiens')

# Get IDs from different databases
species.itis()
itis_results = species.ids.copy()
itis_db = species.db_ids

species.ncbi()
ncbi_results = species.ids.copy()
ncbi_db = species.db_ids

species.gbif()
gbif_results = species.ids.copy()
gbif_db = species.db_ids

print(f"ITIS ({itis_db}): {itis_results}")
print(f"NCBI ({ncbi_db}): {ncbi_results}")
print(f"GBIF ({gbif_db}): {gbif_results}")
```

### Working with Results

```python
from pytaxize.ids import Ids

ids_obj = Ids(['Felis catus', 'Canis lupus'])
ids_obj.itis()

# Iterate through results
for species_name, id_list in ids_obj.ids.items():
    print(f"\nSpecies: {species_name}")
    if id_list:
        for record in id_list:
            print(f"  ID: {record.get('id')}")
            print(f"  Name: {record.get('name')}")
            print(f"  Rank: {record.get('rank', 'Unknown')}")
            print(f"  URI: {record.get('uri', 'N/A')}")
    else:
        print("  No IDs found")
```

### Extracting Just IDs

```python
from pytaxize.ids import Ids

# Get IDs and extract just the ID values
species = Ids(['Homo sapiens', 'Quercus alba'])
species.itis()

# Full results
print("Full results:")
print(species.ids)

# Just the ID values
ids_only = species.extract_ids()
print("\nJust IDs:")
print(ids_only)

# Access specific species ID
homo_sapiens_ids = ids_only.get('Homo sapiens', [])
print(f"\nHomo sapiens IDs: {homo_sapiens_ids}")
```

### Error Handling

```python
from pytaxize.ids import Ids
import warnings

def safe_id_lookup(species_names, database='itis'):
    """Safely look up species IDs with error handling"""

    try:
        ids_obj = Ids(species_names)

        if database == 'itis':
            ids_obj.itis()
        elif database == 'ncbi':
            ids_obj.ncbi()
        elif database == 'gbif':
            ids_obj.gbif()
        else:
            raise ValueError(f"Unsupported database: {database}")

        results = {}
        for name, id_list in ids_obj.ids.items():
            if id_list and id_list[0].get('id'):
                results[name] = {
                    'success': True,
                    'ids': id_list,
                    'count': len(id_list),
                    'database': ids_obj.db_ids
                }
            else:
                results[name] = {
                    'success': False,
                    'message': f'No {database} IDs found',
                    'database': database
                }

        return results

    except Exception as e:
        return {'error': f'Lookup failed: {str(e)}'}

# Test with various inputs
test_species = ['Homo sapiens', 'Invalid species', 'Quercus alba']
results = safe_id_lookup(test_species, database='itis')

for species, result in results.items():
    print(f"\n{species}:")
    if 'error' in result:
        print(f"  Error: {result['error']}")
    elif result['success']:
        print(f"  Found {result['count']} ID(s) in {result['database']}")
    else:
        print(f"  {result['message']}")
```

### Integration with Other Functions

```python
from pytaxize.ids import Ids, scicomm

# Get IDs first
ids_obj = Ids(['Helianthus annuus', 'Quercus alba'])
ids_obj.ncbi()

# Use the Ids object with scicomm
common_names = scicomm.sci2comm(ids_obj)
print(f"Common names: {common_names}")

# Or work with extracted IDs
id_values = ids_obj.extract_ids()
for species, ids in id_values.items():
    print(f"{species}: {ids}")
```

## Data Structure

The `ids` property returns a dictionary with the following structure:

```python
{
    'Species name 1': [
        {
            'id': 'taxonomic_id',
            'name': 'matched_name',
            'rank': 'taxonomic_rank',
            'uri': 'reference_uri'
        },
        # ... more records if multiple matches
    ],
    'Species name 2': [
        # ... records for second species
    ]
}
```

## Database Information

### ITIS (Integrated Taxonomic Information System)
- **Coverage**: Primarily North American species
- **ID Format**: Taxonomic Serial Number (TSN)
- **API**: ITIS Web Services
- **Free**: Yes

### NCBI Taxonomy
- **Coverage**: All domains of life with genetic data
- **ID Format**: Taxonomy ID (TaxID)
- **API**: NCBI E-utilities
- **Requirements**: ENTREZ_KEY recommended

### GBIF (Global Biodiversity Information Facility)
- **Coverage**: Global species with occurrence data
- **ID Format**: GBIF species key
- **API**: GBIF Species API
- **Free**: Yes

## Configuration

### Environment Variables

For NCBI access, you should set your ENTREZ API key:

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

## Notes and Limitations

1. **Name Matching**: Exact spelling is important for good results
2. **Multiple Matches**: Some names may return multiple IDs
3. **Synonyms**: Different databases may recognize different synonyms
4. **Coverage**: Database coverage varies by taxonomic group
5. **API Dependencies**: Results depend on external API availability
6. **Warning System**: Invalid names will generate warnings

## Best Practices

1. **Start with ITIS or NCBI**: These have the most comprehensive coverage
2. **Handle empty results**: Not all names will be found in all databases
3. **Validate results**: Check that returned names match your input
4. **Use appropriate database**: Choose based on your taxonomic focus
5. **Set API keys**: Improves rate limits and reliability
6. **Extract IDs when needed**: Use `extract_ids()` for just the ID values

## Related Functions

- [`scicomm.sci2comm`](scicomm.md): Convert IDs to common names
- [`Classification`](classification.md): Get taxonomic hierarchy from IDs
- [`Children`](children.md): Get taxonomic children from IDs
