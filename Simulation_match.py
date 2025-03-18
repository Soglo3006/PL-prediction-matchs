import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
import random
import numpy as np
import fetch_premier_league_data
from fetch_premier_league_players_data import data_joueur_predictions_buteurs

fetch_premier_league_data.avantageDomicile(fetch_premier_league_data.data_2324)
fetch_premier_league_data.difference_buts(fetch_premier_league_data.data_2324,fetch_premier_league_data.moyenne_dom_but,fetch_premier_league_data.moyenne_ext_but,'difference_moyenne_buts_marques', 'difference_plus_fort_equipe_but_marques')
fetch_premier_league_data.difference_buts(fetch_premier_league_data.data_2324,fetch_premier_league_data.moyenne_con_but_dom,fetch_premier_league_data.moyenne_con_but_ext, 'difference_moyenne_buts_conceder', 'difference_plus_fort_equipe_but_concede')

features_match = ['Home_avgGoal','Away_avgGoal','Home_avgShot','Away_avgShot', 'Home_avgShot_Target','Away_avgShot_Target'
            , 'home_form','away_form', 'home_advantage','moyenne_domcile_buts','moyenne_exterieur_buts','difference_moyenne_buts_marques','difference_moyenne_buts_conceder', 
            'moyenne_conceder_dom', 'moyenne_conceder_ext']

X = fetch_premier_league_data.data_2324[features_match]
y_home = fetch_premier_league_data.data_2324['HomeGoal']
y_away = fetch_premier_league_data.data_2324['AwayGoal']

X_train, X_test, y_train, y_test = train_test_split(X, y_home, test_size=0.2, random_state=1)
W_train, W_test, Z_train, Z_test = train_test_split(X, y_away, test_size=0.2, random_state=1)

model_home = GradientBoostingRegressor(n_estimators=500, learning_rate=0.1, max_depth=7, random_state=1)
model_home.fit(X_train, y_train)

model_away = GradientBoostingRegressor(n_estimators=500, learning_rate=0.1, max_depth=7, random_state=1)
model_away.fit(W_train,Z_train)

def predict_future_match(h_team, a_team, model_1, model_2, data, data2):
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
    moyenne_domcile_buts = fetch_premier_league_data.moyenne_dom_but[h_team]
    moyenne_extérieur_buts = fetch_premier_league_data.moyenne_ext_but[a_team]
    moyenne_conceder_dom = fetch_premier_league_data.moyenne_con_but_dom[h_team]
    moyenne_conceder_ext = fetch_premier_league_data.moyenne_con_but_ext[a_team]
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
    
    JoueurHomeTeam = []
    JoueurAwayTeam = []
    
    for i in range(len(data2)):
        if data2.loc[i,'Team'] == h_team:
            JoueurHomeTeam.append(data2.loc[i])
        elif data2.loc[i,'Team'] == a_team:
            JoueurAwayTeam.append(data2.loc[i])
            
    JoueurHomeTeam = sorted(JoueurHomeTeam, key=lambda x:x['Gls_90'], reverse=True)
    JoueurAwayTeam = sorted(JoueurAwayTeam, key=lambda x:x['Gls_90'], reverse=True)
    
    listWeightHome = []
    listWeightAway = []
    for i in JoueurHomeTeam:
        listWeightHome.append(float(i['Gls_90']))
    for j in JoueurAwayTeam:
        listWeightAway.append(float(j['Gls_90']))
    
    ButeurHome = random.choices(JoueurHomeTeam, weights= listWeightHome, k= prediction_buts_domicile)
    for i in range(len(ButeurHome)):
        ButeurHome[i] = ButeurHome[i]['Player']
        
        
    ButeurAway = random.choices(JoueurAwayTeam, weights= listWeightAway, k= prediction_buts_extérieur)
    for i in range(len(ButeurAway)):
        ButeurAway[i] = ButeurAway[i]['Player']
    
    return f"{h_team} {prediction_buts_domicile} - {prediction_buts_extérieur} {a_team}"

h_team = 'Manchester City'
a_team = 'Luton'
if h_team != a_team:
    predicted_result = predict_future_match(h_team, a_team, model_home, model_away, fetch_premier_league_data.data_2324,data_joueur_predictions_buteurs)
    #print(data_joueur_predictions_buteurs)
    print(f"Prédiction pour {h_team} vs {a_team} : {predicted_result}")
    

    
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
