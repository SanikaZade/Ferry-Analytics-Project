# Real-Time Ferry Ticket Sales & Redemption Analytics — Toronto Island Park

Complete project package for Toronto Government — Parks, Forestry & Recreation.

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
