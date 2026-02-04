# Data Dictionary (Synthetic)


## shipments.csv
- shipment_id (str)
- customer_id (str)
- carrier_id (str)
- origin_warehouse_id (str)
- destination_zone (int 1-8)
- origin_region (str)
- destination_region (str)
- mode (str: PARCEL, LTL)
- service_level (str: ECONOMY, STANDARD, EXPEDITED)
- ship_date (date)
- promised_date (date)
- delivered_date (date)
- distance_miles (float)
- weight_lb (float)
- volume_cuft (float)
- pieces (int)
- is_fragile (0/1)
- is_hazmat (0/1)
- weather_disruption (0/1)
- peak_season (0/1)
- base_cost (float)
- fuel_surcharge (float)
- accessorial_cost (float)
- total_cost (float)
- on_time (0/1)
- days_late (int; 0 if on-time)


## events.csv
- shipment_id (str)
- event_time (timestamp)
- event_type (str: CREATED, PICKED_UP, ARRIVED_SORT, DEPARTED_SORT, OUT_FOR_DELIVERY, DELIVERED)
- facility_id (str; warehouse or sort center)


## carriers.csv
- carrier_id (str)
- carrier_name (str)
- mode (PARCEL or LTL)
- reliability_score (float 0-1)
- cost_index (float; >1 means more expensive)


## warehouses.csv
- warehouse_id (str)
- region (str)
- capacity_index (float)


## customers.csv
- customer_id (str)
- industry (str)
- sla_tier (str: GOLD, SILVER, BRONZE)


## lanes.csv
- origin_region
- destination_region
- typical_distance_miles