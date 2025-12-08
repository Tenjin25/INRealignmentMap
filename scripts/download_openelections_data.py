"""
Download and process Indiana election data from OpenElections GitHub repository
Creates aggregated county-level data for visualization
"""
import pandas as pd
import requests
from pathlib import Path
import json
from collections import defaultdict

# Years to process
YEARS = [2016, 2018, 2020]

# GitHub raw content base URL
BASE_URL = "https://raw.githubusercontent.com/openelections/openelections-data-in/master"

def download_statewide_file(year, election_type='general'):
    """Download statewide precinct file if available"""
    filename = f"{year}1103__in__{election_type}__precinct.csv"
    if year == 2018:
        filename = f"{year}1106__in__{election_type}__precinct.csv"
    elif year == 2016:
        filename = f"{year}1108__in__{election_type}__precinct.csv"
    
    url = f"{BASE_URL}/{year}/{filename}"
    print(f"\nTrying to download: {filename}")
    
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            print(f"✓ Downloaded {filename}")
            return pd.read_csv(url)
        else:
            print(f"✗ File not found: {filename}")
            return None
    except Exception as e:
        print(f"✗ Error downloading {filename}: {e}")
        return None

def aggregate_county_data(df, year):
    """Aggregate precinct data to county level"""
    if df is None or df.empty:
        return None
    
    print(f"\nProcessing {year} data...")
    print(f"  Columns: {list(df.columns)}")
    print(f"  Rows: {len(df)}")
    
    # Find county column
    county_col = None
    for col in ['county', 'County', 'COUNTY']:
        if col in df.columns:
            county_col = col
            break
    
    if not county_col:
        print(f"  ✗ No county column found!")
        return None
    
    # Aggregate by county
    results = defaultdict(lambda: {
        'year': year,
        'county': '',
        'president_dem': 0,
        'president_rep': 0,
        'president_total': 0,
        'governor_dem': 0,
        'governor_rep': 0,
        'governor_total': 0,
        'us_senate_dem': 0,
        'us_senate_rep': 0,
        'us_senate_total': 0
    })
    
    # Group by county
    for county, group in df.groupby(county_col):
        county_name = str(county).strip().upper()
        results[county_name]['county'] = county_name
        
        # Find office and candidate columns
        # Presidential
        if 'office' in df.columns or 'Office' in df.columns:
            office_col = 'office' if 'office' in df.columns else 'Office'
            pres_data = group[group[office_col].str.contains('President', case=False, na=False)]
            if not pres_data.empty:
                # Sum votes by party
                for _, row in pres_data.iterrows():
                    party = str(row.get('party', '')).upper()
                    votes_str = str(row.get('votes', '0')).replace(',', '')
                    try:
                        votes = int(votes_str)
                    except (ValueError, TypeError):
                        votes = 0
                    if 'DEM' in party:
                        results[county_name]['president_dem'] += votes
                    elif 'REP' in party:
                        results[county_name]['president_rep'] += votes
                    results[county_name]['president_total'] += votes
        
        # Governor
        if 'office' in df.columns or 'Office' in df.columns:
            office_col = 'office' if 'office' in df.columns else 'Office'
            gov_data = group[group[office_col].str.contains('Governor', case=False, na=False)]
            if not gov_data.empty:
                for _, row in gov_data.iterrows():
                    party = str(row.get('party', '')).upper()
                    votes = int(row.get('votes', 0) or 0)
                    if 'DEM' in party:
                        results[county_name]['governor_dem'] += votes
                    elif 'REP' in party:
                        results[county_name]['governor_rep'] += votes
                    results[county_name]['governor_total'] += votes
        
        # US Senate
        if 'office' in df.columns or 'Office' in df.columns:
            office_col = 'office' if 'office' in df.columns else 'Office'
            senate_data = group[group[office_col].str.contains('Senate', case=False, na=False)]
            if not senate_data.empty:
                for _, row in senate_data.iterrows():
                    party = str(row.get('party', '')).upper()
                    votes = int(row.get('votes', 0) or 0)
                    if 'DEM' in party:
                        results[county_name]['us_senate_dem'] += votes
                    elif 'REP' in party:
                        results[county_name]['us_senate_rep'] += votes
                    results[county_name]['us_senate_total'] += votes
    
    print(f"  ✓ Aggregated {len(results)} counties")
    return list(results.values())

def main():
    print("=" * 60)
    print("Indiana Election Data Download & Processing")
    print("=" * 60)
    
    all_results = []
    
    for year in YEARS:
        df = download_statewide_file(year)
        county_data = aggregate_county_data(df, year)
        if county_data:
            all_results.extend(county_data)
    
    if not all_results:
        print("\n✗ No data collected!")
        return
    
    # Convert to DataFrame
    results_df = pd.DataFrame(all_results)
    
    # Save as CSV
    csv_path = Path('data/indiana_election_results.csv')
    results_df.to_csv(csv_path, index=False)
    print(f"\n✓ Saved CSV: {csv_path}")
    print(f"  Rows: {len(results_df)}")
    
    # Create nested JSON structure for the map
    json_structure = {
        'state': 'Indiana',
        'results_by_year': {}
    }
    
    for year in YEARS:
        year_data = results_df[results_df['year'] == year]
        json_structure['results_by_year'][str(year)] = {
            'presidential': {},
            'us_senate': {},
            'governor': {}
        }
        
        # Process each contest type
        for _, row in year_data.iterrows():
            county = row['county']
            
            # Presidential
            if row['president_total'] > 0:
                if 'president_1' not in json_structure['results_by_year'][str(year)]['presidential']:
                    json_structure['results_by_year'][str(year)]['presidential']['president_1'] = {
                        'contest_name': 'President of the United States',
                        'results': {}
                    }
                
                json_structure['results_by_year'][str(year)]['presidential']['president_1']['results'][county] = {
                    'dem_votes': int(row['president_dem']),
                    'rep_votes': int(row['president_rep']),
                    'total_votes': int(row['president_total']),
                    'competitiveness': calculate_competitiveness(
                        row['president_dem'], 
                        row['president_rep'], 
                        row['president_total']
                    )
                }
    
    # Save as JSON
    json_path = Path('data/indiana_election_results.json')
    with open(json_path, 'w') as f:
        json.dump(json_structure, f, indent=2)
    
    print(f"✓ Saved JSON: {json_path}")
    print(f"\n✓ Processing complete!")
    print(f"  Years: {YEARS}")
    print(f"  Counties: {results_df['county'].nunique()}")

def calculate_competitiveness(dem_votes, rep_votes, total_votes):
    """Calculate competitiveness metrics"""
    if total_votes == 0:
        return {'category': 'Unknown', 'color': '#999999'}
    
    dem_pct = (dem_votes / total_votes) * 100
    rep_pct = (rep_votes / total_votes) * 100
    margin = abs(dem_pct - rep_pct)
    winner = 'Republican' if rep_pct > dem_pct else 'Democratic'
    
    if margin >= 40:
        category = f"Annihilation {winner}"
        color = '#67000d' if winner == 'Republican' else '#08306b'
    elif margin >= 30:
        category = f"Dominant {winner}"
        color = '#a50f15' if winner == 'Republican' else '#08519c'
    elif margin >= 20:
        category = f"Stronghold {winner}"
        color = '#cb181d' if winner == 'Republican' else '#3182bd'
    elif margin >= 10:
        category = f"Safe {winner}"
        color = '#ef3b2c' if winner == 'Republican' else '#6baed6'
    elif margin >= 5.5:
        category = f"Likely {winner}"
        color = '#fb6a4a' if winner == 'Republican' else '#9ecae1'
    elif margin >= 1:
        category = f"Lean {winner}"
        color = '#fcae91' if winner == 'Republican' else '#c6dbef'
    elif margin >= 0.5:
        category = f"Tilt {winner}"
        color = '#fee8c8' if winner == 'Republican' else '#e1f5fe'
    else:
        category = 'Tossup'
        color = '#f7f7f7'
    
    return {
        'category': category,
        'color': color,
        'party': winner,
        'margin_pct': round(margin, 2)
    }

if __name__ == '__main__':
    main()
