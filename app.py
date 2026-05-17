import streamlit as st
import pandas as pd

st.set_page_config(page_title="Scoreboard & Matchup Calculator", page_icon="🏆", layout="wide")

st.title("🏆 Scoreboard & Pairwise Matchup Calculator")
st.markdown("""
This app converts your tournament scoreboard into an interactive web interface.
You can edit player statistics on the fly, view customized ledger breakdowns, and see an automated results matrix.
""")

# 1. Store initial scoreboard row data securely in persistent session memory
if 'main_scores' not in st.session_state:
st.session_state.main_scores = {
'Mandy': {'Win': 3, 'Loss': 1, 'Draw': 0, 'Special': 0},
'Mario': {'Win': 1, 'Loss': 2, 'Draw': 1, 'Special': 0},
'Rowen': {'Win': 1, 'Loss': 3, 'Draw': 0, 'Special': 2},
'Arf': {'Win': 2, 'Loss': 1, 'Draw': 1, 'Special': 0}
}

st.subheader("1. Overall Player Standings")
st.markdown("💡 *Modify numbers below to update calculations instantly. To add/change players, use the menu parameters below.*")

# Helper tool to clean up inputs
def safe_int(val):
if val is None or pd.isna(val) or val == "":
return 0
try:
return int(float(val))
except:
return 0

# Display data editor using a clean, static dataframe constructed from our secure memory
display_df = pd.DataFrame.from_dict(st.session_state.main_scores, orient='index').reset_index()
display_df.rename(columns={'index': 'Player'}, inplace=True)

# Render interactive grid
user_updates = st.data_editor(display_df, num_rows="dynamic", use_container_width=True)

# Manually extract the values safely to rebuild our internal memory dictionary
stats_dict = {}
try:
if isinstance(user_updates, pd.DataFrame):
for _, row in user_updates.iterrows():
p_name = str(row.get('Player', '')).strip()
if p_name and p_name != 'None' and p_name != 'nan':
stats_dict[p_name] = {
'Win': safe_int(row.get('Win', 0)),
'Loss': safe_int(row.get('Loss', 0)),
'Special': safe_int(row.get('Special', 0))
}
# Update session storage state dynamically
st.session_state.main_scores = stats_dict
except:
pass

# Use our secure local dictionary for all calculations below
active_scores = st.session_state.main_scores
player_list = list(active_scores.keys())

# Safety check for active player count
if len(player_list) < 2:
st.warning("Please ensure there are at least 2 players in the standings table to run matchups.")
st.stop()

# --- SECTION 2: MATCHUP LEDGER BREAKDOWN ---
st.markdown("---")
st.subheader("2. Matchup Ledger Breakdown")

p1 = st.selectbox("Select Player 1 (Perspective)", player_list, index=0)
remaining_players = [p for p in player_list if p != p1]
p2 = st.selectbox("Select Player 2 (Opponent)", remaining_players, index=0)

p1_data = active_scores.get(p1, {'Win': 0, 'Loss': 0, 'Special': 0})
p2_data = active_scores.get(p2, {'Win': 0, 'Loss': 0, 'Special': 0})

p1_w = p1_data.get('Win', 0)
p1_l = p1_data.get('Loss', 0)
p1_s = p1_data.get('Special', 0)

p2_w = p2_data.get('Win', 0)
p2_l = p2_data.get('Loss', 0)
p2_s = p2_data.get('Special', 0)

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

r_data = active_scores.get(row_p, {'Win': 0, 'Loss': 0, 'Special': 0})
c_data = active_scores.get(col_p, {'Win': 0, 'Loss': 0, 'Special': 0})

n_win = r_data.get('Win', 0) + c_data.get('Loss', 0) + r_data.get('Special', 0)
n_loss = c_data.get('Win', 0) + r_data.get('Loss', 0) + c_data.get('Special', 0)
matrix_df.loc[row_p, col_p] = n_win - n_loss

st.dataframe(matrix_df, use_container_width=True)
