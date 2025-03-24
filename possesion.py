import pandas as pd
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from fetch_premier_league_data import moyenne_dom_but, moyenne_ext_but, data_2324, avantageDomicile, difference_buts
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import numpy as np

h_team = 'Manchester City'
a_team = 'Luton'

data = data_2324

avantageDomicile(data)
difference_buts(data,moyenne_dom_but,moyenne_ext_but,'difference_moyenne_buts_marques', 'difference_plus_fort_equipe_but_marques')

features_possession = ['Home_avgGoal','Away_avgGoal','Home_avgShot','Away_avgShot', 'Home_avgShot_Target','Away_avgShot_Target'
            , 'home_form','away_form', 'home_advantage','moyenne_domcile_buts','moyenne_exterieur_buts'
            ,'difference_moyenne_buts_marques','Home_avgPos','Away_avgPos']



A = data[features_possession]
B = data['HomePossesion']
A_train, A_test, B_train, B_test = train_test_split(A, B, test_size=0.2, random_state=1)

model_possession = RandomForestRegressor(n_estimators=1500, max_depth=15,min_samples_split=10, random_state=1)
model_possession.fit(A_train, B_train)

#feature_importances = model_possession.feature_importances_
#plt.barh(features_possession, feature_importances)
#plt.xlabel("Importance des features")
#plt.ylabel("Features")
#plt.show()

home_avg_goal = data[data['HomeTeam'] == h_team]['Home_avgGoal'].values[0]
away_avg_goal = data[data['AwayTeam'] == a_team]['Away_avgGoal'].values[0]
home_avg_shot = data[data['HomeTeam'] == h_team]['Home_avgShot'].values[0]
away_avg_shot = data[data['AwayTeam'] == a_team]['Away_avgShot'].values[0]
home_avg_shot_target = data[data['HomeTeam']== h_team]['Home_avgShot_Target'].values[0]
away_avg_shot_target = data[data['AwayTeam']== a_team]['Away_avgShot_Target'].values[0]
home_form = data[data['HomeTeam'] == h_team]['home_form'].values[0]
away_form = data[data['AwayTeam'] == a_team]['away_form'].values[0]
home_advantage = data[data['HomeTeam'] == h_team]['home_advantage'].values[-1]
moyenne_domcile_buts = moyenne_dom_but[h_team]
moyenne_extérieur_buts = moyenne_ext_but[a_team]
difference_moyenne_buts_marques = moyenne_domcile_buts - moyenne_extérieur_buts
Home_avgPos = data[data['HomeTeam'] == h_team]['Home_avgPos'].values[0]
Away_avgPos = data[data['AwayTeam'] == a_team]['Away_avgPos'].values[0]


match_features = pd.DataFrame([[home_avg_goal, away_avg_goal, home_avg_shot, away_avg_shot, 
                                home_avg_shot_target, away_avg_shot_target, home_form, away_form,home_advantage,
                                moyenne_domcile_buts, moyenne_extérieur_buts,difference_moyenne_buts_marques,Home_avgPos,Away_avgPos]],
                              columns=features_possession)


prediction_possession = model_possession.predict(match_features)[0]

fluctuation = np.random.normal(loc=0, scale=4) 
prediction_possession += fluctuation

prediction_possession = max(20, min(80, prediction_possession))
prediction_possession = round(prediction_possession)
away_possession = 100 - prediction_possession
print(prediction_possession)
print(away_possession)
