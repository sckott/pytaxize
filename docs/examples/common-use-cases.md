# Common Use Cases

This guide demonstrates common use cases for pytaxize in research and data management workflows.

## Use Case 1: Biodiversity Data Cleaning

### Problem
You have a dataset with species names that may contain spelling errors, synonyms, or outdated names.

### Solution

```python
from pytaxize import Ids, scicomm, Classification
import pandas as pd

def clean_species_list(species_list):
    """Clean and validate a list of species names"""
    
    results = []
    
    for species in species_list:
        print(f"Processing: {species}")
        
        # Try to find the species in ITIS
        ids_obj = Ids(species)
        ids_obj.itis()
        
        matches = ids_obj.ids.get(species, [])
        
        if matches:
            # Use the first match
            match = matches[0]
            
            # Get classification to verify it's a species
            classification = Classification(match['id'])
            classification.itis()
            
            hierarchy = classification.classification.get(match['id'], [])
            
            # Extract genus and species from classification
            genus = None
            species_epithet = None
            
            for rank in hierarchy:
                if rank['rankName'] == 'Genus':
                    genus = rank['taxonName']
                elif rank['rankName'] == 'Species':
                    # Extract species epithet from full name
                    full_name = rank['taxonName']
                    if ' ' in full_name:
                        species_epithet = full_name.split()[1]
            
            results.append({
                'original_name': species,
                'validated_name': match['name'],
                'itis_id': match['id'],
                'genus': genus,
                'species': species_epithet,
                'status': 'found',
                'rank': match.get('rank', 'Unknown')
            })
        else:
            results.append({
                'original_name': species,
                'validated_name': None,
                'itis_id': None,
                'genus': None,
                'species': None,
                'status': 'not_found',
                'rank': None
            })
    
    return pd.DataFrame(results)

# Example messy species list
messy_species = [
    "Quercus alba",           # Correct
    "Quercus albus",          # Incorrect (should be alba)
    "Homo sapiens",           # Correct
    "Canis lupis",            # Incorrect (should be lupus)
    "Invalid species name",   # Invalid
    "Felis catus",           # Correct
    "Pinus strobus"          # Correct
]

# Clean the data
cleaned_data = clean_species_list(messy_species)
print(cleaned_data)

# Save results
cleaned_data.to_csv('cleaned_species_data.csv', index=False)
```

## Use Case 2: Literature Mining for Species Names

### Problem
Extract and validate species names from scientific literature or field notes.

### Solution

```python
from pytaxize import tax, Ids
import re

def extract_and_validate_species(text, min_confidence=0.8):
    """Extract species names from text and validate them"""
    
    # Extract names using Global Names Recognition
    extracted = tax.scrapenames(text=text)
    
    if not extracted['data']:
        return {'species': [], 'validation': []}
    
    # Get unique scientific names
    species_names = []
    for item in extracted['data']:
        if 'scientificName' in item:
            name = item['scientificName']
            # Basic filtering for valid binomial names
            if len(name.split()) >= 2:
                species_names.append(name)
    
    # Remove duplicates
    species_names = list(set(species_names))
    
    # Validate each name
    validation_results = []
    
    for name in species_names:
        # Try ITIS validation
        ids_obj = Ids(name)
        ids_obj.itis()
        
        matches = ids_obj.ids.get(name, [])
        
        if matches:
            best_match = matches[0]
            validation_results.append({
                'extracted_name': name,
                'validated_name': best_match['name'],
                'itis_id': best_match['id'],
                'confidence': 'high',
                'database': 'itis'
            })
        else:
            # Try with genus only
            genus = name.split()[0]
            genus_ids = Ids(genus)
            genus_ids.itis()
            
            genus_matches = genus_ids.ids.get(genus, [])
            
            validation_results.append({
                'extracted_name': name,
                'validated_name': name,
                'itis_id': None,
                'confidence': 'low' if not genus_matches else 'medium',
                'database': 'itis'
            })
    
    return {
        'species': species_names,
        'validation': validation_results
    }

# Example scientific text
scientific_text = """
Our study examined the biodiversity of oak forests in North America.
We identified several key species including Quercus alba (white oak),
Quercus rubra (red oak), and Quercus velutina (black oak).
Associated fauna included Sciurus carolinensis (gray squirrel),
Turdus migratorius (American robin), and Odocoileus virginianus (white-tailed deer).
The understory was dominated by Acer saccharum (sugar maple) and 
Fagus grandifolia (American beech).
"""

# Extract and validate species
results = extract_and_validate_species(scientific_text)

print("Extracted species:")
for species in results['species']:
    print(f"  - {species}")

print("\nValidation results:")
for validation in results['validation']:
    print(f"  {validation['extracted_name']}: {validation['confidence']} confidence")
```

## Use Case 3: Phylogenetic Tree Preparation

### Problem
Prepare taxonomic data for phylogenetic analysis by getting complete classifications.

### Solution

```python
from pytaxize import Ids, Classification
import pandas as pd

def prepare_phylogenetic_data(species_list):
    """Prepare taxonomic data for phylogenetic analysis"""
    
    results = []
    
    for species in species_list:
        print(f"Processing {species}...")
        
        # Get ITIS ID
        ids_obj = Ids(species)
        ids_obj.itis()
        
        matches = ids_obj.ids.get(species, [])
        
        if not matches:
            print(f"  No match found for {species}")
            continue
        
        species_id = matches[0]['id']
        
        # Get full classification
        classification = Classification(species_id)
        classification.itis()
        
        hierarchy = classification.classification.get(species_id, [])
        
        if not hierarchy:
            print(f"  No classification found for {species}")
            continue
        
        # Extract taxonomic ranks
        taxonomy = {'species': species, 'itis_id': species_id}
        
        for rank in hierarchy:
            rank_name = rank['rankName'].lower()
            taxon_name = rank['taxonName']
            
            if rank_name in ['kingdom', 'phylum', 'class', 'order', 'family', 'genus']:
                taxonomy[rank_name] = taxon_name
        
        results.append(taxonomy)
    
    return pd.DataFrame(results)

def create_phylogenetic_matrix(df, rank_levels=['kingdom', 'phylum', 'class', 'order', 'family']):
    """Create a binary matrix for phylogenetic analysis"""
    
    matrices = {}
    
    for rank in rank_levels:
        if rank in df.columns:
            # Get unique taxa at this rank
            unique_taxa = df[rank].dropna().unique()
            
            # Create binary matrix
            matrix = pd.DataFrame(0, index=df['species'], columns=unique_taxa)
            
            for idx, row in df.iterrows():
                if pd.notna(row[rank]):
                    matrix.loc[row['species'], row[rank]] = 1
            
            matrices[rank] = matrix
    
    return matrices

# Example species list for phylogenetic study
phylo_species = [
    "Quercus alba",
    "Quercus rubra", 
    "Acer saccharum",
    "Acer rubrum",
    "Pinus strobus",
    "Pinus resinosa",
    "Betula papyrifera",
    "Fagus grandifolia"
]

# Prepare taxonomic data
phylo_data = prepare_phylogenetic_data(phylo_species)
print("Taxonomic data:")
print(phylo_data)

# Create phylogenetic matrices
matrices = create_phylogenetic_matrix(phylo_data)

# Save results
phylo_data.to_csv('phylogenetic_taxonomy.csv', index=False)

for rank, matrix in matrices.items():
    matrix.to_csv(f'phylo_matrix_{rank}.csv')
    print(f"\n{rank.capitalize()} level matrix:")
    print(matrix)
```

## Use Case 4: Biodiversity Assessment

### Problem
Assess taxonomic diversity in ecological samples.

### Solution

```python
from pytaxize import Ids, Classification, Children
import pandas as pd
from collections import Counter, defaultdict

def assess_biodiversity(species_list):
    """Comprehensive biodiversity assessment"""
    
    taxonomy_data = []
    
    # Get taxonomic data for each species
    for species in species_list:
        ids_obj = Ids(species)
        ids_obj.itis()
        
        matches = ids_obj.ids.get(species, [])
        
        if matches:
            species_id = matches[0]['id']
            
            # Get classification
            classification = Classification(species_id)
            classification.itis()
            
            hierarchy = classification.classification.get(species_id, [])
            
            # Extract ranks
            taxonomy = {'species': species}
            for rank in hierarchy:
                rank_name = rank['rankName'].lower()
                taxonomy[rank_name] = rank['taxonName']
            
            taxonomy_data.append(taxonomy)
    
    df = pd.DataFrame(taxonomy_data)
    
    # Calculate diversity metrics
    diversity_metrics = {}
    
    # Species richness
    diversity_metrics['species_richness'] = len(df)
    
    # Family richness
    if 'family' in df.columns:
        diversity_metrics['family_richness'] = df['family'].nunique()
    
    # Genus richness
    if 'genus' in df.columns:
        diversity_metrics['genus_richness'] = df['genus'].nunique()
    
    # Taxonomic composition
    composition = {}
    for rank in ['kingdom', 'phylum', 'class', 'order', 'family']:
        if rank in df.columns:
            composition[rank] = df[rank].value_counts().to_dict()
    
    return {
        'taxonomy_data': df,
        'diversity_metrics': diversity_metrics,
        'composition': composition
    }

def compare_sites(site1_species, site2_species, site1_name="Site 1", site2_name="Site 2"):
    """Compare biodiversity between two sites"""
    
    site1_assessment = assess_biodiversity(site1_species)
    site2_assessment = assess_biodiversity(site2_species)
    
    print(f"=== Biodiversity Comparison ===\n")
    
    print(f"{site1_name}:")
    print(f"  Species richness: {site1_assessment['diversity_metrics']['species_richness']}")
    print(f"  Family richness: {site1_assessment['diversity_metrics'].get('family_richness', 'N/A')}")
    print(f"  Genus richness: {site1_assessment['diversity_metrics'].get('genus_richness', 'N/A')}")
    
    print(f"\n{site2_name}:")
    print(f"  Species richness: {site2_assessment['diversity_metrics']['species_richness']}")
    print(f"  Family richness: {site2_assessment['diversity_metrics'].get('family_richness', 'N/A')}")
    print(f"  Genus richness: {site2_assessment['diversity_metrics'].get('genus_richness', 'N/A')}")
    
    # Find shared and unique species
    site1_set = set(site1_species)
    site2_set = set(site2_species)
    
    shared = site1_set & site2_set
    unique_site1 = site1_set - site2_set
    unique_site2 = site2_set - site1_set
    
    print(f"\nSpecies overlap:")
    print(f"  Shared species: {len(shared)}")
    print(f"  Unique to {site1_name}: {len(unique_site1)}")
    print(f"  Unique to {site2_name}: {len(unique_site2)}")
    
    if shared:
        print(f"  Shared: {list(shared)}")
    
    return {
        'site1': site1_assessment,
        'site2': site2_assessment,
        'comparison': {
            'shared_species': list(shared),
            'unique_site1': list(unique_site1),
            'unique_site2': list(unique_site2)
        }
    }

# Example: Compare forest sites
forest_site_a = [
    "Quercus alba", "Acer saccharum", "Fagus grandifolia",
    "Betula alleghaniensis", "Fraxinus americana", "Carya ovata"
]

forest_site_b = [
    "Quercus rubra", "Acer saccharum", "Pinus strobus", 
    "Betula papyrifera", "Fagus grandifolia", "Abies balsamea"
]

# Compare the sites
comparison = compare_sites(forest_site_a, forest_site_b, "Mature Forest", "Mixed Forest")
```

## Use Case 5: Museum Collection Management

### Problem
Standardize and update taxonomic names in museum collections.

### Solution

```python
from pytaxize import Ids, scicomm, Classification
import pandas as pd
from datetime import datetime

def update_museum_records(collection_df, name_column='scientific_name'):
    """Update taxonomic names in museum collection records"""
    
    updated_records = []
    
    for idx, record in collection_df.iterrows():
        original_name = record[name_column]
        
        print(f"Processing record {idx + 1}: {original_name}")
        
        # Try to validate the name
        ids_obj = Ids(original_name)
        ids_obj.itis()
        
        matches = ids_obj.ids.get(original_name, [])
        
        update_info = {
            'record_id': record.get('record_id', idx),
            'original_name': original_name,
            'update_date': datetime.now().strftime('%Y-%m-%d')
        }
        
        if matches:
            best_match = matches[0]
            current_name = best_match['name']
            itis_id = best_match['id']
            
            # Check if name needs updating
            name_changed = original_name.lower() != current_name.lower()
            
            # Get common names
            try:
                common_names = scicomm.sci2comm(current_name, db='itis')
                common = common_names.get(current_name, [])
                common_name = common[0] if common else None
            except:
                common_name = None
            
            # Get family for organization
            classification = Classification(itis_id)
            classification.itis()
            
            hierarchy = classification.classification.get(itis_id, [])
            family = None
            order = None
            
            for rank in hierarchy:
                if rank['rankName'] == 'Family':
                    family = rank['taxonName']
                elif rank['rankName'] == 'Order':
                    order = rank['taxonName']
            
            update_info.update({
                'current_name': current_name,
                'itis_id': itis_id,
                'common_name': common_name,
                'family': family,
                'order': order,
                'name_changed': name_changed,
                'validation_status': 'validated',
                'confidence': 'high'
            })
        else:
            # Try genus-only search for partial matches
            genus = original_name.split()[0] if ' ' in original_name else original_name
            
            genus_ids = Ids(genus)
            genus_ids.itis()
            
            genus_matches = genus_ids.ids.get(genus, [])
            
            update_info.update({
                'current_name': original_name,  # Keep original
                'itis_id': None,
                'common_name': None,
                'family': None,
                'order': None,
                'name_changed': False,
                'validation_status': 'needs_review',
                'confidence': 'low' if not genus_matches else 'medium',
                'notes': f"Genus {'found' if genus_matches else 'not found'} in ITIS"
            })
        
        # Copy other fields from original record
        for col in record.index:
            if col != name_column and col not in update_info:
                update_info[col] = record[col]
        
        updated_records.append(update_info)
    
    return pd.DataFrame(updated_records)

def generate_update_report(updated_df):
    """Generate a report of the updates made"""
    
    total_records = len(updated_df)
    validated = len(updated_df[updated_df['validation_status'] == 'validated'])
    needs_review = len(updated_df[updated_df['validation_status'] == 'needs_review'])
    name_changes = len(updated_df[updated_df['name_changed'] == True])
    
    print("=== Collection Update Report ===")
    print(f"Total records processed: {total_records}")
    print(f"Successfully validated: {validated} ({validated/total_records*100:.1f}%)")
    print(f"Needs manual review: {needs_review} ({needs_review/total_records*100:.1f}%)")
    print(f"Names updated: {name_changes}")
    
    if name_changes > 0:
        print("\nName changes made:")
        changes = updated_df[updated_df['name_changed'] == True]
        for _, row in changes.iterrows():
            print(f"  {row['original_name']} → {row['current_name']}")
    
    needs_review_df = updated_df[updated_df['validation_status'] == 'needs_review']
    if len(needs_review_df) > 0:
        print(f"\nRecords needing review:")
        for _, row in needs_review_df.iterrows():
            print(f"  {row['original_name']} - {row.get('notes', 'No additional info')}")

# Example museum collection data
museum_data = pd.DataFrame({
    'record_id': ['HERB001', 'HERB002', 'HERB003', 'HERB004', 'HERB005'],
    'scientific_name': [
        'Quercus alba',           # Valid current name
        'Quercus albus',          # Incorrect spelling
        'Acer saccharinum',       # Valid current name  
        'Invalid species name',   # Invalid name
        'Betula papyrifera'      # Valid current name
    ],
    'collector': ['Smith, J.', 'Jones, M.', 'Brown, K.', 'Davis, L.', 'Wilson, R.'],
    'collection_date': ['1995-06-15', '1998-07-20', '2001-05-10', '2003-08-30', '2005-09-12'],
    'locality': ['Forest A', 'Wetland B', 'Park C', 'Field D', 'Trail E']
})

# Update the collection
print("Original collection data:")
print(museum_data)

updated_collection = update_museum_records(museum_data)

print("\nUpdated collection data:")
print(updated_collection[['record_id', 'original_name', 'current_name', 'validation_status', 'name_changed']])

# Generate report
generate_update_report(updated_collection)

# Save updated collection
updated_collection.to_csv('updated_museum_collection.csv', index=False)
```

## Use Case 6: Ecological Survey Data Analysis

### Problem
Analyze species composition and ecological patterns in field survey data.

### Solution

```python
from pytaxize import Ids, Classification
import pandas as pd
import numpy as np
from collections import defaultdict

def analyze_ecological_survey(survey_data, species_col='species', abundance_col='count'):
    """Analyze ecological survey data with taxonomic information"""
    
    # Get taxonomic information for each species
    taxonomy_data = {}
    
    unique_species = survey_data[species_col].unique()
    
    for species in unique_species:
        print(f"Getting taxonomy for {species}...")
        
        ids_obj = Ids(species)
        ids_obj.itis()
        
        matches = ids_obj.ids.get(species, [])
        
        if matches:
            species_id = matches[0]['id']
            
            # Get classification
            classification = Classification(species_id)
            classification.itis()
            
            hierarchy = classification.classification.get(species_id, [])
            
            # Extract taxonomic information
            tax_info = {'itis_id': species_id}
            for rank in hierarchy:
                rank_name = rank['rankName'].lower()
                tax_info[rank_name] = rank['taxonName']
            
            taxonomy_data[species] = tax_info
        else:
            taxonomy_data[species] = {'itis_id': None}
    
    # Merge with survey data
    expanded_data = []
    
    for _, row in survey_data.iterrows():
        species = row[species_col]
        tax_info = taxonomy_data.get(species, {})
        
        combined_row = row.to_dict()
        combined_row.update(tax_info)
        expanded_data.append(combined_row)
    
    expanded_df = pd.DataFrame(expanded_data)
    
    # Calculate ecological metrics
    metrics = calculate_ecological_metrics(expanded_df, abundance_col)
    
    return {
        'data': expanded_df,
        'taxonomy': taxonomy_data,
        'metrics': metrics
    }

def calculate_ecological_metrics(df, abundance_col):
    """Calculate various ecological diversity metrics"""
    
    metrics = {}
    
    # Species richness
    metrics['species_richness'] = df['species'].nunique()
    
    # Total abundance
    metrics['total_abundance'] = df[abundance_col].sum()
    
    # Shannon diversity index
    abundances = df[abundance_col].values
    proportions = abundances / abundances.sum()
    shannon = -np.sum(proportions * np.log(proportions))
    metrics['shannon_diversity'] = shannon
    
    # Simpson diversity index
    simpson = np.sum(proportions ** 2)
    metrics['simpson_diversity'] = 1 - simpson
    
    # Family-level metrics
    if 'family' in df.columns:
        family_richness = df['family'].nunique()
        metrics['family_richness'] = family_richness
        
        # Family abundance distribution
        family_abundance = df.groupby('family')[abundance_col].sum().to_dict()
        metrics['family_abundance'] = family_abundance
    
    # Dominance (most abundant species)
    most_abundant = df.loc[df[abundance_col].idxmax()]
    metrics['dominant_species'] = {
        'species': most_abundant['species'],
        'abundance': most_abundant[abundance_col],
        'proportion': most_abundant[abundance_col] / df[abundance_col].sum()
    }
    
    return metrics

def compare_survey_sites(site_data_list, site_names):
    """Compare multiple survey sites"""
    
    site_analyses = []
    
    for i, site_data in enumerate(site_data_list):
        print(f"\nAnalyzing {site_names[i]}...")
        analysis = analyze_ecological_survey(site_data)
        analysis['site_name'] = site_names[i]
        site_analyses.append(analysis)
    
    # Compare metrics
    print("\n=== Site Comparison ===")
    
    comparison_metrics = pd.DataFrame([
        {
            'site': analysis['site_name'],
            'species_richness': analysis['metrics']['species_richness'],
            'total_abundance': analysis['metrics']['total_abundance'],
            'shannon_diversity': analysis['metrics']['shannon_diversity'],
            'simpson_diversity': analysis['metrics']['simpson_diversity'],
            'family_richness': analysis['metrics'].get('family_richness', 'N/A'),
            'dominant_species': analysis['metrics']['dominant_species']['species']
        }
        for analysis in site_analyses
    ])
    
    print(comparison_metrics)
    
    return site_analyses, comparison_metrics

# Example survey data
site1_data = pd.DataFrame({
    'species': ['Quercus alba', 'Acer saccharum', 'Fagus grandifolia', 'Betula alleghaniensis', 'Carya ovata'],
    'count': [25, 18, 12, 8, 5],
    'plot': [1, 1, 1, 1, 1]
})

site2_data = pd.DataFrame({
    'species': ['Pinus strobus', 'Acer saccharum', 'Betula papyrifera', 'Abies balsamea', 'Picea glauca'],
    'count': [30, 15, 12, 10, 6],
    'plot': [2, 2, 2, 2, 2]
})

site3_data = pd.DataFrame({
    'species': ['Quercus rubra', 'Acer rubrum', 'Nyssa sylvatica', 'Sassafras albidum', 'Liriodendron tulipifera'],
    'count': [20, 16, 14, 9, 7],
    'plot': [3, 3, 3, 3, 3]
})

# Compare all sites
sites_data = [site1_data, site2_data, site3_data]
site_names = ['Mature Hardwood', 'Conifer Stand', 'Mixed Deciduous']

analyses, comparison = compare_survey_sites(sites_data, site_names)

# Save results
comparison.to_csv('site_comparison_metrics.csv', index=False)

for i, analysis in enumerate(analyses):
    analysis['data'].to_csv(f'site_{i+1}_detailed_data.csv', index=False)
```

## Summary

These use cases demonstrate how pytaxize can be integrated into various research workflows:

1. **Data Cleaning**: Validate and standardize species names
2. **Literature Mining**: Extract species names from text
3. **Phylogenetic Analysis**: Prepare taxonomic data for evolutionary studies  
4. **Biodiversity Assessment**: Calculate diversity metrics with taxonomic context
5. **Museum Collections**: Update and maintain taxonomic databases
6. **Ecological Surveys**: Analyze field data with complete taxonomic information

Each workflow can be adapted to your specific needs by modifying the database sources, validation criteria, and output formats.