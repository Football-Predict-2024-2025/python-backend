from flask import Flask, jsonify, url_for, request
from flask_cors import CORS
import pandas as pd

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


@app.route('/api/club/predict', methods=['POST'])
def club_predict():
    try:
        # Parse the JSON data from the client
        data = request.json
        ID_Club1 = data.get('ID_Club1')
        ID_Club2 = data.get('ID_Club2')
        ID_Liga = data.get('ID_Liga')

        # Ensure the necessary data is provided
        if not all([ID_Club1, ID_Club2, ID_Liga]):
            return jsonify({'error': 'Missing data'}), 400

        # Read data based on the league
        if ID_Liga == 1:
            league_data = pd.read_csv('data/EPL_data.csv')
        elif ID_Liga == 5:
            league_data = pd.read_csv('data/Bundesliga_data.csv')
        elif ID_Liga == 3:
            league_data = pd.read_csv('data/Serie_A_data.csv')
        elif ID_Liga == 4:
            league_data = pd.read_csv('data/League_1_data.csv')
        elif ID_Liga == 2:
            league_data = pd.read_csv('data/La_Liga_data.csv')
        else:
            return jsonify({'error': 'Invalid league'}), 400

        # Extract club names and average points
        try:
            teams = [league_data[league_data["ID_Club"] == ID_Club1]["Club"].values[0],
                     league_data[league_data["ID_Club"] == ID_Club2]["Club"].values[0]]
            pts = [league_data.loc[league_data["ID_Club"] == ID_Club1, "AVG"].values[0],
                   league_data.loc[league_data["ID_Club"] == ID_Club2, "AVG"].values[0]]
        except IndexError:
            return jsonify({'error': 'Club not found'}), 404

        # Prepare data for prediction
        data = {
            'Club': teams,
            'PTS': pts
        }

        # Create DataFrame and calculate win probability
        df = pd.DataFrame(data)
        total_pts = df['PTS'].sum()
        df['Win_Probability'] = (df['PTS'] / total_pts * 100).round(0).astype(int).astype(str) + '%'

        # Return results as JSON
        return jsonify(df[['Club', 'Win_Probability']].to_dict(orient='records'))

    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/api/league/get')
def get_data_league():
    for league in leagues:
        league['league_icon'] = url_for('static', filename=league['icon_filename'], _external=True)
    
    return jsonify(leagues)


@app.route('/api/league/<int:league_id>/clubs')
def get_data_clubs_by_leagueid(league_id):
    epl_data = pd.read_csv('data/EPL_data.csv')
    # Filter clubs by the league_id
    league_clubs = epl_data[epl_data["ID_Liga"] == league_id]

    if not league_clubs.empty:
        return jsonify(league_clubs.to_dict(orient='records'))
    else:
        return jsonify({'error': 'League not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
