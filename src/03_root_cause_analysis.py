from __future__ import annotations
ct = pd.crosstab(df[col], df["on_time"])
if ct.shape[0] < 2 or ct.shape[1] < 2:
return {"feature": col, "chi2": np.nan, "p_value": np.nan, "dof": np.nan}


chi2, p, dof, _ = chi2_contingency(ct)
return {"feature": col, "chi2": float(chi2), "p_value": float(p), "dof": int(dof)}




def main() -> None:
cfg = load_config()
ensure_dirs(cfg.paths)
fmt = cfg.output_format


shipments = read_df(cfg.paths.processed_dir / f"shipments_processed.{fmt}")


# Define a set of candidate categorical drivers
drivers = [
"carrier_id",
"mode",
"service_level",
"origin_region",
"destination_region",
"destination_zone",
"weather_disruption",
"peak_season",
"is_fragile",
"is_hazmat",
]


tests = [chi_square_on_time(shipments, d) for d in drivers]
tests_df = pd.DataFrame(tests).sort_values("p_value")
write_df(tests_df, cfg.paths.reports_dir / f"rca_chi_square.{fmt}", fmt)


# Segment analysis: top late lanes (with volume threshold)
lane = (
shipments.groupby(["origin_region", "destination_region", "service_level"], as_index=False)
.agg(shipments=("shipment_id", "count"), otd=("on_time", "mean"), avg_days_late=("days_late", "mean"), avg_cost=("total_cost", "mean"))
)
lane = lane[lane["shipments"] >= 500].sort_values(["otd", "shipments"], ascending=[True, False])
write_df(lane.head(50), cfg.paths.reports_dir / f"rca_top_late_lanes.{fmt}", fmt)


# Congestion proxy: dwell vs. late
tmp = shipments[["dwell_hours", "days_late", "on_time", "origin_warehouse_id"]].dropna()
tmp["dwell_bucket"] = pd.cut(tmp["dwell_hours"], bins=[-np.inf, 8, 16, 24, 36, np.inf], labels=["<=8", "8-16", "16-24", "24-36", ">36"])
dwell = tmp.groupby("dwell_bucket", as_index=False).agg(shipments=("on_time", "size"), otd=("on_time", "mean"), avg_days_late=("days_late", "mean"))
write_df(dwell, cfg.paths.reports_dir / f"rca_dwell_vs_late.{fmt}", fmt)


print("✅ Root-cause analysis outputs written to reports/outputs")




if __name__ == "__main__":
main()