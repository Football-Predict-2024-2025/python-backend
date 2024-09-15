from flask import Flask, jsonify, url_for, request
from flask_cors import CORS
import pandas as pd
from pandas import Interval


app = Flask(__name__)
CORS(app)

# Data liga dipisahkan ke dalam variabel
leagues = [
    {
        'league_id': 1,
        'league_name': 'English Premier League',
        'country': 'England',
        'total_club': 20,
        'icon_filename': 'images/EPL.png'
    },
    {
        'league_id': 2,
        'league_name': 'La Liga',
        'country': 'Spain',
        'total_club': 20,
        'icon_filename': 'images/LaLiga.png'
    },
    {
        'league_id': 3,
        'league_name': 'Serie A',
        'country': 'Italy',
        'total_club': 20,
        'icon_filename': 'images/SerieA.png'
    },
    {
        'league_id': 4,
        'league_name': 'Ligue 1',
        'country': 'France',
        'total_club': 18,
        'icon_filename': 'images/League1.png'
    },
    {
        'league_id': 5,
        'league_name': 'Bundesliga',
        'country': 'Germany',
        'total_club': 18,
        'icon_filename': 'images/Bundesliga.png'
    }
]

#Data Club Masing-masing liga
epl_data = pd.read_csv('data/EPL_data.csv')

#win probability
teams_of_interest = []
firstteam_choice = 3
secondteam_choice = 9
teams_of_interest.append(firstteam_choice)
teams_of_interest.append(secondteam_choice)
# Extract team names (assuming there is one unique club for each ID)
teams = [epl_data[epl_data["ID_Club"] == firstteam_choice]["Club"].values[0],
         epl_data[epl_data["ID_Club"] == secondteam_choice]["Club"].values[0]]

# Extract the average points (AVG) for each team
pts = [epl_data.loc[epl_data["ID_Club"] == firstteam_choice, "AVG"].values[0],
       epl_data.loc[epl_data["ID_Club"] == secondteam_choice, "AVG"].values[0]]

data = {
    'Club': teams,
    'PTS': pts
}

# Create DataFrame
df = pd.DataFrame(data)

# Calculate total points
total_pts = df['PTS'].sum()

# Calculate win probabilities
df['Win Probability'] = df['PTS'] / total_pts * 100

# Format win probabilities as integers with a percent sign
df['Win Probability'] = df['Win Probability'].round(0).astype(int).astype(str) + '%'

# Display the results
print(df[['Club', 'Win Probability']])


@app.route('/api/league/get')
def get_data_league():
    for league in leagues:
        league['league_icon'] = url_for('static', filename=league['icon_filename'], _external=True)
    
    return jsonify(leagues)

@app.route('/api/league/<int:league_id>/clubs')
def get_data_clubs_by_leagueid(league_id):
    # Ambil klub berdasarkan ID liga
    if league_id in epl_data:
        return jsonify(epl_data[league_id])
    else:
        return jsonify({'error': 'League not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
