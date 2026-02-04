from __future__ import annotations
}
overall_df = pd.DataFrame([overall])
write_df(overall_df, cfg.paths.reports_dir / f"kpi_overall.{fmt}", fmt)


# SLA performance by lane
lane = (
shipments.groupby(["origin_region", "destination_region", "service_level"], as_index=False)
.agg(shipments=("shipment_id", "count"), otd=("on_time", "mean"), avg_days_late=("days_late", "mean"))
.sort_values(["otd", "shipments"], ascending=[True, False])
)
write_df(lane, cfg.paths.reports_dir / f"kpi_lane_sla.{fmt}", fmt)


# Carrier performance
carrier = (
shipments.groupby(["carrier_id", "mode"], as_index=False)
.agg(shipments=("shipment_id", "count"), otd=("on_time", "mean"), avg_cost=("total_cost", "mean"), avg_days_late=("days_late", "mean"))
.sort_values("otd")
)
write_df(carrier, cfg.paths.reports_dir / f"kpi_carrier.{fmt}", fmt)


# Warehouse efficiency
wh = (
shipments.groupby(["origin_warehouse_id", "origin_region"], as_index=False)
.agg(shipments=("shipment_id", "count"), avg_dwell_hours=("dwell_hours", "mean"), p90_dwell_hours=("dwell_hours", lambda s: s.quantile(0.9)))
.sort_values("p90_dwell_hours", ascending=False)
)
write_df(wh, cfg.paths.reports_dir / f"kpi_warehouse.{fmt}", fmt)


# Trend: weekly OTD
weekly = (
shipments.groupby("ship_week", as_index=False)
.agg(shipments=("shipment_id", "count"), otd=("on_time", "mean"), avg_cost=("total_cost", "mean"))
)
write_df(weekly, cfg.paths.reports_dir / f"kpi_weekly_trend.{fmt}", fmt)


# Figures
save_bar(
carrier.assign(otd_pct=carrier["otd"] * 100),
x="carrier_id",
y="otd_pct",
title="On-Time Delivery % by Carrier",
outpath=cfg.paths.figures_dir / "otd_by_carrier.png",
)


save_bar(
wh,
x="origin_warehouse_id",
y="p90_dwell_hours",
title="P90 Dwell Hours by Origin Warehouse",
outpath=cfg.paths.figures_dir / "p90_dwell_by_warehouse.png",
)


save_line(
weekly,
x="ship_week",
y="otd",
title="Weekly On-Time Delivery Trend",
outpath=cfg.paths.figures_dir / "weekly_otd_trend.png",
)


print("✅ KPI analytics complete. See reports/outputs and reports/figures")




if __name__ == "__main__":
main()