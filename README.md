# Global + India Momentum Tracker

A simple dashboard for one useful question: **which stocks are moving today, and why?**
It tracks Indian and global stocks, combines price action, news, and macro data,
then ranks potential gainers and losers. Open **Why?** to see the reasoning.
This is a research tool, not a trading bot or a promise about future prices.

## Highlights
- 31 NSE stocks and 13 global stocks
- RSI, MACD, moving averages, and volatility
- News sentiment with NewsAPI and VADER
- Oil, USD/INR, rates, VIX, Nifty, S&P 500, and Nasdaq context
- Real 60-day stock-to-macro correlations
- Historical examples of COVID-19, oil shocks, Fed cycles, and demonetization

## Score and accuracy
The score ranges from `-100` to `+100`: 
technical momentum 45%, 
news sentiment 30%,
macro context 25%.

There is no measured predictive accuracy yet. With no backtest or prediction log, the score is a heuristic ranking, not an accuracy percentage. The price range describes typical recent volatility, not a guarantee.

## Tech stack
- **Frontend:** React and Vite
- **Backend:** Python, FastAPI, Uvicorn, and APScheduler
- **Data and analysis:** yfinance, pandas, NumPy, NewsAPI, and VADER
- **Storage:** JSON cache

## Run locally
You need Python 3.10+ and Node.js 18+.
powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

In a second terminal:
powershell
cd frontend
npm install
"VITE_API_BASE=http://localhost:8000" | Set-Content .env
npm run dev

Open `http://localhost:5173`. The first refresh may take one or two minutes.
The app works without NewsAPI, but headlines improve the news signal.
Edit watchlists and scoring weights in `backend/app/config.py`.
Market data can be delayed or wrong. This is for education, not financial advice.