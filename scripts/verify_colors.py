"""
Verify color coding consistency in Indiana election data.

This script checks:
1. All competitiveness categories have correct colors assigned
2. Color scale is consistent across all years
3. No missing or mismatched color codes
"""

import json
from pathlib import Path

# Define the expected color mapping
EXPECTED_COLORS = {
    # Republican colors (red scale)
    "R_ANNIHILATION": "#67000d",
    "R_DOMINANT": "#a50f15",
    "R_STRONGHOLD": "#cb181d",
    "R_SAFE": "#ef3b2c",
    "R_LIKELY": "#fb6a4a",
    "R_LEAN": "#fcae91",
    "R_TILT": "#fee8c8",
    
    # Tossup
    "TOSSUP": "#f7f7f7",
    
    # Democratic colors (blue scale)
    "D_TILT": "#e1f5fe",
    "D_LEAN": "#c6dbef",
    "D_LIKELY": "#9ecae1",
    "D_SAFE": "#6baed6",
    "D_STRONGHOLD": "#3182bd",
    "D_DOMINANT": "#08519c",
    "D_ANNIHILATION": "#08306b"
}

# Full category names
CATEGORY_NAMES = {
    "R_ANNIHILATION": "Annihilation Republican",
    "R_DOMINANT": "Dominant Republican",
    "R_STRONGHOLD": "Stronghold Republican",
    "R_SAFE": "Safe Republican",
    "R_LIKELY": "Likely Republican",
    "R_LEAN": "Lean Republican",
    "R_TILT": "Tilt Republican",
    "TOSSUP": "Tossup",
    "D_TILT": "Tilt Democratic",
    "D_LEAN": "Lean Democratic",
    "D_LIKELY": "Likely Democratic",
    "D_SAFE": "Safe Democratic",
    "D_STRONGHOLD": "Stronghold Democratic",
    "D_DOMINANT": "Dominant Democratic",
    "D_ANNIHILATION": "Annihilation Democratic"
}

def verify_colors():
    """Verify color coding in the election data JSON."""
    
    data_file = Path('data/indiana_election_results.json')
    
    if not data_file.exists():
        print(f"❌ Error: {data_file} not found")
        return False
    
    print("🔍 Verifying color coding in Indiana election data...\n")
    
    with open(data_file, 'r') as f:
        data = json.load(f)
    
    all_valid = True
    color_usage = {code: 0 for code in EXPECTED_COLORS.keys()}
    mismatches = []
    
    # Check each year
    for year, year_data in data['results_by_year'].items():
        for contest, contest_data in year_data.items():
            for county, county_data in contest_data.items():
                if county == 'Statewide':
                    continue
                
                comp = county_data.get('competitiveness', {})
                code = comp.get('code')
                color = comp.get('color')
                category = comp.get('category')
                party = comp.get('party')
                
                if code:
                    color_usage[code] = color_usage.get(code, 0) + 1
                
                # Verify color matches expected
                if code and code in EXPECTED_COLORS:
                    expected_color = EXPECTED_COLORS[code]
                    if color != expected_color:
                        mismatches.append({
                            'year': year,
                            'contest': contest,
                            'county': county,
                            'code': code,
                            'expected': expected_color,
                            'actual': color
                        })
                        all_valid = False
                elif code:
                    print(f"⚠️  Unknown code: {code} in {year} {contest} {county}")
                    all_valid = False
    
    # Print results
    if mismatches:
        print("❌ COLOR MISMATCHES FOUND:\n")
        for m in mismatches[:10]:  # Show first 10
            print(f"  {m['year']} - {m['contest']} - {m['county']}")
            print(f"    Code: {m['code']}")
            print(f"    Expected: {m['expected']}")
            print(f"    Actual: {m['actual']}\n")
        
        if len(mismatches) > 10:
            print(f"  ... and {len(mismatches) - 10} more mismatches\n")
    
    # Print color usage statistics
    print("\n📊 COLOR USAGE STATISTICS:\n")
    print(f"{'Category':<30} {'Code':<20} {'Color':<10} {'Count':>6}")
    print("-" * 70)
    
    for code in sorted(EXPECTED_COLORS.keys(), key=lambda x: (
        0 if x == "TOSSUP" else (
            1 if x.startswith("R_") else 2
        ),
        x
    )):
        name = CATEGORY_NAMES.get(code, code)
        color = EXPECTED_COLORS[code]
        count = color_usage.get(code, 0)
        print(f"{name:<30} {code:<20} {color:<10} {count:>6}")
    
    print("\n" + "=" * 70)
    
    if all_valid:
        print("✅ All colors are correctly assigned!")
    else:
        print(f"❌ Found {len(mismatches)} color mismatches")
    
    print("\n🎨 Expected Color Scale:")
    print("  Republican: #67000d → #a50f15 → #cb181d → #ef3b2c → #fb6a4a → #fcae91 → #fee8c8")
    print("  Tossup:     #f7f7f7")
    print("  Democratic: #e1f5fe → #c6dbef → #9ecae1 → #6baed6 → #3182bd → #08519c → #08306b")
    
    return all_valid

def main():
    try:
        success = verify_colors()
        exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

if __name__ == '__main__':
    main()
