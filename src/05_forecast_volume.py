from __future__ import annotations
class Config:
random_seed: int
output_format: str
paths: Paths




def load_config() -> Config:
cfg = yaml.safe_load(Path("configs/config.yaml").read_text())
paths = Paths(
raw_dir=Path(cfg["paths"]["raw_dir"]),
processed_dir=Path(cfg["paths"]["processed_dir"]),
reports_dir=Path(cfg["paths"]["reports_dir"]),
figures_dir=Path(cfg["paths"]["figures_dir"]),
)
return Config(random_seed=int(cfg["random_seed"]), output_format=str(cfg["output_format"]).lower(), paths=paths)




def main() -> None:
cfg = load_config()
ensure_dirs(cfg.paths)
fmt = cfg.output_format


shipments = read_df(cfg.paths.processed_dir / f"shipments_processed.{fmt}")
shipments["ship_date"] = pd.to_datetime(shipments["ship_date"])


daily = shipments.groupby(shipments["ship_date"].dt.date, as_index=False).agg(shipments=("shipment_id", "count"))
daily.rename(columns={"ship_date": "date"}, inplace=True)
daily["date"] = pd.to_datetime(daily["date"])
daily = daily.sort_values("date")


# Simple baseline forecast: seasonal naive (weekly)
daily["dow"] = daily["date"].dt.dayofweek


# Train/test split (last 12 weeks)
cutoff = daily["date"].max() - pd.Timedelta(days=84)
train = daily[daily["date"] <= cutoff].copy()
test = daily[daily["date"] > cutoff].copy()


# Compute average by day-of-week from training
dow_avg = train.groupby("dow")["shipments"].mean().to_dict()
test["forecast"] = test["dow"].map(dow_avg).astype(float)


mape = mean_absolute_percentage_error(test["shipments"], test["forecast"])


report = pd.DataFrame([
{"method": "dow_average_baseline", "test_days": int(len(test)), "mape": float(mape)}
])
write_df(report, cfg.paths.reports_dir / f"forecast_volume_report.{fmt}", fmt)


out = test[["date", "shipments", "forecast"]].copy()
write_df(out, cfg.paths.reports_dir / f"forecast_volume_daily.{fmt}", fmt)


save_line(out, x="date", y="shipments", title="Daily Shipment Volume (Actual) — Test Window", outpath=cfg.paths.figures_dir / "daily_volume_actual.png")
save_line(out, x="date", y="forecast", title="Daily Shipment Volume (Forecast) — Baseline", outpath=cfg.paths.figures_dir / "daily_volume_forecast.png")


print("✅ Volume forecast baseline complete. See forecast_volume_report")




if __name__ == "__main__":
main()