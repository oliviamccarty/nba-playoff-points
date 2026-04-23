# NBA Playoff Points Pool

A tiny Streamlit website that auto-updates a playoff points pool leaderboard.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Notes

- Uses NBA.com stats through `nba_api`.
- Season is currently set to `2025-26`.
- Refreshes every 10 minutes.
- Playoff scoring is total points only.
- Players with no playoff stats show as 0.
