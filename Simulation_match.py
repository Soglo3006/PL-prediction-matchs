import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingRegressor
import numpy as np
import simpy 
from fetch_premier_league_data import avantageDomicile, difference_buts, moyenne_con_but_dom, moyenne_con_but_ext, moyenne_dom_but, moyenne_ext_but, data_2324
from détails_simulation import match_process
import matplotlib.pyplot as plt
from features import features_match,features_possession,features_tirs,features_tirsCadre

avantageDomicile(data_2324)
difference_buts(data_2324,moyenne_dom_but,moyenne_ext_but,'difference_moyenne_buts_marques', 'difference_plus_fort_equipe_but_marques')
difference_buts(data_2324,moyenne_con_but_dom,moyenne_con_but_ext, 'difference_moyenne_buts_conceder', 'difference_plus_fort_equipe_but_concede')

def train_models(data, features, teamCategorie):
    X = data[features]
    y_home = data[teamCategorie]
    X_train, X_test, y_train, y_test = train_test_split(X, y_home, test_size=0.2, random_state=1)
    if teamCategorie == 'HomeGoal' or teamCategorie == 'AwayGoal':
        model = RandomForestClassifier(n_estimators=500, max_depth=7, random_state=1)
        model.fit(X_train, y_train)
    elif teamCategorie == 'HomePossesion' or teamCategorie == 'HomeShots' or teamCategorie == 'AwayShots' or teamCategorie == 'HomeShotTarget' or teamCategorie == 'AwayShotTarget':
        model = RandomForestRegressor(n_estimators=1500, max_depth=15, min_samples_split=10, random_state=1)
        model.fit(X_train, y_train)

    return model

model_home = train_models(data_2324, features_match, 'HomeGoal')
model_away = train_models(data_2324, features_match, 'AwayGoal')
model_possession = train_models(data_2324,features_possession, 'HomePossesion')
model_tirsH = train_models(data_2324,features_tirs,'HomeShots')
model_tirsA = train_models(data_2324,features_tirs,'AwayShots')
model_tirsCadreH = train_models(data_2324,features_tirsCadre,'HomeShotTarget')
model_tirsCadreA = train_models(data_2324,features_tirsCadre,'AwayShotTarget')


def predict_future_match(h_team, a_team, model_1, model_2,model_3,data):
    if h_team not in data['HomeTeam'].unique():
        return None
    if a_team not in data['AwayTeam'].unique():
        return None
    
    home_avg_goal = data[data['HomeTeam'] == h_team]['Home_avgGoal'].values[0]
    away_avg_goal = data[data['AwayTeam'] == a_team]['Away_avgGoal'].values[0]
    home_avg_shot = data[data['HomeTeam'] == h_team]['Home_avgShot'].values[0]
    away_avg_shot = data[data['AwayTeam'] == a_team]['Away_avgShot'].values[0]
    home_avg_shot_target = data[data['HomeTeam']== h_team]['Home_avgShot_Target'].values[0]
    away_avg_shot_target = data[data['AwayTeam']== a_team]['Away_avgShot_Target'].values[0]
    home_form = data[data['HomeTeam'] == h_team]['home_form'].values[0]
    away_form = data[data['AwayTeam'] == a_team]['away_form'].values[0]
    home_advantage = data[data['HomeTeam'] == h_team]['home_advantage'].values[0]
    moyenne_domcile_buts = moyenne_dom_but[h_team]
    moyenne_extérieur_buts = moyenne_ext_but[a_team]
    moyenne_conceder_dom = moyenne_con_but_dom[h_team]
    moyenne_conceder_ext = moyenne_con_but_ext[a_team]
    difference_moyenne_buts_marques = moyenne_domcile_buts - moyenne_extérieur_buts
    difference_moyenne_buts_conceder = moyenne_conceder_dom - moyenne_conceder_ext
    Home_avgCorner = data[data['HomeTeam']== h_team]['Home_avgCorner'].values[0]
    Away_avgCorner = data[data['AwayTeam']== a_team]['Away_avgCorner'].values[0]
    Home_avgPos = data[data['HomeTeam'] == h_team]['Home_avgPos'].values[0]
    Away_avgPos = data[data['AwayTeam'] == a_team]['Away_avgPos'].values[0]
    

    match_features = pd.DataFrame([[home_avg_goal, away_avg_goal, home_avg_shot, away_avg_shot,home_avg_shot_target,away_avg_shot_target,
                                    home_form, away_form, home_advantage, moyenne_domcile_buts,moyenne_extérieur_buts, difference_moyenne_buts_marques,
                                    difference_moyenne_buts_conceder, moyenne_conceder_dom, moyenne_conceder_ext,Home_avgCorner,Away_avgCorner,Home_avgPos,Away_avgPos]],
                                  columns=features_match)
    #print(match_features)
    possesion_features = pd.DataFrame([[home_avg_goal, away_avg_goal, home_avg_shot, away_avg_shot, 
                                    home_avg_shot_target, away_avg_shot_target, home_form, away_form,home_advantage,
                                    moyenne_domcile_buts, moyenne_extérieur_buts,difference_moyenne_buts_marques,moyenne_conceder_dom,moyenne_conceder_ext,Home_avgPos,Away_avgPos]],
                                columns=features_possession)
    
    tirs_features = pd.DataFrame([[home_avg_goal, away_avg_goal, home_avg_shot, away_avg_shot,
                                   home_form, away_form,moyenne_domcile_buts, moyenne_extérieur_buts,
                                   difference_moyenne_buts_marques,moyenne_conceder_dom,moyenne_conceder_ext
                                   ,Home_avgPos,Away_avgPos,Home_avgCorner,Away_avgCorner]],
                                columns=features_tirs)
    
    tirsCadres_features = pd.DataFrame([[home_avg_goal, away_avg_goal, home_avg_shot, away_avg_shot,home_avg_shot_target, away_avg_shot_target,
                                   home_form, away_form,home_advantage,moyenne_domcile_buts, moyenne_extérieur_buts,
                                   Home_avgPos,Away_avgPos]], columns=features_tirsCadre)
    
    prediction_buts_domicile = (model_1.predict(match_features)[0])
    prediction_buts_extérieur = (model_2.predict(match_features)[0])
    
    prediction_buts_domicile += np.random.normal(0, 0.7) 
    prediction_buts_extérieur += np.random.normal(0, 0.7)
    
    prediction_buts_domicile = max(0,round(prediction_buts_domicile))
    prediction_buts_extérieur = max(0,round(prediction_buts_extérieur))
        
    prediction_possession = model_3.predict(possesion_features)[0]
    
    fluctuation = np.random.normal(loc=0, scale=4) 
    prediction_possession += fluctuation
    
    prediction_possession = max(20, min(80, prediction_possession))
    home_possesion = round(prediction_possession)
    away_possession = 100 - prediction_possession
    
    prediction_tirs_domicile = (model_tirsH.predict(tirs_features)[0])
    prediction_tirs_extérieur = (model_tirsA.predict(tirs_features)[0])
    
    diff_niveau = abs(prediction_tirs_domicile - prediction_tirs_extérieur)
    scale_dynamic = max(1.5, min(3, diff_niveau / 2))  

    prediction_tirs_domicile += np.random.normal(loc=0, scale=scale_dynamic)
    prediction_tirs_extérieur += np.random.normal(loc=0, scale=scale_dynamic)
    
    print(round(prediction_tirs_domicile),round(prediction_tirs_extérieur))
    
    prediction_tirs_cadre_domicile = (model_tirsCadreH.predict(tirsCadres_features)[0])
    prediction_tirs_cadre_extérieur = (model_tirsCadreA.predict(tirsCadres_features)[0])
    
    prediction_tirs_cadre_domicile += np.random.normal(0, 0.7)
    prediction_tirs_cadre_extérieur += np.random.normal(0, 0.7)
    
    prediction_tirs_cadre_domicile = max(0,round(prediction_tirs_cadre_domicile))
    prediction_tirs_cadre_extérieur = max(0,round(prediction_tirs_cadre_extérieur))
    
    print(round(prediction_tirs_cadre_domicile),round(prediction_tirs_cadre_extérieur))
    
    env = simpy.Environment()
    match_result = env.process(match_process(env, h_team, a_team, prediction_buts_domicile, prediction_buts_extérieur,home_possesion,away_possession))

    env.run()
    buteurs_home, buteurs_away = match_result.value
    
    return prediction_buts_domicile,prediction_buts_extérieur,buteurs_home,buteurs_away



h_team = 'Manchester City'
a_team = 'Wolves'
if h_team != a_team:
    predicted_result = predict_future_match(h_team, a_team, model_home, model_away,model_possession, data_2324)
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
