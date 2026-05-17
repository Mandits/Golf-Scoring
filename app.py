import streamlit as st
import pandas as pd

st.set_page_config(page_title="Scoreboard & Matchup Calculator", page_icon="🏆", layout="wide")

st.title("🏆 Scoreboard & Pairwise Matchup Calculator")
st.markdown("""
This app converts your tournament scoreboard into an interactive web interface.
Adjust player stats using the panel below to update calculations instantly.
""")

# 1. Initialize stable scoreboard memory cleanly on separate lines
if 'mandy_w' not in st.session_state:
st.session_state.mandy_w = 3
st.session_state.mandy_l = 1
st.session_state.mandy_s = 0
st.session_state.mario_w = 1
st.session_state.mario_l = 2
st.session_state.mario_s = 0
st.session_state.rowen_w = 1
st.session_state.rowen_l = 3
st.session_state.rowen_s = 2
st.session_state.arf_w = 2
st.session_state.arf_l = 1
st.session_state.arf_s = 0

# --- SECTION 1: EDIT PLAYER STATS (MOBILE OPTIMIZED) ---
st.subheader("1. Update Player Statistics")
edit_player = st.selectbox("Select a player to modify:", ["Mandy", "Mario", "Rowen", "Arf"])

if edit_player == "Mandy":
st.session_state.mandy_w = st.number_input("Mandy Wins", value=st.session_state.mandy_w, step=1)
st.session_state.mandy_l = st.number_input("Mandy Losses", value=st.session_state.mandy_l, step=1)
st.session_state.mandy_s = st.number_input("Mandy Special Points", value=st.session_state.mandy_s, step=1)
elif edit_player == "Mario":
st.session_state.mario_w = st.number_input("Mario Wins", value=st.session_state.mario_w, step=1)
st.session_state.mario_l = st.number_input("Mario Losses", value=st.session_state.mario_l, step=1)
st.session_state.mario_s = st.number_input("Mario Special Points", value=st.session_state.mario_s, step=1)
elif edit_player == "Rowen":
st.session_state.rowen_w = st.number_input("Rowen Wins", value=st.session_state.rowen_w, step=1)
st.session_state.rowen_l = st.number_input("Rowen Losses", value=st.session_state.rowen_l, step=1)
st.session_state.rowen_s = st.number_input("Rowen Special Points", value=st.session_state.rowen_s, step=1)
elif edit_player == "Arf":
st.session_state.arf_w = st.number_input("Arf Wins", value=st.session_state.arf_w, step=1)
st.session_state.arf_l = st.number_input("Arf Losses", value=st.session_state.arf_l, step=1)
st.session_state.arf_s = st.number_input("Arf Special Points", value=st.session_state.arf_s, step=1)

# Compile current memory state into a clean dictionary
active_scores = {
"Mandy": {"Win": st.session_state.mandy_w, "Loss": st.session_state.mandy_l, "Special": st.session_state.mandy_s},
"Mario": {"Win": st.session_state.mario_w, "Loss": st.session_state.mario_l, "Special": st.session_state.mario_s},
"Rowen": {"Win": st.session_state.rowen_w, "Loss": st.session_state.rowen_l, "Special": st.session_state.rowen_s},
"Arf": {"Win": st.session_state.arf_w, "Loss": st.session_state.arf_l, "Special": st.session_state.arf_s}
}

# Display overall standings grid
st.markdown("### Current Standings Table")
display_df = pd.DataFrame.from_dict(active_scores, orient='index')
st.dataframe(display_df, use_container_width=True)

player_list = list(active_scores.keys())

# --- SECTION 2: MATCHUP LEDGER BREAKDOWN ---
st.markdown("---")
st.subheader("2. Matchup Ledger Breakdown")

p1 = st.selectbox("Select Player 1 (Perspective)", player_list, index=0)
remaining_players = [p for p in player_list if p != p1]
p2 = st.selectbox("Select Player 2 (Opponent)", remaining_players, index=0)

p1_w = active_scores[p1]["Win"]
p1_l = active_scores[p1]["Loss"]
p1_s = active_scores[p1]["Special"]

p2_w = active_scores[p2]["Win"]
p2_l = active_scores[p2]["Loss"]
p2_s = active_scores[p2]["Special"]

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

n_win = active_scores[row_p]["Win"] + active_scores[col_p]["Loss"] + active_scores[row_p]["Special"]
n_loss = active_scores[col_p]["Win"] + active_scores[row_p]["Loss"] + active_scores[col_p]["Special"]
matrix_df.loc[row_p, col_p] = n_win - n_loss

st.dataframe(matrix_df, use_container_width=True)
