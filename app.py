import streamlit as st
import pandas as pd
from nba_api.stats.endpoints import leaguedashplayerstats

st.set_page_config(
    page_title="NBA Playoff Points Pool",
    page_icon="🏀",
    layout="wide",
)

SEASON = "2025-26"

TEAMS = {
    "Fio": [
        "Shai Gilgeous-Alexander",
        "Stephon Castle",
        "OG Anunoby",
        "Jared McCain",
        "Jarrett Allen",
    ],
    "Mack": [
        "Jaylen Brown",
        "James Harden",
        "Alperen Sengun",
        "LeBron James",
        "Sam Hauser",
    ],
    "Kyle": [
        "Victor Wembanyama",
        "Payton Pritchard",
        "Ajay Mitchell",
        "Dylan Harper",
        "Duncan Robinson",
    ],
    "Jesse": [
        "Donovan Mitchell",
        "Anthony Edwards",
        "Jaden McDaniels",
        "Nikola Vučević",
        "Christian Braun",
    ],
    "Ryan": [
        "Jayson Tatum",
        "Derrick White",
        "Jalen Duren",
        "Tobias Harris",
        "Deni Avdija",
    ],
    "Bradley": [
        "Nikola Jokić",
        "Kevin Durant",
        "Aaron Gordon",
        "Tyrese Maxey",
        "Cameron Johnson",
    ],
    "Zelig": [
        "De'Aaron Fox",
        "Jalen Johnson",
        "Devin Vassell",
        "Nickeil Alexander-Walker",
        "CJ McCollum",
    ],
    "Liv": [
        "Jalen Brunson",
        "Cade Cunningham",
        "Julius Randle",
        "Mikal Bridges",
        "Jabari Smith Jr.",
    ],
    "Joe": [
        "Chet Holmgren",
        "Jamal Murray",
        "Keldon Johnson",
        "Neemias Queta",
        "Aaron Wiggins",
    ],
    "Kling": [
        "Karl-Anthony Towns",
        "Jalen Williams",
        "Evan Mobley",
        "Amen Thompson",
        "Isaiah Joe",
    ],
}


@st.cache_data(ttl=600)
def get_playoff_points() -> pd.DataFrame:
    stats = leaguedashplayerstats.LeagueDashPlayerStats(
        season=SEASON,
        season_type_all_star="Playoffs",
        per_mode_detailed="Totals",
        timeout=30,
    )
    df = stats.get_data_frames()[0]

    keep_cols = ["PLAYER_NAME", "TEAM_ABBREVIATION", "GP", "PTS"]
    df = df[keep_cols].copy()
    df = df.rename(
        columns={
            "PLAYER_NAME": "Player",
            "TEAM_ABBREVIATION": "NBA Team",
            "GP": "Games",
            "PTS": "Points",
        }
    )

    df["Points"] = pd.to_numeric(df["Points"], errors="coerce").fillna(0).astype(int)
    df["Games"] = pd.to_numeric(df["Games"], errors="coerce").fillna(0).astype(int)

    return df


def build_pool_tables(stats_df: pd.DataFrame):
    rows = []

    for owner, players in TEAMS.items():
        for player in players:
            match = stats_df[stats_df["Player"].str.lower() == player.lower()]

            if not match.empty:
                row = match.iloc[0]
                points = int(row["Points"])
                games = int(row["Games"])
                nba_team = row["NBA Team"]
                status = "Matched"
            else:
                points = 0
                games = 0
                nba_team = ""
                status = "No playoff stats yet"

            rows.append(
                {
                    "Owner": owner,
                    "Player": player,
                    "NBA Team": nba_team,
                    "Games": games,
                    "Points": points,
                    "Status": status,
                }
            )

    player_table = pd.DataFrame(rows)

    leaderboard = (
        player_table.groupby("Owner", as_index=False)["Points"]
        .sum()
        .sort_values("Points", ascending=False)
        .reset_index(drop=True)
    )
    leaderboard.insert(0, "Rank", leaderboard.index + 1)

    return leaderboard, player_table


st.title("🏀 NBA Playoff Points Pool")
st.caption("Auto-updating leaderboard based on NBA playoff player total points.")

try:
    stats_df = get_playoff_points()
    leaderboard, player_table = build_pool_tables(stats_df)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Leader", leaderboard.iloc[0]["Owner"])
    with col2:
        st.metric("Winning Points", int(leaderboard.iloc[0]["Points"]))
    with col3:
        st.metric("Refreshes Every", "10 min")

    st.subheader("Leaderboard")
    st.dataframe(leaderboard, use_container_width=True, hide_index=True)

    st.subheader("Drafted Player Breakdown")
    st.dataframe(
        player_table.sort_values(["Owner", "Points"], ascending=[True, False]),
        use_container_width=True,
        hide_index=True,
    )

    unmatched = player_table[player_table["Status"] != "Matched"]
    if not unmatched.empty:
        st.warning(
            "Some players have no playoff stats yet. This can mean they have not played, are eliminated, "
            "or their name needs a spelling fix."
        )
        st.dataframe(
            unmatched[["Owner", "Player", "Status"]],
            use_container_width=True,
            hide_index=True,
        )

    with st.expander("Raw NBA playoff player totals"):
        st.dataframe(
            stats_df.sort_values("Points", ascending=False),
            use_container_width=True,
            hide_index=True,
        )

except Exception as e:
    st.error("Could not load NBA playoff stats.")
    st.write("Try refreshing in a minute. NBA stats sometimes rate-limits requests.")
    st.exception(e)
