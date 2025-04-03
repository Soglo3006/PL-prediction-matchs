from fetch_premier_league_data import data_2324
from predict_match import predict_future_match,model_home,model_away,model_possession 
import random

home_team = str(random.choice(data_2324['HomeTeam'].unique()))
away_team = str(random.choice(data_2324['AwayTeam'].unique()))
if home_team != away_team:
    predicted_result = predict_future_match(home_team, away_team, model_home, model_away,model_possession, data_2324)
    prediction_buts_domicile,prediction_buts_extérieur,buteurs_home,buteurs_away,passeur_home, passeur_away, yellow_home_players, yellow_away_players , red_home_players, red_away_players, joueur_remplacer_home, joueur_remplacer_away, joueur_rentre_home, joueur_rentre_away = predicted_result
    prediction = {
            "score": f"{prediction_buts_domicile} - {prediction_buts_extérieur}",
            "buteurs_home": buteurs_home,
            "buteurs_away": buteurs_away,
            "passeur_home": passeur_home,
            "passeur_away": passeur_away,
            " yellow_home_players":  yellow_home_players, 
            "yellow_away_players ":  yellow_away_players,
            "red_home_players": red_home_players,
            "red_away_players" : red_away_players,
            "joueur_remplacer_home": joueur_remplacer_home,
            "joueur_remplacer_away": joueur_remplacer_away,
            "joueur_rentre_home": joueur_rentre_home,
            "joueur_rentre_away": joueur_rentre_away
        }    
    
    print(f"Prédiction pour {home_team} vs {away_team} : {prediction}")
