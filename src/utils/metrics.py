from __future__ import annotations


import numpy as np
import pandas as pd




def otd_rate(df: pd.DataFrame, on_time_col: str = "on_time") -> float:
"""On-time delivery rate."""
if df.empty:
return float("nan")
return float(np.mean(df[on_time_col].astype(int)))




def weighted_mean(values: pd.Series, weights: pd.Series) -> float:
values = values.astype(float)
weights = weights.astype(float)
denom = weights.sum()
if denom == 0:
return float("nan")
return float((values * weights).sum() / denom)




def cost_per_mile(df: pd.DataFrame) -> float:
if df.empty:
return float("nan")
miles = df["distance_miles"].astype(float).replace(0, np.nan)
return float((df["total_cost"].astype(float) / miles).mean())




def percentiles(series: pd.Series, ps=(0.5, 0.9, 0.95)) -> dict:
s = series.dropna().astype(float)
if s.empty:
return {f"p{int(p*100)}": float("nan") for p in ps}
return {f"p{int(p*100)}": float(np.quantile(s, p)) for p in ps}