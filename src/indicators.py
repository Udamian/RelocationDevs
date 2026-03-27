"""
indicators.py
Calculo de indicadores derivados y Relocation Score.
"""

import pandas as pd


def estimated_net_salary(gross_salary: float, tax_rate: float) -> float:
    return gross_salary * (1 - tax_rate / 100)


def estimated_purchasing_power(net_salary: float, cost_of_living_index: float) -> float:
    if cost_of_living_index == 0:
        return 0.0
    return net_salary / cost_of_living_index


def estimated_annual_savings(net_salary: float, cost_of_living_index: float,
                              savings_rate: float = 0.3) -> float:
    return net_salary * savings_rate


def relocation_score(row: pd.Series, weights: dict = None) -> float:
    if weights is None:
        weights = {
            "purchasing_power_index": 0.30,
            "job_market_score":       0.25,
            "quality_of_life_index":  0.25,
            "tax_rate_inv":           0.20,
        }
    tax_inv = max(0, 100 - row.get("tax_rate", 0))
    score = (
        row.get("purchasing_power_index", 0) * weights["purchasing_power_index"]
        + row.get("job_market_score",     0) * weights["job_market_score"]
        + row.get("quality_of_life_index",0) * weights["quality_of_life_index"]
        + tax_inv                             * weights["tax_rate_inv"]
    )
    return round(score, 2)


def add_derived_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["net_salary"] = df.apply(
        lambda r: estimated_net_salary(r["average_salary"], r["tax_rate"]), axis=1)
    df["purchasing_power"] = df.apply(
        lambda r: estimated_purchasing_power(r["net_salary"], r["cost_of_living_index"]), axis=1)
    df["annual_savings"] = df.apply(
        lambda r: estimated_annual_savings(r["net_salary"], r["cost_of_living_index"]), axis=1)
    df["relocation_score"] = df.apply(relocation_score, axis=1)
    return df
