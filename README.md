# NBA Playoff Points Pool

A tiny Streamlit website that auto-updates a playoff points pool leaderboard.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Host it free

1. Make a GitHub repo.
2. Upload `app.py` and `requirements.txt`.
3. Go to Streamlit Community Cloud.
4. Create a new app from the repo.
5. Main file path: `app.py`.

The app refreshes NBA playoff totals every 10 minutes.

## Notes

- Uses NBA.com stats through `nba_api`.
- Season is currently set to `2025-26`.
- Playoff scoring is total points only.
- Players with no playoff stats show as 0.
- Corrected `Jarret Allen` to `Jarrett Allen`.
