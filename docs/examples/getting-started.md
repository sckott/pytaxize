# Getting Started with pytaxize

This guide will walk you through the basic functionality of pytaxize with practical examples.

## Installation

First, install pytaxize:

```bash
pip install pytaxize
```

For development or to get the latest features:

```bash
pip install git+https://github.com/sckott/pytaxize.git
```

## Setting Up API Keys

Some functions require API keys. Set your NCBI API key as an environment variable:

```bash
export ENTREZ_KEY="your_ncbi_api_key_here"
```

Or in Python:

```python
import os
os.environ['ENTREZ_KEY'] = 'your_ncbi_api_key_here'
```

You can get a free NCBI API key from: https://www.ncbi.nlm.nih.gov/account/

## Basic Usage Examples

### 1. Getting Random Taxonomic Names

Perfect for testing and learning:

```python
from pytaxize import tax

# Get 5 random genus names
genera = tax.names_list(rank='genus', size=5)
print("Random genera:", genera)

# Get species names
species = tax.names_list(rank='species', size=3)
print("Random species:", species)

# Get family names
families = tax.names_list(rank='family', size=4)
print("Random families:", families)
```

### 2. Getting Taxonomic IDs from Names

The `Ids` class is your gateway to taxonomic databases:

```python
from pytaxize import Ids

# Single species
single_species = Ids('Helianthus annuus')  # Sunflower
single_species.itis()
print("ITIS results:", single_species.ids)

# Multiple species
species_list = ['Helianthus annuus', 'Quercus alba', 'Pinus contorta']
multi_species = Ids(species_list)
multi_species.itis()

for species_name, results in multi_species.ids.items():
    print(f"\n{species_name}:")
    for result in results:
        print(f"  ID: {result['id']}")
        print(f"  Name: {result['name']}")
        print(f"  Rank: {result.get('rank', 'Unknown')}")
```

### 3. Converting Scientific Names to Common Names

```python
from pytaxize import scicomm

# Single name
common = scicomm.sci2comm('Helianthus annuus')
print("Common names:", common)

# Multiple names
animals = ['Canis lupus', 'Felis catus', 'Homo sapiens']
common_names = scicomm.sci2comm(animals)

for scientific, common_list in common_names.items():
    if common_list:
        print(f"{scientific}: {', '.join(common_list)}")
    else:
        print(f"{scientific}: No common names found")
```

### 4. Getting Taxonomic Classifications

```python
from pytaxize import Classification

# Get full taxonomic hierarchy
species_class = Classification(99208)  # ITIS TSN for Quercus alba
species_class.itis()

print("Taxonomic classification for Quercus alba:")
hierarchy = species_class.classification['99208']
for rank in hierarchy:
    print(f"  {rank['rankName']}: {rank['taxonName']}")
```

### 5. Finding Taxonomic Children

```python
from pytaxize import Children

# Get genera within a family
family_children = Children(180539)  # ITIS TSN for Felidae
family_children.itis()

print("Genera in Felidae (cat family):")
for child in family_children.children['180539']:
    print(f"  {child['taxonName']} ({child['rankName']})")
```

## Practical Workflows

### Workflow 1: Complete Species Information

```python
from pytaxize import Ids, Classification, scicomm

def get_species_info(species_name):
    """Get comprehensive information about a species"""
    
    print(f"=== Information for {species_name} ===\n")
    
    # Step 1: Get taxonomic IDs
    ids_obj = Ids(species_name)
    ids_obj.itis()
    
    if not ids_obj.ids[species_name]:
        print("No ITIS record found")
        return
    
    # Use the first matching ID
    species_id = ids_obj.ids[species_name][0]['id']
    print(f"ITIS ID: {species_id}")
    
    # Step 2: Get full classification
    classification = Classification(species_id)
    classification.itis()
    
    print("\nTaxonomic Classification:")
    hierarchy = classification.classification[species_id]
    for rank in hierarchy:
        print(f"  {rank['rankName']}: {rank['taxonName']}")
    
    # Step 3: Get common names
    common_names = scicomm.sci2comm(species_name)
    print(f"\nCommon Names: {common_names.get(species_name, ['None found'])}")

# Try it with a few species
species_to_check = ["Quercus alba", "Pinus contorta", "Helianthus annuus"]
for species in species_to_check:
    get_species_info(species)
    print("\n" + "="*50 + "\n")
```

### Workflow 2: Taxonomic Name Resolution

```python
from pytaxize import tax

def resolve_names_from_text(text_content):
    """Extract and resolve taxonomic names from text"""
    
    # Extract names from text
    results = tax.scrapenames(text=text_content)
    
    if not results['data']:
        print("No taxonomic names found in text")
        return
    
    print("Extracted taxonomic names:")
    unique_names = set()
    
    for item in results['data']:
        if 'scientificName' in item:
            name = item['scientificName']
            unique_names.add(name)
            print(f"  - {name}")
    
    return list(unique_names)

# Example text with species names
sample_text = """
The study examined three oak species: Quercus alba (white oak), 
Quercus rubra (red oak), and Quercus velutina (black oak). 
We also observed Pinus strobus and Acer saccharum in the forest.
"""

extracted_names = resolve_names_from_text(sample_text)
```

### Workflow 3: Building a Taxonomic Tree

```python
from pytaxize import Ids, Children, Classification

def build_family_tree(family_name):
    """Build a simple taxonomic tree for a family"""
    
    # Step 1: Get family ID
    family_ids = Ids(family_name)
    family_ids.itis()
    
    if not family_ids.ids[family_name]:
        print(f"Family {family_name} not found")
        return
    
    family_id = family_ids.ids[family_name][0]['id']
    print(f"Family: {family_name} (ID: {family_id})")
    
    # Step 2: Get genera in the family
    genera = Children(family_id)
    genera.itis()
    
    family_genera = genera.children.get(family_id, [])
    print(f"Found {len(family_genera)} genera")
    
    # Step 3: Get species for each genus (limit to first few)
    for genus in family_genera[:3]:  # Limit to first 3 genera
        genus_name = genus['taxonName']
        genus_id = genus['tsn']
        print(f"\n  Genus: {genus_name}")
        
        # Get species in this genus
        species = Children(genus_id)
        species.itis()
        
        genus_species = species.children.get(genus_id, [])
        for sp in genus_species[:5]:  # Limit to 5 species per genus
            print(f"    Species: {sp['taxonName']}")

# Build tree for cat family
build_family_tree("Felidae")
```

## Working with Different Databases

### ITIS vs NCBI Comparison

```python
from pytaxize import Ids, scicomm

def compare_databases(species_name):
    """Compare results from ITIS and NCBI"""
    
    print(f"Comparing databases for: {species_name}")
    
    # ITIS
    itis_ids = Ids(species_name)
    itis_ids.itis()
    print(f"ITIS results: {len(itis_ids.ids[species_name])} matches")
    
    # NCBI (if ENTREZ_KEY is set)
    try:
        ncbi_ids = Ids(species_name)
        ncbi_ids.ncbi()
        print(f"NCBI results: {len(ncbi_ids.ids[species_name])} matches")
        
        # Get common names from NCBI
        ncbi_common = scicomm.sci2comm(species_name, db='ncbi')
        print(f"NCBI common names: {ncbi_common}")
        
    except Exception as e:
        print(f"NCBI error (check ENTREZ_KEY): {e}")
    
    # ITIS common names
    itis_common = scicomm.sci2comm(species_name, db='itis')
    print(f"ITIS common names: {itis_common}")

compare_databases("Homo sapiens")
```

## Error Handling Best Practices

```python
from pytaxize import Ids, scicomm

def safe_species_lookup(species_name):
    """Safely look up species with comprehensive error handling"""
    
    try:
        # Try to get IDs
        ids_obj = Ids(species_name)
        ids_obj.itis()
        
        results = ids_obj.ids.get(species_name, [])
        
        if not results:
            return {
                'status': 'not_found',
                'message': f'No ITIS records found for {species_name}',
                'suggestions': 'Check spelling or try a different database'
            }
        
        # Get the best match
        best_match = results[0]
        
        # Try to get common names
        try:
            common_names = scicomm.sci2comm(species_name, db='itis')
            common = common_names.get(species_name, [])
        except Exception as e:
            common = f"Error getting common names: {e}"
        
        return {
            'status': 'success',
            'itis_id': best_match['id'],
            'matched_name': best_match['name'],
            'rank': best_match.get('rank', 'Unknown'),
            'common_names': common,
            'total_matches': len(results)
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error looking up {species_name}: {str(e)}'
        }

# Test with various inputs
test_species = [
    "Quercus alba",      # Valid species
    "Homo sapiens",      # Well-known species
    "Invalid species",   # Invalid name
    "Quercus"           # Genus name
]

for species in test_species:
    result = safe_species_lookup(species)
    print(f"\n{species}: {result}")
```

## Next Steps

Now that you've learned the basics, you can:

1. **Explore specific databases**: Check out the [ITIS](../api/itis.md), [COL](../api/col.md), and [NCBI](../api/ncbi.md) documentation
2. **Learn advanced workflows**: See [Common Use Cases](common-use-cases.md) for more complex examples
3. **Integrate with your research**: Use pytaxize in your biodiversity or ecological research projects
4. **Contribute**: Help improve pytaxize by reporting issues or contributing code

## Common Issues and Solutions

### Issue: "No results found"
**Solution**: Check spelling, try wildcards, or use a different database

### Issue: "ENTREZ_KEY not set" 
**Solution**: Set your NCBI API key as an environment variable

### Issue: Rate limiting
**Solution**: Add delays between requests or use API keys for higher limits

### Issue: Different results from different databases
**Solution**: This is normal - databases have different coverage and update schedules

Remember that taxonomic databases are constantly evolving, so results may change over time as new research updates classifications.