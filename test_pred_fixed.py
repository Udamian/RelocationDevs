import pandas as pd
from src.model import load_model

df = pd.read_csv("data/processed/cities_processed.csv")
profile = {
    "role": "Data Scientist",
    "specialization": "AI/ML",
    "years_experience": 4,
    "education_level": "Bachelor"
}

pipeline = load_model()
pred_df = pd.DataFrame({
    "city_name": df["country"], # The model was trained with countries in the city_name column
    "role": profile["role"],
    "specialization": profile["specialization"],
    "years_experience": profile["years_experience"],
    "education_level": profile["education_level"]
})
df["predicted_salary"] = pipeline.predict(pred_df)

print("CITIES:")
cols = ["city_name", "country", "predicted_salary"]
specific = df[df['city_name'].isin(['Zurich', 'Budapest', 'Geneva', 'Madrid'])]
print(specific[cols].to_string())
