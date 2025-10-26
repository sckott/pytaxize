# Taxonomic Children

The `Children` class provides functionality to retrieve direct taxonomic children (subordinate taxa) for given taxonomic identifiers from ITIS.

::: pytaxize.children.Children

## Overview

The `Children` class allows you to get immediate taxonomic children for a given taxon from ITIS. For example, if you provide a family ID, you'll get back all genera within that family. If you provide a genus ID, you'll get back all species within that genus.

## Class Methods

### Constructor

```python
from pytaxize import Children

# Single ID
children_obj = Children(179913)

# Multiple IDs
children_obj = Children([179913, 180543])
```

### Database Methods

#### itis()

::: pytaxize.children.Children.itis

Get taxonomic children from ITIS (Integrated Taxonomic Information System).

**Examples:**

```python
from pytaxize import Children

# Single TSN
children_obj = Children(179913)
result = children_obj.itis()
print(result)

# Multiple TSNs
children_obj = Children([179913, 180543])
result = children_obj.itis()
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
from pytaxize import Children

# Get children for a family (ITIS TSN for Felidae)
family_children = Children(180539)
result = family_children.itis()

print("Children of Felidae:")
children_list = result.get(180539, [])
for child in children_list:
    if isinstance(child, dict):
        print(f"  {child.get('taxonName', 'Unknown')}: {child.get('tsn', 'No TSN')}")
```

### Multiple Parents

```python
from pytaxize import Children

# Get children for multiple families
family_ids = [180539, 180540]  # Felidae and Canidae
families = Children(family_ids)
result = families.itis()

for parent_id, children_list in result.items():
    print(f"\nChildren of parent {parent_id}:")
    if children_list:
        for child in children_list:
            if isinstance(child, dict):
                print(f"  {child.get('taxonName', 'Unknown')} ({child.get('rankName', 'Unknown rank')})")
    else:
        print("  No children found")
```

### Building Taxonomic Trees

```python
from pytaxize import Children

def build_subtree(parent_id, max_depth=2, current_depth=0):
    """Recursively build a taxonomic subtree"""
    if current_depth >= max_depth:
        return {}
    
    children_obj = Children(parent_id)
    result = children_obj.itis()
    
    subtree = {}
    parent_children = result.get(parent_id, [])
    
    if parent_children:
        for child in parent_children:
            if isinstance(child, dict):
                child_id = child.get('tsn')
                child_name = child.get('taxonName')
                child_rank = child.get('rankName')
                
                if child_id and child_name:
                    subtree[child_name] = {
                        'id': child_id,
                        'rank': child_rank,
                        'children': build_subtree(child_id, max_depth, current_depth + 1)
                    }
    
    return subtree

# Build a tree starting from a family
carnivora_tree = build_subtree(180539, max_depth=2)
print("Family subtree:", carnivora_tree)
```

### Filtering Children by Rank

```python
from pytaxize import Children

def get_children_by_rank(parent_id, target_rank="genus"):
    """Get only children of a specific taxonomic rank"""
    children_obj = Children(parent_id)
    result = children_obj.itis()
    
    filtered_children = []
    all_children = result.get(parent_id, [])
    
    if all_children:
        for child in all_children:
            if isinstance(child, dict):
                child_rank = child.get('rankName', '').lower()
                if child_rank == target_rank.lower():
                    filtered_children.append(child)
    
    return filtered_children

# Get only genera within Felidae
felidae_genera = get_children_by_rank(180539, "genus")
print("Genera in Felidae:")
for genus in felidae_genera:
    print(f"  {genus.get('taxonName', 'Unknown')}")
```

## Data Structure

The `itis()` method returns a dictionary with the following structure:

```python
{
    parent_id_1: [
        {
            'tsn': 'child_id_1',
            'taxonName': 'Child Taxon Name',
            'rankName': 'Genus',
            'parentTsn': 'parent_id_1'
        },
        {
            'tsn': 'child_id_2', 
            'taxonName': 'Another Child',
            'rankName': 'Genus',
            'parentTsn': 'parent_id_1'
        }
    ],
    parent_id_2: [
        # ... children of second parent
    ]
}
```

## Error Handling

```python
from pytaxize import Children
import warnings

def safe_get_children(parent_id):
    """Safely get children with error handling"""
    try:
        children_obj = Children(parent_id)
        result = children_obj.itis()
        
        children_list = result.get(parent_id, [])
        
        if not children_list:
            return {"warning": f"No children found for ID {parent_id}"}
        
        # Filter out None results
        valid_children = [child for child in children_list if child is not None]
        
        return {"success": True, "count": len(valid_children), "children": valid_children}
        
    except Exception as e:
        return {"error": f"Failed to get children: {str(e)}"}

# Test error handling
result = safe_get_children(180539)
if "error" in result:
    print(f"Error: {result['error']}")
elif "warning" in result:
    print(f"Warning: {result['warning']}")
else:
    print(f"Found {result['count']} children")
```

## Notes and Limitations

1. **ITIS Only**: Currently only supports ITIS database
2. **Direct Children Only**: Returns immediate children, not all descendants
3. **Warning System**: Uses Python warnings for invalid IDs
4. **Return Format**: Returns dictionaries with TSN as keys
5. **Hierarchical Completeness**: Not all taxa have children in ITIS

## Best Practices

1. **Check for Empty Results**: Not all taxa have children
2. **Handle Warnings**: Invalid IDs will generate warnings
3. **Validate Results**: Check that results are not None
4. **Use Valid TSNs**: Ensure TSNs are valid ITIS identifiers
5. **Consider Recursion**: For building complete taxonomic trees

## Integration Examples

### With Ids Class

```python
from pytaxize import Ids, Children

# First get IDs for family names
family_names = ["Felidae", "Canidae"]
ids_obj = Ids(family_names)
ids_obj.itis()

# Then get children for each family
for name, id_list in ids_obj.ids.items():
    if id_list:
        family_id = int(id_list[0]['id'])  # Use first match
        children_obj = Children(family_id)
        result = children_obj.itis()
        
        print(f"\nChildren of {name}:")
        children_list = result.get(family_id, [])
        for child in children_list:
            if child and isinstance(child, dict):
                print(f"  {child.get('taxonName', 'Unknown')}")
```

### With Classification

```python
from pytaxize import Children, Classification

def get_family_overview(family_id):
    """Get both classification and children for a family"""
    # Get the classification
    classification = Classification(family_id)
    class_result = classification.itis()
    
    # Get the children
    children = Children(family_id)
    children_result = children.itis()
    
    return {
        'classification': class_result,
        'children': children_result
    }

overview = get_family_overview(180539)  # Felidae
print("Family overview:", overview)
```

## Related Functions

- [`Ids`](ids.md): Get taxonomic IDs from names
- [`Classification`](classification.md): Get complete taxonomic hierarchy
- [`itis`](itis.md): Direct ITIS database functions including `hierarchy_down`
- [`col`](col.md): Alternative source for taxonomic children