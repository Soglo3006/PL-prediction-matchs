import pandas as pd
import numpy as np
import random
from détails_simulation import simulate_match
from fetch_premier_league_data import avantageDomicile, difference_buts,moyenne_con_but_dom, moyenne_con_but_ext, moyenne_dom_but, moyenne_ext_but,data_2324
from features import features_match,features_possession,features_tirs,features_tirsCadre, features_cartons_jaunes,features_cartons_rouges,features_corners,features_foul,features_xG
from model import train_models

avantageDomicile(data_2324)
difference_buts(data_2324,moyenne_dom_but,moyenne_ext_but,'difference_moyenne_buts_marques', 'difference_plus_fort_equipe_but_marques')
difference_buts(data_2324,moyenne_con_but_dom,moyenne_con_but_ext, 'difference_moyenne_buts_conceder', 'difference_plus_fort_equipe_but_concede')

model_home = train_models(data_2324, features_match, 'HomeGoal')
model_away = train_models(data_2324, features_match, 'AwayGoal')
model_possession = train_models(data_2324,features_possession, 'HomePossesion')
model_tirsH = train_models(data_2324,features_tirs,'HomeShots')
model_tirsA = train_models(data_2324,features_tirs,'AwayShots')
model_tirsCadreH = train_models(data_2324,features_tirsCadre,'HomeShotTarget')
model_tirsCadreA = train_models(data_2324,features_tirsCadre,'AwayShotTarget')
model_xGH = train_models(data_2324,features_xG,'Home_xG')
model_xGA = train_models(data_2324,features_xG,'Away_xG')
model_foulH = train_models(data_2324,features_foul,'HFouls')
model_foulA = train_models(data_2324,features_foul,'AFouls')
model_cornerH = train_models(data_2324,features_corners,'HCorners')
model_cornerA = train_models(data_2324,features_corners,'ACorners')
model_yellowH = train_models(data_2324,features_cartons_jaunes,'HYellow')
model_yellowA = train_models(data_2324,features_cartons_jaunes,'AYellow')
model_redH = train_models(data_2324,features_cartons_rouges,'HRed')
model_redA = train_models(data_2324,features_cartons_rouges,'ARed')

"""
prediction_buts_domicile = (model_buts_dom.predict(match_feature)[0]) + np.random.normal(0, 0.7)
prediction_buts_extérieur = (model_buts_extérieur.predict(match_feature)[0]) + np.random.normal(0, 0.7)

prediction_buts_domicile = max(0,round(prediction_buts_domicile))
prediction_buts_extérieur = max(0,round(prediction_buts_extérieur))

prediction_tirs_cadre_domicile = (model_tirsCadreH.predict(tirs_cadre_stat_features)[0]) + np.random.normal(0, 0.7)
prediction_tirs_cadre_extérieur = (model_tirsCadreA.predict(tirs_cadre_stat_features)[0]) + np.random.normal(0, 0.7)

prediction_tirs_cadre_domicile = max(0,round(prediction_tirs_cadre_domicile))
prediction_tirs_cadre_extérieur = max(0,round(prediction_tirs_cadre_extérieur))
"""
def predict_match_stats(model_buts_dom,model_buts_extérieur,model_possesion_dom,pos_features,match_feature,
                        tirs_stats_features,tirs_cadre_stat_features,yellow_features,red_features,corners_stats_features, fouls_features,XG_features):
    
    prediction_buts_domicile = (model_buts_dom.predict(match_feature)[0]) + np.random.normal(0, 0.7)
    prediction_buts_extérieur = (model_buts_extérieur.predict(match_feature)[0]) + np.random.normal(0, 0.7)

    prediction_buts_domicile = max(0,round(prediction_buts_domicile))
    prediction_buts_extérieur = max(0,round(prediction_buts_extérieur))
        
    prediction_possession = model_possesion_dom.predict(pos_features)[0] + np.random.normal(loc=0, scale=4)

    prediction_possession = max(20, min(80, prediction_possession))
    home_possesion = round(prediction_possession)
    away_possession = 100 - home_possesion
    
    print(home_possesion,away_possession)

    prediction_tirs_domicile = (model_tirsH.predict(tirs_stats_features)[0])
    prediction_tirs_extérieur = (model_tirsA.predict(tirs_stats_features)[0])

    diff_niveau = abs(prediction_tirs_domicile - prediction_tirs_extérieur)
    scale_dynamic = max(1.5, min(4, (diff_niveau / 1.5) + 0.5))  

    prediction_tirs_domicile += np.random.normal(loc=0, scale=scale_dynamic)
    prediction_tirs_extérieur += np.random.normal(loc=0, scale=scale_dynamic)

    print(round(prediction_tirs_domicile),round(prediction_tirs_extérieur))

    prediction_tirs_cadre_domicile = (model_tirsCadreH.predict(tirs_cadre_stat_features)[0]) + np.random.normal(0, 0.7)
    prediction_tirs_cadre_extérieur = (model_tirsCadreA.predict(tirs_cadre_stat_features)[0]) + np.random.normal(0, 0.7)

    prediction_tirs_cadre_domicile = min(prediction_tirs_domicile, max(0, round(prediction_tirs_cadre_domicile)))
    prediction_tirs_cadre_extérieur = min(prediction_tirs_extérieur, max(0, round(prediction_tirs_cadre_extérieur)))

    print(round(prediction_tirs_cadre_domicile),round(prediction_tirs_cadre_extérieur))
    
    prediction_carton_jaunes_domicile = (model_yellowH.predict(yellow_features)[0]) + np.random.normal(0, 0.7)
    prediction_carton_jaunes_extérieur = (model_yellowA.predict(yellow_features)[0]) + np.random.normal(0, 0.7)
    
    prediction_carton_jaunes_domicile = max(0,round(prediction_carton_jaunes_domicile))
    prediction_carton_jaunes_extérieur = max(0,round(prediction_carton_jaunes_extérieur))
    
    print(round(prediction_carton_jaunes_domicile),round(prediction_carton_jaunes_extérieur))
    
    prediction_carton_rouges_domicile = (model_redH.predict(red_features)[0]) + np.random.normal(-0.3, 0.5)
    prediction_carton_rouges_extérieur = (model_redA.predict(red_features)[0]) + np.random.normal(-0.3, 0.5)
    
    if random.random() > 0.08:  
        prediction_carton_rouges_domicile = 0
    if random.random() > 0.08:  
        prediction_carton_rouges_extérieur = 0
   
    prediction_carton_rouges_domicile = min(1, max(0, round(prediction_carton_rouges_domicile)))
    prediction_carton_rouges_extérieur = min(1, max(0, round(prediction_carton_rouges_extérieur)))
    
    print((prediction_carton_rouges_domicile),(prediction_carton_rouges_extérieur))
    
    prediction_corner_domicile = (model_cornerH.predict(corners_stats_features)[0]) + np.random.normal(0, 0.7)
    prediction_corner_extérieur = (model_cornerA.predict(corners_stats_features)[0]) + np.random.normal(0, 0.7)
    
    prediction_corner_domicile = max(0,round(prediction_corner_domicile))
    prediction_corner_extérieur = max(0,round(prediction_corner_extérieur))
    
    print(round(prediction_corner_domicile),round(prediction_corner_extérieur))
    
    prediction_fouls_domicile = (model_foulH.predict(fouls_features)[0]) + np.random.normal(0, 0.7)
    prediction_fouls_extérieur = (model_foulA.predict(fouls_features)[0]) + np.random.normal(0, 0.7)
    
    prediction_fouls_domicile = max(0,round(prediction_fouls_domicile))
    prediction_fouls_extérieur = max(0,round(prediction_fouls_extérieur))
    
    print(round(prediction_fouls_domicile),round(prediction_fouls_extérieur))
    
    prediction_XG_domicile = safe_xG_prediction(model_xGH, XG_features)
    prediction_XG_extérieur = safe_xG_prediction(model_xGA, XG_features)
    
    print((prediction_XG_domicile),(prediction_XG_extérieur))
    
    return home_possesion,away_possession,prediction_buts_domicile,prediction_buts_extérieur

def safe_xG_prediction(model, XG_features):
    xG = -1  
    while xG < 0:  
        xG = model.predict(XG_features)[0] + np.random.normal(0, 0.7)  
    return round(xG, 2)

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
    Home_avgFouls = data[data['HomeTeam']== h_team]['Home_avgFouls'].values[0]
    Away_avgFouls = data[data['AwayTeam']== a_team]['Away_avgFouls'].values[0]
    

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
    
    carton_jaunes_features = pd.DataFrame([[ Home_avgFouls,Away_avgFouls,home_form, away_form,home_advantage,
                                   Home_avgPos,Away_avgPos,moyenne_conceder_dom,moyenne_conceder_ext]], columns=features_cartons_jaunes)
    
    carton_rouge_features = pd.DataFrame([[ Home_avgFouls,Away_avgFouls,home_form, away_form,home_advantage,
                                   Home_avgPos,Away_avgPos,moyenne_conceder_dom,moyenne_conceder_ext]], columns=features_cartons_rouges)
    
    corners_features = pd.DataFrame([[home_avg_shot, away_avg_shot,home_avg_shot_target, away_avg_shot_target,
                                   home_form, away_form,home_advantage,Home_avgPos,Away_avgPos]], columns=features_corners)
    
    foul_features = pd.DataFrame([[home_form, away_form,home_advantage, Home_avgPos,
                                   Away_avgPos,moyenne_conceder_dom,moyenne_conceder_ext]], columns=features_foul)
    
    xG_features = pd.DataFrame([[home_avg_goal, away_avg_goal, home_avg_shot, away_avg_shot,home_avg_shot_target, away_avg_shot_target,
                                   home_form, away_form,home_advantage,moyenne_conceder_dom,moyenne_conceder_ext,
                                   Home_avgPos,Away_avgPos,Home_avgCorner,Away_avgCorner, difference_moyenne_buts_marques,
                                   difference_moyenne_buts_conceder]], columns=features_xG)
    
    
    home_possession, away_possession, prediction_buts_domicile, prediction_buts_extérieur = predict_match_stats(
    model_1, model_2, model_3, possesion_features, match_features, tirs_features, tirsCadres_features,carton_jaunes_features,
    carton_rouge_features, corners_features, foul_features, xG_features
    )
    buteurs_home,buteurs_away,passeur_home, passeur_away = simulate_match(h_team,a_team,prediction_buts_domicile,prediction_buts_extérieur,home_possession,away_possession)
    
    return prediction_buts_domicile,prediction_buts_extérieur,buteurs_home,buteurs_away,passeur_home, passeur_away