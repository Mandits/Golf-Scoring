import ui
import dialogs

# 1. Base Scoreboard Data
players = [
   {'Player': 'Mandy', 'Win': 3, 'Loss': 1, 'Draw': 0, 'Special': 0},
   {'Player': 'Mario', 'Win': 1, 'Loss': 2, 'Draw': 1, 'Special': 0},
   {'Player': 'Rowen', 'Win': 1, 'Loss': 3, 'Draw': 0, 'Special': 2},
   {'Player': 'Arf',   'Win': 2, 'Loss': 1, 'Draw': 1, 'Special': 0}
]

def get_player_stats(name):
   for p in players:
       if p['Player'] == name:
           return p
   return None

# 2. Main Logic Calculation
def calculate_matchup(p1_name, p2_name):
   p1 = get_player_stats(p1_name)
   p2 = get_player_stats(p2_name)

   if not p1 or not p2:
       return 0, 0, 0

   net_win = p1['Win'] + p2['Loss'] + p1['Special']
   net_loss = p2['Win'] + p1['Loss'] + p2['Special']
   total = net_win - net_loss
   return net_win, net_loss, total

# 3. iPad UI Actions
def update_calculator(sender):
   # Get values from dropdown picks
   p1 = v['player1_pick'].title
   p2 = v['player2_pick'].title

   if p1 == p2:
       v['result_label'].text = "Select two different players."
       return

   net_win, net_loss, total = calculate_matchup(p1, p2)

   summary = (
       f"Perspective: {p1} vs {p2}\n\n"
       f"➕ Additions ({p1} Wins + {p2} Losses + {p1} Special): {net_win}\n"
       f"➖ Deductions ({p2} Wins + {p1} Losses + {p2} Special): {net_loss}\n\n"
       f"🏆 TOTAL POINTS FOR {p1.upper()}: {total:+}"
   )
   v['result_label'].text = summary

def change_p1(sender):
   names = [p['Player'] for p in players]
   sel = dialogs.list_dialog('Select Player 1', names)
   if sel:
       sender.title = sel
       update_calculator(None)

def change_p2(sender):
   names = [p['Player'] for p in players]
   sel = dialogs.list_dialog('Select Player 2', names)
   if sel:
       sender.title = sel
       update_calculator(None)

def view_standings(sender):
   # Display an interactive grid to edit stats right on the iPad
   edited = dialogs.form_dialog(title="Edit Player Wins", fields=[
       {'type': 'number', 'title': 'Mandy Wins', 'key': 'Mandy', 'value': players[0]['Win']},
       {'type': 'number', 'title': 'Mario Wins', 'key': 'Mario', 'value': players[1]['Win']},
       {'type': 'number', 'title': 'Rowen Wins', 'key': 'Rowen', 'value': players[2]['Win']},
       {'type': 'number', 'title': 'Arf Wins',   'key': 'Arf',   'value': players[3]['Win']},
   ])
   if edited:
       players[0]['Win'] = int(edited['Mandy'] or 0)
       players[1]['Win'] = int(edited['Mario'] or 0)
       players[2]['Win'] = int(edited['Rowen'] or 0)
       players[3]['Win'] = int(edited['Arf'] or 0)
       update_calculator(None)

# 4. Building the iPad View Layout
v = ui.View()
v.name = 'Scoreboard Calculator'
v.background_color = '#f0f4f8'

# Headings & Layout Buttons
lbl = ui.Label(frame=(20, 20, 300, 40), text="🏆 Matchup Pairwise Ledger", font=('<system-bold>', 20))
v.add_subview(lbl)

btn_edit = ui.Button(frame=(20, 70, 200, 40), title="✏️ Edit Player Wins Data")
btn_edit.background_color = '#007fff'
btn_edit.tint_color = 'white'
btn_edit.corner_radius = 5
btn_edit.action = view_standings
v.add_subview(btn_edit)

# Selection controls
lbl_vs = ui.Label(frame=(140, 145, 50, 40), text="VS", font=('<system-bold>', 16), alignment=ui.ALIGN_CENTER)
v.add_subview(lbl_vs)

btn_p1 = ui.Button(name='player1_pick', frame=(20, 140, 110, 50), title="Mandy")
btn_p1.background_color = '#ffffff'
btn_p1.tint_color = '#333333'
btn_p1.border_width = 1
btn_p1.border_color = '#cccccc'
btn_p1.action = change_p1
v.add_subview(btn_p1)

btn_p2 = ui.Button(name='player2_pick', frame=(200, 140, 110, 50), title="Mario")
btn_p2.background_color = '#ffffff'
btn_p2.tint_color = '#333333'
btn_p2.border_width = 1
btn_p2.border_color = '#cccccc'
btn_p2.action = change_p2
v.add_subview(btn_p2)

# Result Box
res_box = ui.TextView(name='result_label', frame=(20, 210, 290, 200))
res_box.font = ('<system>', 14)
res_box.editable = False
res_box.background_color = '#ffffff'
res_box.border_width = 1
res_box.border_color = '#e0e0e0'
v.add_subview(res_box)

# Present the app on iPad screen
v.present('sheet')
update_calculator(None)
