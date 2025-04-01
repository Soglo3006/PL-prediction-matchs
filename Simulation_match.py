from fetch_premier_league_data import data_2324
import matplotlib.pyplot as plt
from Predict_match import predict_future_match
from Predict_match import model_home,model_away,model_possession
import streamlit as st

h_team = 'Manchester City'
a_team = 'Wolves'
if h_team != a_team:
    predicted_result = predict_future_match(h_team, a_team, model_home, model_away,model_possession, data_2324)
    prediction_buts_domicile,prediction_buts_extérieur,buteurs_home,buteurs_away,passeur_home, passeur_away, yellow_home_players, yellow_away_players , red_home_players, red_away_players, Joueur_remplacer_home, Joueur_remplacer_away, Joueur_rentre_home, Joueur_rentre_away = predicted_result
    prediction = {
            "score": f"{prediction_buts_domicile} - {prediction_buts_extérieur}",
            "buteurs_home": buteurs_home,
            "buteurs_away": buteurs_away,
            "passeur_home": passeur_home,
            "passeur_away": passeur_away,
            " yellow_home_players":  yellow_home_players, 
            "yellow_away_players ":  yellow_away_players,
            "red_home_players": red_home_players,
            "red_away_players" : red_away_players
        }    
    
    print(f"Prédiction pour {h_team} vs {a_team} : {prediction}")
