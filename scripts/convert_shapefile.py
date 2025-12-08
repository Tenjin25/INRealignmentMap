"""
Convert Indiana counties shapefile to GeoJSON format
"""
import geopandas as gpd
import json
from pathlib import Path

# Paths
input_shp = Path('data/tl_2020_18_county20/tl_2020_18_county20.shp')
output_geojson = Path('data/tl_2020_18_county20.geojson')

print(f"Reading shapefile: {input_shp}")
# Read the shapefile
gdf = gpd.read_file(input_shp)

# Display info about the data
print(f"\nShapefile Info:")
print(f"  - Number of counties: {len(gdf)}")
print(f"  - CRS: {gdf.crs}")
print(f"  - Columns: {list(gdf.columns)}")

# Reproject to WGS84 (EPSG:4326) for web mapping
if gdf.crs != "EPSG:4326":
    print(f"\nReprojecting from {gdf.crs} to EPSG:4326 (WGS84)...")
    gdf = gdf.to_crs("EPSG:4326")

# Show sample of county names
print(f"\nSample county names:")
name_col = 'NAME' if 'NAME' in gdf.columns else 'NAMELSAD' if 'NAMELSAD' in gdf.columns else gdf.columns[0]
print(gdf[name_col].head(10).tolist())

# Export to GeoJSON
print(f"\nExporting to GeoJSON: {output_geojson}")
gdf.to_file(output_geojson, driver='GeoJSON')

# Verify the output
print(f"\n✓ GeoJSON created successfully!")
print(f"  - Feature count: {len(gdf)}")
print(f"  - File size: {output_geojson.stat().st_size / 1024:.2f} KB")
print(f"  - Output: {output_geojson.absolute()}")
