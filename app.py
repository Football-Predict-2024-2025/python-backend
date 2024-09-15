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


@app.route('/api/club/predict')
def club_predict():
    # Mendapatkan parameter liga dan id tim dari query string
    league = 1
    firstteam_choice = 1
    secondteam_choice = 2

    # Membaca data sesuai liga
    if league == 1:
        epl_data = pd.read_csv('data/EPL_data.csv')
    elif league == 5:
        epl_data = pd.read_csv('data/Bundesliga_data.csv')
    elif league == 3:
        epl_data = pd.read_csv('data/Serie_A_data.csv')
    elif league == 4:
        epl_data = pd.read_csv('data/League_1_data.csv')
    elif league == 2:
        epl_data = pd.read_csv('data/La_Liga_data.csv')
    else:
        return jsonify({'error': 'Invalid league'}), 400

    # Tim yang dipilih
    teams_of_interest = [firstteam_choice, secondteam_choice]

    # Ekstrak nama klub
    teams = [epl_data[epl_data["ID_Club"] == firstteam_choice]["Club"].values[0],
             epl_data[epl_data["ID_Club"] == secondteam_choice]["Club"].values[0]]

    # Ekstrak poin rata-rata (AVG) untuk masing-masing tim
    pts = [epl_data.loc[epl_data["ID_Club"] == firstteam_choice, "AVG"].values[0],
           epl_data.loc[epl_data["ID_Club"] == secondteam_choice, "AVG"].values[0]]

    data = {
        'Club': teams,
        'PTS': pts
    }

    # Membuat DataFrame
    df = pd.DataFrame(data)

    # Menghitung total poin
    total_pts = df['PTS'].sum()

    # Menghitung probabilitas menang
    df['Win_Probability'] = df['PTS'] / total_pts * 100

    # Format probabilitas menang menjadi integer dengan tanda persen
    df['Win_Probability'] = df['Win_Probability'].round(0).astype(int).astype(str) + '%'

    # Return hasil dalam bentuk JSON
    return jsonify(df[['Club', 'Win_Probability']].to_dict(orient='records'))


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
