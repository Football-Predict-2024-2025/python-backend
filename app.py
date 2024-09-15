from flask import Flask, jsonify, url_for, request
from flask_cors import CORS

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

# Data klub berdasarkan ID liga
clubs = {
    1: [
        {'position': 1, 'club_name': 'Manchester City', 'points': 91, 'played': 38, 'win': 28, 'draw': 7, 'lose': 3, 'goal_for': 96, 'goal_against': 34, 'goal_diff': 62},
        {'position': 2, 'club_name': 'Arsenal', 'points': 89, 'played': 38, 'win': 28, 'draw': 5, 'lose': 5, 'goal_for': 91, 'goal_against': 29, 'goal_diff': 62},
        {'position': 3, 'club_name': 'Liverpool', 'points': 82, 'played': 38, 'win': 24, 'draw': 10, 'lose': 4, 'goal_for': 86, 'goal_against': 41, 'goal_diff': 45},
        {'position': 4, 'club_name': 'Aston Villa', 'points': 68, 'played': 38, 'win': 20, 'draw': 8, 'lose': 10, 'goal_for': 76, 'goal_against': 61, 'goal_diff': 15},
        {'position': 5, 'club_name': 'Tottenham Hotspur', 'points': 66, 'played': 38, 'win': 19, 'draw': 6, 'lose': 12, 'goal_for': 74, 'goal_against': 61, 'goal_diff': 13},
    ],
}

@app.route('/api/league/get')
def get_data_league():
    for league in leagues:
        league['league_icon'] = url_for('static', filename=league['icon_filename'], _external=True)
    
    return jsonify(leagues)

@app.route('/api/league/<int:league_id>/clubs')
def get_data_clubs_by_leagueid(league_id):
    # Ambil klub berdasarkan ID liga
    if league_id in clubs:
        return jsonify(clubs[league_id])
    else:
        return jsonify({'error': 'League not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
