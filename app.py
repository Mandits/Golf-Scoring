import streamlit as st
import pandas as pd

st.set_page_config(page_title="Scoreboard & Matchup Calculator", page_icon="🏆", layout="wide")

st.title("🏆 Scoreboard & Pairwise Matchup Calculator")
st.markdown("""
This app converts your tournament scoreboard into an interactive web interface.
You can edit player statistics on the fly, view customized ledger breakdowns, and see an automated results matrix.
""")

# 1. Initialize stable starting data in the app memory
if 'scoreboard_data' not in st.session_state:
st.session_state.scoreboard_data = pd.DataFrame({
'Player': ['Mandy', 'Mario', 'Rowen', 'Arf'],
'Win': [3, 1, 1, 2],
'Loss': [1, 2, 3, 1],
'Draw': [0, 1, 0, 1],
'Special': [0, 0, 2, 0]
})

st.subheader("1. Overall Player Standings")
st.markdown("💡 *Double-click any cell below to change a player's stats or add a new row. Keep the column name as 'Player'!*")

# Helper function to completely eliminate blank cell crashes
def safe_int(val):
if val is None or pd.isna(val) or val == "":
return 0
try:
return int(float(val))
except:
return 0

# Create the interactive editor linked directly to stable memory
edited_output = st.data_editor(st.session_state.scoreboard_data, num_rows="dynamic", key="player_stats_editor", use_container_width=True)

# Process data safely from the stable session storage instead of raw editor outputs
try:
if isinstance(edited_output, pd.DataFrame):
st.session_state.scoreboard_data = edited_output
except:
pass

stable_df = st.session_state.scoreboard_data

# Ensure 'Player' column is present in our stable dataframe
if 'Player' not in stable_df.columns:
st.error("⚠️ **Error:** The column named 'Player' was modified or deleted. Please make sure one column is titled exactly 'Player'.")
st.stop()

# Convert rows to lookup dictionary
stats_dict = {}
for _, row in stable_df.dropna(subset=['Player']).iterrows():
p_name = str(row['Player']).strip()
if p_name:
stats_dict[p_name] = {
'Win': safe_int(row.get('Win', 0)),
'Loss': safe_int(row.get('Loss', 0)),
'Special': safe_int(row.get('Special', 0))
}

player_list = list(stats_dict.keys())

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

p1_data = stats_dict.get(p1, {'Win': 0, 'Loss': 0, 'Special': 0})
p2_data = stats_dict.get(p2, {'Win': 0, 'Loss': 0, 'Special': 0})

p1_w = p1_data['Win']
p1_l = p1_data['Loss']
p1_s = p1_data['Special']

p2_w = p2_data['Win']
p2_l = p2_data['Loss']
p2_s = p2_data['Special']

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

r_data = stats_dict.get(row_p, {'Win': 0, 'Loss': 0, 'Special': 0})
c_data = stats_dict.get(col_p, {'Win': 0, 'Loss': 0, 'Special': 0})

n_win = r_data['Win'] + c_data['Loss'] + r_data['Special']
n_loss = c_data['Win'] + r_data['Loss'] + c_data['Special']
matrix_df.loc[row_p, col_p] = n_win - n_loss

st.dataframe(matrix_df, use_container_width=True)
