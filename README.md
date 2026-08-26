# Real-Time Ferry Ticket Sales & Redemption Analytics — Toronto Island Park

Ferries are the only public access route to the Toronto Islands, running year-round from the Jack Layton Ferry Terminal to Centre Island, Hanlan's Point, and Ward's Island. Ticket sales and redemptions have long been logged every 15 minutes — but until now, that data sat unused, with no centralized system to answer basic operational questions: When is demand highest? How many people are actually on the grounds right now? Where should staff and vessels be deployed?

This project builds that missing analytics layer, covering the full pipeline from raw CSV to a decision-ready dashboard:

261,538 interval records, May 2015 → December 2025
12.97M ticket sales and 12.79M redemptions analyzed
Zero missing values; outliers statistically identified, not blindly removed

## 🔬 Methodology
1. Data Ingestion
Load the raw CSV (_id, Timestamp, Sales Count, Redemption Count)
Parse Timestamp to native datetime objects
Sort chronologically to guarantee correct time-series behavior

2. Data Cleaning
Missing timestamps — detected and dropped, count reported live in the dashboard
Outlier detection — IQR method (values beyond Q3 + 3×IQR flagged, not silently removed — inspection shows they reflect genuine high-season spikes, not data errors)
Consistency checks — interval-spacing validation confirms the expected 15-minute cadence during operating hours

All three cleaning steps are surfaced live in the dashboard's Data Quality tab — not just described in a report — so the pipeline is auditable, not a black box.

3. Feature Engineering
Feature	Derivation
Hour of day	Timestamp.dt.hour
Day of week	Timestamp.dt.day_name()
Weekend flag	dayofweek >= 5
Month / Season	Timestamp.dt.month → mapped to Winter/Spring/Summer/Fall
Net Passenger Movement	Sales Count − Redemption Count

4. Exploratory Data Analysis
Hourly & daily demand curves
Seasonal comparison (summer accounts for 64.3% of annual volume vs. 3.4% in winter)
Sales-vs-redemption distribution analysis
1-hour and 4-hour rolling averages (toggle between Sales / Redemptions)

5. Key Performance Indicators
Tickets Sold per Hour / Tickets Redeemed per Hour
Net Passenger Movement (Sales − Redemptions)
Peak Demand Window (daily peak: 11:00–14:00; weekly peak: Sat–Sun; seasonal peak: Jun–Aug)
Off-Season Utilization Index — off-peak demand as a % of summer peak

## 📊 Dashboard Modules
Time-Series — raw / hourly / daily views with rolling averages
Peak vs Off-Peak — hourly bar chart, day-of-week comparison, hour×day heatmap
Seasonal Trends — monthly line trend, seasonal pie split, weekday vs weekend, distribution histogram
Data Explorer — filtered record table with CSV export
Data Quality — live cleaning summary, outlier detection, interval-consistency table
Live Feed Simulator — replays the most recent intervals to approximate a near real-time operational view

Filters: date range, hour of day, year, season, weekday/weekend User roles: Operations Team · Policy Planner · Management Stakeholder — each gets a tailored insight panel

## Folder structure
```
Ferry_Analytics_Project/
├── dashboard/                              -> Streamlit web app (interactive analytics)
│   ├── app.py
│   ├── requirements.txt
│   ├── .streamlit/config.toml              -> forces light theme
│   ├── Toronto_Island_Ferry_Tickets.csv    -> source dataset (2015-2025)
│   └── README.md
├── reports/                                -> written deliverables
│   ├── Ferry_Analytics_Research_Paper.docx    -> includes 3 embedded charts
│   └── Ferry_Analytics_Executive_Summary.docx
└── README.md                               -> this file
```

## Quick start (dashboard)
```bash
cd dashboard
pip install -r requirements.txt
streamlit run app.py
```
##  🧰 Tech Stack
Layer	Tool	Purpose
Language	Python 3.10+	Core data processing & app logic
Web framework	Streamlit	Interactive dashboard, filters, tabs, session state
Data processing	Pandas	CSV ingestion, cleaning, resampling, groupby aggregation
Numerical ops	NumPy	Statistical calculations (IQR, means, thresholds)
Visualization	Plotly (express + graph_objects)	Interactive time-series, bar, heatmap, pie charts
Report generation	python-docx / docx.js	Research paper & executive summary as Word documents
Charting for reports	Matplotlib	Static publication-quality figures embedded in the research paper
Deployment	Streamlit Community Cloud	Free, zero-config hosting directly from GitHub
Config	.streamlit/config.toml	Forces a consistent light theme for all users 

## Requirement coverage
| Brief requirement | Where it's delivered |
|---|---|
| Data Ingestion (load, convert timestamps, sort) | dashboard/app.py `load_data()` |
| Data Cleaning (missing timestamps, outliers, consistency) | app.py `load_data()` logic + **Data Quality tab** |
| Feature Engineering (hour, day of week, month/season, weekend) | app.py `load_data()` |
| EDA (hourly/daily trends, seasonal comparison, distribution, rolling averages) | Time-Series, Peak vs Off-Peak, Seasonal Trends tabs + 3 charts in research paper |
| KPIs (Sold/hr, Redeemed/hr, Net Movement, Peak Windows, Off-Season Index) | KPI cards at top of dashboard |
| Real-time KPI cards | Dashboard header |
| Interactive time-series plots | Time-Series tab |
| Date & time filters | Sidebar (date range, hour, year, season, day type) |
| Peak vs off-peak comparison | Peak vs Off-Peak tab |
| User roles (Operations / Policy / Management) | Sidebar role selector + tailored insight panel |
| Near real-time framing | Live Feed Simulator tab |
| Research paper (EDA, insights, recommendations) | reports/Ferry_Analytics_Research_Paper.docx |
| Executive summary | reports/Ferry_Analytics_Executive_Summary.docx |

## QA notes
- All figures independently re-verified against the raw CSV.
- App smoke-tested by direct script execution and live `streamlit run` — both clean, zero errors.
- Edge cases stress-tested (sparse filters, empty results, tiny datasets) — all handled gracefully.
- Deprecated `use_container_width` replaced with `width='stretch'`; requirements.txt pinned with upper bounds.
- Research paper docx validated with python-docx (strict OOXML parser) after fixing an image
  content-type bug in the chart-embedding step — confirmed 3 images load correctly, no corruption.
