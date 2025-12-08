"""
Download Indiana election data CSV files from OpenElections GitHub
"""
import requests
from pathlib import Path

# GitHub raw content base URL
BASE_URL = "https://raw.githubusercontent.com/openelections/openelections-data-in/master"

# Files to download
files_to_download = [
    # 2020 General Election - Statewide precinct file
    "2020/20201103__in__general__precinct.csv",
    # 2018 General Election - Statewide precinct file  
    "2018/20181106__in__general__precinct.csv",
    # 2016 General Election - County-level file
    "2016/20161108__in__general__county.csv",
    # 2024 Recent counties
    "20241105__in__general__greene__precinct.csv",
    "20241105__in__general__hendricks__precinct.csv",
]

def download_file(file_path, output_dir='data/openelections'):
    """Download a single file from GitHub"""
    url = f"{BASE_URL}/{file_path}"
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Get filename
    filename = file_path.split('/')[-1]
    output_file = output_path / filename
    
    print(f"Downloading: {filename}...", end=' ')
    
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            with open(output_file, 'wb') as f:
                f.write(response.content)
            size_kb = len(response.content) / 1024
            print(f"✓ ({size_kb:.1f} KB)")
            return True
        else:
            print(f"✗ (Status {response.status_code})")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    print("=" * 60)
    print("Downloading Indiana Election Data from OpenElections")
    print("=" * 60)
    print()
    
    success_count = 0
    for file_path in files_to_download:
        if download_file(file_path):
            success_count += 1
    
    print()
    print("=" * 60)
    print(f"✓ Downloaded {success_count}/{len(files_to_download)} files")
    print(f"✓ Files saved to: data/openelections/")
    print("=" * 60)

if __name__ == '__main__':
    main()
