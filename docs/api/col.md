# Catalogue of Life (COL)

The `col` module provides access to the Catalogue of Life API for searching and retrieving taxonomic information.

::: pytaxize.col

## Overview

The Catalogue of Life is a comprehensive global index of known species of animals, plants, fungi and micro-organisms. The COL module provides functions to search for taxa and retrieve their children.

## Functions

### search

::: pytaxize.col.search

Search the Catalogue of Life for taxonomic records.

**Parameters:**

- `name` (str, optional): The scientific name to search for. Supports wildcards (* and %)
- `id` (str, optional): The record ID to retrieve
- `start` (int, optional): Starting position for results (default: 0)
- `checklist` (str, optional): Checklist to search within

**Returns:**

- Dictionary containing search results and metadata

**Examples:**

```python
from pytaxize import col

# Search by name
results = col.search(name="Puma concolor")
print(results)

# Search with wildcards
results = col.search(name="Puma*")

# Search by ID
results = col.search(id="6163618")

# Paginated search
results = col.search(name="Quercus", start=10)
```

### children

::: pytaxize.col.children

Get direct taxonomic children for a given taxon.

**Parameters:**

- `name` (str, optional): The scientific name of the parent taxon
- `id` (str, optional): The record ID of the parent taxon  
- `format` (str, optional): Response format
- `start` (int, optional): Starting position for results (default: 0)
- `checklist` (str, optional): Checklist to search within

**Returns:**

- Dictionary containing child taxa and metadata

**Examples:**

```python
from pytaxize import col

# Get children by name
children = col.children(name="Felidae")
for child in children.get('results', []):
    print(f"Child: {child['name']}")

# Get children by ID
children = col.children(id="6163618")

# Paginated results
children = col.children(name="Animalia", start=20)
```

## Usage Examples

### Basic Taxonomic Search

```python
from pytaxize import col

# Search for a specific species
species_results = col.search(name="Panthera leo")
if species_results.get('results'):
    for result in species_results['results']:
        print(f"Name: {result['name']}")
        print(f"ID: {result['id']}")
        print(f"Rank: {result.get('rank', 'Unknown')}")
        print(f"Status: {result.get('status', 'Unknown')}")
```

### Exploring Taxonomic Hierarchy

```python
from pytaxize import col

# Start with a family
family_name = "Felidae"
family_results = col.search(name=family_name)

if family_results.get('results'):
    family_id = family_results['results'][0]['id']
    
    # Get all genera in the family
    genera = col.children(id=family_id)
    
    print(f"Genera in {family_name}:")
    for genus in genera.get('results', []):
        print(f"  {genus['name']}")
        
        # Get species in each genus
        genus_children = col.children(id=genus['id'])
        species_count = len(genus_children.get('results', []))
        print(f"    ({species_count} species)")
```

### Wildcard Searches

```python
from pytaxize import col

# Find all oak species (Quercus)
oak_search = col.search(name="Quercus*")

print("Oak species found:")
for result in oak_search.get('results', []):
    if result.get('rank') == 'species':
        print(f"  {result['name']}")
```

### Working with Multiple Pages

```python
from pytaxize import col

def get_all_results(name, max_results=1000):
    """Get all search results for a name, handling pagination"""
    all_results = []
    start = 0
    page_size = 50  # COL typically returns 50 results per page
    
    while len(all_results) < max_results:
        results = col.search(name=name, start=start)
        page_results = results.get('results', [])
        
        if not page_results:
            break
            
        all_results.extend(page_results)
        
        # Check if we've got all results
        if len(page_results) < page_size:
            break
            
        start += page_size
    
    return all_results[:max_results]

# Get all Quercus entries
all_oaks = get_all_results("Quercus*", max_results=200)
print(f"Found {len(all_oaks)} oak entries")
```

### Taxonomic Validation

```python
from pytaxize import col

def validate_species_name(name):
    """Check if a species name exists in COL"""
    results = col.search(name=name)
    
    if not results.get('results'):
        return {"valid": False, "message": "No results found"}
    
    exact_matches = [r for r in results['results'] 
                    if r['name'].lower() == name.lower()]
    
    if exact_matches:
        match = exact_matches[0]
        return {
            "valid": True,
            "name": match['name'],
            "id": match['id'], 
            "rank": match.get('rank'),
            "status": match.get('status')
        }
    else:
        return {
            "valid": False,
            "message": f"No exact match found",
            "suggestions": [r['name'] for r in results['results'][:5]]
        }

# Validate some names
names_to_check = ["Homo sapiens", "Tyrannosaurus rex", "Invalid name"]
for name in names_to_check:
    result = validate_species_name(name)
    print(f"{name}: {result}")
```

## Data Structure

### Search Results Structure

```python
{
    "results": [
        {
            "id": "6163618",
            "name": "Puma concolor", 
            "rank": "species",
            "status": "accepted name",
            "match_type": "exact",
            "kingdom": "Animalia",
            "phylum": "Chordata",
            "class": "Mammalia",
            "order": "Carnivora",
            "family": "Felidae",
            "genus": "Puma",
            "authorship": "(Linnaeus, 1771)",
            # ... additional fields
        }
    ],
    "start": 0,
    "page_size": 50,
    "total_results": 1
}
```

### Children Results Structure

```python
{
    "results": [
        {
            "id": "6163620",
            "name": "Puma concolor concolor",
            "rank": "subspecies", 
            "status": "accepted name",
            "parent_id": "6163618",
            "authorship": "(Linnaeus, 1771)"
        },
        # ... more children
    ],
    "parent": {
        "id": "6163618", 
        "name": "Puma concolor",
        "rank": "species"
    }
}
```

## Parameters and Options

### Wildcards

- `*` (asterisk): Matches any number of characters
- `%` (percent): Also matches any number of characters
- Minimum 3 characters required (excluding wildcards)

```python
# These are equivalent
col.search(name="Quercus*")
col.search(name="Quercus%") 
```

### Pagination

- `start`: Starting position (0-based)
- Results are typically returned in pages of 50
- Use pagination for large result sets

### Checklists

COL includes multiple taxonomic checklists. You can specify which to search:

```python
# Search specific checklist (if available)
results = col.search(name="Panthera leo", checklist="mammals")
```

## Error Handling

```python
from pytaxize import col

def safe_col_search(name):
    """Safely search COL with error handling"""
    try:
        results = col.search(name=name)
        
        if not results:
            return {"error": "No response from API"}
            
        if not results.get('results'):
            return {"error": "No results found", "query": name}
            
        return {"success": True, "data": results}
        
    except Exception as e:
        return {"error": f"API error: {str(e)}", "query": name}

# Use the safe function
result = safe_col_search("Homo sapiens")
if "error" in result:
    print(f"Error: {result['error']}")
else:
    print(f"Found {len(result['data']['results'])} results")
```

## API Information

- **Base URL**: `http://www.catalogueoflife.org/col/webservice`
- **Format**: XML responses converted to Python dictionaries
- **Rate Limits**: No explicit limits, but please be respectful
- **Authentication**: None required
- **Coverage**: Global coverage across all kingdoms

## Notes and Limitations

1. **Name Matching**: Exact spelling is important for best results
2. **Wildcards**: Require minimum 3 characters (excluding wildcards)
3. **Status**: Results may include synonyms and accepted names
4. **Updates**: COL is updated regularly with new taxonomic information
5. **Coverage**: Varies by taxonomic group, strongest for well-studied taxa

## Best Practices

1. **Use wildcards judiciously**: Can return many results
2. **Check result status**: Distinguish between accepted names and synonyms
3. **Handle pagination**: Large searches may require multiple API calls
4. **Validate exact matches**: Check that returned names match your query
5. **Cache results**: Avoid repeated calls for the same data

## Related Functions

- [`Ids.gbif()`](ids.md#gbif): GBIF uses COL data for some taxonomic information
- [`Children.col()`](children.md): Alternative interface for getting children
- [`Classification.col()`](classification.md): Get full classifications using COL data