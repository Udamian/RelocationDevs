"""
model.py
Pipeline de prediccion salarial con scikit-learn.
"""

import joblib
import pandas as pd
from pathlib import Path
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

MODELS_DIR          = Path(__file__).parent.parent / "models"
CATEGORICAL_FEATURES = ["role", "specialization", "city_name", "education_level"]
NUMERICAL_FEATURES   = ["years_experience"]


def build_preprocessor() -> ColumnTransformer:
    return ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL_FEATURES),
        ("num", StandardScaler(), NUMERICAL_FEATURES),
    ])


def build_pipeline(model_type: str = "gbr") -> Pipeline:
    estimator = (
        GradientBoostingRegressor(n_estimators=100, random_state=42)
        if model_type == "gbr" else LinearRegression()
    )
    return Pipeline([("preprocessor", build_preprocessor()), ("model", estimator)])


def train(df: pd.DataFrame, target: str = "gross_salary", model_type: str = "gbr") -> dict:
    X = df[CATEGORICAL_FEATURES + NUMERICAL_FEATURES]
    y = df[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    pipeline = build_pipeline(model_type)
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    metrics = {
        "mae": round(mean_absolute_error(y_test, y_pred), 2),
        "r2":  round(r2_score(y_test, y_pred), 4),
    }
    save_model(pipeline)
    return metrics


def save_model(pipeline: Pipeline, name: str = "salary_model.pkl") -> None:
    joblib.dump(pipeline, MODELS_DIR / name)
    print(f"Modelo guardado: {MODELS_DIR / name}")


def load_model(name: str = "salary_model.pkl") -> Pipeline:
    path = MODELS_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Modelo no encontrado: {path}")
    return joblib.load(path)


def predict(profile: dict) -> float:
    pipeline = load_model()
    return round(float(pipeline.predict(pd.DataFrame([profile]))[0]), 2)
