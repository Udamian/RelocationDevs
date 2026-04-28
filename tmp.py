import pandas as pd
df = pd.read_csv('data/processed/cities_processed.csv')
us = df[df['country'] == 'United States']
print("Total US cities:", len(us))
print(us[['city_name', 'lat', 'lon']].head(10).to_string())
if 'lat' in df.columns:
    missing_lat = us['lat'].isnull().sum()
    print("US cities missing lat:", missing_lat)
