from __future__ import annotations


from dataclasses import dataclass
from pathlib import Path
import pandas as pd




@dataclass(frozen=True)
class Paths:
raw_dir: Path
processed_dir: Path
reports_dir: Path
figures_dir: Path




def ensure_dirs(paths: Paths) -> None:
for p in [paths.raw_dir, paths.processed_dir, paths.reports_dir, paths.figures_dir]:
p.mkdir(parents=True, exist_ok=True)




def write_df(df: pd.DataFrame, path: Path, fmt: str = "csv") -> None:
path.parent.mkdir(parents=True, exist_ok=True)
if fmt == "csv":
df.to_csv(path, index=False)
elif fmt == "parquet":
df.to_parquet(path, index=False)
else:
raise ValueError(f"Unsupported format: {fmt}")




def read_df(path: Path) -> pd.DataFrame:
if path.suffix.lower() == ".csv":
return pd.read_csv(path)
if path.suffix.lower() in {".parquet", ".pq"}:
return pd.read_parquet(path)
raise ValueError(f"Unsupported file type: {path.suffix}")