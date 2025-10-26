# Utilities

The `utils` module provides utility functions used throughout the pytaxize package for data manipulation and validation.

::: pytaxize.utils

## Overview

The utilities module contains helper functions that support the main functionality of pytaxize. These functions handle common tasks like data validation, type conversion, and list manipulation.

## Functions

### assert_range_numeric

::: pytaxize.utils.assert_range_numeric

Validate that a numeric value falls within a specified range.

**Parameters:**
- `x` (int or None): Value to validate
- `start` (int): Minimum allowed value (inclusive)
- `stop` (int): Maximum allowed value (exclusive)

**Raises:**
- `ValueError`: If value is outside the specified range

**Examples:**

```python
from pytaxize.utils import assert_range_numeric

# Valid range
assert_range_numeric(5, 1, 10)  # No error

# Invalid range
try:
    assert_range_numeric(15, 1, 10)
except ValueError as e:
    print(f"Error: {e}")  # Error: value must be between 1 and 10
```

### str2list

::: pytaxize.utils.str2list

Convert a string to a list, or validate that input is already a list.

**Parameters:**
- `x` (str or list): Input to convert or validate

**Returns:**
- `list`: The input as a list

**Raises:**
- `TypeError`: If input is neither string nor list

**Examples:**

```python
from pytaxize.utils import str2list

# Convert string to list
result = str2list("Homo sapiens")
print(result)  # ['Homo sapiens']

# List remains unchanged
result = str2list(["Homo sapiens", "Quercus alba"])
print(result)  # ['Homo sapiens', 'Quercus alba']

# Error for invalid type
try:
    str2list(123)
except TypeError as e:
    print(f"Error: {e}")
```

### flatten

::: pytaxize.utils.flatten

Flatten a nested list structure into a single list.

**Parameters:**
- `a_list` (list): List of lists to flatten

**Returns:**
- `list`: Flattened list

**Examples:**

```python
from pytaxize.utils import flatten

# Flatten nested lists
nested = [['a', 'b'], ['c', 'd'], ['e']]
result = flatten(nested)
print(result)  # ['a', 'b', 'c', 'd', 'e']

# Works with mixed types
mixed = [[1, 2], ['a', 'b'], [3.14]]
result = flatten(mixed)
print(result)  # [1, 2, 'a', 'b', 3.14]
```

### lists2dict

::: pytaxize.utils.lists2dict

Create a dictionary from two lists (keys and values).

**Parameters:**
- `vals` (list): List of values
- `names` (list): List of keys

**Returns:**
- `dict`: Dictionary created from the two lists

**Raises:**
- `TypeError`: If either parameter is not a list

**Examples:**

```python
from pytaxize.utils import lists2dict

# Create dictionary from two lists
species = ["Homo sapiens", "Quercus alba"]
common = ["Human", "White oak"]
result = lists2dict(species, common)
print(result)  # {"Human": "Homo sapiens", "White oak": "Quercus alba"}

# Error handling
try:
    lists2dict("not a list", ["a", "b"])
except TypeError as e:
    print(f"Error: {e}")
```

## Usage Examples

### Data Validation Pipeline

```python
from pytaxize.utils import assert_range_numeric, str2list

def validate_query_parameters(names, page_size=50, max_names=1000):
    """Validate parameters for a taxonomic query"""
    
    # Ensure names is a list
    name_list = str2list(names)
    
    # Validate page size
    assert_range_numeric(page_size, 1, 101)  # 1-100 allowed
    
    # Check total number of names
    if len(name_list) > max_names:
        raise ValueError(f"Too many names: {len(name_list)} (max: {max_names})")
    
    return {
        'names': name_list,
        'page_size': page_size,
        'count': len(name_list)
    }

# Example usage
try:
    params = validate_query_parameters("Homo sapiens", page_size=25)
    print(f"Valid parameters: {params}")
    
    # This will raise an error
    params = validate_query_parameters("Species", page_size=150)
except (ValueError, TypeError) as e:
    print(f"Validation error: {e}")
```

### Data Processing Pipeline

```python
from pytaxize.utils import flatten, lists2dict

def process_taxonomic_results(nested_results, species_names):
    """Process nested API results into a clean format"""
    
    # Flatten nested results
    flat_results = flatten(nested_results)
    
    # Create species-to-result mapping
    if len(flat_results) == len(species_names):
        species_dict = lists2dict(flat_results, species_names)
        return species_dict
    else:
        # Handle mismatched lengths
        print(f"Warning: {len(flat_results)} results for {len(species_names)} species")
        return dict(zip(species_names, flat_results))

# Example usage
api_results = [
    [{'id': 1, 'name': 'Homo sapiens'}],
    [{'id': 2, 'name': 'Quercus alba'}],
    [{'id': 3, 'name': 'Pinus strobus'}]
]

species_list = ['Human', 'White oak', 'White pine']
processed = process_taxonomic_results(api_results, species_list)
print(processed)
```

### Configuration Validation

```python
from pytaxize.utils import assert_range_numeric, str2list

class TaxizeConfig:
    """Configuration class with validation"""
    
    def __init__(self, timeout=30, max_results=100, databases=None):
        # Validate timeout
        assert_range_numeric(timeout, 1, 301)  # 1-300 seconds
        self.timeout = timeout
        
        # Validate max results
        assert_range_numeric(max_results, 1, 1001)  # 1-1000 results
        self.max_results = max_results
        
        # Ensure databases is a list
        if databases is None:
            databases = ['itis']
        self.databases = str2list(databases)
    
    def __repr__(self):
        return f"TaxizeConfig(timeout={self.timeout}, max_results={self.max_results}, databases={self.databases})"

# Example usage
try:
    # Valid configuration
    config1 = TaxizeConfig(timeout=60, max_results=500, databases="itis")
    print(config1)
    
    # Multiple databases
    config2 = TaxizeConfig(databases=['itis', 'ncbi', 'gbif'])
    print(config2)
    
    # Invalid configuration
    config3 = TaxizeConfig(timeout=500)  # Will raise ValueError
except (ValueError, TypeError) as e:
    print(f"Configuration error: {e}")
```

## Internal Usage

These utility functions are used throughout pytaxize for:

### Input Validation
- Ensuring parameters are within valid ranges
- Converting single strings to lists for batch processing
- Type checking and conversion

### Data Processing
- Flattening nested API responses
- Creating lookup dictionaries from parallel lists
- Normalizing data structures

### Error Prevention
- Validating user inputs before API calls
- Ensuring consistent data types across modules
- Preventing common programming errors

## Best Practices

### When to Use These Functions

1. **assert_range_numeric**: Use when validating numeric parameters that must fall within specific bounds
2. **str2list**: Use when functions should accept both single items and lists
3. **flatten**: Use when processing nested API responses or hierarchical data
4. **lists2dict**: Use when creating lookup tables or mappings from parallel data

### Error Handling

```python
from pytaxize.utils import str2list, assert_range_numeric

def safe_utility_usage(names, page_size):
    """Example of safe utility function usage"""
    
    try:
        # Convert names to list
        name_list = str2list(names)
        print(f"Processing {len(name_list)} names")
        
        # Validate page size
        assert_range_numeric(page_size, 1, 101)
        print(f"Using page size: {page_size}")
        
        return True
        
    except TypeError as e:
        print(f"Type error: {e}")
        return False
    except ValueError as e:
        print(f"Value error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

# Test error handling
safe_utility_usage("Homo sapiens", 50)     # Valid
safe_utility_usage(["Species 1", "Species 2"], 25)  # Valid  
safe_utility_usage(123, 50)                 # Type error
safe_utility_usage("Species", 200)          # Value error
```

## Performance Notes

- **str2list**: Very fast operation, minimal overhead
- **flatten**: Linear time complexity O(n) where n is total number of elements
- **lists2dict**: Linear time complexity O(n) where n is length of lists
- **assert_range_numeric**: Constant time operation O(1)

These utilities are designed to be lightweight and efficient for use in data processing pipelines.

## Related Functions

- Used internally by [`Ids`](ids.md), [`Classification`](classification.md), and [`Children`](children.md) classes
- Support functions in [`tax`](tax.md) module for data validation
- Error handling in [`scicomm`](scicomm.md) functions