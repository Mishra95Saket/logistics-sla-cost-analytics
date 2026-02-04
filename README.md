### @author - Saket Mishra

## Business Questions Answered


1) **Where are we missing SLAs and why?**
- On-time delivery (OTD %) by lane (origin→destination), service level, carrier, and warehouse.
- Identify “hot lanes” and “hot facilities” driving late deliveries.


2) **What are the biggest drivers of shipping cost?**
- Cost per shipment and per mile by mode, carrier, zone, weight/volume, and accessorials.
- Quantify contributions using regression + SHAP.


3) **How efficient are our warehouses (dwell time & throughput)?**
- Dock-to-ship dwell time distribution and bottlenecks.
- Inbound/outbound throughput, backlog risk, and peak-day behavior.


4) **Which shipments are high-risk for delay before dispatch?**
- Predict delay risk (classification) using features available at dispatch.
- Provide an actionable “delay risk score” for operations triage.


## Data (Synthetic)
This repo does **not** use open-source datasets.


Generated tables:
- `shipments.csv` — order & shipment facts
- `events.csv` — shipment status events (pickup, sort, out-for-delivery, delivered)
- `warehouses.csv`, `carriers.csv`, `customers.csv`, `lanes.csv`


See `data/README.md` for schema and definitions.


## Quickstart


### Option A — Conda (recommended)
```bash
conda env create -f environment.yml
conda activate logistics-ops
python -m src.00_generate_data
python -m src.01_validate_and_clean
python -m src.02_kpi_analytics
python -m src.03_root_cause_analysis
python -m src.04_model_delay_risk
python -m src.05_forecast_volume


### Option B-pip
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m src.00_generate_data
python -m src.01_validate_and_clean
python -m src.02_kpi_analytics
python -m src.03_root_cause_analysis
python -m src.04_model_delay_risk
python -m src.05_forecast_volume


### Assumptions
Seasonality (weekly + monthly + holiday spikes)
Capacity constraints & congestion
Weather disruptions (random regional storms)
Carrier-specific reliability
Accessorial charges


Next Steps
Add a BI layer: publish KPIs to Power BI/Tableau with a star schema.
Causal analysis: apply causal inference (DoWhy/EconML) to estimate impact of carrier changes or warehouse staffing.
Optimization: route & carrier assignment optimization (MILP) using cost + SLA risk.
Streaming simulation: generate event streams and build near-real-time SLA monitoring.
Data quality gates: Great Expectations checks + automated anomaly detection.
