import pandas as pd
import json
from pathlib import Path

def clean_column_name(col):
    """Remove extra spaces and quotes from column names"""
    return col.strip().strip('"')

def calculate_margin_category(rep_pct, dem_pct):
    """Calculate political category based on margin between Republican and Democratic votes"""
    margin = rep_pct - dem_pct
    
    if margin >= 40:
        return "Annihilation Republican"
    elif margin >= 30:
        return "Dominant Republican"
    elif margin >= 20:
        return "Stronghold Republican"
    elif margin >= 10:
        return "Safe Republican"
    elif margin >= 5.51:
        return "Likely Republican"
    elif margin >= 1:
        return "Lean Republican"
    elif margin >= 0.51:
        return "Tilt Republican"
    elif margin >= -0.5:
        return "Tossup"
    elif margin >= -0.99:
        return "Tilt Democratic"
    elif margin >= -5.50:
        return "Lean Democratic"
    elif margin >= -9.99:
        return "Likely Democratic"
    elif margin >= -19.99:
        return "Safe Democratic"
    elif margin >= -29.99:
        return "Stronghold Democratic"
    elif margin >= -39.99:
        return "Dominant Democratic"
    else:
        return "Annihilation Democratic"

def aggregate_election_data(csv_file, year):
    """
    Aggregate election data by county for a specific year.
    Focus on Presidential, US Senate, and statewide offices (excluding legislature).
    """
    print(f"Processing {csv_file}...")
    
    # Read CSV and clean column names
    df = pd.read_csv(csv_file, skipinitialspace=True)
    df.columns = [clean_column_name(col) for col in df.columns]
    
    print(f"Columns found: {list(df.columns)}")
    
    # Clean the data - remove quotes and extra spaces
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].str.strip().str.strip('"')
    
    # Find the votes column (handle variations)
    votes_col = None
    for col in df.columns:
        if 'vote' in col.lower():
            votes_col = col
            break
    
    if not votes_col:
        print(f"Error: Could not find votes column. Columns: {list(df.columns)}")
        return {}
    
    print(f"Using votes column: {votes_col}")
    
    # Convert votes to numeric
    df[votes_col] = pd.to_numeric(df[votes_col], errors='coerce').fillna(0).astype(int)
    
    # Filter for Presidential, US Senate, and statewide offices (excluding legislature)
    # Include: President, US Senator, Governor, Attorney General, Secretary of State, etc.
    # Exclude: State Representative, State Senator, US Representative (districts)
    statewide_keywords = [
        'president', 'senator', 'governor', 'attorney general', 
        'secretary of state', 'auditor', 'treasurer'
    ]
    exclude_keywords = ['representative', 'district', 'congressional']
    
    def is_statewide(office_name):
        office_lower = office_name.lower()
        # Check if it contains statewide keywords
        has_statewide = any(keyword in office_lower for keyword in statewide_keywords)
        # Check if it's NOT a district/legislative race
        is_district = any(keyword in office_lower for keyword in exclude_keywords)
        return has_statewide and not is_district
    
    df['is_statewide'] = df['Office'].apply(is_statewide)
    df = df[df['is_statewide']]
    
    print(f"Filtered to {len(df)} rows for statewide races")
    print(f"Unique offices: {df['Office Category'].unique()}")
    
    # Group by county, office, candidate, and party to get totals
    county_col = 'Reporting County Name'
    office_col = 'Office'
    office_cat_col = 'Office Category'
    candidate_col = 'Name on Ballot'
    party_col = 'Political Party'
    
    aggregated = df.groupby([
        county_col, 
        office_col, 
        office_cat_col,
        candidate_col, 
        party_col
    ])[votes_col].sum().reset_index()
    
    # Create nested structure: office -> county -> candidates with margin categories
    result = {}
    
    for office_cat in aggregated[office_cat_col].unique():
        office_data = aggregated[aggregated[office_cat_col] == office_cat]
        office_name = office_data[office_col].iloc[0]
        
        counties = {}
        for county in office_data[county_col].unique():
            county_data = office_data[office_data[county_col] == county]
            
            candidates = []
            total_votes = county_data[votes_col].sum()
            
            # Calculate Republican and Democratic percentages
            rep_votes = county_data[county_data[party_col] == 'Republican'][votes_col].sum()
            dem_votes = county_data[county_data[party_col] == 'Democratic'][votes_col].sum()
            
            rep_pct = (rep_votes / total_votes * 100) if total_votes > 0 else 0
            dem_pct = (dem_votes / total_votes * 100) if total_votes > 0 else 0
            
            for _, row in county_data.iterrows():
                if row[votes_col] > 0:  # Only include candidates with votes
                    candidates.append({
                        'name': row[candidate_col],
                        'party': row[party_col],
                        'votes': int(row[votes_col]),
                        'percentage': round(row[votes_col] / total_votes * 100, 2) if total_votes > 0 else 0
                    })
            
            # Sort by votes descending
            candidates.sort(key=lambda x: x['votes'], reverse=True)
            
            # Calculate margin category
            margin_category = calculate_margin_category(rep_pct, dem_pct)
            margin = rep_pct - dem_pct
            
            counties[county] = {
                'total_votes': int(total_votes),
                'candidates': candidates,
                'margin': round(margin, 2),
                'category': margin_category,
                'republican_pct': round(rep_pct, 2),
                'democratic_pct': round(dem_pct, 2)
            }
        
        result[office_cat] = {
            'office_name': office_name,
            'counties': counties
        }
    
    print(f"  Found {len(result)} statewide offices")
    print(f"  Offices: {list(result.keys())}")
    
    return result

def main():
    data_dir = Path('data')
    
    # Define files to process
    files_to_process = [
        ('AllOfficeResults2018-aligned.csv', 2018),
        ('AllOfficeResults2020-aligned.csv', 2020),
        ('AllOfficeResults2022-aligned.csv', 2022),
        ('AllOfficeResults2024-aligned.csv', 2024),
    ]
    
    all_results = {}
    
    for filename, year in files_to_process:
        filepath = data_dir / filename
        if filepath.exists():
            all_results[year] = aggregate_election_data(filepath, year)
        else:
            print(f"Warning: {filepath} not found, skipping...")
    
    # Save to JSON
    output_file = data_dir / 'indiana_election_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\nAggregated data saved to {output_file}")
    print(f"Years included: {list(all_results.keys())}")
    
    # Print summary
    for year, data in all_results.items():
        print(f"\n{year}:")
        for office_cat, office_data in list(data.items())[:3]:
            num_counties = len(office_data['counties'])
            print(f"  {office_cat}: {num_counties} counties")

if __name__ == '__main__':
    main()
