import pandas as pd
import json
from pathlib import Path

def normalize_county_name(county_name):
    """Normalize county name variations to match GeoJSON format"""
    if not county_name or not isinstance(county_name, str):
        return county_name
    
    # Normalize to title case and strip whitespace
    county = county_name.strip()
    
    # Handle specific known variations
    if county.lower() in ['saint joseph', 'st joseph', 'st. joseph']:
        return 'St. Joseph'
    if county.lower() in ['laport', 'la porte', 'laporte']:
        return 'Laporte'
    if county.lower() in ['dekalb', 'de kalb']:
        return 'Dekalb'
    
    # Default: capitalize first letter of each word
    return county.title()

def get_competitiveness_info(margin_pct, winner):
    """Get detailed competitiveness information"""
    colors = {
        'R_ANNIHILATION': '#67000d',
        'R_DOMINANT': '#a50f15',
        'R_STRONGHOLD': '#cb181d',
        'R_SAFE': '#ef3b2c',
        'R_LIKELY': '#fb6a4a',
        'R_LEAN': '#fcae91',
        'R_TILT': '#fee8c8',
        'TOSSUP': '#f7f7f7',
        'D_TILT': '#e1f5fe',
        'D_LEAN': '#c6dbef',
        'D_LIKELY': '#9ecae1',
        'D_SAFE': '#6baed6',
        'D_STRONGHOLD': '#3182bd',
        'D_DOMINANT': '#08519c',
        'D_ANNIHILATION': '#08306b'
    }
    
    abs_margin = abs(margin_pct)
    
    if abs_margin < 0.5:
        return {'category': 'Tossup', 'party': 'Even', 'code': 'TOSSUP', 'color': colors['TOSSUP']}
    
    party = 'Republican' if winner == 'REP' else 'Democratic'
    
    if abs_margin >= 40:
        cat = 'Annihilation'
        code = 'R_ANNIHILATION' if winner == 'REP' else 'D_ANNIHILATION'
    elif abs_margin >= 30:
        cat = 'Dominant'
        code = 'R_DOMINANT' if winner == 'REP' else 'D_DOMINANT'
    elif abs_margin >= 20:
        cat = 'Stronghold'
        code = 'R_STRONGHOLD' if winner == 'REP' else 'D_STRONGHOLD'
    elif abs_margin >= 10:
        cat = 'Safe'
        code = 'R_SAFE' if winner == 'REP' else 'D_SAFE'
    elif abs_margin >= 5.5:
        cat = 'Likely'
        code = 'R_LIKELY' if winner == 'REP' else 'D_LIKELY'
    elif abs_margin >= 1:
        cat = 'Lean'
        code = 'R_LEAN' if winner == 'REP' else 'D_LEAN'
    else:
        cat = 'Tilt'
        code = 'R_TILT' if winner == 'REP' else 'D_TILT'
    
    return {
        'category': cat,
        'party': party,
        'code': code,
        'color': colors[code]
    }

def get_margin_category(margin_pct):
    """Calculate political category based on margin percentage"""
    if abs(margin_pct) < 0.5:
        return "Tossup"
    elif 0.5 <= margin_pct < 1:
        return "Tilt Republican"
    elif 1 <= margin_pct < 5.5:
        return "Lean Republican"
    elif 5.5 <= margin_pct < 10:
        return "Likely Republican"
    elif 10 <= margin_pct < 20:
        return "Safe Republican"
    elif 20 <= margin_pct < 30:
        return "Stronghold Republican"
    elif 30 <= margin_pct < 40:
        return "Dominant Republican"
    elif margin_pct >= 40:
        return "Annihilation Republican"
    elif -1 < margin_pct <= -0.5:
        return "Tilt Democratic"
    elif -5.5 < margin_pct <= -1:
        return "Lean Democratic"
    elif -10 < margin_pct <= -5.5:
        return "Likely Democratic"
    elif -20 < margin_pct <= -10:
        return "Safe Democratic"
    elif -30 < margin_pct <= -20:
        return "Stronghold Democratic"
    elif -40 < margin_pct <= -30:
        return "Dominant Democratic"
    elif margin_pct <= -40:
        return "Annihilation Democratic"
    return "Tossup"

def aggregate_alloffice_format(csv_file, year):
    """Aggregate AllOfficeResults format data (2018, 2020, 2022, 2024)"""
    print(f"Processing {csv_file}...")
    
    df = pd.read_csv(csv_file, skipinitialspace=True)
    df.columns = [col.strip().strip('"') for col in df.columns]
    
    # Check for both "OfficeCategory" and "Office Category" column names
    office_cat_col = None
    if 'OfficeCategory' in df.columns:
        office_cat_col = 'OfficeCategory'
    elif 'Office Category' in df.columns:
        office_cat_col = 'Office Category'
    else:
        print(f"  Warning: '{csv_file}' does not have OfficeCategory or 'Office Category' column. Wrong format for AllOfficeResults.")
        return None
    
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].str.strip().str.strip('"')
    
    statewide_offices = ['US Senator', 'Presidential Electors For US President & Vp', 
                        'Governor & Lieutenant Governor', 'Governor & Lt. Governor',
                        'Secretary Of State', 'Treasurer Of State', 'Auditor Of State', 
                        'Attorney General']
    
    df = df[df[office_cat_col].isin(statewide_offices)]
    
    if len(df) == 0:
        print(f"  No statewide races found")
        return {}
    
    # Handle different column name formats
    county_col = 'ReportingCountyName' if 'ReportingCountyName' in df.columns else 'Reporting County Name'
    office_col = 'Office'
    ballot_col = 'NameonBallot' if 'NameonBallot' in df.columns else 'Name on Ballot'
    party_col = 'PoliticalParty' if 'PoliticalParty' in df.columns else 'Political Party'
    votes_col = 'TotalVotes' if 'TotalVotes' in df.columns else 'Total Votes'
    
    df[votes_col] = pd.to_numeric(df[votes_col], errors='coerce').fillna(0).astype(int)
    aggregated = df.groupby([county_col, office_col, ballot_col, party_col])[votes_col].sum().reset_index()
    
    result = {}
    for office in aggregated[office_col].unique():
        office_data = aggregated[aggregated[office_col] == office]
        contest_key = f"{office} ({year})"
        counties = {}
        
        for county in office_data[county_col].unique():
            # Normalize county name to match GeoJSON
            normalized_county = normalize_county_name(county)
            county_data = office_data[office_data[county_col] == county]
            
            # Build all_parties dict and get top candidates
            all_parties = {}
            dem_votes = 0
            rep_votes = 0
            dem_candidate = None
            rep_candidate = None
            other_votes = 0
            
            for _, row in county_data.iterrows():
                votes = int(row[votes_col])
                party = row[party_col]
                
                if party in ['Democratic', 'Democrat', 'DEM']:
                    dem_votes += votes
                    if dem_candidate is None:
                        dem_candidate = row[ballot_col]
                    all_parties['DEM'] = dem_votes
                elif party in ['Republican', 'REP']:
                    rep_votes += votes
                    if rep_candidate is None:
                        rep_candidate = row[ballot_col]
                    all_parties['REP'] = rep_votes
                elif party in ['Libertarian', 'LIB']:
                    other_votes += votes
                    all_parties['LIB'] = all_parties.get('LIB', 0) + votes
                else:
                    other_votes += votes
                    if party not in all_parties:
                        all_parties[party] = 0
                    all_parties[party] += votes
            
            total_votes = dem_votes + rep_votes + other_votes
            two_party_total = dem_votes + rep_votes
            
            if two_party_total > 0:
                margin = rep_votes - dem_votes
                margin_pct = round((margin / two_party_total) * 100, 2)
                winner = 'REP' if rep_votes > dem_votes else 'DEM'
            else:
                margin = 0
                margin_pct = 0
                winner = 'TIE'
            
            counties[normalized_county] = {
                'county': normalized_county,
                'contest': contest_key,
                'year': str(year),
                'dem_candidate': dem_candidate or 'N/A',
                'rep_candidate': rep_candidate or 'N/A',
                'dem_votes': dem_votes,
                'rep_votes': rep_votes,
                'other_votes': other_votes,
                'total_votes': total_votes,
                'two_party_total': two_party_total,
                'margin': margin,
                'margin_pct': margin_pct,
                'winner': winner,
                'competitiveness': get_competitiveness_info(margin_pct, winner),
                'all_parties': all_parties
            }
        
        result[contest_key] = counties
    
    print(f"  Found {len(result)} statewide races")
    return result

def aggregate_openelections_data(csv_file, year):
    """Aggregate OpenElections format data"""
    print(f"Processing {csv_file}...")
    
    df = pd.read_csv(csv_file)
    statewide_offices = ['President', 'U.S. Senate', 'U.S. Senator', 'Governor', 'Secretary Of State',
                        'Secretary of State', 'Treasurer Of State', 'Treasurer of State',
                        'Auditor Of State', 'Auditor of State', 'Attorney General']
    
    df = df[df['office'].isin(statewide_offices)]
    
    if len(df) == 0:
        print(f"  No statewide races found")
        return {}
    
    df['votes'] = pd.to_numeric(df['votes'], errors='coerce').fillna(0).astype(int)
    
    result = {}
    for office in df['office'].unique():
        office_data = df[df['office'] == office]
        contest_key = f"{office} ({year})"
        counties = {}
        
        for county in office_data['county'].unique():
            # Normalize county name to match GeoJSON
            normalized_county = normalize_county_name(county)
            county_data = office_data[office_data['county'] == county]
            
            all_parties = {}
            dem_votes = 0
            rep_votes = 0
            dem_candidate = None
            rep_candidate = None
            other_votes = 0
            
            for _, row in county_data.iterrows():
                votes = int(row['votes'])
                party = row['party']
                candidate = row['candidate']
                
                if party in ['Democratic', 'Democrat', 'DEM']:
                    dem_votes += votes
                    if dem_candidate is None:
                        dem_candidate = candidate
                    all_parties['DEM'] = dem_votes
                elif party in ['Republican', 'REP']:
                    rep_votes += votes
                    if rep_candidate is None:
                        rep_candidate = candidate
                    all_parties['REP'] = rep_votes
                elif party in ['Libertarian', 'LIB']:
                    other_votes += votes
                    all_parties['LIB'] = all_parties.get('LIB', 0) + votes
                else:
                    other_votes += votes
                    if party not in all_parties:
                        all_parties[party] = 0
                    all_parties[party] += votes
            
            total_votes = dem_votes + rep_votes + other_votes
            two_party_total = dem_votes + rep_votes
            
            if two_party_total > 0:
                margin = rep_votes - dem_votes
                margin_pct = round((margin / two_party_total) * 100, 2)
                winner = 'REP' if rep_votes > dem_votes else 'DEM'
            else:
                margin = 0
                margin_pct = 0
                winner = 'TIE'
            
            counties[normalized_county] = {
                'county': normalized_county,
                'contest': contest_key,
                'year': str(year),
                'dem_candidate': dem_candidate or 'N/A',
                'rep_candidate': rep_candidate or 'N/A',
                'dem_votes': dem_votes,
                'rep_votes': rep_votes,
                'other_votes': other_votes,
                'total_votes': total_votes,
                'two_party_total': two_party_total,
                'margin': margin,
                'margin_pct': margin_pct,
                'winner': winner,
                'competitiveness': get_competitiveness_info(margin_pct, winner),
                'all_parties': all_parties
            }
        
        result[contest_key] = counties
    
    print(f"  Found {len(result)} statewide races")
    return result

def aggregate_multiple_precinct_files(precinct_files, year):
    """Aggregate multiple precinct-level files"""
    print(f"Aggregating {len(precinct_files)} precinct files for {year}...")
    
    all_dfs = []
    for pf in precinct_files:
        try:
            df = pd.read_csv(pf)
            all_dfs.append(df)
        except Exception as e:
            print(f"  Error reading {pf.name}: {e}")
    
    if not all_dfs:
        return {}
    
    combined_df = pd.concat(all_dfs, ignore_index=True)
    statewide_offices = ['President', 'U.S. Senate', 'Governor', 'Secretary Of State',
                        'Secretary of State', 'Treasurer Of State', 'Treasurer of State',
                        'Auditor Of State', 'Auditor of State', 'Attorney General']
    
    combined_df = combined_df[combined_df['office'].isin(statewide_offices)]
    
    if len(combined_df) == 0:
        print(f"  No statewide races found")
        return {}
    
    combined_df['votes'] = pd.to_numeric(combined_df['votes'], errors='coerce').fillna(0).astype(int)
    aggregated = combined_df.groupby(['county', 'office', 'candidate', 'party'])['votes'].sum().reset_index()
    
    result = {}
    for office in aggregated['office'].unique():
        office_data = aggregated[aggregated['office'] == office]
        contest_key = f"{office} ({year})"
        counties = {}
        
        for county in office_data['county'].unique():
            # Normalize county name to match GeoJSON
            normalized_county = normalize_county_name(county)
            county_data = office_data[office_data['county'] == county]
            
            all_parties = {}
            dem_votes = 0
            rep_votes = 0
            dem_candidate = None
            rep_candidate = None
            other_votes = 0
            
            for _, row in county_data.iterrows():
                votes = int(row['votes'])
                party = row['party']
                candidate = row['candidate']
                
                if party in ['Democratic', 'Democrat', 'DEM']:
                    dem_votes += votes
                    if dem_candidate is None:
                        dem_candidate = candidate
                    all_parties['DEM'] = dem_votes
                elif party in ['Republican', 'REP']:
                    rep_votes += votes
                    if rep_candidate is None:
                        rep_candidate = candidate
                    all_parties['REP'] = rep_votes
                elif party in ['Libertarian', 'LIB']:
                    other_votes += votes
                    all_parties['LIB'] = all_parties.get('LIB', 0) + votes
                else:
                    other_votes += votes
                    if party not in all_parties:
                        all_parties[party] = 0
                    all_parties[party] += votes
            
            total_votes = dem_votes + rep_votes + other_votes
            two_party_total = dem_votes + rep_votes
            
            if two_party_total > 0:
                margin = rep_votes - dem_votes
                margin_pct = round((margin / two_party_total) * 100, 2)
                winner = 'REP' if rep_votes > dem_votes else 'DEM'
            else:
                margin = 0
                margin_pct = 0
                winner = 'TIE'
            
            counties[normalized_county] = {
                'county': normalized_county,
                'contest': contest_key,
                'year': str(year),
                'dem_candidate': dem_candidate or 'N/A',
                'rep_candidate': rep_candidate or 'N/A',
                'dem_votes': dem_votes,
                'rep_votes': rep_votes,
                'other_votes': other_votes,
                'total_votes': total_votes,
                'two_party_total': two_party_total,
                'margin': margin,
                'margin_pct': margin_pct,
                'winner': winner,
                'competitiveness': get_competitiveness_info(margin_pct, winner),
                'all_parties': all_parties
            }
        
        result[contest_key] = counties
    
    print(f"  Found {len(result)} statewide races")
    return result

def main():
    data_dir = Path('data')
    year_folders = ['2002', '2004', '2006', '2008', '2010', '2012', '2014', '2016', '2018', '2020', '2022', '2024']
    all_results = {}
    
    for year_str in year_folders:
        year_path = data_dir / year_str
        
        # Check for AllOfficeResults format (2020, 2022, 2024)
        alloffice_file = data_dir / f'AllOfficeResults-{year_str}.csv'
        if not alloffice_file.exists():
            alloffice_file = data_dir / f'AllOfficeResults{year_str}.csv'
        
        if alloffice_file.exists():
            year = int(year_str)
            year_data = aggregate_alloffice_format(alloffice_file, year)
            if year_data:  # Only update if we got valid data
                if year not in all_results:
                    all_results[year] = {}
                all_results[year].update(year_data)
            continue
        
        if not year_path.exists():
            continue
        
        # Find county-level files
        general_files = list(year_path.glob('*__general__county.csv'))
        
        # If no county files, look for precinct files
        if not general_files:
            counties_path = year_path / 'counties'
            if counties_path.exists():
                precinct_files = list(counties_path.glob('*__general__*__precinct.csv'))
            else:
                precinct_files = list(year_path.glob('*__general__*__precinct.csv'))
            
            if precinct_files:
                year = int(year_str)
                year_data = aggregate_multiple_precinct_files(precinct_files, year)
                if year not in all_results:
                    all_results[year] = {}
                all_results[year].update(year_data)
                continue
        
        for csv_file in general_files:
            year = int(csv_file.name[:4])
            year_data = aggregate_openelections_data(csv_file, year)
            if year not in all_results:
                all_results[year] = {}
            all_results[year].update(year_data)
    
    # Filter out uncontested races (where one major party has < 1% of two-party vote)
    for year in list(all_results.keys()):
        for contest_name in list(all_results[year].keys()):
            contest_data = all_results[year][contest_name]
            total_dem = sum(county['dem_votes'] for county in contest_data.values())
            total_rep = sum(county['rep_votes'] for county in contest_data.values())
            two_party_total = total_dem + total_rep
            
            # Remove contest if either party has < 1% of two-party vote
            if two_party_total > 0:
                dem_pct = (total_dem / two_party_total) * 100
                rep_pct = (total_rep / two_party_total) * 100
                if dem_pct < 1.0 or rep_pct < 1.0:
                    print(f"  Excluding uncontested race: {contest_name} (Dem: {dem_pct:.1f}%, Rep: {rep_pct:.1f}%)")
                    del all_results[year][contest_name]
    
    # Build final structure with metadata
    from datetime import datetime
    
    final_output = {
        "meta": {
            "years_covered": [str(y) for y in sorted(all_results.keys())],
            "exclusions": ["Congressional districts (gerrymandered)", "State legislature districts"],
            "focus": "Statewide Indiana elections - clean geographic political patterns",
            "processed_date": datetime.now().strftime("%Y-%m-%d")
        },
        "results_by_year": {}
    }
    
    # Reorganize: Year -> Contest -> Counties
    for year in sorted(all_results.keys()):
        year_str = str(year)
        final_output["results_by_year"][year_str] = all_results[year]
    
    output_file = data_dir / 'indiana_election_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_output, f, indent=2)
    
    print(f"\n✓ Aggregated data saved to {output_file}")
    print(f"✓ Years included: {sorted(all_results.keys())}")
    
    for year in sorted(all_results.keys()):
        data = all_results[year]
        print(f"\n{year}:")
        for contest_name in sorted(data.keys()):
            num_counties = len(data[contest_name])
            print(f"  • {contest_name}: {num_counties} counties")

if __name__ == '__main__':
    main()
