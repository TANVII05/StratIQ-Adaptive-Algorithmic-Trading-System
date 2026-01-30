import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# ==============================
# CONFIG
# ==============================
st.set_page_config(page_title="Algobot Strategy Dashboard", layout="wide")
st.title("📈 Algobot Strategy Dashboard")
st.markdown("Select a market file, choose date range, and run your strategy with live charts & backtest.")

DATA_FOLDER = "data"

# ==============================
# HELPERS
# ==============================
@st.cache_data
def list_data_files(folder):
    if not os.path.exists(folder):
        return []
    return sorted([
        f for f in os.listdir(folder)
        if f.lower().endswith((".csv", ".xlsx", ".xls"))
    ])

@st.cache_data
def detect_date_column(df):
    for col in df.columns:
        try:
            parsed = pd.to_datetime(df[col], errors="coerce")
            if parsed.notna().sum() / len(df) > 0.6:
                return col
        except:
            pass
    return None

def detect_close_column(df):
    priority = ["close", "Close", "CLOSE", "Adj Close", "adjclose"]
    for col in priority:
        if col in df.columns:
            return col
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    return numeric_cols[-1] if numeric_cols else None

# ==============================
# INDICATORS
# ==============================
def compute_indicators(df):
    df = df.copy()

    df["EMA_13"] = df["close"].ewm(span=13, adjust=False).mean()
    df["EMA_34"] = df["close"].ewm(span=34, adjust=False).mean()

    delta = df["close"].diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)

    roll_up = up.ewm(com=13, adjust=False).mean()
    roll_down = down.ewm(com=13, adjust=False).mean()

    rs = roll_up / (roll_down + 1e-9)
    df["RSI"] = 100 - (100 / (1 + rs))

    return df

# ==============================
# STRATEGY LOGIC
# ==============================
def generate_signals(df):
    df = df.copy()

    df["long_cond"] = (df["EMA_13"] > df["EMA_34"]) & (df["RSI"] > 50)
    df["short_cond"] = (df["EMA_13"] < df["EMA_34"]) & (df["RSI"] < 50)

    df["signal"] = 0
    position = 0

    for i in range(len(df)):
        if position == 0:
            if df["long_cond"].iloc[i]:
                df["signal"].iloc[i] = 1
                position = 1
            elif df["short_cond"].iloc[i]:
                df["signal"].iloc[i] = -1
                position = -1

        elif position == 1 and df["short_cond"].iloc[i]:
            df["signal"].iloc[i] = -1
            position = -1

        elif position == -1 and df["long_cond"].iloc[i]:
            df["signal"].iloc[i] = 1
            position = 1

    return df

# ==============================
# BACKTEST ENGINE
# ==============================
def backtest(df, initial_capital=10000, fixed_size=1):
    df = df.copy().reset_index()

    cash = initial_capital
    pos = 0
    entry_price = 0
    equity_curve = []
    trades = []

    for i, row in df.iterrows():
        price = row["close"]
        signal = row["signal"]
        date = row.iloc[0]

        if signal == 1 and pos <= 0:
            if pos < 0:
                pnl = pos * (entry_price - price)
                cash += abs(pos) * price
                trades.append((date, "EXIT SHORT", price, pnl))
                pos = 0

            pos = fixed_size
            entry_price = price
            cash -= fixed_size * price
            trades.append((date, "BUY", price, 0))

        elif signal == -1 and pos >= 0:
            if pos > 0:
                pnl = pos * (price - entry_price)
                cash += pos * price
                trades.append((date, "EXIT LONG", price, pnl))
                pos = 0

            pos = -fixed_size
            entry_price = price
            cash += fixed_size * price
            trades.append((date, "SELL", price, 0))

        equity = cash + pos * price
        equity_curve.append((date, equity))

    eq_df = pd.DataFrame(equity_curve, columns=["Date", "EquITY"])
    trade_df = pd.DataFrame(trades, columns=["Date", "Action", "Price", "PnL"])

    return eq_df, trade_df

# ==============================
# SIDEBAR — FILE PICKER
# ==============================
st.sidebar.header("📂 Market File Selection")

files = list_data_files(DATA_FOLDER)

if not files:
    st.error("No files found in 'data/' folder")
    st.stop()

selected_file = st.sidebar.selectbox("Select Symbol / Index", files)

file_path = os.path.join(DATA_FOLDER, selected_file)

# ==============================
# LOAD FILE
# ==============================
if selected_file.lower().endswith(".csv"):
    df = pd.read_csv(file_path)
else:
    df = pd.read_excel(file_path)

date_col = detect_date_column(df)
close_col = detect_close_column(df)

if date_col is None or close_col is None:
    st.error("Couldn't detect Date or Close column in file")
    st.stop()

df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
df = df.dropna(subset=[date_col])
df = df.sort_values(date_col)

df = df.rename(columns={close_col: "close"})
df = df.set_index(date_col)

st.success(f"Loaded: {selected_file}")

# ==============================
# DATE FILTER
# ==============================
st.sidebar.header("📅 Date Range")

min_date = df.index.min().date()
max_date = df.index.max().date()

start_date = st.sidebar.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("End Date", max_date, min_value=min_date, max_value=max_date)

if start_date > end_date:
    start_date, end_date = end_date, start_date

df = df.loc[str(start_date):str(end_date)]

# ==============================
# STRATEGY SETTINGS
# ==============================
st.sidebar.header("⚙ Strategy Settings")
initial_capital = st.sidebar.number_input("Initial Capital (₹)", value=10000, step=1000)
fixed_size = st.sidebar.number_input("Fixed Trade Size", value=1, min_value=1)

run = st.sidebar.button("🚀 Run Strategy")

# ==============================
# RUN STRATEGY
# ==============================
if run:
    df = compute_indicators(df)
    df = generate_signals(df)
    equity, trades = backtest(df, initial_capital, fixed_size)

    # ==============================
    # CHART
    # ==============================
    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True,
        row_heights=[0.7, 0.3],
        vertical_spacing=0.05,
        subplot_titles=("Price + EMAs + Signals", "RSI")
    )

    fig.add_trace(go.Scatter(x=df.index, y=df["close"], name="Close"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["EMA_13"], name="EMA 13"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["EMA_34"], name="EMA 34"), row=1, col=1)

    buys = df[df["signal"] == 1]
    sells = df[df["signal"] == -1]

    fig.add_trace(go.Scatter(
        x=buys.index, y=buys["close"],
        mode="markers", name="BUY",
        marker=dict(symbol="triangle-up", size=10)
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=sells.index, y=sells["close"],
        mode="markers", name="SELL",
        marker=dict(symbol="triangle-down", size=10)
    ), row=1, col=1)

    fig.add_trace(go.Scatter(x=df.index, y=df["RSI"], name="RSI"), row=2, col=1)

    fig.update_layout(height=800, hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    # ==============================
    # EQUITY CURVE
    # ==============================
    st.subheader("📊 Equity Curve")
    eq_fig = go.Figure()
    eq_fig.add_trace(go.Scatter(x=equity["Date"], y=equity["EquITY"], name="Equity"))
    st.plotly_chart(eq_fig, use_container_width=True)

    # ==============================
    # METRICS
    # ==============================
    start_eq = equity["EquITY"].iloc[0]
    end_eq = equity["EquITY"].iloc[-1]
    ret = ((end_eq - start_eq) / start_eq) * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("Start Capital", f"₹{start_eq:,.2f}")
    col2.metric("End Capital", f"₹{end_eq:,.2f}")
    col3.metric("Return %", f"{ret:.2f}%")

    # ==============================
    # TRADES
    # ==============================
    st.subheader("📑 Trade Log")
    st.dataframe(trades.tail(30))

    st.success("Strategy executed successfully! 🎯")
