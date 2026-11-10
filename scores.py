import os
from datetime import datetime
from zoneinfo import ZoneInfo

import truststore
import requests
from dotenv import load_dotenv

load_dotenv()
truststore.inject_into_ssl()

API_URL = "https://v2.nba.api-sports.io/games"
API_KEY = os.getenv("NBA_API_KEY")

def get_nba_today():
    return datetime.now(ZoneInfo("America/New_York")).date()

def fetch_games(game_date):
    if not API_KEY:
        raise RuntimeError("NBA_API_KEY environment variable is not set")

    headers = {
    "x-apisports-key": API_KEY
    }
    
    params = {
        "date": game_date.isoformat()
    }
    
    response = requests.get(
        API_URL,
        headers=headers,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    if data["errors"]:
        raise RuntimeError(f"API-Sports returned an error: {data['errors']}")

    return data["response"]

def transform_games(games):
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

    return nbascores_games

def main():
    nba_today = get_nba_today()

    try:
        games = fetch_games(nba_today)
        nbascores_games = transform_games(games)
        print(f"Fetching NBA games for {nba_today}:")

        for game in nbascores_games:
            print(game)

    except requests.exceptions.Timeout:
        print("API-Sports API request timed out. Please try again later.")

    except requests.exceptions.HTTPError as error:
        print(f"API-Sports returned an HTTP error: {error}")

    except requests.exceptions.RequestException as error:
        print(f"Unable to reach API-Sports: {error}")

    except RuntimeError as error:
        print(error)

if __name__ == "__main__":
    main()