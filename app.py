import pandas as pd
import numpy as np

def automate_points_sheet(input_csv_path, output_csv_path):
# 1. Load the spreadsheet data
df = pd.read_csv(input_csv_path, header=None)

# Initialize a tracking dictionary for the summary table
player_totals = {
'Mandy': {'Win': 0.0, 'Loss': 0.0, 'Draw': 0.0, 'Special': 0.0},
'Mario': {'Win': 0.0, 'Loss': 0.0, 'Draw': 0.0, 'Special': 0.0},
'Rowen': {'Win': 0.0, 'Loss': 0.0, 'Draw': 0.0, 'Special': 0.0},
'Arf': {'Win': 0.0, 'Loss': 0.0, 'Draw': 0.0, 'Special': 0.0}
}

# Define layout coordinates for the 6 matchup blocks:
# (row_start, name_col, label_col, value_col)
matchup_blocks = [
(6, 0, 1, 2), # Mandy-Mario
(6, 4, 5, 6), # Mandy-Rowen
(6, 8, 9, 10), # Mandy-Arf
(17, 0, 1, 2), # Arf-Mario
(17, 4, 5, 6), # Arf-Rowen
(17, 8, 9, 10), # Rowen-Mario
]

# 2. Iterate through each matchup block and perform calculations
for r_start, name_col, label_col, value_col in matchup_blocks:
matchup_name = df.iloc[r_start, name_col]
if pd.isna(matchup_name):
continue

# Extract individual player names from the block header (e.g., "Mandy-Mario")
p1, p2 = matchup_name.split('-')

# Helper function to safely convert cell values to floats
def clean_val(row_offset):
val = df.iloc[r_start + row_offset, value_col]
try:
return float(val) if not pd.isna(val) else 0.0
except ValueError:
return 0.0

# Read the raw user inputs for the matchup
p1_wins = clean_val(1) # e.g., Mandy wins
p2_loss = clean_val(2) # e.g., Mario Loss
p1_special = clean_val(3) # e.g., Mandy Special

p2_win = clean_val(5) # e.g., Mario Win
p1_loss = clean_val(6) # e.g., Mandy Loss
p2_special = clean_val(7) # e.g., Mario Special

# Calculate intermediate fields
net_win = p1_wins + p2_loss + p1_special
net_loss = p2_win + p1_loss + p2_special
total = net_win - net_loss

# Write calculated fields back to the DataFrame
df.iloc[r_start + 4, value_col] = net_win # Net win row
df.iloc[r_start + 8, value_col] = net_loss # Net Loss row
df.iloc[r_start + 9, value_col] = total # Total row

# Accumulate metrics for the summary table
if p1 in player_totals:
player_totals[p1]['Win'] += p1_wins
player_totals[p1]['Loss'] += p1_loss
player_totals[p1]['Special'] += p1_special
if p2 in player_totals:
player_totals[p2]['Win'] += p2_win
player_totals[p2]['Loss'] += p2_loss
player_totals[p2]['Special'] += p2_special

# 3. Populate the Master Summary Table (Rows 1 to 4, Columns E to H)
player_row_indices = {df.iloc[r, 3]: r for r in range(1, 5) if not pd.isna(df.iloc[r, 3])}

for player, row_idx in player_row_indices.items():
if player in player_totals:
df.iloc[row_idx, 4] = player_totals[player]['Win'] # Column E
df.iloc[row_idx, 5] = player_totals[player]['Loss'] # Column F
df.iloc[row_idx, 6] = player_totals[player]['Draw'] # Column G
df.iloc[row_idx, 7] = player_totals[player]['Special'] # Column H

# 4. Save the fully updated sheet
df.to_csv(output_csv_path, index=False, header=False)
print(f"Successfully processed and updated points sheet saved to: {output_csv_path}")

# Run the automation script
automate_points_sheet("Puitns.xlsx - Sheet1.csv", "Processed_Points.csv")
