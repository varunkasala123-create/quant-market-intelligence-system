🧠 Repository Description (README Intro)

A modular, data-driven market intelligence system designed to analyze multi-asset financial data, generate probabilistic trade signals, and evaluate strategy performance using machine learning and rule-based risk controls.

The system integrates real-time data ingestion, feature engineering, regime detection, model training, backtesting, and a live decision dashboard to support structured intraday and swing trading analysis.

🚀 Key Features
📊 Data Pipeline
Multi-asset data ingestion (crypto, equities, ETFs via Alpaca API)
Continuous dataset building with deduplication and time-series integrity
Centralized parquet-based storage system
→ see:
🧠 Feature Engineering Engine
Technical indicators:
EMA (20, 50, 200)
RSI
ATR (volatility modeling)
Derived signals:
Trend strength
Volume spikes
Price deviation from moving averages
→ see:
🤖 Machine Learning Models
LightGBM-based classification model
ATR-normalized labeling strategy
Walk-forward validation split (time-series aware)
GPU-enabled training
→ see:
📈 Strategy Backtesting Engine
Walk-forward backtesting with:
Slippage & commission simulation
TP/SL based on ATR
Equity curve + drawdown tracking
Performance metrics:
Win rate
Sharpe ratio
Profit factor
→ see:
🧭 Market Regime Detection
Classifies market into:
UPTREND
DOWNTREND
SIDEWAYS
Based on EMA crossover + volatility filtering
→ see:
⚠️ Risk Management System
Dynamic position sizing based on:
Stop-loss distance
Account risk %
Capital exposure constraints
→ see:
🧠 Signal Filtering Logic
Probability-based entry thresholds
Regime-aware filtering (avoids sideways markets)
Confidence-ranked trade selection
→ see:
📰 News Sentiment Layer (Experimental)
Basic sentiment extraction from news headlines
Score aggregation for additional signal context
→ see:
📊 Live Dashboard (Streamlit)
Displays:
Intraday & swing trade opportunities
Confidence scores
Expected returns
Manual trade execution logging system
→ see:
🔄 Automated Market Scanner
Multi-threaded asset scanning
Continuous live signal generation
Separate intraday & swing strategies
→ see:
⚙️ Tech Stack
Python
Pandas, NumPy
LightGBM (ML model)
Streamlit (dashboard)
Alpaca API (market data)
Joblib (model persistence)
Parquet (data storage)
