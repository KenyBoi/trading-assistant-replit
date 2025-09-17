# Copilot Instructions for Trading Assistant Bot

## Project Overview
- **Purpose:** AI-powered trading assistant with real-time market briefs, stock scanning, and an interactive dashboard.
- **Architecture:**
  - **Flask** serves API endpoints (`/api/brief`, `/api/scan`, `/api/status`, `/api/webhook`) and the main web UI.
  - **Streamlit** (run via `app/dashboard.py`) provides the dashboard UI, launched in parallel with Flask.
  - **Configuration** is managed via `app/config.py` and environment variables (see below).
  - **Market data** is fetched using `yfinance` in `app/market_brief.py`.

## Key Files & Structure
- `main.py`: Entry point. Starts Flask (API/UI) and Streamlit (dashboard) in parallel threads.
- `app/config.py`: Loads config from environment (API keys, capital, risk, timezone, watchlist).
- `app/market_brief.py`: Generates market summaries using yfinance and config.
- `README.md`: Documents API endpoints, setup, and secrets.

## Configuration & Secrets
- Set via environment variables or Replit Secrets:
  - `OPENAI_API_KEY` (optional, for AI features)
  - `CAPITAL` (default: 25000)
  - `RISK_PER_TRADE` (default: 0.01)
- Timezone is fixed to `US/Eastern` in config.
- Default watchlist is hardcoded in config.

## Developer Workflows
- **Run locally:** `python main.py` (requires Flask, Streamlit, yfinance, pytz)
- **Dashboard:** Access at `/dashboard` (redirects to Streamlit on port 8501)
- **API:** Access at `/api/*` endpoints (see README)
- **Debugging:**
  - Flask runs with `debug=False` by default. Change in `main.py` if needed.
  - Streamlit logs to console.
- **Testing:** No explicit test suite present. Add tests in a `tests/` directory if needed.

## Project Conventions
- **No database**: All state is in memory or via config/env.
- **Error handling:** Minimal; errors in data fetch print to console.
- **Component boundaries:**
  - API logic is expected in `api/routes.py` (not present in repo; add if needed).
  - Dashboard logic is expected in `app/dashboard.py` (not present in repo; add if needed).
- **Extend endpoints** by adding to Flask blueprint (`api_bp`).

## Integration Points
- **yfinance**: For all market data.
- **OpenAI**: Optional, for AI features (not shown in current code).
- **Streamlit**: For dashboard UI.

## Examples
- To add a new API endpoint, extend `api/routes.py` and register with `api_bp`.
- To change the dashboard, edit or create `app/dashboard.py` (Streamlit app).
- To update config, edit `app/config.py` or set new environment variables.

---

**For more details, see `README.md` and code comments.**
