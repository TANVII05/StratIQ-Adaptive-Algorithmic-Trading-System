# 🚀 StratIQ — Algorithmic Trading Bot  

StratIQ is a hybrid, rule-based and regime-adaptive algorithmic trading system designed to capture medium-term market trends while maintaining strict risk control. The strategy combines trend detection, momentum confirmation, and volatility filters to generate high-quality trading signals.

This repository contains the complete codebase, research notebooks, technical documentation, and an interactive analytics dashboard.

---

## 📁 Repository Structure
StratIQ-AlgoTrading-BatraHedge/
├── app/
│ └── streamlit_app.py 
├── notebooks/
│ └── Strategy.ipynb 
├── docs/
│ └── StratIQ_Technical_Report.pdf
├── data/ 
├── outputs/ 
├── assets/
│ └── screenshots/ 
├── requirements.txt 
└── README.md 


---

## 🧠 Project Overview

StratIQ is built to reduce market noise and improve signal reliability by requiring multiple confirmations before trade execution:

- **Trend Confirmation:** EMA (13 / 34) crossover
- **Momentum Filter:** RSI-based regime validation
- **Volatility / Participation Filter:** Trades taken only during expansion phases
- **Risk Management:** Fixed risk per trade with minimum 1:2 risk-reward ratio

The system supports long and short trading on indices and applies conservative execution logic for equities.

---

## ✨ Key Features

- 📈 Trend-following using EMA crossovers  
- ⚡ Momentum confirmation via RSI  
- 🌪️ Volatility & participation filters  
- 🛡️ Strict stop-loss and target-based exits  
- 📊 Long-term backtesting and performance analysis  
- 🖥️ Interactive Streamlit dashboard  

---

## 🛠️ Tech Stack

- **Language:** Python  
- **Data Analysis:** pandas, numpy  
- **Visualization:** plotly  
- **Dashboard:** Streamlit  
- **Research:** Jupyter Notebook  

---

## 📊 Interactive Dashboard

The Streamlit dashboard provides:
- Equity curve visualization
- Win/Loss distribution
- Asset-wise PnL breakdown
- Detailed trade logs with filters

### ▶️ Run the Dashboard Locally

```bash
pip install -r requirements.txt
streamlit run app/streamlit_app.py


