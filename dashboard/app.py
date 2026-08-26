"""
Real-Time Ferry Ticket Sales & Redemption Analytics
Toronto Island Park — Streamlit Dashboard
Data source: Toronto Island Ferry Ticket Counts (Jack Layton Ferry Terminal)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, time

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Toronto Island Ferry Analytics",
    page_icon="⛴️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── PREMIUM CSS + PARTICLE ANIMATION ─────────────────────────────────────────
import streamlit.components.v1 as components
components.html("""
<script>
if (!window.parent.document.getElementById('premium-theme-css')) {
  const css = `
*, *::before, *::after { box-sizing: border-box; }
:root {
    --blue: #2563EB; --teal: #0D9488; --amber: #D97706;
    --violet: #7C3AED; --rose: #E11D48;
    --slate: #1E293B; --slate-md: #475569; --slate-lt: #94A3B8;
    --bg: #F8FAFC; --card: #FFFFFF;
    --border: rgba(148,163,184,0.2);
    --shadow: 0 4px 24px rgba(37,99,235,0.08);
    --shadow-h: 0 10px 40px rgba(37,99,235,0.16);
    --r: 16px; --r-sm: 10px;
}
html, body, [data-testid="stApp"], [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    font-family: 'Inter', sans-serif !important;
    color: var(--slate) !important;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] {
    background: linear-gradient(165deg,#1E293B 0%,#0F172A 100%) !important;
    border-right: none !important;
    box-shadow: 4px 0 32px rgba(0,0,0,0.18);
}
[data-testid="stSidebar"] * { color: #CBD5E1 !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #F8FAFC !important; }
[data-testid="stSidebar"] hr  { border-color: rgba(255,255,255,0.08) !important; }
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: #fff; border-radius: 14px; padding: 5px;
    border: 1px solid var(--border);
    box-shadow: 0 2px 10px rgba(37,99,235,0.06); gap: 3px;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    border-radius: 10px !important; font-weight: 600 !important;
    font-size: 0.80rem !important; color: var(--slate-md) !important;
    padding: 8px 16px !important; transition: all .2s ease !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: linear-gradient(135deg,#2563EB,#1D4ED8) !important;
    color: #fff !important;
    box-shadow: 0 4px 14px rgba(37,99,235,0.38) !important;
}
[data-testid="stTabs"] [data-baseweb="tab-highlight"] { display: none; }
[data-testid="stMetricValue"] { color: var(--slate) !important; font-weight:700 !important; }
.kpi-card {
    background: var(--card); border: 1px solid var(--border);
    border-radius: var(--r); padding: 22px 24px;
    box-shadow: var(--shadow); position: relative; overflow: hidden;
    transition: transform .25s ease, box-shadow .25s ease;
}
.kpi-card::before {
    content:''; position:absolute; top:0; left:0; right:0; height:3px;
    background: linear-gradient(90deg,var(--blue),var(--teal));
    border-radius: var(--r) var(--r) 0 0;
}
.kpi-card:hover { transform: translateY(-5px); box-shadow: var(--shadow-h); }
.kpi-icon { font-size:1.5rem; margin-bottom:10px; display:block; }
.kpi-label {
    font-size:.70rem; font-weight:700; color:var(--slate-lt);
    text-transform:uppercase; letter-spacing:.07em; margin-bottom:8px;
}
.kpi-value {
    font-size:2rem; font-weight:800; line-height:1.1;
    background: linear-gradient(135deg,var(--blue),var(--teal));
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
}
.kpi-sub { color:var(--slate-lt); font-size:.75rem; margin-top:6px; font-weight:500; }
.section-title {
    font-size:1.05rem; font-weight:700; color:var(--slate);
    margin:14px 0 8px; display:flex; align-items:center; gap:8px;
}
.section-title::before {
    content:''; display:inline-block; width:4px; height:1rem;
    background:linear-gradient(180deg,var(--blue),var(--teal));
    border-radius:4px; flex-shrink:0;
}
.badge {
    display:inline-block; padding:4px 12px; border-radius:999px;
    font-size:.72rem; font-weight:700; letter-spacing:.03em;
    transition: transform .15s ease; margin:2px;
}
.badge:hover { transform:scale(1.06); }
.badge-peak { background:linear-gradient(135deg,#FEE2E2,#FECACA); color:#B91C1C; border:1px solid #FCA5A5; }
.badge-off  { background:linear-gradient(135deg,#EFF6FF,#DBEAFE); color:#1D4ED8; border:1px solid #BFDBFE; }
.hero-banner {
    background: linear-gradient(135deg,#1E293B 0%,#1e3a5f 55%,#0f4c81 100%);
    border-radius:20px; padding:32px 36px; margin-bottom:28px;
    position:relative; overflow:hidden;
    box-shadow:0 8px 40px rgba(37,99,235,0.22);
}
.hero-banner::after {
    content:'⛴️'; position:absolute; right:36px; top:50%;
    transform:translateY(-50%); font-size:5rem; opacity:.10;
}
.hero-title { font-size:1.9rem; font-weight:800; color:#fff; margin:0 0 6px; }
.hero-sub   { color:#94A3B8; font-size:.88rem; font-weight:500; margin:0; }
.hero-pill  {
    display:inline-block; background:rgba(37,99,235,.3);
    border:1px solid rgba(99,179,237,.4); color:#93C5FD;
    border-radius:999px; padding:3px 14px; font-size:.73rem;
    font-weight:600; margin-top:12px;
}
.stDownloadButton > button {
    background: linear-gradient(135deg,var(--blue),#1D4ED8) !important;
    color:#fff !important; border:none !important; border-radius:10px !important;
    font-weight:600 !important; box-shadow:0 4px 12px rgba(37,99,235,.28) !important;
    transition:all .2s ease !important;
}
.stDownloadButton > button:hover {
    transform:translateY(-2px) !important;
    box-shadow:0 6px 20px rgba(37,99,235,.4) !important;
}
[data-testid="stExpander"] {
    border:1px solid var(--border) !important;
    border-radius:var(--r-sm) !important;
    background:#FAFBFF !important;
}
footer { visibility:hidden; }
.kpi-card {
  transform-style: preserve-3d;
  will-change: transform;
}
`;
  window.parent.document.head.insertAdjacentHTML('beforeend', `<style id="premium-theme-css">${css}
[data-testid="stSelectbox"] > div > div {
    background-color: rgba(217, 119, 6, 0.15) !important;
    border: 1px solid var(--amber) !important;
    color: var(--amber) !important;
}
[data-testid="stSelectbox"] label p {
    color: var(--amber) !important;
}
</style>`);
  window.parent.document.head.insertAdjacentHTML('beforeend', `<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">`);
}

if (!window.parent.document.getElementById('particle-canvas')) {
  window.parent.document.body.insertAdjacentHTML('afterbegin', `<canvas id="particle-canvas" style="position:fixed; top:0; left:0; width:100vw; height:100vh; pointer-events:none; z-index:0;"></canvas>`);
  var c = window.parent.document.getElementById('particle-canvas');
  var ctx = c.getContext('2d');
  var W, H, pts = [], mouse = {x:-9999, y:-9999};
  function resize(){ W = c.width = window.parent.innerWidth; H = c.height = window.parent.innerHeight; }
  resize();
  window.parent.addEventListener('resize', resize);
  window.parent.document.addEventListener('mousemove', function(e){ mouse.x=e.clientX; mouse.y=e.clientY; });
  for(var i=0;i<75;i++){
    pts.push({
      x: Math.random()*1920, y: Math.random()*1080,
      vx:(Math.random()-.5)*.5, vy:(Math.random()-.5)*.5,
      r: Math.random()*2+.5, a: Math.random()*.35+.1
    });
  }
  // ── 3D CARD TILT ──
  function initTilt() {
    var doc = window.parent.document;
    doc.querySelectorAll('.kpi-card').forEach(function(card) {
      if (card.dataset.tiltInit) return;
      card.dataset.tiltInit = '1';
      card.addEventListener('mousemove', function(e) {
        var r = card.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width  - 0.5;
        var y = (e.clientY - r.top)  / r.height - 0.5;
        card.style.transform = 'perspective(600px) rotateX('+(-y*12)+'deg) rotateY('+(x*12)+'deg) translateY(-6px)';
        card.style.boxShadow = '0 20px 50px rgba(37,99,235,0.22)';
      });
      card.addEventListener('mouseleave', function() {
        card.style.transform = '';
        card.style.boxShadow = '';
      });
    });
  }
  // ── CLICK BURST ──
  var bursts = [];
  window.parent.document.addEventListener('click', function(e) {
    for (var b = 0; b < 14; b++) {
      var angle = (Math.PI * 2 / 14) * b;
      var speed = 2.5 + Math.random() * 3;
      pts.push({
        x: e.clientX, y: e.clientY,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        r: Math.random() * 3 + 1,
        a: 0.9, burst: true, life: 1.0
      });
    }
  });
  function loop(){
    ctx.clearRect(0,0,W,H);
    initTilt();
    pts = pts.filter(function(p){ return !p.burst || p.life > 0; });
    pts.forEach(function(p){
      if (p.burst) {
        p.life -= 0.04;
        p.a = p.life * 0.9;
        p.vx *= 0.94; p.vy *= 0.94;
      } else {
        var dx=p.x-mouse.x, dy=p.y-mouse.y, d=Math.hypot(dx,dy);
        if(d<130 && d>0){ var f=(130-d)/130*2.8; p.x+=dx/d*f; p.y+=dy/d*f; }
        if(p.x<0||p.x>W) p.vx*=-1;
        if(p.y<0||p.y>H) p.vy*=-1;
      }
      p.x+=p.vx; p.y+=p.vy;
      if (!p.burst) { if(p.x<0||p.x>W) p.vx*=-1; if(p.y<0||p.y>H) p.vy*=-1; }
      ctx.beginPath(); ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
      var col = p.burst ? '220,38,127' : '37,99,235';
      ctx.fillStyle='rgba('+col+','+Math.max(0,p.a)+')'; ctx.fill();
    });
    var normal = pts.filter(function(p){ return !p.burst; });
    for(var i=0;i<normal.length;i++){
      for(var j=i+1;j<normal.length;j++){
        var d=Math.hypot(normal[i].x-normal[j].x,normal[i].y-normal[j].y);
        if(d<115){ var a=(1-d/115)*.15;
          ctx.beginPath(); ctx.moveTo(normal[i].x,normal[i].y); ctx.lineTo(normal[j].x,normal[j].y);
          ctx.strokeStyle='rgba(37,99,235,'+a+')'; ctx.lineWidth=.8; ctx.stroke(); }
      }
      var md=Math.hypot(normal[i].x-mouse.x,normal[i].y-mouse.y);
      if(md<160){ var ma=(1-md/160)*.3;
        ctx.beginPath(); ctx.moveTo(normal[i].x,normal[i].y); ctx.lineTo(mouse.x,mouse.y);
        ctx.strokeStyle='rgba(13,148,136,'+ma+')'; ctx.lineWidth=.7; ctx.stroke(); }
    }
    window.parent.requestAnimationFrame(loop);
  }
  loop();
}
</script>
""", height=0, width=0)

# ── CHART CONSTANTS ───────────────────────────────────────────────────────────
PLOTLY_TEMPLATE = "plotly_white"
COLOR_SALES  = "#2563EB"
COLOR_REDEEM = "#D97706"
COLOR_NET    = "#0D9488"

def chart_layout(fig, height=400):
    fig.update_layout(
        template=PLOTLY_TEMPLATE, height=height,
        margin=dict(t=30, l=10, r=10, b=10),
        paper_bgcolor="#FFFFFF", plot_bgcolor="#F8FAFC",
        font=dict(family="Inter, sans-serif", size=12, color="#1E293B"),
        legend=dict(orientation="h", y=1.1),
    )
    return fig

# ── DATA LOADING ──────────────────────────────────────────────────────────────
import os

@st.cache_data(show_spinner="Loading ferry ticket data…")
def load_data(path="Toronto_Island_Ferry_Tickets.csv"):
    if not os.path.exists(path):
        # Fallback if running from the root directory instead of the dashboard directory
        fallback_path = os.path.join("dashboard", path)
        if os.path.exists(fallback_path):
            path = fallback_path
            
    raw = pd.read_csv(path)
    raw_rows = len(raw)
    df = raw.copy()
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
    missing_ts = int(df["Timestamp"].isna().sum())
    df = df.dropna(subset=["Timestamp"]).sort_values("Timestamp").reset_index(drop=True)

    neg_sales  = int((df["Sales Count"] < 0).sum())
    neg_redeem = int((df["Redemption Count"] < 0).sum())
    df["Sales Count"]      = df["Sales Count"].clip(lower=0)
    df["Redemption Count"] = df["Redemption Count"].clip(lower=0)

    for col in ["Sales Count", "Redemption Count"]:
        q1, q3 = df[col].quantile([.25, .75])
        iqr = q3 - q1
        df[col + "_Outlier"] = df[col] > (q3 + 3 * iqr)

    gap_min = df["Timestamp"].diff().dt.total_seconds() / 60
    pct_15  = float((gap_min == 15).mean() * 100) if len(gap_min.dropna()) else 0.0

    report = dict(
        raw_rows=raw_rows, final_rows=len(df),
        missing_timestamps_dropped=missing_ts,
        negative_sales_clipped=neg_sales,
        negative_redemptions_clipped=neg_redeem,
        sales_outliers_flagged=int(df["Sales Count_Outlier"].sum()),
        redemption_outliers_flagged=int(df["Redemption Count_Outlier"].sum()),
        pct_15min_intervals=round(pct_15, 1),
    )

    df["Date"]      = df["Timestamp"].dt.date
    df["Hour"]      = df["Timestamp"].dt.hour
    df["DayOfWeek"] = df["Timestamp"].dt.day_name()
    df["IsWeekend"] = df["Timestamp"].dt.dayofweek >= 5
    df["Month"]     = df["Timestamp"].dt.month
    df["MonthName"] = df["Timestamp"].dt.strftime("%b")
    df["Year"]      = df["Timestamp"].dt.year

    def season(m):
        if m in (12, 1, 2): return "Winter"
        if m in (3, 4, 5):  return "Spring"
        if m in (6, 7, 8):  return "Summer"
        return "Fall"
    df["Season"]      = df["Month"].apply(season)
    df["NetMovement"] = df["Sales Count"] - df["Redemption Count"]
    return df, report

df, cleaning_report = load_data()
DOW_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# ── SIDEBAR FILTERS ───────────────────────────────────────────────────────────
st.sidebar.markdown("## ⛴️ Ferry Analytics")
st.sidebar.caption("Jack Layton Ferry Terminal · Toronto Island Park")
st.sidebar.markdown("---")
st.sidebar.markdown("### 📅 Date & Time")

min_date, max_date = df["Timestamp"].min().date(), df["Timestamp"].max().date()
date_range = st.sidebar.date_input("Date range", value=(min_date, max_date),
                                    min_value=min_date, max_value=max_date)
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

hour_range       = st.sidebar.slider("Hour of day", 0, 23, (0, 23))
years_available  = sorted(df["Year"].unique())
years_selected   = st.sidebar.multiselect("Year(s)", years_available, default=years_available)
seasons_selected = st.sidebar.multiselect("Season(s)", ["Winter", "Spring", "Summer", "Fall"],
                                           default=["Winter", "Spring", "Summer", "Fall"])
day_type         = st.sidebar.radio("Day type", ["All", "Weekday only", "Weekend only"])
st.sidebar.markdown("---")
st.sidebar.markdown("### 👤 Role View")
role = st.sidebar.selectbox("Viewing as",
    ["Operations Team", "Policy Planner", "Management Stakeholder"])

# ── APPLY FILTERS ─────────────────────────────────────────────────────────────
mask = (
    (df["Date"] >= start_date) & (df["Date"] <= end_date) &
    (df["Hour"] >= hour_range[0]) & (df["Hour"] <= hour_range[1]) &
    (df["Year"].isin(years_selected)) & (df["Season"].isin(seasons_selected))
)
fdf = df[mask].copy()
if day_type == "Weekday only":   fdf = fdf[~fdf["IsWeekend"]]
elif day_type == "Weekend only": fdf = fdf[fdf["IsWeekend"]]

if fdf.empty:
    st.warning("No data matches the selected filters. Please broaden your selection.")
    st.stop()

# ── KPI COMPUTATIONS ──────────────────────────────────────────────────────────
total_sales  = int(fdf["Sales Count"].sum())
total_redeem = int(fdf["Redemption Count"].sum())
net_movement = total_sales - total_redeem

hourly_totals = fdf.set_index("Timestamp")[["Sales Count", "Redemption Count"]].resample("h").sum()
sold_per_hr   = hourly_totals["Sales Count"].mean()   if not hourly_totals.empty else 0
redeem_per_hr = hourly_totals["Redemption Count"].mean() if not hourly_totals.empty else 0

hourly_avg  = fdf.groupby("Hour")[["Sales Count", "Redemption Count"]].mean()
peak_hour   = int(hourly_avg["Sales Count"].idxmax())
peak_hr_val = hourly_avg["Sales Count"].max()

season_avg = fdf.groupby("Season")["Sales Count"].mean()
if "Summer" in season_avg.index and season_avg.get("Summer", 0) > 0:
    off_idx = round(season_avg.drop("Summer", errors="ignore").mean() / season_avg["Summer"] * 100, 1)
else:
    off_idx = float("nan")

# ── HERO BANNER ───────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-banner">
  <p class="hero-title">⛴️ Toronto Island Ferry Analytics</p>
  <p class="hero-sub">Jack Layton Ferry Terminal &nbsp;·&nbsp; Real-Time Ticket Sales &amp; Redemption</p>
  <span class="hero-pill">📅 {fdf['Timestamp'].min():%b %d, %Y} &nbsp;→&nbsp;
  {fdf['Timestamp'].max():%b %d, %Y} &nbsp;·&nbsp; {len(fdf):,} records &nbsp;·&nbsp; {role}</span>
</div>
""", unsafe_allow_html=True)

# ── KPI CARDS ─────────────────────────────────────────────────────────────────
c1, c2, c3 = st.columns(3)
for col, icon, lbl, val, sub in [
    (c1, "🎫", "Tickets Sold / Hour",     f"{sold_per_hr:,.1f}",   f"{total_sales:,} total sold"),
    (c2, "✅", "Tickets Redeemed / Hour", f"{redeem_per_hr:,.1f}", f"{total_redeem:,} total redeemed"),
    (c3, "🔀", "Net Passenger Movement",  f"{net_movement:,}",      "Sales − Redemptions"),
]:
    with col:
        st.markdown(f"""<div class="kpi-card">
            <span class="kpi-icon">{icon}</span>
            <div class="kpi-label">{lbl}</div>
            <div class="kpi-value">{val}</div>
            <div class="kpi-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
c4, c5 = st.columns(2)
for col, icon, lbl, val, sub in [
    (c4, "⏰",  "Peak Demand Window",    f"{peak_hour}:00 – {peak_hour+1}:00",
     f"{peak_hr_val:.0f} avg tickets / 15-min interval"),
    (c5, "🌤️", "Off-Season Utilization", f"{off_idx}%" if not np.isnan(off_idx) else "N/A",
     "Off-peak demand vs. summer peak"),
]:
    with col:
        st.markdown(f"""<div class="kpi-card">
            <span class="kpi-icon">{icon}</span>
            <div class="kpi-label">{lbl}</div>
            <div class="kpi-value">{val}</div>
            <div class="kpi-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Time-Series", "⏰ Peak vs Off-Peak", "📅 Seasonal Trends",
    "🗂️ Data Explorer", "🧹 Data Quality", "🔴 Live Feed Simulator"
])

# ═══ TAB 1 ════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-title">Sales vs Redemptions Over Time</div>', unsafe_allow_html=True)

    granularity = st.radio("Aggregate by", ["Raw 15-min", "Hourly", "Daily"], horizontal=True, index=1)
    ts = fdf.set_index("Timestamp")[["Sales Count", "Redemption Count", "NetMovement"]]
    if granularity == "Hourly":  ts_plot = ts.resample("h").sum()
    elif granularity == "Daily": ts_plot = ts.resample("D").sum()
    else:                        ts_plot = ts

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ts_plot.index, y=ts_plot["Sales Count"],
        name="Sales", line=dict(color=COLOR_SALES, width=2)))
    fig.add_trace(go.Scatter(x=ts_plot.index, y=ts_plot["Redemption Count"],
        name="Redemptions", line=dict(color=COLOR_REDEEM, width=2)))
    chart_layout(fig, 430)
    st.plotly_chart(fig, width='stretch')

    st.markdown('<div class="section-title">Net Passenger Movement</div>', unsafe_allow_html=True)
    fig_net = px.area(ts_plot, x=ts_plot.index, y="NetMovement", template=PLOTLY_TEMPLATE)
    fig_net.update_traces(line_color=COLOR_NET, fillcolor="rgba(13,148,136,0.14)")
    chart_layout(fig_net, 300)
    fig_net.update_layout(yaxis_title="Sales − Redemptions")
    st.plotly_chart(fig_net, width='stretch')

    st.markdown('<div class="section-title">Rolling Averages (1-Hour / 4-Hour)</div>', unsafe_allow_html=True)
    roll_metric = st.radio("Metric", ["Sales Count", "Redemption Count"], horizontal=True, key="roll_metric")
    roll = fdf.set_index("Timestamp")[roll_metric].resample("15min").sum().fillna(0)
    roll_df = pd.DataFrame({
        "Raw (15-min)":       roll,
        "1-Hour Rolling Avg": roll.rolling(4,  min_periods=1).mean(),
        "4-Hour Rolling Avg": roll.rolling(16, min_periods=1).mean(),
    })
    lc = COLOR_SALES if roll_metric == "Sales Count" else COLOR_REDEEM
    fig_roll = px.line(roll_df.tail(2000), template=PLOTLY_TEMPLATE,
                       color_discrete_sequence=["#CBD5E1", lc, "#7C3AED"])
    chart_layout(fig_roll, 360)
    fig_roll.update_layout(yaxis_title=roll_metric)
    st.plotly_chart(fig_roll, width='stretch')
    st.caption("Showing the most recent 2,000 filtered intervals.")

# ═══ TAB 2 ════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-title">Hourly Demand Profile</div>', unsafe_allow_html=True)
    hourly = fdf.groupby("Hour")[["Sales Count", "Redemption Count"]].mean().reset_index()
    threshold = hourly["Sales Count"].quantile(0.66)
    hourly["Period"] = np.where(hourly["Sales Count"] >= threshold, "Peak", "Off-Peak")

    fig_hr = px.bar(hourly, x="Hour", y="Sales Count", color="Period",
                    color_discrete_map={"Peak": "#E11D48", "Off-Peak": "#2563EB"},
                    template=PLOTLY_TEMPLATE)
    chart_layout(fig_hr, 380)
    st.plotly_chart(fig_hr, width='stretch')

    peak_hours = hourly[hourly["Period"] == "Peak"]["Hour"].tolist()
    off_hours  = hourly[hourly["Period"] == "Off-Peak"]["Hour"].tolist()
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**🔴 Peak Windows**")
        st.markdown(" ".join(f'<span class="badge badge-peak">{h}:00–{h+1}:00</span>' for h in peak_hours),
                    unsafe_allow_html=True)
    with c2:
        st.markdown("**🔵 Off-Peak Windows**")
        st.markdown(" ".join(f'<span class="badge badge-off">{h}:00–{h+1}:00</span>' for h in off_hours),
                    unsafe_allow_html=True)

    st.markdown('<div class="section-title">Demand by Day of Week</div>', unsafe_allow_html=True)
    dow = fdf.groupby("DayOfWeek")[["Sales Count", "Redemption Count"]].mean().reindex(DOW_ORDER).reset_index()
    fig_dow = px.bar(dow, x="DayOfWeek", y=["Sales Count", "Redemption Count"],
                     barmode="group", template=PLOTLY_TEMPLATE,
                     color_discrete_sequence=[COLOR_SALES, COLOR_REDEEM])
    chart_layout(fig_dow, 360)
    fig_dow.update_layout(yaxis_title="Avg per 15-min interval")
    st.plotly_chart(fig_dow, width='stretch')

    st.markdown('<div class="section-title">Hour × Day-of-Week Heatmap</div>', unsafe_allow_html=True)
    heat = fdf.pivot_table(index="Hour", columns="DayOfWeek",
                            values="Sales Count", aggfunc="mean").reindex(columns=DOW_ORDER)
    fig_heat = px.imshow(heat, aspect="auto", color_continuous_scale="Blues", template=PLOTLY_TEMPLATE)
    chart_layout(fig_heat, 430)
    st.plotly_chart(fig_heat, width='stretch')

# ═══ TAB 3 ════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">Monthly Sales & Redemption Trend</div>', unsafe_allow_html=True)
    monthly = fdf.groupby(["Year", "Month"]).agg(
        Sales=("Sales Count", "sum"), Redemptions=("Redemption Count", "sum")
    ).reset_index()
    monthly["Period"] = pd.to_datetime(dict(year=monthly.Year, month=monthly.Month, day=1))
    fig_mo = px.line(monthly, x="Period", y=["Sales", "Redemptions"],
                     template=PLOTLY_TEMPLATE, color_discrete_sequence=[COLOR_SALES, COLOR_REDEEM])
    fig_mo.update_traces(line=dict(width=2.5))
    chart_layout(fig_mo, 380)
    st.plotly_chart(fig_mo, width='stretch')

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section-title">Seasonal Sales Share</div>', unsafe_allow_html=True)
        season_tot = (fdf.groupby("Season")["Sales Count"].sum()
                        .reindex(["Winter", "Spring", "Summer", "Fall"]).reset_index())
        fig_pie = px.pie(season_tot, names="Season", values="Sales Count", hole=0.55,
                         template=PLOTLY_TEMPLATE,
                         color_discrete_sequence=["#94A3B8", "#0D9488", "#2563EB", "#D97706"])
        fig_pie.update_traces(textfont_size=13)
        fig_pie.update_layout(height=360, margin=dict(t=20, l=10, r=10, b=10))
        st.plotly_chart(fig_pie, width='stretch')
    with c2:
        st.markdown('<div class="section-title">Weekday vs Weekend</div>', unsafe_allow_html=True)
        wk = (fdf.groupby("IsWeekend")["Sales Count"].mean()
                .rename({True: "Weekend", False: "Weekday"}).reset_index())
        wk.columns = ["Type", "Avg Sales / Interval"]
        fig_wk = px.bar(wk, x="Type", y="Avg Sales / Interval", template=PLOTLY_TEMPLATE,
                         color="Type", color_discrete_map={"Weekday": COLOR_SALES, "Weekend": "#7C3AED"})
        chart_layout(fig_wk, 360)
        fig_wk.update_layout(showlegend=False)
        st.plotly_chart(fig_wk, width='stretch')

    st.markdown('<div class="section-title">Sales vs Redemption Distribution</div>', unsafe_allow_html=True)
    fig_hist = px.histogram(fdf, x=["Sales Count", "Redemption Count"],
                            nbins=60, barmode="overlay", opacity=0.65,
                            template=PLOTLY_TEMPLATE,
                            color_discrete_sequence=[COLOR_SALES, COLOR_REDEEM])
    chart_layout(fig_hist, 360)
    st.plotly_chart(fig_hist, width='stretch')

# ═══ TAB 4 ════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-title">Sales vs Redemptions Scatter</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        fig_sc = px.scatter(
            fdf, x="Sales Count", y="Redemption Count",
            color="DayOfWeek", hover_data=["Timestamp", "Season"],
            template=PLOTLY_TEMPLATE, opacity=0.65,
            color_discrete_sequence=["#2563EB","#0D9488","#D97706","#7C3AED","#E11D48","#059669","#F59E0B"]
        )
        chart_layout(fig_sc, 400)
        st.plotly_chart(fig_sc, width='stretch')
    with c2:
        fig_box = px.box(fdf, x="DayOfWeek", y="Sales Count", template=PLOTLY_TEMPLATE,
                         color="IsWeekend",
                         color_discrete_map={True: "#7C3AED", False: "#2563EB"})
        chart_layout(fig_box, 400)
        st.plotly_chart(fig_box, width='stretch')

    st.markdown('<div class="section-title">Sales Distribution by Season</div>', unsafe_allow_html=True)
    fig_sbox = px.box(fdf, x="Season", y="Sales Count",
                      category_orders={"Season": ["Winter", "Spring", "Summer", "Fall"]},
                      color="Season", template=PLOTLY_TEMPLATE,
                      color_discrete_sequence=["#94A3B8", "#0D9488", "#2563EB", "#D97706"])
    chart_layout(fig_sbox, 360)
    st.plotly_chart(fig_sbox, width='stretch')

    st.markdown('<div class="section-title">Filtered Records</div>', unsafe_allow_html=True)
    st.dataframe(
        fdf[["Timestamp", "Sales Count", "Redemption Count", "NetMovement", "DayOfWeek", "Season"]]
        .sort_values("Timestamp", ascending=False),
        width='stretch', height=280,
    )
    csv = fdf.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download filtered data as CSV", csv, "ferry_filtered_data.csv", "text/csv")

# ═══ TAB 5 ════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-title">Data Ingestion & Cleaning Summary</div>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Raw rows loaded",           f"{cleaning_report['raw_rows']:,}")
    m2.metric("Rows after cleaning",       f"{cleaning_report['final_rows']:,}")
    m3.metric("Missing timestamps dropped",f"{cleaning_report['missing_timestamps_dropped']:,}")
    m4.metric("15-min interval %",         f"{cleaning_report['pct_15min_intervals']}%")

    st.markdown('<div class="section-title">Outlier Detection (IQR × 3)</div>', unsafe_allow_html=True)
    st.caption("Values beyond Q3 + 3×IQR are **flagged** (not removed) — genuine high-season demand spikes.")
    oc1, oc2 = st.columns(2)
    oc1.metric("Sales Count outliers",
               f"{cleaning_report['sales_outliers_flagged']:,}",
               f"{cleaning_report['sales_outliers_flagged']/cleaning_report['final_rows']*100:.1f}% of rows")
    oc2.metric("Redemption Count outliers",
               f"{cleaning_report['redemption_outliers_flagged']:,}",
               f"{cleaning_report['redemption_outliers_flagged']/cleaning_report['final_rows']*100:.1f}% of rows")

    st.markdown('<div class="section-title">Sales Outliers Over Time</div>', unsafe_allow_html=True)
    fig_out = px.scatter(fdf, x="Timestamp", y="Sales Count",
                         color="Sales Count_Outlier",
                         color_discrete_map={True: "#E11D48", False: "#2563EB"},
                         opacity=0.55, template=PLOTLY_TEMPLATE)
    chart_layout(fig_out, 360)
    st.plotly_chart(fig_out, width='stretch')

    with st.expander("📋 View Flagged Records"):
        outlier_view = fdf[fdf["Sales Count_Outlier"] | fdf["Redemption Count_Outlier"]][[
            "Timestamp", "Sales Count", "Redemption Count",
            "Sales Count_Outlier", "Redemption Count_Outlier"
        ]].sort_values("Timestamp", ascending=False)
        st.dataframe(outlier_view.head(200), width='stretch', height=260)
        st.caption(f"{len(outlier_view):,} flagged records in current filter (showing up to 200).")

    st.markdown('<div class="section-title">Time Gap Distribution Between Records</div>', unsafe_allow_html=True)
    gaps = fdf.set_index("Timestamp").index.to_series().diff().dt.total_seconds().div(60).dropna()
    gap_counts = gaps.value_counts().head(8).rename("Occurrences").reset_index()
    gap_counts.columns = ["Gap (minutes)", "Occurrences"]
    gap_counts["Gap (str)"] = gap_counts["Gap (minutes)"].astype(str) + " min"
    fig_gaps = px.bar(gap_counts, x="Gap (str)", y="Occurrences",
                      text="Occurrences", color="Occurrences",
                      color_continuous_scale="Blues", template=PLOTLY_TEMPLATE)
    chart_layout(fig_gaps, 360)
    fig_gaps.update_layout(showlegend=False)
    st.plotly_chart(fig_gaps, width='stretch')
    st.caption("Nominal cadence = 15 min. Longer gaps expected overnight and in winter off-season.")

# ═══ TAB 6 ════════════════════════════════════════════════════════════════════
with tab6:
    st.markdown('<div class="section-title">Near Real-Time Feed Simulator</div>', unsafe_allow_html=True)
    st.caption("Replays the most recent 200 intervals one at a time — simulating live terminal data arrival.")

    live_src = fdf.sort_values("Timestamp").tail(200).reset_index(drop=True)
    if "live_idx" not in st.session_state:
        st.session_state.live_idx = min(20, len(live_src))

    b1, b2, b3, _ = st.columns([1, 1, 2, 2])
    with b1:
        if st.button("▶️ Advance"): st.session_state.live_idx = min(st.session_state.live_idx + 1, len(live_src))
    with b2:
        if st.button("↺ Reset"):    st.session_state.live_idx = min(20, len(live_src))
    with b3:
        auto_play = st.toggle("⚡ Auto-advance", value=False, key="auto_play")
    if auto_play and st.session_state.live_idx < len(live_src):
        import time as _time
        _time.sleep(0.6)
        st.session_state.live_idx = min(st.session_state.live_idx + 1, len(live_src))
        st.rerun()

    visible = live_src.iloc[:st.session_state.live_idx]
    if not visible.empty:
        latest = visible.iloc[-1]
        lc1, lc2, lc3 = st.columns(3)
        lc1.metric("Latest interval",              latest["Timestamp"].strftime("%Y-%m-%d %H:%M"))
        lc2.metric("Tickets sold (this interval)", int(latest["Sales Count"]))
        lc3.metric("Redeemed (this interval)",     int(latest["Redemption Count"]))

        fig_live = go.Figure()
        fig_live.add_trace(go.Scatter(x=visible["Timestamp"], y=visible["Sales Count"],
            name="Sales", mode="lines+markers", line=dict(color=COLOR_SALES, width=2)))
        fig_live.add_trace(go.Scatter(x=visible["Timestamp"], y=visible["Redemption Count"],
            name="Redemptions", mode="lines+markers", line=dict(color=COLOR_REDEEM, width=2)))
        chart_layout(fig_live, 400)
        st.plotly_chart(fig_live, width='stretch')
    else:
        st.info("No data in the current filter selection.")

# ── ROLE INSIGHT ───────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown('<div class="section-title">Insights for your Role</div>', unsafe_allow_html=True)
if role == "Operations Team":
    st.info(f"**Staffing guidance:** Peak demand consistently occurs around **{peak_hour}:00**. "
            f"Consider elevated staffing between {min(peak_hours) if peak_hours else 11}:00 "
            f"and {(max(peak_hours)+1) if peak_hours else 15}:00 on high-traffic days.")
elif role == "Policy Planner":
    st.info(f"**Seasonal planning:** Off-season utilization runs at **{off_idx}%** of peak-summer levels, "
            "indicating room for shoulder-season promotions or adjusted winter schedules.")
else:
    st.info(f"**Executive snapshot:** Over the selected window, the terminal processed **{total_sales:,}** "
            f"ticket sales and **{total_redeem:,}** redemptions — net movement: **{net_movement:,}** passengers.")

st.caption("Built for Toronto Government · Parks, Forestry & Recreation — Ferry Analytics Dashboard.")
