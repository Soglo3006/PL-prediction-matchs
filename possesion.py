import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from Simulation_match import train_goal_models, prediction_buts_domicile, prediction_buts_extérieur
from fetch_premier_league_data import data_2324

features_possesion =['Home_avgGoal','Away_avgGoal','Home_avgShot','Away_avgShot', 'Home_avgShot_Target',
                     'Away_avgShot_Target']

h_team = 'Manchester City'
a_team = 'Luton'

data = data_2324

model_home = train_goal_models(data_2324, features_possesion, 'HomePossesion',RandomForestRegressor)

home_avg_goal = data[data['HomeTeam'] == h_team]['Home_avgGoal'].values[-1]
away_avg_goal = data[data['AwayTeam'] == a_team]['Away_avgGoal'].values[-1]
home_avg_shot = data[data['HomeTeam'] == h_team]['Home_avgShot'].values[-1]
away_avg_shot = data[data['AwayTeam'] == a_team]['Away_avgShot'].values[-1]
home_avg_shot_target = data[data['HomeTeam']== h_team]['Home_avgShot_Target'].values[-1]
away_avg_shot_target = data[data['AwayTeam']== a_team]['Away_avgShot_Target'].values[-1]
ButsDomicile = 4
ButsExterieur = 2

match_features = pd.DataFrame([[home_avg_goal, away_avg_goal, home_avg_shot, away_avg_shot, home_avg_shot_target, away_avg_shot_target]]
                              ,columns = features_possesion)

prediction_possesion = model_home.predict(match_features)

print(prediction_possesion)