import streamlit as st
import pandas as pd

st.set_page_config(page_title="Scoreboard & Matchup Calculator", page_icon="🏆", layout="wide")

st.title("🏆 Scoreboard & Pairwise Matchup Calculator")
st.markdown("This app converts your tournament scoreboard into an interactive web interface. Adjust player stats using the panel below to update calculations instantly.")

st.subheader("1. Update Player Statistics")
edit_player = st.selectbox("Select a player to modify:", ["Mandy", "Mario", "Rowen", "Arf"])

st.session_state.current_w = st.number_input("Selected Player Wins", value=1, step=1)
st.session_state.current_l = st.number_input("Selected Player Losses", value=1, step=1)
st.session_state.current_s = st.number_input("Selected Player Special Points", value=0, step=1)

active_scores = {
"Mandy": {"Win": 3, "Loss": 1, "Special": 0},
"Mario": {"Win": 1, "Loss": 2, "Special": 0},
"Rowen": {"Win": 1, "Loss": 3, "Special": 2},
"Arf": {"Win": 2, "Loss": 1, "Special": 0}
}

active_scores[edit_player]["Win"] = st.session_state.current_w
active_scores[edit_player]["Loss"] = st.session_state.current_l
active_scores[edit_player]["Special"] = st.session_state.current_s

st.markdown("### Current Standings Table")
display_df = pd.DataFrame.from_dict(active_scores, orient='index')
st.dataframe(display_df, use_container_width=True)

st.markdown("---")
st.subheader("2. Matchup Ledger Breakdown")

p1 = st.selectbox("Select Player 1 (Perspective)", ["Mandy", "Mario", "Rowen", "Arf"], index=0)
p2 = st.selectbox("Select Player 2 (Opponent)", ["Mandy", "Mario", "Rowen", "Arf"], index=1)

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
st.write(f"🔹 {p1} Wins: `{p1_w}` | Add {p2} Losses: `{p2_l}` | {p1} Special: `{p1_s}`")
st.info(f"**Net Win Subtotal:** `{net_win}`")
st.write(f"🔸 Less {p2} Wins: `{p2_w}` | {p1} Losses: `{p1_l}` | {p2} Special: `{p2_s}`")
st.error(f"**Net Loss Subtotal:** `{net_loss}`")

st.success(f"### Total Points for {p1}: `{total_score}`")

st.markdown("---")
st.subheader("3. Automated Pairwise Points Matrix")

matrix_df = pd.DataFrame(index=["Mandy", "Mario", "Rowen", "Arf"], columns=["Mandy", "Mario", "Rowen", "Arf"])

matrix_df.loc["Mandy", "Mandy"] = 0
matrix_df.loc["Mandy", "Mario"] = (active_scores["Mandy"]["Win"] + active_scores["Mario"]["Loss"] + active_scores["Mandy"]["Special"]) - (active_scores["Mario"]["Win"] + active_scores["Mandy"]["Loss"] + active_scores["Mario"]["Special"])
matrix_df.loc["Mandy", "Rowen"] = (active_scores["Mandy"]["Win"] + active_scores["Rowen"]["Loss"] + active_scores["Mandy"]["Special"]) - (active_scores["Rowen"]["Win"] + active_scores["Mandy"]["Loss"] + active_scores["Rowen"]["Special"])
matrix_df.loc["Mandy", "Arf"] = (active_scores["Mandy"]["Win"] + active_scores["Arf"]["Loss"] + active_scores["Mandy"]["Special"]) - (active_scores["Arf"]["Win"] + active_scores["Mandy"]["Loss"] + active_scores["Arf"]["Special"])

matrix_df.loc["Mario", "Mandy"] = (active_scores["Mario"]["Win"] + active_scores["Mandy"]["Loss"] + active_scores["Mario"]["Special"]) - (active_scores["Mandy"]["Win"] + active_scores["Mario"]["Loss"] + active_scores["Mandy"]["Special"])
matrix_df.loc["Mario", "Mario"] = 0
matrix_df.loc["Mario", "Rowen"] = (active_scores["Mario"]["Win"] + active_scores["Rowen"]["Loss"] + active_scores["Mario"]["Special"]) - (active_scores["Rowen"]["Win"] + active_scores["Mario"]["Loss"] + active_scores["Rowen"]["Special"])
matrix_df.loc["Mario", "Arf"] = (active_scores["Mario"]["Win"] + active_scores["Arf"]["Loss"] + active_scores["Mario"]["Special"]) - (active_scores["Arf"]["Win"] + active_scores["Mario"]["Loss"] + active_scores["Arf"]["Special"])

matrix_df.loc["Rowen", "Mandy"] = (active_scores["Rowen"]["Win"] + active_scores["Mandy"]["Loss"] + active_scores["Rowen"]["Special"]) - (active_scores["Mandy"]["Win"] + active_scores["Rowen"]["Loss"] + active_scores["Mandy"]["Special"])
matrix_df.loc["Rowen", "Mario"] = (active_scores["Rowen"]["Win"] + active_scores["Mario"]["Loss"] + active_scores["Rowen"]["Special"]) - (active_scores["Mario"]["Win"] + active_scores["Rowen"]["Loss"] + active_scores["Mario"]["Special"])
matrix_df.loc["Rowen", "Rowen"] = 0
matrix_df.loc["Rowen", "Arf"] = (active_scores["Rowen"]["Win"] + active_scores["Arf"]["Loss"] + active_scores["Rowen"]["Special"]) - (active_scores["Arf"]["Win"] + active_scores["Rowen"]["Loss"] + active_scores["Arf"]["Special"])

matrix_df.loc["Arf", "Mandy"] = (active_scores["Arf"]["Win"] + active_scores["Mandy"]["Loss"] + active_scores["Arf"]["Special"]) - (active_scores["Mandy"]["Win"] + active_scores["Arf"]["Loss"] + active_scores["Mandy"]["Special"])
matrix_df.loc["Arf", "Mario"] = (active_scores["Arf"]["Win"] + active_scores["Mario"]["Loss"] + active_scores["Arf"]["Special"]) - (active_scores["Mario"]["Win"] + active_scores["Arf"]["Loss"] + active_scores["Mario"]["Special"])
matrix_df.loc["Arf", "Rowen"] = (active_scores["Arf"]["Win"] + active_scores["Rowen"]["Loss"] + active_scores["Arf"]["Special"]) - (active_scores["Rowen"]["Win"] + active_scores["Arf"]["Loss"] + active_scores["Rowen"]["Special"])
matrix_df.loc["Arf", "Arf"] = 0

st.dataframe(matrix_df, use_container_width=True)
