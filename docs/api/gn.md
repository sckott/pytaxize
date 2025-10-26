# Global Names Services

The `gn` module provides access to Global Names services including the Global Names Index (GNI) and Global Names Resolver (GNR).

::: pytaxize.gn

## Overview

Global Names services provide comprehensive tools for taxonomic name recognition, parsing, and resolution. The `gn` module includes two main sub-modules:

- **GNI (Global Names Index)**: Search and parse scientific names
- **GNR (Global Names Resolver)**: Resolve names against multiple data sources

## Sub-modules

### Global Names Index (GNI)

::: pytaxize.gn.gni

The Global Names Index provides functions for parsing and searching scientific names.

#### parse

::: pytaxize.gn.gni.parse

Parse scientific names to extract their components.

**Parameters:**
- `names` (list): List of scientific names to parse

**Returns:**
- List of dictionaries containing parsed name components

**Examples:**

```python
from pytaxize import gn

# Parse scientific names
names = ['Cyanistes caeruleus', 'Helianthus annuus', 'Homo sapiens']
results = gn.gni.parse(names=names)

for result in results:
    print(f"Name: {result.get('scientificName', 'Unknown')}")
    print(f"Genus: {result.get('genus', 'Unknown')}")
    print(f"Species: {result.get('species', 'Unknown')}")
```

#### search

::: pytaxize.gn.gni.search

Search the Global Names Index for names matching a pattern.

**Parameters:**
- `search_term` (str): Search pattern (supports wildcards). Default: "ani*"
- `per_page` (int): Results per page. Default: 30
- `page` (int): Page number to retrieve. Default: 1

**Returns:**
- Dictionary containing search results and metadata

**Examples:**

```python
from pytaxize import gn

# Search for names starting with 'Quer'
results = gn.gni.search(search_term="Quer*", per_page=10)

print(f"Found {len(results.get('names', []))} results")
for name in results.get('names', []):
    print(f"  {name}")
```

#### details

::: pytaxize.gn.gni.details

Get detailed information about a specific name string ID.

**Parameters:**
- `id` (int): Name string ID. Default: 17802847
- `all_records` (int): Include all records (1) or just best (0). Default: 1

**Returns:**
- Dictionary containing detailed name information

**Examples:**

```python
from pytaxize import gn

# Get details for a specific name ID
details = gn.gni.details(id=17802847)
print(f"Name: {details.get('name', 'Unknown')}")
print(f"Canonical: {details.get('canonical', 'Unknown')}")
```

### Global Names Resolver (GNR)

::: pytaxize.gn.gnr

The Global Names Resolver resolves scientific names against multiple taxonomic data sources.

#### resolve

::: pytaxize.gn.gnr.resolve

Resolve scientific names against taxonomic databases.

**Parameters:**
- `names` (str or list): Scientific name(s) to resolve. Default: "Homo sapiens"
- `source` (str, optional): Specific data source to use
- `format` (str): Response format. Default: "json"
- `resolve_once` (str): Resolve each name only once. Default: "false"
- `with_context` (str): Include context information. Default: "false"
- `best_match_only` (str): Return only best matches. Default: "false"
- `header_only` (str): Return headers only. Default: "false"
- `preferred_data_sources` (str): Use preferred data sources. Default: "false"
- `http` (str): HTTP method to use. Default: "get"

**Returns:**
- Dictionary containing resolution results

**Examples:**

```python
from pytaxize import gn

# Resolve a single name
result = gn.gnr.resolve(names="Homo sapiens")
print(result)

# Resolve multiple names
names = ["Quercus alba", "Pinus strobus", "Acer saccharum"]
results = gn.gnr.resolve(names=names)

for name_result in results.get('data', []):
    supplied_name = name_result.get('supplied_name_string')
    print(f"\nSupplied: {supplied_name}")
    
    for result in name_result.get('results', []):
        matched_name = result.get('canonical_form')
        data_source = result.get('data_source_title')
        print(f"  Match: {matched_name} (Source: {data_source})")
```

#### datasources

::: pytaxize.gn.gnr.datasources

Get information about available data sources in GNR.

**Returns:**
- List of dictionaries containing data source information

**Examples:**

```python
from pytaxize import gn

# Get all available data sources
sources = gn.gnr.datasources()

print(f"Found {len(sources)} data sources:")
for source in sources[:10]:  # Show first 10
    print(f"  {source['id']}: {source['title']}")
```

## Usage Examples

### Basic Name Resolution Workflow

```python
from pytaxize import gn

def resolve_species_names(species_list):
    """Resolve a list of species names using GNR"""
    
    # First, resolve against all data sources
    resolution = gn.gnr.resolve(names=species_list)
    
    results = {}
    
    for name_result in resolution.get('data', []):
        supplied_name = name_result.get('supplied_name_string')
        results[supplied_name] = {
            'matches': [],
            'best_match': None
        }
        
        # Process all matches
        for match in name_result.get('results', []):
            match_info = {
                'canonical_form': match.get('canonical_form'),
                'data_source': match.get('data_source_title'),
                'score': match.get('score', 0)
            }
            results[supplied_name]['matches'].append(match_info)
        
        # Find best match (highest score)
        if results[supplied_name]['matches']:
            best = max(results[supplied_name]['matches'], 
                      key=lambda x: x['score'])
            results[supplied_name]['best_match'] = best
    
    return results

# Example usage
species = ["Quercus alba", "Homo sapiens", "Invalid species"]
resolved = resolve_species_names(species)

for name, info in resolved.items():
    print(f"\nName: {name}")
    if info['best_match']:
        best = info['best_match']
        print(f"  Best match: {best['canonical_form']}")
        print(f"  Source: {best['data_source']}")
        print(f"  Score: {best['score']}")
    else:
        print("  No matches found")
```

### Name Parsing and Validation

```python
from pytaxize import gn

def validate_and_parse_names(names_list):
    """Parse and validate scientific names"""
    
    # Parse the names first
    parsed = gn.gni.parse(names=names_list)
    
    validation_results = []
    
    for i, name in enumerate(names_list):
        parse_result = parsed[i] if i < len(parsed) else {}
        
        # Check if parsing was successful
        is_parsed = bool(parse_result.get('parsed'))
        
        result = {
            'original': name,
            'parsed_successfully': is_parsed,
            'canonical': parse_result.get('canonical'),
            'genus': parse_result.get('genus'),
            'species': parse_result.get('species'),
            'authorship': parse_result.get('authorship')
        }
        
        # Additional validation
        if is_parsed:
            # Check if it's a binomial name
            parts = result['canonical'].split() if result['canonical'] else []
            result['is_binomial'] = len(parts) == 2
            result['is_valid_format'] = result['is_binomial'] and result['genus'] and result['species']
        else:
            result['is_binomial'] = False
            result['is_valid_format'] = False
        
        validation_results.append(result)
    
    return validation_results

# Example usage
test_names = [
    "Homo sapiens",           # Valid binomial
    "Quercus alba L.",        # Valid with authority
    "Quercus",               # Genus only
    "invalid name format",    # Invalid
    "Canis lupus familiaris" # Trinomial
]

validated = validate_and_parse_names(test_names)

for result in validated:
    print(f"\nOriginal: {result['original']}")
    print(f"Valid format: {result['is_valid_format']}")
    if result['canonical']:
        print(f"Canonical: {result['canonical']}")
    if result['authorship']:
        print(f"Author: {result['authorship']}")
```

### Finding Data Sources

```python
from pytaxize import gn

def find_relevant_datasources(keywords):
    """Find data sources relevant to specific keywords"""
    
    all_sources = gn.gnr.datasources()
    relevant_sources = []
    
    for source in all_sources:
        title = source.get('title', '').lower()
        description = source.get('description', '').lower()
        
        # Check if any keyword appears in title or description
        for keyword in keywords:
            if keyword.lower() in title or keyword.lower() in description:
                relevant_sources.append({
                    'id': source['id'],
                    'title': source['title'],
                    'description': source.get('description', 'No description')
                })
                break
    
    return relevant_sources

# Find sources for specific groups
plant_sources = find_relevant_datasources(['plant', 'flora', 'botanical'])
animal_sources = find_relevant_datasources(['animal', 'fauna', 'zoological'])

print("Plant-related data sources:")
for source in plant_sources[:5]:
    print(f"  {source['id']}: {source['title']}")

print("\nAnimal-related data sources:")  
for source in animal_sources[:5]:
    print(f"  {source['id']}: {source['title']}")
```

### Targeted Resolution with Specific Sources

```python
from pytaxize import gn

def resolve_with_specific_sources(names, source_ids):
    """Resolve names against specific data sources"""
    
    # Convert source IDs to string format required by API
    source_string = '|'.join(map(str, source_ids))
    
    # Resolve with specific sources
    results = gn.gnr.resolve(
        names=names,
        preferred_data_sources=source_string,
        best_match_only="true"
    )
    
    resolved_names = {}
    
    for name_result in results.get('data', []):
        supplied_name = name_result.get('supplied_name_string')
        
        matches = name_result.get('results', [])
        if matches:
            best_match = matches[0]  # Since we requested best_match_only
            resolved_names[supplied_name] = {
                'matched_name': best_match.get('canonical_form'),
                'source': best_match.get('data_source_title'),
                'source_id': best_match.get('data_source_id'),
                'score': best_match.get('score')
            }
        else:
            resolved_names[supplied_name] = None
    
    return resolved_names

# Example: Resolve against ITIS and Catalogue of Life only
species = ["Quercus alba", "Pinus strobus"]
itis_col_sources = [3, 1]  # Example source IDs for ITIS and COL

resolved = resolve_with_specific_sources(species, itis_col_sources)

for name, match in resolved.items():
    print(f"\nName: {name}")
    if match:
        print(f"  Resolved to: {match['matched_name']}")
        print(f"  Source: {match['source']}")
        print(f"  Score: {match['score']}")
    else:
        print("  No match found in specified sources")
```

## Error Handling

```python
from pytaxize import gn
from pytaxize.gn.gni import NoResultError

def safe_name_resolution(names):
    """Safely resolve names with comprehensive error handling"""
    
    results = {
        'successful': [],
        'failed': [],
        'errors': []
    }
    
    try:
        # Try to resolve names
        resolution = gn.gnr.resolve(names=names)
        
        if resolution and 'data' in resolution:
            for name_result in resolution['data']:
                name = name_result.get('supplied_name_string')
                
                if name_result.get('results'):
                    results['successful'].append(name)
                else:
                    results['failed'].append(name)
            
            results['resolution_data'] = resolution
        else:
            results['errors'].append("No data returned from API")
            
    except NoResultError as e:
        results['errors'].append(f"No results error: {e}")
    except Exception as e:
        results['errors'].append(f"Unexpected error: {e}")
    
    return results

# Test error handling
test_names = ["Valid name", "Invalid name", "Homo sapiens"]
results = safe_name_resolution(test_names)

print(f"Successful: {len(results['successful'])}")
print(f"Failed: {len(results['failed'])}")
if results['errors']:
    print(f"Errors: {results['errors']}")
```

## API Information

### Global Names Index (GNI)
- **Base URL**: `http://gni.globalnames.org/`
- **Rate Limits**: No explicit limits, but please be respectful
- **Authentication**: None required
- **Coverage**: Comprehensive index of scientific names

### Global Names Resolver (GNR)
- **Base URL**: `http://resolver.globalnames.org/`
- **Rate Limits**: No explicit limits, but please be respectful  
- **Authentication**: None required
- **Data Sources**: 100+ taxonomic databases

## Notes and Limitations

1. **Network Dependency**: Requires internet connection for all functions
2. **Response Time**: Large queries may take time to process
3. **Data Quality**: Results depend on quality of underlying data sources
4. **Name Variants**: May not catch all spelling variations or synonyms
5. **Taxonomic Coverage**: Coverage varies by taxonomic group

## Best Practices

1. **Batch Processing**: Process multiple names at once when possible
2. **Error Handling**: Always include try-catch blocks for network operations
3. **Result Validation**: Check scores and multiple sources for important names
4. **Caching**: Cache results to avoid repeated API calls
5. **Rate Limiting**: Add delays for large batch operations

## Related Functions

- [`tax.scrapenames`](tax.md#scrapenames): Extract names from text using Global Names services
- [`Ids`](ids.md): Get taxonomic IDs which can be cross-referenced with GN results
- [`scicomm`](scicomm.md): Convert between scientific and common names