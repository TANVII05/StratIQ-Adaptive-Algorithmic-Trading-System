#  StratIQ - Algorithmic Trading Bot  

StratIQ is a hybrid, rule-based and regime-adaptive algorithmic trading system designed to capture medium-term market trends while maintaining strict risk control. The strategy combines trend detection, momentum confirmation, and volatility filters to generate high-quality trading signals.

This repository contains the complete codebase, research notebooks, technical documentation, and an interactive analytics dashboard.

---



## 🧠 Project Overview

StratIQ is built to reduce market noise and improve signal reliability by requiring multiple confirmations before trade execution:

- **Trend Confirmation:** EMA (13 / 34) crossover
- **Momentum Filter:** RSI-based regime validation alongside Volume and ADX
- **Volatility / Participation Filter:** Trades taken only during expansion phases
- **Risk Management:** Fixed risk per trade with minimum 1:2 risk-reward ratio

The system supports long and short trading on indices and applies conservative execution logic for equities.

---

## ✨ Key Features

- Trend-following using EMA crossovers  
- Momentum confirmation via RSI  
- Volatility & participation filters  
- Strict stop-loss and target-based exits  
- Long-term backtesting and performance analysis  
- Interactive Streamlit dashboard  

---

## 🛠️ Tech Stack

- **Language:** Python  
- **Data Analysis:** pandas, numpy  
- **Visualization:** plotly, matplotlib, seaborn
- **Dashboard:** Streamlit  
- **Research:** Jupyter Notebook  

---

## 📊 Interactive Dashboard

The Streamlit dashboard provides:
- Equity curve visualization
- Win/Loss distribution
- Asset-wise PnL breakdown
- Detailed trade logs with filters


---

## 📈 Outputs

The project can generate the following outputs:

- Trade logs (CSV)
- Equity curves
- Asset-wise performance metrics
- Win/Loss distribution analysis

All generated files are stored inside the `Results/` directory.





