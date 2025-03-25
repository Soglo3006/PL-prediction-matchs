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
    'moyenne_conceder_dom', 'moyenne_conceder_ext',   
    'Home_avgCorner', 'Away_avgCorner',   
    'difference_moyenne_buts_marques',   
    'difference_moyenne_buts_conceder', 
    'home_advantage'  
]



