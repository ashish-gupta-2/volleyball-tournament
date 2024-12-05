from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Teams and players
teams = {"Team A": [], "Team B": [], "Team C": [], "Team D": []}
players = {}
MAX_PLAYERS_PER_TEAM = 7

# Register a player
@app.route('/register_player', methods=['POST'])
def register_player():
    data = request.json
    name = data['name']
    min_bid = float(data['min_bid'])
    
    if name in players:
        return jsonify({"success": False, "message": f"Player {name} is already registered."})
    
    players[name] = {"min_bid": min_bid, "highest_bid": 0, "team": None}
    return jsonify({"success": True, "message": f"Player {name} registered successfully with a minimum bid of {min_bid}."})

# Place a bid
@app.route('/place_bid', methods=['POST'])
def place_bid():
    data = request.json
    team = data['team']
    player_name = data['player_name']
    bid = float(data['bid'])
    
    if team not in teams:
        return jsonify({"success": False, "message": "Invalid team name."})
    
    if len(teams[team]) >= MAX_PLAYERS_PER_TEAM:
        return jsonify({"success": False, "message": f"{team} already has {MAX_PLAYERS_PER_TEAM} players."})
    
    if player_name not in players:
        return jsonify({"success": False, "message": "Player not found."})
    
    if players[player_name]["team"] is not None:
        return jsonify({"success": False, "message": f"Player {player_name} is already assigned to {players[player_name]['team']}."})
    
    if bid < players[player_name]["min_bid"]:
        return jsonify({"success": False, "message": f"Bid must be at least {players[player_name]['min_bid']}."})
    
    if bid > players[player_name]["highest_bid"]:
        players[player_name]["highest_bid"] = bid
        players[player_name]["team"] = team
        teams[team].append(player_name)
        return jsonify({"success": True, "message": f"{team} successfully bid {bid} for {player_name}."})
    else:
        return jsonify({"success": False, "message": "Your bid is not higher than the current highest bid."})

# Display teams and players
@app.route('/get_teams', methods=['GET'])
def get_teams():
    return jsonify({"teams": teams})

# Home route to serve the UI
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
