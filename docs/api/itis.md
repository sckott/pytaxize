# ITIS (Integrated Taxonomic Information System)

The `itis` module provides access to ITIS Web Services for retrieving taxonomic information from the Integrated Taxonomic Information System.

::: pytaxize.itis

## Overview

ITIS is a partnership of federal agencies and other organizations to provide authoritative taxonomic information on plants, animals, fungi, and microbes of North America and the world.

## Functions

### accepted_names

::: pytaxize.itis.accepted_names

Get accepted taxonomic names for a given Taxonomic Serial Number (TSN).

**Parameters:**
- `tsn` (int): Taxonomic Serial Number

**Returns:**
- List of dictionaries containing accepted name information

**Examples:**

```python
from pytaxize import itis

# Get accepted names for a TSN
accepted = itis.accepted_names(tsn=183671)
print(accepted)
```

### common_names

::: pytaxize.itis.common_names

Retrieve common names associated with a TSN.

**Parameters:**
- `tsn` (int): Taxonomic Serial Number

**Returns:**
- List of dictionaries containing common name information

**Examples:**

```python
from pytaxize import itis

# Get common names
common = itis.common_names(tsn=183671)
for name in common:
    print(f"Common name: {name['commonName']}")
    print(f"Language: {name.get('language', 'N/A')}")
```

### hierarchy_full

::: pytaxize.itis.hierarchy_full

Get the full taxonomic hierarchy for a TSN.

**Parameters:**
- `tsn` (int): Taxonomic Serial Number

**Returns:**
- List of dictionaries representing the complete taxonomic hierarchy

**Examples:**

```python
from pytaxize import itis

# Get full hierarchy
hierarchy = itis.hierarchy_full(tsn=183671)
for rank in hierarchy:
    print(f"{rank['rankName']}: {rank['taxonName']}")
```

### hierarchy_up

::: pytaxize.itis.hierarchy_up

Get the taxonomic hierarchy above a given TSN.

**Parameters:**
- `tsn` (int): Taxonomic Serial Number

**Returns:**
- List of dictionaries representing parent taxa

**Examples:**

```python
from pytaxize import itis

# Get hierarchy above
parents = itis.hierarchy_up(tsn=183671)
for parent in parents:
    print(f"{parent['rankName']}: {parent['taxonName']}")
```

### hierarchy_down

::: pytaxize.itis.hierarchy_down

Get the taxonomic hierarchy below a given TSN.

**Parameters:**
- `tsn` (int): Taxonomic Serial Number

**Returns:**
- List of dictionaries representing child taxa

**Examples:**

```python
from pytaxize import itis

# Get hierarchy below
children = itis.hierarchy_down(tsn=180543)
for child in children:
    print(f"{child['rankName']}: {child['taxonName']}")
```

### full_record

::: pytaxize.itis.full_record

Get the complete taxonomic record for a TSN.

**Parameters:**
- `tsn` (int): Taxonomic Serial Number

**Returns:**
- Dictionary containing complete record information

**Examples:**

```python
from pytaxize import itis

# Get full record
record = itis.full_record(tsn=183671)
print(f"Scientific name: {record['scientificName']['combinedName']}")
print(f"Author: {record['scientificName'].get('authorship', 'N/A')}")
print(f"Rank: {record['taxRank']['rankName']}")
```

### any_match_count

::: pytaxize.itis.any_match_count

Get the number of matches for a search term.

**Parameters:**
- `x` (str): Search term

**Returns:**
- Integer count of matches

**Examples:**

```python
from pytaxize import itis

# Count matches
count = itis.any_match_count("Quercus")
print(f"Found {count} matches for Quercus")
```

### comment_detail

::: pytaxize.itis.comment_detail

Get comment details for a TSN.

**Parameters:**
- `tsn` (int): Taxonomic Serial Number

**Returns:**
- List of comment dictionaries

### core_metadata

::: pytaxize.itis.core_metadata

Get core metadata for a TSN.

**Parameters:**
- `tsn` (int): Taxonomic Serial Number

**Returns:**
- Dictionary containing core metadata

### coverage

::: pytaxize.itis.coverage

Get coverage information.

**Returns:**
- Dictionary containing coverage information

### credibility_rating

::: pytaxize.itis.credibility_rating

Get credibility rating for a TSN.

**Parameters:**
- `tsn` (int): Taxonomic Serial Number

**Returns:**
- Dictionary containing credibility information

### credibility_ratings

::: pytaxize.itis.credibility_ratings

Get all credibility ratings.

**Returns:**
- List of all possible credibility ratings

### currency

::: pytaxize.itis.currency

Get currency information for a TSN.

**Parameters:**
- `tsn` (int): Taxonomic Serial Number

**Returns:**
- Dictionary containing currency information

### date_data

::: pytaxize.itis.date_data

Get date information for a TSN.

**Parameters:**
- `tsn` (int): Taxonomic Serial Number

**Returns:**
- Dictionary containing date information

### experts

::: pytaxize.itis.experts

Get expert information for a TSN.

**Parameters:**
- `tsn` (int): Taxonomic Serial Number

**Returns:**
- List of expert dictionaries

### geographic_divisions

::: pytaxize.itis.geographic_divisions

Get geographic divisions.

**Returns:**
- List of geographic divisions

### geographic_values

::: pytaxize.itis.geographic_values

Get geographic values for a TSN.

**Parameters:**
- `tsn` (int): Taxonomic Serial Number

**Returns:**
- List of geographic value dictionaries

### global_species_completeness

::: pytaxize.itis.global_species_completeness

Get global species completeness information for a TSN.

**Parameters:**
- `tsn` (int): Taxonomic Serial Number

**Returns:**
- Dictionary containing completeness information

### jurisdiction_origin_values

::: pytaxize.itis.jurisdiction_origin_values

Get jurisdiction origin values.

**Returns:**
- List of jurisdiction origin values

### jurisdiction_values

::: pytaxize.itis.jurisdiction_values

Get jurisdiction values.

**Returns:**
- List of jurisdiction values

### jurisdictional_origin

::: pytaxize.itis.jurisdictional_origin

Get jurisdictional origin for a TSN.

**Parameters:**
- `tsn` (int): Taxonomic Serial Number

**Returns:**
- Dictionary containing jurisdictional origin information

### rank_name

::: pytaxize.itis.rank_name

Get rank name information for a TSN.

**Parameters:**
- `tsn` (int): Taxonomic Serial Number

**Returns:**
- Dictionary containing rank information

### terms

::: pytaxize.itis.terms

Get terms of use and other service information.

**Returns:**
- Dictionary containing terms and service information

## Usage Examples

### Basic Taxonomic Information

```python
from pytaxize import itis

# Start with a TSN (Taxonomic Serial Number)
tsn = 183671  # Quercus alba (white oak)

# Get basic information
record = itis.full_record(tsn)
print(f"Scientific name: {record['scientificName']['combinedName']}")

# Get common names
common = itis.common_names(tsn)
if common and common[0]:
    for name in common:
        print(f"Common name: {name['commonName']}")

# Get accepted names (in case this is a synonym)
accepted = itis.accepted_names(tsn)
if accepted:
    print(f"Accepted name: {accepted[0]['acceptedName']}")
```

### Taxonomic Hierarchy

```python
from pytaxize import itis

tsn = 183671  # Quercus alba

# Get complete hierarchy
hierarchy = itis.hierarchy_full(tsn)
print("Complete taxonomic hierarchy:")
for rank in hierarchy:
    print(f"  {rank['rankName']}: {rank['taxonName']}")

# Get just the parent taxa
parents = itis.hierarchy_up(tsn)
print("\nParent taxa:")
for parent in parents:
    print(f"  {parent['rankName']}: {parent['taxonName']}")

# Get child taxa (if any)
children = itis.hierarchy_down(tsn)
if children:
    print("\nChild taxa:")
    for child in children:
        print(f"  {child['rankName']}: {child['taxonName']}")
```

### Search and Metadata

```python
from pytaxize import itis

# Count how many entries match a search
oak_count = itis.any_match_count("Quercus")
print(f"Found {oak_count} matches for 'Quercus'")

# Get metadata about a record
tsn = 183671
metadata = itis.core_metadata(tsn)
print(f"Record created: {metadata.get('create_date', 'Unknown')}")
print(f"Last updated: {metadata.get('update_date', 'Unknown')}")

# Check credibility
credibility = itis.credibility_rating(tsn)
if credibility:
    print(f"Credibility rating: {credibility.get('rating', 'Unknown')}")
```

### Geographic Information

```python
from pytaxize import itis

tsn = 183671

# Get geographic distribution
geo_values = itis.geographic_values(tsn)
if geo_values:
    print("Geographic distribution:")
    for geo in geo_values:
        print(f"  {geo.get('geographicValue', 'Unknown')}")

# Get jurisdictional information
jurisdiction = itis.jurisdictional_origin(tsn)
if jurisdiction:
    print(f"Jurisdiction: {jurisdiction.get('jurisdiction', 'Unknown')}")
    print(f"Origin: {jurisdiction.get('origin', 'Unknown')}")
```

## Data Structure

ITIS functions typically return dictionaries or lists of dictionaries with the following common fields:

### Full Record Structure
```python
{
    'scientificName': {
        'combinedName': 'Quercus alba',
        'authorship': 'L.',
        'kingdom': 'Plantae',
        # ... more fields
    },
    'taxRank': {
        'rankId': 220,
        'rankName': 'Species',
        'directionId': 1
    },
    # ... additional metadata
}
```

### Hierarchy Structure
```python
[
    {
        'tsn': '202422',
        'taxonName': 'Plantae',
        'rankName': 'Kingdom',
        'parentTsn': '0'
    },
    {
        'tsn': '846494',
        'taxonName': 'Viridiplantae',
        'rankName': 'Subkingdom', 
        'parentTsn': '202422'
    },
    # ... continues up to species
]
```

## Error Handling

```python
from pytaxize import itis

# Handle invalid TSNs
try:
    record = itis.full_record(tsn=999999)  # Invalid TSN
    if not record:
        print("No record found for this TSN")
except Exception as e:
    print(f"Error: {e}")

# Check for empty results
common = itis.common_names(tsn=183671)
if common and common[0]:  # ITIS may return [None] for no results
    for name in common:
        print(name['commonName'])
else:
    print("No common names found")
```

## API Information

- **Base URL**: `https://itis.gov/ITISWebService/`
- **Format**: SOAP/XML responses converted to Python dictionaries
- **Rate Limits**: No explicit limits, but please be respectful
- **Authentication**: None required
- **Coverage**: Primarily North American taxa, expanding globally

## Notes

1. **TSN Format**: TSNs are integers, typically 6 digits
2. **Empty Results**: Many functions return `[None]` when no data is found
3. **Hierarchies**: ITIS uses a tree structure with parent-child relationships
4. **Updates**: ITIS data is regularly updated and reviewed
5. **Scope**: Strong coverage for North American species

## Best Practices

1. **Check for None**: Always verify results aren't None or empty
2. **Use TSNs**: More reliable than name-based searches
3. **Handle synonyms**: Use `accepted_names()` to get current names
4. **Validate hierarchy**: Check parent-child relationships make sense
5. **Cache results**: Avoid repeated calls for the same TSN

## Related Functions

- [`Ids.itis()`](ids.md#itis): Get TSNs from species names
- [`Classification.itis()`](classification.md): Get classifications using ITIS
- [`Children.itis()`](children.md): Get taxonomic children using ITIS