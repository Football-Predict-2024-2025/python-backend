from flask import Flask, jsonify, url_for
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Data liga 
dataleagues = [
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

@app.route('/api/league/get')
def get_data_leagues():
    # Menambahkan URL untuk ikon setiap liga
    for league in dataleagues:
        league['league_icon'] = url_for('static', filename=league['icon_filename'], _external=True)
    return jsonify(dataleagues)

if __name__ == '__main__':
    app.run(debug=True)
