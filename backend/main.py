from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fetch_premier_league_data import data_2324
from Predict_match import predict_future_match, model_home, model_away, model_possession
from fetch_premier_league_players_data import data_joueur_predictions_buteurs

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MatchRequest(BaseModel):
    home_team: str
    away_team: str 


@app.get("/")
def read_root():
    return {"status": "API is running", "message": "Premier League Match Predictor"}

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/predict_match")
def predict_match(request:MatchRequest):
    home_team = request.home_team
    away_team = request.away_team

    if home_team == away_team:
        return {"error": "Home team and away team must be different."}
    
    predicted_result = predict_future_match(home_team, away_team, model_home, model_away,model_possession, data_2324)

    (prediction_buts_domicile, prediction_buts_exterieur, 
        buteurs_home, buteurs_away, 
        passeur_home, passeur_away, 
        yellow_home_players, yellow_away_players, 
        red_home_players, red_away_players, 
        joueur_remplacer_home, joueur_remplacer_away, 
        joueur_rentre_home, joueur_rentre_away,
        home_possesion, away_possession,
        prediction_tirs_domicile, prediction_tirs_exterieur,
        prediction_tirs_cadre_domicile, prediction_tirs_cadre_exterieur,
        prediction_fouls_domicile, prediction_fouls_exterieur,
        prediction_corner_domicile, prediction_corner_exterieur) = predicted_result  

    home_lineup = data_joueur_predictions_buteurs[home_team]['Starting11Players'][['Player', 'Pos']].to_dict('records')
    home_bench = data_joueur_predictions_buteurs[home_team]['BenchPlayers'][['Player', 'Pos']].to_dict('records')
    
    away_lineup = data_joueur_predictions_buteurs[away_team]['Starting11Players'][['Player', 'Pos']].to_dict('records')
    away_bench = data_joueur_predictions_buteurs[away_team]['BenchPlayers'][['Player', 'Pos']].to_dict('records')
     
    prediction = {
            "possesion": {
                "home_team": home_possesion,
                "away_team": away_possession
            },
            "tirs": {
                "home_team": round(prediction_tirs_domicile),
                "away_team": round(prediction_tirs_exterieur)
            },
            "tirs_cadres": {
                "home_team": prediction_tirs_cadre_domicile,
                "away_team": prediction_tirs_cadre_exterieur
            },
            "fouls": {
                "home_team": prediction_fouls_domicile,
                "away_team": prediction_fouls_exterieur
            },
            "corners": {
                "home_team": prediction_corner_domicile,
                "away_team": prediction_corner_exterieur
            },
            "score": {
                "home_team": prediction_buts_domicile,
                "away_team": prediction_buts_exterieur
            },
            "buteurs": {
                "home_team": buteurs_home,
                "away_team": buteurs_away
            },
            "passeur": {
                "home_team": passeur_home,
                "away_team": passeur_away
            },
            "yellow_cards": {
                "home_team": yellow_home_players,
                "away_team": yellow_away_players
            },
            "red_cards": {
                "home_team": red_home_players,
                "away_team": red_away_players
            },
            "joueurs_remplaces": {
                "home_team": joueur_remplacer_home,
                "away_team": joueur_remplacer_away
            },
            "joueurs_rentres": {
                "home_team": joueur_rentre_home,
                "away_team": joueur_rentre_away
            },
            "lineups": {
            "home_team": {
                "starting_11": home_lineup,
                "bench": home_bench
            },
            "away_team": {
                "starting_11": away_lineup,
                "bench": away_bench
            }
        }
        }
    return prediction

