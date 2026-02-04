from __future__ import annotations


from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd




def save_bar(df: pd.DataFrame, x: str, y: str, title: str, outpath: Path, top_n: int = 15) -> None:
"""Saves a simple bar chart without hard-coding colors."""
outpath.parent.mkdir(parents=True, exist_ok=True)


plot_df = df.sort_values(y, ascending=False).head(top_n)
plt.figure(figsize=(10, 5))
plt.bar(plot_df[x].astype(str), plot_df[y].astype(float))
plt.xticks(rotation=45, ha="right")
plt.title(title)
plt.tight_layout()
plt.savefig(outpath, dpi=160)
plt.close()




def save_line(df: pd.DataFrame, x: str, y: str, title: str, outpath: Path) -> None:
outpath.parent.mkdir(parents=True, exist_ok=True)


plot_df = df.sort_values(x)
plt.figure(figsize=(10, 5))
plt.plot(plot_df[x], plot_df[y])
plt.title(title)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(outpath, dpi=160)
plt.close()