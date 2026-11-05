import os
import truststore
import requests

truststore.inject_into_ssl()

API_URL = "https://v2.nba.api-sports.io/games"
API_KEY = os.getenv("NBA_API_KEY")

if not API_KEY:
    raise RuntimeError("NBA_API_KEY environment variable is not set")

headers = {
    "x-apisports-key": API_KEY
}

params = {
    "date": "2026-11-05"
}


response = requests.get(
        API_URL, 
        headers=headers,
        params=params
)

data = response.json()

games = data["response"]

nbascores_games = []

for game in games:
    nbascores_game = {
        "external_id": game["id"],
        "status": game["status"]["long"],
        "start_time": game["date"]["start"],
        "away_team": game["teams"]["visitors"]["name"],
        "away_code": game["teams"]["visitors"]["code"],
        "away_score": game["scores"]["visitors"]["points"],
        "home_team": game["teams"]["home"]["name"],
        "home_code": game["teams"]["home"]["code"],
        "home_score": game["scores"]["home"]["points"],
    }

    nbascores_games.append(nbascores_game)

for game in nbascores_games:
    print(game)


