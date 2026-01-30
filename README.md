#  StratIQ - Algorithmic Trading Bot 👨‍💻

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

## 🚀 Future Scope

The StratIQ framework is designed to be extensible and scalable. The following enhancements can be explored in future iterations of the project:

1. **Expanded Stock Universe**  
   Extend the strategy to include all remaining stocks across multiple market capitalizations (large-cap, mid-cap, and small-cap) to improve diversification and coverage.

2. **Derivatives Market Expansion**  
   Enhance the strategy for derivatives trading by incorporating **Futures and Options**, supported by improved entry–exit logic and optimized risk management techniques.

3. **Index Returns via Derivatives**  
   Improve index-level return calculations using F&O trading, enabling more accurate hedging and leveraged exposure strategies.

4. **Advanced Trailing Stop-Loss Mechanisms**  
   Implement dynamic trailing stop-loss methods to maximize profit capture while protecting gains during trend reversals.

These improvements will help evolve StratIQ into a more comprehensive, execution-ready algorithmic trading system suitable for real-world deployment.

---

## 🧾 Conclusion

StratIQ demonstrates a structured and disciplined approach to algorithmic trading by combining trend-following logic with momentum confirmation and robust risk management.  

The system emphasizes consistency, capital preservation, and adaptability across different market regimes rather than speculative high returns. Backtesting over long historical periods shows stable performance, controlled drawdowns, and resilience during volatile market conditions.

This project serves as a strong foundation for building production-grade algorithmic trading systems and reflects practical, execution-aware strategy design.

---

## 👥 Team Members

**Team StratIQ**

- Tanvi Patange  
- Madhav Tandon
- Harsh Thakkar
- Nilang Bhuva







