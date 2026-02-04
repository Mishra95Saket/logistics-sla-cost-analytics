from __future__ import annotations
delivered_ts = delivered + pd.to_timedelta(rng.integers(11, 20, size=len(shipments)), unit="h")


created_facility = shipments["origin_warehouse_id"].values
sort_facility = rng.choice(sort_centers, size=len(shipments), replace=True)
delivery_facility = rng.choice(wh_ids, size=len(shipments), replace=True)


events = []
for i, sid in enumerate(shipments["shipment_id"].values):
events.extend(
[
(sid, base_ts[i], "CREATED", created_facility[i]),
(sid, pickup[i], "PICKED_UP", created_facility[i]),
(sid, arrived_sort[i], "ARRIVED_SORT", sort_facility[i]),
(sid, departed_sort[i], "DEPARTED_SORT", sort_facility[i]),
(sid, ofd[i], "OUT_FOR_DELIVERY", delivery_facility[i]),
(sid, delivered_ts[i], "DELIVERED", delivery_facility[i]),
]
)


return pd.DataFrame(events, columns=["shipment_id", "event_time", "event_type", "facility_id"]).sort_values(
["shipment_id", "event_time"]
)




def main() -> None:
cfg = load_config()
rng = np.random.default_rng(cfg.random_seed)
ensure_dirs(cfg.paths)


warehouses_df, carriers_df, customers_df, lanes_df = make_reference_tables(rng)
shipments_df = generate_shipments(cfg, rng, warehouses_df, carriers_df, customers_df, lanes_df)
events_df = generate_events(shipments_df, rng, warehouses_df)


fmt = cfg.output_format


write_df(warehouses_df, cfg.paths.raw_dir / f"warehouses.{fmt}", fmt)
write_df(carriers_df, cfg.paths.raw_dir / f"carriers.{fmt}", fmt)
write_df(customers_df, cfg.paths.raw_dir / f"customers.{fmt}", fmt)
write_df(lanes_df, cfg.paths.raw_dir / f"lanes.{fmt}", fmt)
write_df(shipments_df, cfg.paths.raw_dir / f"shipments.{fmt}", fmt)
write_df(events_df, cfg.paths.raw_dir / f"events.{fmt}", fmt)


print("✅ Synthetic logistics data generated:")
print(f" - {cfg.paths.raw_dir / f'shipments.{fmt}'}")
print(f" - {cfg.paths.raw_dir / f'events.{fmt}'}")




if __name__ == "__main__":
main()