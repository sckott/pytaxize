# NCBI Taxonomy

The `ncbi` module provides access to NCBI (National Center for Biotechnology Information) Taxonomy database through integration with other pytaxize modules.

## Overview

NCBI Taxonomy is a comprehensive database covering all organisms represented in genetic databases. While pytaxize doesn't have a dedicated `ncbi` module, NCBI functionality is integrated throughout the package, particularly in the `Ids` class and `scicomm` module.

## NCBI Integration Points

### Getting NCBI Taxonomy IDs

The primary way to access NCBI taxonomy data is through the `Ids` class:

```python
from pytaxize import Ids

# Get NCBI taxonomy IDs
species = Ids(['Homo sapiens', 'Escherichia coli'])
species.ncbi()
print(species.ids)
```

### Common Names from NCBI

The `scicomm` module can retrieve common names from NCBI:

```python
from pytaxize import scicomm

# Get common names from NCBI
common = scicomm.sci2comm('Homo sapiens', db='ncbi')
print(common)
```

## Configuration

### API Key Setup

NCBI requires an API key for enhanced access. Set it as an environment variable:

```bash
export ENTREZ_KEY="your_ncbi_api_key_here"
```

Or in Python:

```python
import os
os.environ['ENTREZ_KEY'] = 'your_ncbi_api_key_here'
```

### Getting an API Key

1. Create an NCBI account at https://www.ncbi.nlm.nih.gov/account/
2. Go to account settings
3. Generate an API key
4. Set the key in your environment

## Usage Examples

### Basic NCBI ID Retrieval

```python
from pytaxize import Ids
import os

# Make sure API key is set
os.environ['ENTREZ_KEY'] = 'your_api_key'

# Get NCBI taxonomy IDs
species_list = [
    'Homo sapiens',
    'Mus musculus', 
    'Drosophila melanogaster',
    'Escherichia coli',
    'Saccharomyces cerevisiae'
]

ids_obj = Ids(species_list)
ids_obj.ncbi()

print("NCBI Taxonomy IDs:")
for species, results in ids_obj.ids.items():
    if results:
        for result in results:
            print(f"  {species}: {result['id']} ({result['name']})")
    else:
        print(f"  {species}: No NCBI ID found")
```

### Comparing NCBI with Other Databases

```python
from pytaxize import Ids

def compare_ncbi_itis(species_name):
    """Compare NCBI and ITIS results for a species"""
    
    # Get NCBI data
    ncbi_ids = Ids(species_name)
    ncbi_ids.ncbi()
    
    # Get ITIS data
    itis_ids = Ids(species_name)
    itis_ids.itis()
    
    print(f"Comparison for: {species_name}")
    
    # NCBI results
    ncbi_results = ncbi_ids.ids.get(species_name, [])
    print(f"NCBI matches: {len(ncbi_results)}")
    for result in ncbi_results:
        print(f"  ID: {result['id']}, Name: {result['name']}")
    
    # ITIS results
    itis_results = itis_ids.ids.get(species_name, [])
    print(f"ITIS matches: {len(itis_results)}")
    for result in itis_results:
        print(f"  ID: {result['id']}, Name: {result['name']}")

# Compare databases
compare_ncbi_itis("Homo sapiens")
```

### Getting Common Names from NCBI

```python
from pytaxize import scicomm
import os

# Ensure API key is set
os.environ['ENTREZ_KEY'] = 'your_api_key'

def get_ncbi_common_names(species_list):
    """Get common names for species from NCBI"""
    
    results = {}
    
    for species in species_list:
        try:
            common = scicomm.sci2comm(species, db='ncbi')
            common_names = common.get(species, [])
            
            if common_names:
                results[species] = common_names
                print(f"{species}: {', '.join(common_names)}")
            else:
                results[species] = []
                print(f"{species}: No common names found")
                
        except Exception as e:
            print(f"Error getting common names for {species}: {e}")
            results[species] = None
    
    return results

# Example species
species = [
    'Homo sapiens',
    'Canis lupus',
    'Felis catus',
    'Bos taurus',
    'Sus scrofa'
]

common_names = get_ncbi_common_names(species)
```

### Working with Microorganisms

NCBI has excellent coverage for microorganisms:

```python
from pytaxize import Ids, scicomm

def analyze_microbes(microbe_list):
    """Analyze microbial species using NCBI data"""
    
    # Get NCBI IDs
    ids_obj = Ids(microbe_list)
    ids_obj.ncbi()
    
    analysis = {}
    
    for microbe in microbe_list:
        results = ids_obj.ids.get(microbe, [])
        
        if results:
            best_match = results[0]  # Use first/best match
            
            # Try to get common names
            try:
                common = scicomm.sci2comm(microbe, db='ncbi')
                common_names = common.get(microbe, [])
            except:
                common_names = []
            
            analysis[microbe] = {
                'ncbi_id': best_match['id'],
                'matched_name': best_match['name'],
                'rank': best_match.get('rank', 'Unknown'),
                'common_names': common_names,
                'found': True
            }
        else:
            analysis[microbe] = {
                'found': False,
                'error': 'No NCBI match found'
            }
    
    return analysis

# Example microorganisms
microbes = [
    'Escherichia coli',
    'Bacillus subtilis',
    'Saccharomyces cerevisiae', 
    'Plasmodium falciparum',
    'Mycobacterium tuberculosis'
]

microbe_analysis = analyze_microbes(microbes)

for microbe, data in microbe_analysis.items():
    print(f"\n{microbe}:")
    if data['found']:
        print(f"  NCBI ID: {data['ncbi_id']}")
        print(f"  Matched name: {data['matched_name']}")
        print(f"  Rank: {data['rank']}")
        if data['common_names']:
            print(f"  Common names: {', '.join(data['common_names'])}")
    else:
        print(f"  {data['error']}")
```

## NCBI Database Features

### Coverage
- **Comprehensive**: All domains of life with genetic data
- **Microorganisms**: Excellent coverage of bacteria, archaea, viruses
- **Model organisms**: Complete coverage of research organisms
- **Metagenomics**: Environmental and uncultured organisms

### Data Types
- **Taxonomy IDs**: Unique numeric identifiers
- **Scientific names**: Current accepted names
- **Common names**: Vernacular names when available
- **Lineages**: Complete taxonomic hierarchies
- **Genetic codes**: Translation tables for organisms

### Advantages
- Regularly updated with new genetic data
- Phylogenetically informed classifications
- Integration with genetic databases
- Standardized identifiers across NCBI services

## Rate Limits and Best Practices

### Rate Limits
- **Without API key**: 3 requests per second
- **With API key**: 10 requests per second
- Burst requests may be temporarily blocked

### Best Practices

```python
import time
from pytaxize import Ids

def batch_ncbi_lookup(species_list, batch_size=10, delay=0.2):
    """Perform NCBI lookups in batches with rate limiting"""
    
    all_results = {}
    
    # Process in batches
    for i in range(0, len(species_list), batch_size):
        batch = species_list[i:i + batch_size]
        
        print(f"Processing batch {i//batch_size + 1}: {len(batch)} species")
        
        try:
            # Process batch
            ids_obj = Ids(batch)
            ids_obj.ncbi()
            
            # Add results
            all_results.update(ids_obj.ids)
            
            # Rate limiting delay
            if i + batch_size < len(species_list):
                time.sleep(delay)
                
        except Exception as e:
            print(f"Error processing batch: {e}")
            # Add empty results for failed batch
            for species in batch:
                all_results[species] = []
    
    return all_results

# Example usage
large_species_list = [f"Species_{i}" for i in range(50)]  # Mock large list
results = batch_ncbi_lookup(large_species_list)
```

## Error Handling

### Common Errors and Solutions

```python
from pytaxize import Ids, scicomm

def robust_ncbi_query(species):
    """Robust NCBI querying with error handling"""
    
    result = {
        'species': species,
        'success': False,
        'data': None,
        'error': None
    }
    
    try:
        # Check if API key is set
        import os
        if not os.environ.get('ENTREZ_KEY'):
            result['error'] = 'ENTREZ_KEY not set'
            return result
        
        # Try to get NCBI ID
        ids_obj = Ids(species)
        ids_obj.ncbi()
        
        matches = ids_obj.ids.get(species, [])
        
        if not matches:
            result['error'] = 'No NCBI matches found'
            return result
        
        # Get additional data
        best_match = matches[0]
        
        # Try common names
        try:
            common = scicomm.sci2comm(species, db='ncbi')
            common_names = common.get(species, [])
        except Exception:
            common_names = []
        
        result['success'] = True
        result['data'] = {
            'ncbi_id': best_match['id'],
            'name': best_match['name'],
            'rank': best_match.get('rank'),
            'common_names': common_names,
            'total_matches': len(matches)
        }
        
    except Exception as e:
        result['error'] = str(e)
    
    return result

# Test error handling
test_species = ['Homo sapiens', 'Invalid species', 'Escherichia coli']

for species in test_species:
    result = robust_ncbi_query(species)
    print(f"\n{species}:")
    if result['success']:
        print(f"  Success: {result['data']}")
    else:
        print(f"  Error: {result['error']}")
```

## Integration with Other Services

### NCBI + ITIS Comparison

```python
from pytaxize import Ids

def ncbi_itis_integration(species_list):
    """Compare NCBI and ITIS data for species"""
    
    comparison = {}
    
    for species in species_list:
        # Get NCBI data
        ncbi_obj = Ids(species)
        ncbi_obj.ncbi()
        ncbi_results = ncbi_obj.ids.get(species, [])
        
        # Get ITIS data
        itis_obj = Ids(species)
        itis_obj.itis()
        itis_results = itis_obj.ids.get(species, [])
        
        comparison[species] = {
            'ncbi': {
                'found': bool(ncbi_results),
                'count': len(ncbi_results),
                'ids': [r['id'] for r in ncbi_results]
            },
            'itis': {
                'found': bool(itis_results),
                'count': len(itis_results),
                'ids': [r['id'] for r in itis_results]
            }
        }
    
    return comparison

# Example comparison
species = ['Homo sapiens', 'Quercus alba', 'Escherichia coli']
comparison = ncbi_itis_integration(species)

for species, data in comparison.items():
    print(f"\n{species}:")
    print(f"  NCBI: {data['ncbi']['count']} matches")
    print(f"  ITIS: {data['itis']['count']} matches")
```

## Notes and Limitations

1. **API Key Required**: Essential for reliable access
2. **Rate Limits**: Must respect API rate limits
3. **Network Dependency**: Requires internet connection
4. **Coverage Bias**: Best for organisms with genetic data
5. **Name Changes**: Taxonomy updates may change IDs

## Related Functions

- [`Ids.ncbi()`](ids.md#ncbi): Get NCBI taxonomy IDs
- [`scicomm.sci2comm()`](scicomm.md): Get common names from NCBI
- [ITIS module](itis.md): Alternative taxonomic database
- [Global Names](gn.md): Cross-database name resolution