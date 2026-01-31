import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import re

# ==============================
# 1. APP CONFIGURATION
# ==============================
st.set_page_config(
    page_title="StratIQ Analytics",
    layout="wide",
    page_icon="⚡"
)

st.title("⚡ StratIQ: Algorithmic Strategy Dashboard")
st.markdown("### 📊 Live Backtest Analysis (Source: all_trades.csv)")
st.markdown("---")

# ==============================
# 2. DATA LOADER (Robust)
# ==============================
@st.cache_data
def load_data():
    # Paths to check
    possible_paths = ["all_trades.csv", "outputs/csv/all_trades.csv", "data/all_trades.csv"]
    file_path = None
    
    for f in possible_paths:
        if os.path.exists(f):
            file_path = f
            break
            
    if not file_path:
        return None

    df = pd.read_csv(file_path)

    # Regex Date Cleaner (Extract YYYY-MM-DD from messy text)
    def extract_clean_date(val):
        if pd.isna(val): return None
        match = re.search(r'(\d{4}-\d{2}-\d{2})', str(val))
        return match.group(1) if match else None

    # Apply cleaning
    if "Entry Date" in df.columns:
        df["Clean_Date"] = df["Entry Date"].apply(extract_clean_date)
        df["Entry_Date_Parsed"] = pd.to_datetime(df["Clean_Date"], errors="coerce")
    
    # Rename columns for internal use
    df = df.rename(columns={
        "Entry": "Entry_Price", 
        "Exit": "Exit_Price",
        "Entry Date": "Raw_Entry_Date"
    })

    # Drop invalid rows & Sort
    df = df.dropna(subset=["Entry_Date_Parsed"])
    df = df.sort_values("Entry_Date_Parsed")
    
    return df

# Load Data
df = load_data()

if df is None:
    st.error("❌ 'all_trades.csv' not found. Please ensure the file exists.")
    st.stop()

# ==============================
# 3. SIDEBAR FILTERS
# ==============================
st.sidebar.header("🔍 Filter Dashboard")

# Asset Filter
all_symbols = sorted(df["Symbol"].unique())
selected_symbols = st.sidebar.multiselect("Select Assets", all_symbols, default=all_symbols)

# Direction Filter
all_directions = df["Direction"].unique()
selected_directions = st.sidebar.multiselect("Trade Direction", all_directions, default=all_directions)

# Date Range Filter
min_date = df["Entry_Date_Parsed"].min().date()
max_date = df["Entry_Date_Parsed"].max().date()

try:
    start_date = st.sidebar.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
    end_date = st.sidebar.date_input("End Date", max_date, min_value=min_date, max_value=max_date)
except:
    st.sidebar.warning("Date range error. Resetting.")
    start_date, end_date = min_date, max_date

# Apply Filters
mask = (
    (df["Symbol"].isin(selected_symbols)) &
    (df["Direction"].isin(selected_directions)) &
    (df["Entry_Date_Parsed"].dt.date >= start_date) &
    (df["Entry_Date_Parsed"].dt.date <= end_date)
)
filtered_df = df[mask].copy()

if filtered_df.empty:
    st.warning("⚠️ No trades found for this selection.")
    st.stop()

# ==============================
# 4. KPI CALCULATIONS (Fixed Win Rate)
# ==============================
total_trades = len(filtered_df)

# FIX: Calculate Wins/Losses based on PnL > 0 (More reliable than string matching)
wins = filtered_df[filtered_df["PnL"] > 0]
losses = filtered_df[filtered_df["PnL"] <= 0]

win_count = len(wins)
loss_count = len(losses)
win_rate = (win_count / total_trades * 100) if total_trades > 0 else 0.0

net_pnl = filtered_df["PnL"].sum()
gross_profit = wins["PnL"].sum()
gross_loss = abs(losses["PnL"].sum())
avg_win = wins["PnL"].mean() if not wins.empty else 0
avg_loss = losses["PnL"].mean() if not losses.empty else 0
profit_factor = (gross_profit / gross_loss) if gross_loss != 0 else 0

# ==============================
# 5. TOP METRICS ROW
# ==============================
col1, col2, col3, col4 = st.columns(4)
col1.metric("Net PnL", f"{net_pnl:,.2f}")
col2.metric("Win Rate", f"{win_rate:.1f}%") # This will now work 100%
col3.metric("Profit Factor", f"{profit_factor:.2f}")
col4.metric("Total Trades", f"{total_trades}")

st.markdown("---")

# ==============================
# 6. SPLIT VIEW: P&L TABLE (Left) + EQUITY CHART (Right)
# ==============================
col_stats, col_charts = st.columns([1, 2])

with col_stats:
    st.subheader("📋 Net P&L Statement")
    
    # Financial Statement Data
    stats_data = {
        "Metric": [
            "Total Gross Profit",
            "Total Gross Loss",
            "Net Profit / Loss",
            "Largest Win",
            "Largest Loss",
            "Average Win",
            "Average Loss",
            "Risk : Reward Ratio"
        ],
        "Value": [
            f"{gross_profit:,.2f}",
            f"-{gross_loss:,.2f}",
            f"{net_pnl:,.2f}",
            f"{filtered_df['PnL'].max():,.2f}",
            f"{filtered_df['PnL'].min():,.2f}",
            f"{avg_win:,.2f}",
            f"{avg_loss:,.2f}",
            f"1 : {abs(avg_win/avg_loss):.2f}" if avg_loss != 0 else "N/A"
        ]
    }
    # Display as a clean table
    st.dataframe(pd.DataFrame(stats_data), hide_index=True, use_container_width=True)

with col_charts:
    st.subheader("📈 Portfolio Growth Curve")
    # Equity Curve Logic
    filtered_df = filtered_df.sort_values("Entry_Date_Parsed")
    filtered_df["Cumulative_PnL"] = filtered_df["PnL"].cumsum()
    
    fig_eq = px.line(filtered_df, x="Entry_Date_Parsed", y="Cumulative_PnL", 
                     labels={"Cumulative_PnL": "Net PnL", "Entry_Date_Parsed": "Date"})
    fig_eq.update_traces(line_color='#2ecc71', fill='tozeroy')
    fig_eq.update_layout(height=400)
    st.plotly_chart(fig_eq, use_container_width=True)

# ==============================
# 7. TABS FOR VISUALS (Asset Perf + Pie Chart + Raw Data)
# ==============================
st.markdown("### 📊 Detailed Analysis")
tab1, tab2, tab3 = st.tabs(["📊 Asset Performance", "🥧 Win/Loss Distribution", "📑 Raw Trade Logs"])

with tab1:
    # Bar chart of PnL by Symbol
    symbol_perf = filtered_df.groupby("Symbol")["PnL"].sum().sort_values(ascending=False).reset_index()
    fig_bar = px.bar(symbol_perf, x="Symbol", y="PnL", color="PnL", 
                     color_continuous_scale="RdYlGn", title="Net Profit by Asset")
    st.plotly_chart(fig_bar, use_container_width=True)

with tab2:
    # Win/Loss Pie Chart
    outcome_labels = ["Wins", "Losses"]
    outcome_values = [win_count, loss_count]
    
    fig_pie = px.pie(names=outcome_labels, values=outcome_values, 
                     color=outcome_labels,
                     color_discrete_map={"Wins": "#27ae60", "Losses": "#e74c3c"},
                     title=f"Win Rate: {win_rate:.1f}%")
    st.plotly_chart(fig_pie, use_container_width=True)

with tab3:
    # Raw Data Table
    st.markdown("#### Detailed Trade Log")
    # Columns to show
    display_cols = ["Entry_Date_Parsed", "Symbol", "Direction", "Entry_Price", "Exit_Price", "SL", "Target", "PnL", "Result"]
    valid_cols = [c for c in display_cols if c in filtered_df.columns]

    st.dataframe(
        filtered_df[valid_cols].sort_values("Entry_Date_Parsed", ascending=False),
        use_container_width=True,
        height=400
    )
