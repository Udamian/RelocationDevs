import pandas as pd
df = pd.read_csv('data/processed/cities_processed.csv')
us = df[df['country'] == 'United States'].sort_values('relocation_score', ascending=False)
print(us[['city_name', 'relocation_score']].head(15).to_string())
