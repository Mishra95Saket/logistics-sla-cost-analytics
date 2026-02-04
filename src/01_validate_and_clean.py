from __future__ import annotations
"shipment_id",
"ship_date",
"promised_date",
"delivered_date",
"total_cost",
"distance_miles",
"on_time",
"days_late",
}
missing = required_cols - set(shipments.columns)
if missing:
raise ValueError(f"Missing required columns: {missing}")


# Parse dates
for c in ["ship_date", "promised_date", "delivered_date"]:
shipments[c] = pd.to_datetime(shipments[c])


# Fix any negative/zero distance
shipments["distance_miles"] = shipments["distance_miles"].astype(float)
shipments.loc[shipments["distance_miles"] <= 0, "distance_miles"] = np.nan


# Recompute on_time/days_late in case of generator changes
late_days = (shipments["delivered_date"] - shipments["promised_date"]).dt.days
late_days = late_days.clip(lower=0)
shipments["days_late"] = late_days.astype(int)
shipments["on_time"] = (shipments["days_late"] == 0).astype(int)


# Add derived columns
shipments["ship_week"] = shipments["ship_date"].dt.to_period("W").astype(str)
shipments["ship_month"] = shipments["ship_date"].dt.to_period("M").astype(str)
shipments["transit_days_actual"] = (shipments["delivered_date"] - shipments["ship_date"]).dt.days.clip(lower=0)
shipments["transit_days_promised"] = (shipments["promised_date"] - shipments["ship_date"]).dt.days.clip(lower=0)


# Dwell approximation from events: CREATED -> DEPARTED_SORT
events["event_time"] = pd.to_datetime(events["event_time"])
created = events[events["event_type"] == "CREATED"].set_index("shipment_id")["event_time"]
departed = events[events["event_type"] == "DEPARTED_SORT"].set_index("shipment_id")["event_time"]
dwell_hours = (departed - created).dt.total_seconds() / 3600.0
shipments = shipments.merge(dwell_hours.rename("dwell_hours"), how="left", left_on="shipment_id", right_index=True)


# Persist processed
write_df(shipments, cfg.paths.processed_dir / f"shipments_processed.{fmt}", fmt)
write_df(events, cfg.paths.processed_dir / f"events_processed.{fmt}", fmt)


print("✅ Clean + feature-enriched data written to data/processed/")




if __name__ == "__main__":
main()