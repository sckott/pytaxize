# Taxonomic Classification

The `Classification` class provides functionality to retrieve complete taxonomic hierarchies (classifications) for given taxonomic identifiers from ITIS and NCBI databases.

## Overview

The `Classification` class allows you to get the complete taxonomic hierarchy for a given taxon, from kingdom down to the specified taxon level. This is useful for understanding the full taxonomic context of a species or higher taxon.

## Class Methods

### Constructor

```python
from pytaxize import Classification

# Single ID
classification_obj = Classification(99208)

# Multiple IDs
classification_obj = Classification([99208, 180543])
```

### Database Methods

#### itis()

Get taxonomic classification from ITIS (Integrated Taxonomic Information System).

**Examples:**

```python
from pytaxize import Classification

# Single TSN
classification_obj = Classification(99208)
result = classification_obj.itis()
print(result)

# Multiple TSNs
classification_obj = Classification([99208, 180543])
result = classification_obj.itis()
print(result)
```

#### ncbi()

Get taxonomic classification from NCBI Taxonomy database.

**Examples:**

```python
from pytaxize import Classification

classification_obj = Classification(9606)  # Homo sapiens
result = classification_obj.ncbi()
print(result)
```

## Properties

### ids

Get the original input IDs.

**Returns:**
- List of taxonomic IDs that were queried

## Usage Examples

### Basic Usage

```python
from pytaxize import Classification

# Get classification for a species (ITIS TSN for Quercus alba)
species_class = Classification(99208)
result = species_class.itis()

print("Classification for Quercus alba:")
for taxon_id, hierarchy in result.items():
    print(f"Taxon ID: {taxon_id}")
    if hierarchy:
        for rank in hierarchy:
            if isinstance(rank, dict):
                print(f"  {rank.get('rankName', 'Unknown')}: {rank.get('taxonName', 'Unknown')}")
```

### Multiple Taxa

```python
from pytaxize import Classification

# Get classifications for multiple species
species_ids = [99208, 183671]  # Multiple oak species
species = Classification(species_ids)
result = species.itis()

for taxon_id, hierarchy in result.items():
    if hierarchy:
        print(f"\nClassification for ID {taxon_id}:")
        for rank in hierarchy:
            if isinstance(rank, dict):
                print(f"  {rank.get('rankName', 'Unknown')}: {rank.get('taxonName', 'Unknown')}")
```

### Extracting Specific Ranks

```python
from pytaxize import Classification

def get_rank_from_classification(classification_list, target_rank):
    """Extract a specific rank from a classification"""
    for rank_info in classification_list:
        if isinstance(rank_info, dict):
            rank_name = rank_info.get('rankName', '').lower()
            if rank_name == target_rank.lower():
                return rank_info.get('taxonName')
    return None

# Get classification
oak_class = Classification(99208)
result = oak_class.itis()

# Extract specific ranks
hierarchy = result.get(99208, [])
kingdom = get_rank_from_classification(hierarchy, 'Kingdom')
family = get_rank_from_classification(hierarchy, 'Family')
genus = get_rank_from_classification(hierarchy, 'Genus')

print(f"Kingdom: {kingdom}")
print(f"Family: {family}")
print(f"Genus: {genus}")
```

### Building Taxonomic Summaries

```python
from pytaxize import Classification

def summarize_classification(taxon_id, database='itis'):
    """Create a summary of taxonomic classification"""
    classification_obj = Classification(taxon_id)
    
    if database == 'itis':
        result = classification_obj.itis()
    elif database == 'ncbi':
        result = classification_obj.ncbi()
    else:
        raise ValueError("Database must be 'itis' or 'ncbi'")
    
    hierarchy = result.get(taxon_id, [])
    
    if not hierarchy:
        return {"error": f"No classification found for ID {taxon_id}"}
    
    summary = {}
    for rank_info in hierarchy:
        if isinstance(rank_info, dict):
            rank = rank_info.get('rankName', 'Unknown')
            name = rank_info.get('taxonName', 'Unknown')
            summary[rank] = name
    
    return summary

# Get summary
oak_summary = summarize_classification(99208)
print("Oak classification summary:")
for rank, name in oak_summary.items():
    print(f"  {rank}: {name}")
```

### Comparing Classifications Across Databases

```python
from pytaxize import Classification

def compare_classifications(itis_id, ncbi_id):
    """Compare classifications from ITIS and NCBI"""
    
    # ITIS classification
    itis_class = Classification(itis_id)
    itis_result = itis_class.itis()
    itis_hierarchy = itis_result.get(itis_id, [])
    
    # NCBI classification (requires taxonomy ID)
    ncbi_class = Classification(ncbi_id)
    ncbi_result = ncbi_class.ncbi()
    ncbi_hierarchy = ncbi_result.get(ncbi_id, [])
    
    print("ITIS Classification:")
    for rank in itis_hierarchy:
        if isinstance(rank, dict):
            print(f"  {rank.get('rankName', 'Unknown')}: {rank.get('taxonName', 'Unknown')}")
    
    print("\nNCBI Classification:")
    for rank in ncbi_hierarchy:
        if isinstance(rank, dict):
            print(f"  {rank.get('rankName', 'Unknown')}: {rank.get('taxonName', 'Unknown')}")

# Compare human classifications (example IDs)
compare_classifications(180092, 9606)  # ITIS and NCBI IDs for Homo sapiens
```

## Data Structure

The classification methods return a dictionary with the following structure:

```python
{
    taxon_id_1: [
        {
            'tsn': 'parent_id_1',
            'taxonName': 'Kingdom Name',
            'rankName': 'Kingdom',
            'parentTsn': '0'
        },
        {
            'tsn': 'parent_id_2',
            'taxonName': 'Phylum Name', 
            'rankName': 'Phylum',
            'parentTsn': 'parent_id_1'
        },
        # ... continues down to the target taxon
        {
            'tsn': 'taxon_id_1',
            'taxonName': 'Species Name',
            'rankName': 'Species',
            'parentTsn': 'genus_id'
        }
    ],
    taxon_id_2: [
        # ... classification for second taxon
    ]
}
```

## Database-Specific Information

### ITIS (Integrated Taxonomic Information System)
- **ID Format**: Taxonomic Serial Number (TSN) - integers
- **Coverage**: Primarily North American species
- **Hierarchy**: Kingdom → Phylum → Class → Order → Family → Genus → Species
- **API**: ITIS Web Services

### NCBI Taxonomy
- **ID Format**: Taxonomy ID (TaxID) - integers
- **Coverage**: All domains of life with genetic data
- **Hierarchy**: Based on phylogenetic relationships
- **Requirements**: ENTREZ_KEY recommended for better rate limits

## Working with Hierarchies

### Finding Common Ancestors

```python
from pytaxize import Classification

def find_common_ancestor(id1, id2, database='itis'):
    """Find the lowest common ancestor of two taxa"""
    
    # Get classifications
    class1 = Classification(id1)
    class2 = Classification(id2)
    
    if database == 'itis':
        result1 = class1.itis()
        result2 = class2.itis()
    elif database == 'ncbi':
        result1 = class1.ncbi()
        result2 = class2.ncbi()
    
    hierarchy1 = result1.get(id1, [])
    hierarchy2 = result2.get(id2, [])
    
    # Create lookup for first hierarchy
    h1_ranks = {}
    for rank in hierarchy1:
        if isinstance(rank, dict):
            h1_ranks[rank.get('rankName')] = rank.get('taxonName')
    
    # Find common ranks
    for rank in reversed(hierarchy2):  # Start from highest rank
        if isinstance(rank, dict):
            rank_name = rank.get('rankName')
            rank_taxon = rank.get('taxonName')
            if rank_name in h1_ranks and h1_ranks[rank_name] == rank_taxon:
                return {
                    'rank': rank_name,
                    'name': rank_taxon,
                    'id': rank.get('tsn')
                }
    
    return None

# Find common ancestor of two oak species
common = find_common_ancestor(99208, 183671)
if common:
    print(f"Common ancestor: {common['name']} ({common['rank']})")
```

## Error Handling

```python
from pytaxize import Classification
import warnings

def safe_get_classification(taxon_id, database='itis'):
    """Safely get classification with error handling"""
    try:
        classification_obj = Classification(taxon_id)
        
        if database == 'itis':
            result = classification_obj.itis()
        elif database == 'ncbi':
            result = classification_obj.ncbi()
        else:
            raise ValueError(f"Unsupported database: {database}")
        
        hierarchy = result.get(taxon_id, [])
        
        if not hierarchy:
            return {"warning": f"No classification found for ID {taxon_id}"}
        
        # Filter out None values
        valid_hierarchy = [rank for rank in hierarchy if rank is not None]
        
        return {"success": True, "ranks": len(valid_hierarchy), "classification": valid_hierarchy}
        
    except Exception as e:
        return {"error": f"Failed to get classification: {str(e)}"}

# Use the safe function
result = safe_get_classification(99208)
if "error" in result:
    print(f"Error: {result['error']}")
elif "warning" in result:
    print(f"Warning: {result['warning']}")
else:
    print(f"Found classification with {result['ranks']} ranks")
```

## Notes and Limitations

1. **Complete Hierarchies**: Returns full hierarchy from kingdom to target taxon
2. **Database Consistency**: Different databases may have different hierarchies
3. **ID Requirements**: Must use database-specific IDs
4. **Rank Variations**: Some databases use different rank names
5. **Historical Changes**: Taxonomic classifications change over time
6. **Warning System**: Invalid IDs will generate warnings

## Best Practices

1. **Validate IDs**: Ensure IDs are valid for the chosen database
2. **Handle Empty Results**: Not all IDs may have complete classifications
3. **Check Hierarchy Order**: Results are typically ordered from highest to lowest rank
4. **Use Appropriate Database**: Choose based on your taxonomic needs
5. **Set API Keys**: For NCBI, improves rate limits and reliability

## Integration Examples

### With Ids Class

```python
from pytaxize import Ids, Classification

# First get IDs for species names
species_names = ["Quercus alba", "Pinus contorta"]
ids_obj = Ids(species_names)
ids_obj.itis()

# Then get classifications
for name, id_list in ids_obj.ids.items():
    if id_list and id_list[0]['id']:
        species_id = int(id_list[0]['id'])  # Use first match
        classification_obj = Classification(species_id)
        result = classification_obj.itis()
        
        print(f"\nClassification for {name}:")
        hierarchy = result.get(species_id, [])
        for rank in hierarchy:
            if isinstance(rank, dict):
                print(f"  {rank.get('rankName', 'Unknown')}: {rank.get('taxonName', 'Unknown')}")
```

### With Children Class

```python
from pytaxize import Classification, Children

def get_taxonomic_context(taxon_id):
    """Get both classification and children for context"""
    
    # Get classification (parents)
    classification = Classification(taxon_id)
    class_result = classification.itis()
    
    # Get children
    children = Children(taxon_id)
    children_result = children.itis()
    
    return {
        'classification': class_result,
        'children': children_result
    }

context = get_taxonomic_context(180539)  # Felidae family
print("Taxonomic context:", context)
```

## Related Functions

- [`Ids`](ids.md): Get taxonomic IDs from names
- [`Children`](children.md): Get immediate taxonomic children
- [`itis`](itis.md): Direct ITIS database functions including hierarchy functions
- [`col`](col.md): Alternative source for taxonomic classifications