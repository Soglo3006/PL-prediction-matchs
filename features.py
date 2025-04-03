from fetch_premier_league_data import moyenne_dom_but,moyenne_ext_but,moyenne_con_but_dom,moyenne_con_but_ext

def create_match_features(home_team, away_team, data):
    home_avg_goal = data[data['HomeTeam'] == home_team]['Home_avgGoal'].values[0]
    away_avg_goal = data[data['AwayTeam'] == away_team]['Away_avgGoal'].values[0]
    
    home_avg_shot = data[data['HomeTeam'] == home_team]['Home_avgShot'].values[0]
    away_avg_shot = data[data['AwayTeam'] == away_team]['Away_avgShot'].values[0]
    
    home_avg_shot_target = data[data['HomeTeam'] == home_team]['Home_avgShot_Target'].values[0]
    away_avg_shot_target = data[data['AwayTeam'] == away_team]['Away_avgShot_Target'].values[0]
    
    home_form = data[data['HomeTeam'] == home_team]['home_form'].values[0]
    away_form = data[data['AwayTeam'] == away_team]['away_form'].values[0]
    
    home_advantage = data[data['HomeTeam'] == home_team]['home_advantage'].values[0]
    
    moyenne_domcile_buts = moyenne_dom_but[home_team]
    moyenne_exterieur_buts = moyenne_ext_but[away_team]
    
    moyenne_conceder_dom = moyenne_con_but_dom[home_team]
    moyenne_conceder_ext = moyenne_con_but_ext[away_team]
    
    difference_moyenne_buts_marques = moyenne_domcile_buts - moyenne_exterieur_buts
    difference_moyenne_buts_conceder = moyenne_conceder_dom - moyenne_conceder_ext
    
    home_avg_corner = data[data['HomeTeam'] == home_team]['Home_avgCorner'].values[0]
    away_avg_corner = data[data['AwayTeam'] == away_team]['Away_avgCorner'].values[0]
    
    home_avg_pos = data[data['HomeTeam'] == home_team]['Home_avgPos'].values[0]
    away_avg_pos = data[data['AwayTeam'] == away_team]['Away_avgPos'].values[0]
    
    home_avg_fouls = data[data['HomeTeam'] == home_team]['Home_avgFouls'].values[0]
    away_avg_fouls = data[data['AwayTeam'] == away_team]['Away_avgFouls'].values[0]
    
    home_avg_yellow = data[data['HomeTeam']== home_team]['Home_avgYellow'].values[0]
    away_avg_yellow = data[data['AwayTeam']== away_team]['Away_avgYellow'].values[0]
    
    match_data = {
        "Home_avgGoal": home_avg_goal, "Away_avgGoal": away_avg_goal,
        "Home_avgShot": home_avg_shot, "Away_avgShot": away_avg_shot,
        "Home_avgShot_Target": home_avg_shot_target, "Away_avgShot_Target": away_avg_shot_target,
        "home_form": home_form, "away_form": away_form,
        "home_advantage": home_advantage,
        "moyenne_conceder_dom": moyenne_conceder_dom, "moyenne_conceder_ext": moyenne_conceder_ext,
        "Home_avgCorner": home_avg_corner, "Away_avgCorner": away_avg_corner,
        "Home_avgPos": home_avg_pos, "Away_avgPos": away_avg_pos,
        "Home_avgFouls": home_avg_fouls, "Away_avgFouls": away_avg_fouls,
        "difference_moyenne_buts_marques": difference_moyenne_buts_marques,
        "difference_moyenne_buts_conceder": difference_moyenne_buts_conceder,
        "moyenne_domcile_buts": moyenne_domcile_buts ,
        "moyenne_exterieur_buts": moyenne_exterieur_buts,
        "Home_avgYellow": home_avg_yellow,
        "Away_avgYellow": away_avg_yellow,
    }

    return match_data


features_possession = [
    'Home_avgGoal','Away_avgGoal','Home_avgShot',
    'Away_avgShot', 'Home_avgShot_Target'
    ,'Away_avgShot_Target','home_form','away_form',
    'home_advantage','moyenne_domcile_buts','moyenne_exterieur_buts',
    'difference_moyenne_buts_marques','moyenne_conceder_dom',
    'moyenne_conceder_ext','Home_avgPos','Away_avgPos'
                       ]

features_match = [
    'Home_avgGoal','Away_avgGoal','Home_avgShot',
    'Away_avgShot', 'Home_avgShot_Target','Away_avgShot_Target'
    ,'home_form','away_form', 'home_advantage','moyenne_domcile_buts',
    'moyenne_exterieur_buts','difference_moyenne_buts_marques',
    'difference_moyenne_buts_conceder','moyenne_conceder_dom',
    'moyenne_conceder_ext','Home_avgCorner','Away_avgCorner',
    'Home_avgPos','Away_avgPos'
            ]

features_tirs =  [
    'Home_avgGoal','Away_avgGoal','Home_avgShot','Away_avgShot','home_form'
    ,'away_form','moyenne_domcile_buts','moyenne_exterieur_buts'
    ,'difference_moyenne_buts_marques','moyenne_conceder_dom', 'moyenne_conceder_ext'
    ,'Home_avgCorner','Away_avgCorner','Home_avgPos','Away_avgPos'
                  ]

features_tirsCadre = [
    'Home_avgGoal','Away_avgGoal','Home_avgShot','Away_avgShot',
    'Home_avgShot_Target','Away_avgShot_Target','home_form','away_form',
    'home_advantage','moyenne_conceder_dom', 'moyenne_conceder_ext'
    ,'Home_avgPos','Away_avgPos'
                  ]

features_cartons_jaunes = [
    'Home_avgFouls', 'Away_avgFouls',    
    'home_form', 'away_form',    
    'Home_avgPos', 'Away_avgPos',  
    'moyenne_conceder_dom', 'moyenne_conceder_ext',    
    'home_advantage' 
]


features_cartons_rouges = [
    'Home_avgFouls', 'Away_avgFouls',  
    'home_form', 'away_form',  
    'Home_avgYellow', 'Away_avgYellow',
    'Home_avgPos', 'Away_avgPos',  
    'home_advantage'
]

features_corners = [
    'Home_avgShot', 'Away_avgShot',  
    'Home_avgShot_Target', 'Away_avgShot_Target',  
    'Home_avgPos', 'Away_avgPos',    
    'home_form', 'away_form',  
    'home_advantage'  
]


features_foul = [
    'Home_avgPos', 'Away_avgPos',   
    'home_form', 'away_form',  
    'moyenne_conceder_dom', 'moyenne_conceder_ext',  
    'home_advantage'
]

features_xG = [
    'Home_avgShot', 'Away_avgShot',  
    'Home_avgShot_Target', 'Away_avgShot_Target', 
    'Home_avgGoal', 'Away_avgGoal',    
    'Home_avgPos', 'Away_avgPos',  
    'home_form', 'away_form',      
    'Home_avgCorner', 'Away_avgCorner',   
    'home_advantage'  
]



