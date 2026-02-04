import pandas as pd
from src.utils.metrics import otd_rate, weighted_mean




def test_otd_rate_basic():
df = pd.DataFrame({"on_time": [1, 0, 1, 1]})
assert abs(otd_rate(df) - 0.75) < 1e-9




def test_weighted_mean_basic():
s = pd.Series([10, 20, 30])
w = pd.Series([1, 2, 3])
assert abs(weighted_mean(s, w) - (10*1 + 20*2 + 30*3) / 6) < 1e-9