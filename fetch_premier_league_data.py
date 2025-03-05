import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Charger les données depuis un fichier CSV
data_2324 = pd.read_csv('season-2324.csv')


data_2324['away_code'] = data_2324['AwayTeam'].astype("category").cat.codes

data_2324['home_code'] = data_2324['HomeTeam'].astype("category").cat.codes

data_2324['goal_diff'] = data_2324['HomeGoal'] - data_2324['AwayGoal']

def moyenne_Stats(data, team_col, stat_col, new_col):
    data[new_col] = 0.0
    grouped = data.groupby(team_col)
    for team, team_matches in grouped:
        for i in range(len(team_matches)):
            derniersMatchs = max(0,i-4)
            window = team_matches.iloc[derniersMatchs:i+1][stat_col]
            data.loc[team_matches.index[i], new_col] = float(window.mean()) 
    return data

data_2324 = moyenne_Stats(data_2324, 'HomeTeam','HomeGoal', 'Home_avgGoal')
data_2324 = moyenne_Stats(data_2324, 'AwayTeam','AwayGoal', 'Away_avgGoal')
data_2324 = moyenne_Stats(data_2324, 'HomeTeam','HomeShots', 'Home_avgShot')
data_2324 = moyenne_Stats(data_2324, 'AwayTeam','AwayShots', 'Away_avgShot')
data_2324 = moyenne_Stats(data_2324, 'HomeTeam','HCorners', 'Home_avgCorner')
data_2324 = moyenne_Stats(data_2324, 'AwayTeam','ACorners', 'Away_avgCorner')
data_2324 = moyenne_Stats(data_2324, 'HomeTeam','HYellow', 'Home_avgYellow')
data_2324 = moyenne_Stats(data_2324, 'AwayTeam','AYellow', 'Away_avgYellow')
data_2324 = moyenne_Stats(data_2324, 'HomeTeam','HRed', 'Home_avgRed')
data_2324 = moyenne_Stats(data_2324, 'AwayTeam','ARed', 'Away_avgRed')

# ligne et colonne
# row and column

def calculate_form(data, team_col, result_col, new_col):
    form_list = []
    for i in range(len(data)):
        team = data.loc[i, team_col]
        past_matches = data.loc[:i-1]
        team_matches = past_matches[past_matches[team_col] == team]
        
        form_score = 0
        if len(team_matches) > 0:
            last_five = team_matches.tail(5)
            for result in last_five[result_col]:
                if result == 'H':
                    form_score += 1
                elif result == 'A':
                    form_score -= 1
        
        form_list.append(form_score)
    
    data[new_col] = form_list
    return data

data_2324 = calculate_form(data_2324, 'HomeTeam', 'FullTimeResult', 'home_form')
data_2324 = calculate_form(data_2324, 'AwayTeam', 'FullTimeResult', 'away_form')
    
print(data_2324)
    





