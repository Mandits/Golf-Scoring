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

# 1. Safety check for column presence
if 'Player' not in edited_df.columns:
st.error("⚠️ **Error:** The column named 'Player' was modified or deleted. Please make sure one column is titled exactly 'Player'.")
st.stop()

# Safely convert data to a dictionary lookup to prevent KeyErrors entirely
stats_dict = edited_df.dropna(subset=['Player']).set_index('Player').to_dict(orient='index')
player_list = list(stats_dict.keys())

# Helper function to completely eliminate NoneType/Blank cell crashes
def safe_int(val):
if val is None or pd.isna(val) or val == "":
return 0
try:
return int(float(val))
except:
return 0

# 2. Safety check for player count
if len(player_list) < 2:
st.warning("Please ensure there are at least 2 players in the standings table.")
st.stop()

# --- SECTION 2: MATCHUP LEDGER BREAKDOWN ---
st.markdown("---")
st.subheader("2. Matchup Ledger Breakdown")

p1 = st.selectbox("Select Player 1 (Perspective)", player_list, index=0)
remaining_players = [p for p in player_list if p != p1]
p2 = st.selectbox("Select Player 2 (Opponent)", remaining_players, index=0)

# Extract statistics using our safe_int tool
p1_data = stats_dict.get(p1, {})
p2_data = stats_dict.get(p2, {})

p1_w = safe_int(p1_data.get('Win', 0))
p1_l = safe_int(p1_data.get('Loss', 0))
p1_s = safe_int(p1_data.get('Special', 0))

p2_w = safe_int(p2_data.get('Win', 0))
p2_l = safe_int(p2_data.get('Loss', 0))
p2_s = safe_int(p2_data.get('Special', 0))

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

# --- SECTION 3: AUTOMATED PAIRWISE POINTS MATRIX ---
st.markdown("---")
st.subheader("3. Automated Pairwise Points Matrix")
st.markdown("This matrix automatically displays the finalized **Total Points** for the player listed on the **Row** vs the player on the **Column**.")

matrix_df = pd.DataFrame(index=player_list, columns=player_list)

for row_p in player_list:
for col_p in player_list:
if row_p == col_p:
matrix_df.loc[row_p, col_p] = 0
continue

r_data = stats_dict.get(row_p, {})
c_data = stats_dict.get(col_p, {})

r_w = safe_int(r_data.get('Win', 0))
r_l = safe_int(r_data.get('Loss', 0))
r_s = safe_int(r_data.get('Special', 0))

c_w = safe_int(c_data.get('Win', 0))
c_l = safe_int(c_data.get('Loss', 0))
c_s = safe_int(c_data.get('Special', 0))

n_win = r_w + c_l + r_s
n_loss = c_w + r_l + c_s
matrix_df.loc[row_p, col_p] = n_win - n_loss

st.dataframe(matrix_df, use_container_width=True)
