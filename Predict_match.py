import pandas as pd
import numpy as np
import random
from détails_simulation import simulate_match
from fetch_premier_league_data import avantage_domicile, difference_buts,moyenne_con_but_dom, moyenne_con_but_ext, moyenne_dom_but, moyenne_ext_but,data_2324
from features import features_match,features_possession,features_tirs,features_tirsCadre, features_cartons_jaunes,features_cartons_rouges,features_corners,features_foul,features_xG, create_match_features
from model import train_models

avantage_domicile(data_2324)
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

def predict_match_stats(model_buts_dom,model_buts_exterieur,model_possesion_dom,pos_features,match_feature,
                        tirs_stats_features,tirs_cadre_stat_features,yellow_features,red_features,corners_stats_features, fouls_features,xg_features):
    
    prediction_buts_domicile = (model_buts_dom.predict(match_feature)[0]) + np.random.normal(0, 0.7)
    prediction_buts_exterieur = (model_buts_exterieur.predict(match_feature)[0]) + np.random.normal(0, 0.7)

    prediction_buts_domicile = max(0,round(prediction_buts_domicile))
    prediction_buts_exterieur = max(0,round(prediction_buts_exterieur))
        
    prediction_possession = model_possesion_dom.predict(pos_features)[0] + np.random.normal(loc=0, scale=4)

    prediction_possession = max(20, min(80, prediction_possession))
    home_possesion = round(prediction_possession)
    away_possession = 100 - home_possesion
    
    print("Possesion domicile:"f"{home_possesion}","Possesion exterireur:"f"{away_possession}")

    prediction_tirs_domicile = (model_tirsH.predict(tirs_stats_features)[0])
    prediction_tirs_exterieur = (model_tirsA.predict(tirs_stats_features)[0])

    diff_niveau = abs(prediction_tirs_domicile - prediction_tirs_exterieur)
    scale_dynamic = max(1.5, min(4, (diff_niveau / 1.5) + 0.5))  

    prediction_tirs_domicile += np.random.normal(loc=0, scale=scale_dynamic)
    prediction_tirs_exterieur += np.random.normal(loc=0, scale=scale_dynamic)
    
    print("tirs domicile:"f"{round(prediction_tirs_domicile)}","tirs exterireur:"f"{round(prediction_tirs_exterieur)}")

    prediction_tirs_cadre_domicile = (model_tirsCadreH.predict(tirs_cadre_stat_features)[0]) + np.random.normal(0, 0.7)
    prediction_tirs_cadre_exterieur = (model_tirsCadreA.predict(tirs_cadre_stat_features)[0]) + np.random.normal(0, 0.7)

    prediction_tirs_cadre_domicile = min(prediction_tirs_domicile, max(0, round(prediction_tirs_cadre_domicile)))
    prediction_tirs_cadre_exterieur = min(prediction_tirs_exterieur, max(0, round(prediction_tirs_cadre_exterieur)))
    
    print("tirs cadre domicile:"f"{round(prediction_tirs_cadre_domicile)}","tirs cadres exterireur:"f"{round(prediction_tirs_cadre_exterieur)}")
    
    
    prediction_carton_jaunes_domicile = (model_yellowH.predict(yellow_features)[0]) + np.random.normal(0, 0.7)
    prediction_carton_jaunes_exterieur = (model_yellowA.predict(yellow_features)[0]) + np.random.normal(0, 0.7)
    
    prediction_carton_jaunes_domicile = max(0,round(prediction_carton_jaunes_domicile))
    prediction_carton_jaunes_exterieur = max(0,round(prediction_carton_jaunes_exterieur))
    
    print("Cartons jaunes domicile:"f"{round(prediction_carton_jaunes_domicile)}","cartons jaunes exterireur:"f"{round(prediction_carton_jaunes_exterieur)}")
    
    prediction_carton_rouges_domicile = (model_redH.predict(red_features)[0]) + np.random.normal(-0.3, 0.5)
    prediction_carton_rouges_exterieur = (model_redA.predict(red_features)[0]) + np.random.normal(-0.3, 0.5)
    
    if random.random() > 0.08:  
        prediction_carton_rouges_domicile = 0
    if random.random() > 0.08:  
        prediction_carton_rouges_exterieur = 0
   
    prediction_carton_rouges_domicile = min(1, max(0, round(prediction_carton_rouges_domicile)))
    prediction_carton_rouges_exterieur = min(1, max(0, round(prediction_carton_rouges_exterieur)))
    
    print("Cartons rouges domicile:"f"{prediction_carton_rouges_domicile}","cartons rouges exterireur:"f"{prediction_carton_rouges_exterieur}")
    
    prediction_corner_domicile = (model_cornerH.predict(corners_stats_features)[0]) + np.random.normal(0, 0.7)
    prediction_corner_exterieur = (model_cornerA.predict(corners_stats_features)[0]) + np.random.normal(0, 0.7)
    
    prediction_corner_domicile = max(0,round(prediction_corner_domicile))
    prediction_corner_exterieur = max(0,round(prediction_corner_exterieur))
    
    print("Corners domicile:"f"{round(prediction_corner_domicile)}","Corners exterireur:"f"{round(prediction_corner_exterieur)}")
    
    prediction_fouls_domicile = (model_foulH.predict(fouls_features)[0]) + np.random.normal(0, 0.7)
    prediction_fouls_exterieur = (model_foulA.predict(fouls_features)[0]) + np.random.normal(0, 0.7)
    
    prediction_fouls_domicile = max(0,round(prediction_fouls_domicile))
    prediction_fouls_exterieur = max(0,round(prediction_fouls_exterieur))
    
    print("Fautes domicile:"f"{round(prediction_fouls_domicile)}","Fautes exterireur:"f"{round(prediction_fouls_exterieur)}")

    
    prediction_xg_domicile = model_xGH.predict(xg_features)[0]
    prediction_xg_exterieur = model_xGA.predict(xg_features)[0]
    
    facteur_buts = 0.25  
    facteur_tirs_cadres = 0.10  
    
    prediction_xg_domicile += (prediction_buts_domicile * facteur_buts) + (prediction_tirs_cadre_domicile * facteur_tirs_cadres)
    prediction_xg_exterieur += (prediction_buts_exterieur * facteur_buts) + (prediction_tirs_cadre_exterieur * facteur_tirs_cadres)
    
    prediction_xg_domicile += np.random.normal(0, 0.1)
    prediction_xg_exterieur += np.random.normal(0, 0.1)
    
    prediction_xg_domicile = max(0, round(prediction_xg_domicile, 2))
    prediction_xg_exterieur = max(0, round(prediction_xg_exterieur, 2))
    
    #print((prediction_xg_domicile),(prediction_xg_exterieur))
    
    return home_possesion,away_possession,prediction_buts_domicile,prediction_buts_exterieur, prediction_fouls_domicile, prediction_fouls_exterieur, prediction_carton_jaunes_domicile, prediction_carton_jaunes_exterieur, prediction_carton_rouges_domicile, prediction_carton_rouges_exterieur

def predict_future_match(h_team, a_team, model_1, model_2, model_3, data):
    
    match_data = create_match_features(h_team, a_team, data)
    
    match_features = pd.DataFrame([[match_data[f] for f in features_match]], columns=features_match)
    possesion_features = pd.DataFrame([[match_data[f] for f in features_possession]], columns=features_possession)
    tirs_features = pd.DataFrame([[match_data[f] for f in features_tirs]], columns=features_tirs)
    tirs_cadres_features = pd.DataFrame([[match_data[f] for f in features_tirsCadre]], columns=features_tirsCadre)
    carton_jaunes_features = pd.DataFrame([[match_data[f] for f in features_cartons_jaunes]], columns=features_cartons_jaunes)
    carton_rouge_features = pd.DataFrame([[match_data[f] for f in features_cartons_rouges]], columns=features_cartons_rouges)
    corners_features = pd.DataFrame([[match_data[f] for f in features_corners]], columns=features_corners)
    foul_features = pd.DataFrame([[match_data[f] for f in features_foul]], columns=features_foul)
    xg_features = pd.DataFrame([[match_data[f] for f in features_xG]], columns=features_xG)

    
    _, _, prediction_buts_domicile, prediction_buts_exterieur,_,_,home_yellow,away_yellow,home_red, away_red = predict_match_stats(
        model_1, model_2, model_3, possesion_features, match_features, tirs_features, tirs_cadres_features,
        carton_jaunes_features, carton_rouge_features, corners_features, foul_features, xg_features
    )
    
    buteurs_home, buteurs_away, passeur_home, passeur_away, yellow_home_players, yellow_away_players,red_home_players, red_away_players, joueur_remplacer_home, joueur_remplacer_away, joueur_rentre_home, joueur_rentre_away  = simulate_match(
        h_team, a_team, prediction_buts_domicile, prediction_buts_exterieur,home_yellow,away_yellow,home_red,away_red)
    

    return prediction_buts_domicile, prediction_buts_exterieur, buteurs_home, buteurs_away, passeur_home, passeur_away, yellow_home_players, yellow_away_players, red_home_players, red_away_players, joueur_remplacer_home, joueur_remplacer_away, joueur_rentre_home, joueur_rentre_away
