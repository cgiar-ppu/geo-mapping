import pandas as pd
import json

# Load the Excel files
df_countries_map = pd.read_excel("Countries Map 2.xlsx")
df_priority_countries = pd.read_excel("Priority Countries 2.xlsx")

# Load the GeoJSON file
with open("geojson.json") as f:
    geojson = json.load(f)

# Get all unique countries from both Excel files, excluding null values
excel_countries = set(df_countries_map['Country'].dropna().unique()) | set(df_priority_countries['Country'].dropna().unique())

# Get all country names from GeoJSON
geojson_countries = {feature['properties']['name'] for feature in geojson['features']}

# Find countries in Excel files that don't match GeoJSON names
mismatched_countries = excel_countries - geojson_countries

print("\nAnalysis of country name mismatches:")
print("=====================================")

if mismatched_countries:
    print("\nThe following countries from your Excel files don't match the map's country names:")
    for country in sorted(mismatched_countries):
        print(f"- {country}")
    
    print("\nPossible matches in GeoJSON:")
    print("----------------------------")
    # For each mismatched country, try to find similar names in GeoJSON
    for country in sorted(mismatched_countries):
        possible_matches = [gc for gc in geojson_countries 
                          if country.lower() in gc.lower() or 
                          gc.lower() in country.lower()]
        if possible_matches:
            print(f"\nFor '{country}', consider these possible matches:")
            for match in sorted(possible_matches):
                print(f"  - {match}")
else:
    print("No country name mismatches found!")

print("\nSummary:")
print(f"Total countries in Excel files: {len(excel_countries)}")
print(f"Total countries in GeoJSON: {len(geojson_countries)}")
print(f"Total mismatches found: {len(mismatched_countries)}")

# Print all GeoJSON country names for reference
print("\nAll available country names in GeoJSON:")
print("=====================================")
for country in sorted(geojson_countries):
    print(f"- {country}") 