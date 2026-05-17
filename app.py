import streamlit as st
import pandas as pd

st.set_page_config(page_title="Scoreboard & Matchup Calculator", page_icon="🏆", layout="wide")

st.title("🏆 Scoreboard & Pairwise Matchup Calculator")
st.markdown("""
This app converts your tournament scoreboard into an interactive web interface.
You can edit player statistics on the fly, view customized ledger breakdowns, and see an automated results matrix.
""")

# Default starting data
default_data = {
'Player': ['Mandy', 'Mario', 'Rowen', 'Arf'],
'Win': [3, 1, 1, 2],
'Loss': [1, 2, 3, 1],
'Draw': [0, 1, 0, 1],
'Special': [0, 0, 2, 0]
}

st.subheader("1. Overall Player Standings")
st.markdown("💡 *Double-click any cell below to change a player's stats or add a new row. Keep the column name as 'Player'!*")

# Create the interactive editor
df_players = pd.DataFrame(default_data)
edited_df = st.data_editor(df_players, num_rows="dynamic", key="player_stats_editor", use_container_width=True)

# --- SAFETY CHECK FOR KEYERROR ---
if 'Player' not in edited_df.columns:
st.error("⚠️ **Error:** The column named 'Player' was modified or deleted. Please make sure one column is titled exactly 'Player' so the matchup calculations can work.")
else:
# Safely pull data now that we know 'Player' exists
stats = edited_df.set_index('Player')
player_list = edited_df['Player'].dropna().tolist()

# Layout partitions
col1, col2 = st.columns([1, 1.2])

with col1:
st.subheader("2. Matchup Ledger Breakdown")

if len(player_list) >= 2:
p1 = st.selectbox("Select Player 1 (Perspective)", player_list, index=0)
remaining_players = [p for p in player_list if p != p1]
p2 = st.selectbox("Select Player 2 (Opponent)", remaining_players, index=0)

try:
p1_w = int(stats.loc[p1, 'Win'])
p1_l = int(stats.loc[p1, 'Loss'])
p1_s = int(stats.loc[p1, 'Special'])

p2_w = int(stats.loc[p2, 'Win'])
p2_l = int(stats.loc[p2, 'Loss'])
p2_s = int(stats.loc[p2, 'Special'])

net_win = p1_w + p2_l + p1_s
net_loss = p2_w + p1_l + p2_s
total_score = net_win - net_loss

st.markdown(f"### 📊 Breakdown: **{p1}** vs **{p2}**")
st.markdown(f"**Additions (Wins & Advantages):**")
st.write(f"🔹 {p1} Wins: `{p1_w}`")
st.write(f"🔹 Add: {p2} Losses: `{p2_l}`")
st.write(f"🔹 {p1} Special: `{p1_s}`")
st.info(f"**Net Win Subtotal:** `{net_win}`")

st.markdown(f"**Deductions (Losses & Disadvantages):**")
st.write(f"🔸 Less: {p2} Wins: `{p2_w}`")
st.write(f"🔸 {p1} Losses: `{p1_l}`")
st.write(f"🔸 {p2} Special: `{p2_s}`")
st.error(f"**Net Loss Subtotal:** `{net_loss}`")

if total_score >= 0:
st.success(f"### Total Points for {p1}: `+{total_score}`")
else:
st.error(f"### Total Points for {p1}: `{total_score}`")
except Exception as e:
st.warning("Please fill out all numeric cells (Win, Loss, Special) for your players to see the calculation.")
else:
st.warning("Please ensure there are at least 2 players in the standings table.")

with col2:
st.subheader("3. Automated Pairwise Points Matrix")
st.markdown("This matrix automatically displays the finalized **Total Points** for the player listed on the **Row** vs the player on the **Column**.")

if len(player_list) > 0:
matrix_df = pd.DataFrame(index=player_list, columns=player_list)
for row_p in player_list:
for col_p in player_list:
if row_p == col_p:
matrix_df.loc[row_p, col_p] = 0
else:
try:
r_w, r_l, r_s = int(stats.loc[row_p, 'Win']), int(stats.loc[row_p, 'Loss']), int(stats.loc[row_p, 'Special'])
c_w, c_l, c_s = int(stats.loc[col_p, 'Win']), int(stats.loc[col_p, 'Loss']), int(stats.loc[col_p, 'Special'])

n_win = r_w + c_l + r_s
n_loss = c_w + r_l + c_s
matrix_df.loc[row_p, col_p] = n_win - n_loss
except:
matrix_df.loc[row_p, col_p] = 0

st.dataframe(
matrix_df.style.background_gradient(cmap="coolwarm", axis=None).format("{:}"),
use_container_width=True
)
