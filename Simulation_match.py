import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
import numpy as np
import simpy 
from fetch_premier_league_data import avantageDomicile, difference_buts, moyenne_con_but_dom, moyenne_con_but_ext, moyenne_dom_but, moyenne_ext_but, data_2324
from détails_simulation import match_process
import matplotlib.pyplot as plt
from possesion import train_models_possesion, predict_future_match_possesion, features_possession

avantageDomicile(data_2324)
difference_buts(data_2324,moyenne_dom_but,moyenne_ext_but,'difference_moyenne_buts_marques', 'difference_plus_fort_equipe_but_marques')
difference_buts(data_2324,moyenne_con_but_dom,moyenne_con_but_ext, 'difference_moyenne_buts_conceder', 'difference_plus_fort_equipe_but_concede')

features_match = ['Home_avgGoal','Away_avgGoal','Home_avgShot','Away_avgShot', 'Home_avgShot_Target','Away_avgShot_Target'
            , 'home_form','away_form', 'home_advantage','moyenne_domcile_buts','moyenne_exterieur_buts','difference_moyenne_buts_marques','difference_moyenne_buts_conceder', 
            'moyenne_conceder_dom', 'moyenne_conceder_ext']



def train_models(data, features, teamCategorie, model_type):
    X = data[features]
    y_home = data[teamCategorie]
    X_train, X_test, y_train, y_test = train_test_split(X, y_home, test_size=0.2, random_state=1)
    model = model_type(n_estimators=500, max_depth=7, random_state=1)
    model.fit(X_train, y_train)

    return model

model_home = train_models(data_2324, features_match, 'HomeGoal',RandomForestClassifier)
model_away = train_models(data_2324, features_match, 'AwayGoal',RandomForestClassifier)

def predict_future_match(h_team, a_team, model_1, model_2, data):
    if h_team not in data['HomeTeam'].unique():
        return None
    if a_team not in data['AwayTeam'].unique():
        return None
    
    home_avg_goal = data[data['HomeTeam'] == h_team]['Home_avgGoal'].values[-1]
    away_avg_goal = data[data['AwayTeam'] == a_team]['Away_avgGoal'].values[-1]
    home_avg_shot = data[data['HomeTeam'] == h_team]['Home_avgShot'].values[-1]
    away_avg_shot = data[data['AwayTeam'] == a_team]['Away_avgShot'].values[-1]
    home_avg_shot_target = data[data['HomeTeam']== h_team]['Home_avgShot_Target'].values[-1]
    away_avg_shot_target = data[data['AwayTeam']== a_team]['Away_avgShot_Target'].values[-1]
    home_form = data[data['HomeTeam'] == h_team]['home_form'].values[-1]
    away_form = data[data['AwayTeam'] == a_team]['away_form'].values[-1]
    home_advantage = data[data['HomeTeam'] == h_team]['home_advantage'].values[-1]
    moyenne_domcile_buts = moyenne_dom_but[h_team]
    moyenne_extérieur_buts = moyenne_ext_but[a_team]
    moyenne_conceder_dom = moyenne_con_but_dom[h_team]
    moyenne_conceder_ext = moyenne_con_but_ext[a_team]
    difference_moyenne_buts_marques = moyenne_domcile_buts - moyenne_extérieur_buts
    difference_moyenne_buts_conceder = moyenne_conceder_dom - moyenne_conceder_ext
    

    match_features = pd.DataFrame([[home_avg_goal, away_avg_goal, home_avg_shot, away_avg_shot,home_avg_shot_target,away_avg_shot_target,
                                    home_form, away_form, home_advantage, moyenne_domcile_buts,moyenne_extérieur_buts, difference_moyenne_buts_marques,
                                    difference_moyenne_buts_conceder, moyenne_conceder_dom, moyenne_conceder_ext]],
                                  columns=features_match)
    #print(match_features)
    
    prediction_buts_domicile = (model_1.predict(match_features)[0])
    prediction_buts_extérieur = (model_2.predict(match_features)[0])
    
    prediction_buts_domicile += np.random.normal(0, 0.7) 
    prediction_buts_extérieur += np.random.normal(0, 0.7)
    
    prediction_buts_domicile = max(0,round(prediction_buts_domicile))
    prediction_buts_extérieur = max(0,round(prediction_buts_extérieur))
    
    model_possession = train_models_possesion(data,features_possession, 'HomePossesion',RandomForestRegressor)
    
    home_possesion, away_possesion = predict_future_match_possesion(data, h_team, a_team, model_possession)
    
    env = simpy.Environment()
    match_result = env.process(match_process(env, h_team, a_team, prediction_buts_domicile, prediction_buts_extérieur,home_possesion,away_possesion))

    env.run()
    buteurs_home, buteurs_away = match_result.value
    
    return prediction_buts_domicile,prediction_buts_extérieur,buteurs_home,buteurs_away



h_team = 'Manchester City'
a_team = 'Luton'
if h_team != a_team:
    predicted_result = predict_future_match(h_team, a_team, model_home, model_away, data_2324)
    prediction_buts_domicile,prediction_buts_extérieur,buteurs_home,buteurs_away = predicted_result
    prediction = {
            "score": f"{prediction_buts_domicile} - {prediction_buts_extérieur}",
            "buteurs_home": buteurs_home,
            "buteurs_away": buteurs_away
        }    
    
    print(f"Prédiction pour {h_team} vs {a_team} : {prediction}")

"""
# Prédictions sur les données de test
y_pred_home = model_home.predict(X_test)
y_pred_away = model_away.predict(W_test)

# Évaluation du modèle pour les buts à domicile
mae_home = mean_absolute_error(y_test, y_pred_home)
r2_home = r2_score(y_test, y_pred_home)

# Évaluation du modèle pour les buts à l'extérieur
mae_away = mean_absolute_error(Z_test, y_pred_away)
r2_away = r2_score(Z_test, y_pred_away)

# Affichage des résultats
print(" Évaluation du modèle - Buts domicile")
print(f"MAE : {mae_home:.2f} (Erreur moyenne absolue)")
print(f"R² : {r2_home:.2f} (Qualité de prédiction)")

print("\n Évaluation du modèle - Buts extérieur")
print(f"MAE : {mae_away:.2f} (Erreur moyenne absolue)")
print(f"R² : {r2_away:.2f} (Qualité de prédiction)")
"""
