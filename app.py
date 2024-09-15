from flask import Flask, jsonify, url_for
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

@app.route('/api/league/get')
def league_to_json():
    data = [
        {
            'league_id': 1,
            'league_name': 'English Premiere League',
            'country': 'England',
            'total_club': 20,
            'league_icon': url_for('static', filename='images/EPL.png', _external=True)
        },
        {
            'league_id': 2,
            'league_name': 'La Liga',
            'country': 'Spain',
            'total_club': 20,
            'league_icon': url_for('static', filename='images/LaLiga.png', _external=True)
        },
        {
            'league_id': 3,
            'league_name': 'Serie A',
            'country': 'Italy',
            'total_club': 20,
            'league_icon': url_for('static', filename='images/SerieA.png', _external=True)
        },
        {
            'league_id': 4,
            'league_name': 'League1',
            'country': 'France',
            'total_club': 18,
            'league_icon': url_for('static', filename='images/League1.png', _external=True)
        },
        {
            'league_id': 5,
            'league_name': 'Bundesliga',
            'country': 'Germany',
            'total_club': 18,
            'league_icon': url_for('static', filename='images/Bundesliga.png', _external=True)
        }
    ]
    json_league = jsonify(data)

    return json_league

if __name__ == '__main__':
    app.run(debug=True)
