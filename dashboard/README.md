# Toronto Island Ferry Analytics Dashboard

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

The `.streamlit/config.toml` file forces the light theme by default.
`Toronto_Island_Ferry_Tickets.csv` is already included in this folder.

## Dashboard tabs
1. **Time-Series** — raw/hourly/daily sales vs redemptions, net movement, 1-hr & 4-hr rolling averages (Sales or Redemptions)
2. **Peak vs Off-Peak** — hourly demand profile, peak/off-peak windows, day-of-week comparison, hour×day heatmap
3. **Seasonal Trends** — monthly trend, seasonal split, weekday vs weekend, sales-vs-redemption distribution
4. **Data Explorer** — filtered record table with CSV export
5. **Data Quality** — data cleaning summary (rows dropped, outliers flagged via IQR), interval-consistency check
6. **Live Feed Simulator** — replays the most recent intervals one at a time to approximate a near real-time view

## KPI cards
- Tickets Sold per Hour / Tickets Redeemed per Hour (with running totals)
- Net Passenger Movement (Sales − Redemptions)
- Peak Demand Window
- Off-Season Utilization Index

## Filters
Date range, hour of day, year, season, weekday/weekend, plus a role selector
(Operations Team / Policy Planner / Management Stakeholder) that adjusts the insight panel.

## Tested with
Python 3, streamlit 1.62.0, pandas 3.0.2, numpy 2.4.4, plotly 6.9.0
(version ranges pinned in requirements.txt to avoid future breaking changes)
