# Tax Module

The `tax` module provides core taxonomic functions including random name generation, taxonomic name extraction, and search capabilities.

::: pytaxize.tax

## Functions

### names_list

::: pytaxize.tax.names_list

Generate random taxonomic names for testing and examples.

**Parameters:**

- `rank` (str): Taxonomic rank - one of 'species', 'genus', 'family', 'order'. Default: 'genus'
- `size` (int): Number of names to return. Default: 10
- `as_dataframe` (bool): Return as pandas DataFrame. Default: False

**Returns:**

- List of taxonomic names or DataFrame if `as_dataframe=True`

**Examples:**

```python
from pytaxize import tax

# Get 10 random genus names
genera = tax.names_list(size=10)

# Get species names
species = tax.names_list('species', size=5)

# Get as DataFrame
df = tax.names_list('family', size=20, as_dataframe=True)
```

### vascan_search

::: pytaxize.tax.vascan_search

Search the CANADENSYS Vascan API for Canadian plant taxa.

**Parameters:**

- `q` (str or list): Query term(s) - taxonomic names to search for
- `format` (str): Response format - 'json' or 'xml'. Default: 'json'
- `raw` (bool): Return raw response. Default: False

**Returns:**

- Dictionary containing search results or raw response if `raw=True`

**Examples:**

```python
from pytaxize import tax

# Single name search
result = tax.vascan_search(q=["Helianthus annuus"])

# Multiple names
result = tax.vascan_search(q=["Helianthus annuus", "Crataegus dodgei"])

# Raw response
raw_result = tax.vascan_search(q=["Helianthus annuus"], raw=True)

# XML format
xml_result = tax.vascan_search(q=["Helianthus annuus"], format="xml")
```

### scrapenames

::: pytaxize.tax.scrapenames

Extract taxonomic names from text, URLs, or files using the Global Names Recognition and Discovery service.

**Parameters:**

- `url` (str, optional): URL to a web page, PDF, or document
- `file` (str, optional): Path to a local file
- `text` (str, optional): Text content to analyze
- `engine` (int, optional): Recognition engine - 0 (both), 1 (TaxonFinder), 2 (NetiNeti). Default: 0
- `unique` (bool, optional): Return unique names only. Default: True
- `verbatim` (bool, optional): Include verbatim strings. Default: False
- `detect_language` (bool, optional): Enable language detection. Default: True
- `all_data_sources` (bool, optional): Resolve against all data sources. Default: False
- `data_source_ids` (str, optional): Pipe-separated list of data source IDs
- `as_dataframe` (bool, optional): Return as DataFrame. Default: False

**Returns:**

- Dictionary with 'meta' and 'data' keys containing metadata and extracted names

**Examples:**

```python
from pytaxize import tax

# Extract names from a website
result = tax.scrapenames(url='https://en.wikipedia.org/wiki/Spider')
print(result['data'])  # Extracted names
print(result['meta'])  # Metadata

# Extract from PDF
pdf_result = tax.scrapenames(
    url='http://www.example.com/paper.pdf'
)

# Extract from text
text_result = tax.scrapenames(
    text='A spider named Pardosa moesta Banks, 1892'
)

# With additional options
detailed_result = tax.scrapenames(
    url='https://en.wikipedia.org/wiki/Spider',
    unique=True,
    all_data_sources=True,
    as_dataframe=True
)
```

## Helper Functions

### names_list_helper

Internal helper function for `names_list()`. Not intended for direct use.

## Usage Examples

### Getting Test Data

```python
from pytaxize import tax

# Get different taxonomic ranks
species = tax.names_list('species', 10)
genera = tax.names_list('genus', 10) 
families = tax.names_list('family', 10)
orders = tax.names_list('order', 10)

print(f"Species: {species}")
print(f"Genera: {genera}")
print(f"Families: {families}")
print(f"Orders: {orders}")
```

### Text Mining for Names

```python
from pytaxize import tax

# Analyze a scientific paper
paper_url = "https://example.com/biodiversity-paper.pdf"
names = tax.scrapenames(url=paper_url)

# Extract unique scientific names
scientific_names = [item['scientificName'] for item in names['data'] 
                   if 'scientificName' in item]

print(f"Found {len(scientific_names)} scientific names")
```

### Canadian Flora Search

```python
from pytaxize import tax

# Search for Canadian plants
canadian_plants = ["Acer saccharum", "Betula papyrifera", "Picea glauca"]
results = tax.vascan_search(q=canadian_plants)

for plant in results:
    print(f"Plant: {plant}")
```

## Data Sources

### names_list Data Sources

- **Species names**: Plant species from botanical databases
- **Genus names**: Plant genera 
- **Family names**: APG (Angiosperm Phylogeny Group) families
- **Order names**: APG orders

### vascan_search Data Source

- **CANADENSYS Vascan**: Database of Canadian vascular plants
- API endpoint: `http://data.canadensys.net/vascan/api/`

### scrapenames Data Source  

- **Global Names Recognition and Discovery**: `https://finder.globalnames.org/`
- Supports multiple recognition engines and data sources
- Can process various document formats (HTML, PDF, images, etc.)

## Error Handling

```python
from pytaxize import tax

try:
    # This might fail if the service is down
    result = tax.scrapenames(url="https://invalid-url.com")
except Exception as e:
    print(f"Error occurred: {e}")

# Always check for results
result = tax.vascan_search(q=["Nonexistent species"])
if result and 'results' in result:
    print("Found results")
else:
    print("No results found")
```

## Notes

- The `scrapenames` function requires an internet connection
- Large documents may take time to process
- Some functions may have rate limits - avoid rapid successive calls
- Results may vary depending on the quality and format of input text/documents