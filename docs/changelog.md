# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive MkDocs documentation with API reference
- Getting started guide and common use cases examples
- Contributing guidelines for developers

### Changed
- Improved documentation structure and navigation

## [0.7.2] - 2024-01-15

### Added
- Support for Python 3.13 and 3.14
- Enhanced error handling in core functions

### Changed
- Updated dependencies to latest versions
- Improved performance of name resolution functions

### Fixed
- Fixed issues with ITIS API responses
- Resolved encoding problems with special characters in species names

## [0.7.1] - 2023-09-20

### Added
- New `scrapenames()` function for extracting taxonomic names from text
- Support for Global Names Recognition and Discovery service

### Changed
- Migrated from pandas to polars for better performance
- Updated ITIS API endpoints

### Fixed
- Fixed memory issues with large taxonomic datasets
- Improved handling of API timeouts

## [0.7.0] - 2023-06-15

### Added
- Support for Encyclopedia of Life (EOL) API
- New `Children` class for retrieving taxonomic children
- New `Classification` class for taxonomic hierarchies

### Changed
- **BREAKING**: Refactored main API structure
- Improved consistency across database interfaces
- Updated to use newer API versions where available

### Deprecated
- Old function-based API (will be removed in v0.8.0)

### Fixed
- Fixed issues with NCBI taxonomy ID resolution
- Improved error messages for invalid inputs

## [0.6.5] - 2023-03-10

### Added
- Support for Catalogue of Life API v4
- New utility functions for data validation

### Changed
- Improved GBIF species matching
- Enhanced documentation with more examples

### Fixed
- Fixed bug in `vascan_search()` with multiple names
- Resolved issues with special characters in taxonomic names

## [0.6.4] - 2022-12-20

### Added
- Support for Python 3.11
- New configuration options for API timeouts

### Changed
- Migrated CI/CD to GitHub Actions
- Updated all dependencies to latest versions

### Fixed
- Fixed deprecation warnings from pandas
- Improved handling of malformed API responses

## [0.6.3] - 2022-09-15

### Added
- Support for GBIF species API
- New functions for taxonomic name validation

### Changed
- Improved error handling for network issues
- Better support for rate limiting

### Fixed
- Fixed issues with Unicode characters in species names
- Resolved problems with empty API responses

## [0.6.2] - 2022-06-30

### Added
- Support for multiple output formats in core functions
- New examples in documentation

### Changed
- Improved performance of batch operations
- Enhanced logging and debugging information

### Fixed
- Fixed memory leak in long-running operations
- Corrected issues with CSV output formatting

## [0.6.1] - 2022-04-20

### Added
- Support for Python 3.10
- New utility functions for data export

### Changed
- Updated ITIS web service endpoints
- Improved documentation structure

### Fixed
- Fixed compatibility issues with newer pandas versions
- Resolved SSL certificate issues with some APIs

## [0.6.0] - 2022-01-15

### Added
- **NEW**: `scicomm` module for scientific/common name conversion
- Support for NCBI taxonomy database
- New `Ids` class for unified taxonomic ID retrieval

### Changed
- **BREAKING**: Restructured package organization
- Improved API consistency across modules
- Enhanced error handling and validation

### Deprecated
- Several old function names (see migration guide)

### Fixed
- Fixed issues with XML parsing in ITIS responses
- Improved handling of synonyms and accepted names

## [0.5.8] - 2021-10-12

### Added
- Support for CANADENSYS Vascan API
- New functions for Canadian plant species

### Changed
- Updated dependencies for security patches
- Improved test coverage

### Fixed
- Fixed bug in name list generation
- Corrected issues with API parameter encoding

## [0.5.7] - 2021-07-20

### Added
- New utility functions for taxonomic data cleaning
- Support for batch processing of species lists

### Changed
- Improved documentation with more examples
- Enhanced error messages for common issues

### Fixed
- Fixed timeout issues with slow API responses
- Resolved problems with empty search results

## [0.5.6] - 2021-04-15

### Added
- Support for Python 3.9
- New configuration options for API keys

### Changed
- Updated ITIS API integration
- Improved handling of API rate limits

### Fixed
- Fixed issues with special characters in queries
- Corrected problems with CSV file reading

## [0.5.5] - 2021-01-30

### Added
- New functions for taxonomic hierarchy retrieval
- Support for additional ITIS services

### Changed
- Improved performance of data retrieval operations
- Enhanced documentation

### Fixed
- Fixed bug in species name parsing
- Resolved issues with network connectivity checks

## [0.5.0] - 2020-08-15

### Added
- Initial stable release
- Core functionality for taxonomic name resolution
- Support for ITIS database
- Basic utility functions

### Changed
- Established consistent API patterns
- Comprehensive test suite

### Fixed
- Initial bug fixes and stability improvements

---

## Migration Guides

### Migrating from 0.6.x to 0.7.x

The 0.7.0 release introduced significant changes to the API structure:

**Old way:**
```python
import pytaxize
results = pytaxize.get_ids("Quercus alba")
```

**New way:**
```python
from pytaxize import Ids
ids_obj = Ids("Quercus alba")
ids_obj.itis()
results = ids_obj.ids
```

### Migrating from 0.5.x to 0.6.x

The 0.6.0 release restructured the package organization:

**Old way:**
```python
from pytaxize.itis import get_common_names
```

**New way:**
```python
from pytaxize import itis
itis.common_names()
```

---

## Links

- [GitHub Repository](https://github.com/sckott/pytaxize)
- [PyPI Package](https://pypi.org/project/pytaxize/)
- [Documentation](https://pytaxize.readthedocs.io/)
- [Issue Tracker](https://github.com/sckott/pytaxize/issues)