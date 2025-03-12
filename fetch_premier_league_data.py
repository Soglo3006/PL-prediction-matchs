import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import random

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

def avantageDomicile(data):
    Équipe_victoires_domicile = {}
    for i in data['HomeTeam'].unique():
        Équipe_victoires_domicile[i] = 0
    for y in range(len(data)):
        if data.loc[y,'FullTimeResult'] == 'H':
            Équipe_victoires_domicile[data.loc[y,'HomeTeam']] += 1
    for j in Équipe_victoires_domicile:
        Équipe_victoires_domicile[j] = round(Équipe_victoires_domicile[j]/19,2)
    porucentage_victoire = dict(sorted(Équipe_victoires_domicile.items()))
    for i in range(len(data)):
        if porucentage_victoire[data.loc[i,'HomeTeam']] > porucentage_victoire[data_2324.loc[i,'AwayTeam']]:
            data.loc[i,'home_advantage'] = 1
        else:
            data.loc[i,'home_advantage'] = 0


def moyenne_stats_buts(data,dictionnaire,équipe,but):
    for i in data[équipe].unique():
        dictionnaire[i] = 0
    for y in range(len(data)):
        for j in dictionnaire:
            if data.loc[y,équipe] == j:
                dictionnaire[j] += int(data.loc[y,but])
    moyenne_buts_domicile = dict(sorted(dictionnaire.items()))
    for moy in moyenne_buts_domicile:
        moyenne_buts_domicile[moy] = round(moyenne_buts_domicile[moy]/19,2)
    for k in range(len(data)):
        for nom_équipe in moyenne_buts_domicile:
            if nom_équipe == data.loc[k,équipe]:
                data.loc[k,'moyenne_domcile_buts'] = moyenne_buts_domicile[nom_équipe]
    return moyenne_buts_domicile

Équipe_domicile= {}
Équipe_extérieur = {}
moy_buts_conceder_dom = {}
moy_buts_conceder_ext = {}
print(moyenne_stats_buts(data_2324,Équipe_domicile,'HomeTeam','HomeGoal'))
print(moyenne_stats_buts(data_2324,Équipe_extérieur,'AwayTeam','AwayGoal'))
print(moyenne_stats_buts(data_2324,moy_buts_conceder_dom,'HomeTeam','AwayGoal'))
print(moyenne_stats_buts(data_2324,moy_buts_conceder_ext,'AwayTeam','HomeGoal'))

def difference_buts(data, moyenne_dom, moyenne_ext):
    dom = moyenne_dom
    ext = moyenne_ext
    for i in range(len(data)):
        if dom[data.loc[i,'HomeTeam']]> ext[data.loc[i,'AwayTeam']] : 
            data.loc[i,'difference_moyenne'] = dom[data.loc[i,'HomeTeam']] - ext[data.loc[i,'AwayTeam']]
            data.loc[i,'difference_nom'] = data.loc[i,'HomeTeam']
        else:
            data.loc[i,'difference_moyenne'] = ext[data.loc[i,'AwayTeam']] - dom[data.loc[i,'HomeTeam']]
            data.loc[i,'difference_nom'] = data.loc[i,'AwayTeam']

data_2324 = moyenne_Stats(data_2324, 'HomeTeam','HomeGoal', 'Home_avgGoal')
data_2324 = moyenne_Stats(data_2324, 'AwayTeam','AwayGoal', 'Away_avgGoal')
data_2324 = moyenne_Stats(data_2324, 'HomeTeam','HomeShots', 'Home_avgShot')
data_2324 = moyenne_Stats(data_2324, 'AwayTeam','AwayShots', 'Away_avgShot')
data_2324 = moyenne_Stats(data_2324, 'HomeTeam','HCorners', 'Home_avgCorner')
data_2324 = moyenne_Stats(data_2324, 'AwayTeam','ACorners', 'Away_avgCorner')
#data_2324 = moyenne_Stats(data_2324, 'HomeTeam','HYellow', 'Home_avgYellow')
#data_2324 = moyenne_Stats(data_2324, 'AwayTeam','AYellow', 'Away_avgYellow')
#data_2324 = moyenne_Stats(data_2324, 'HomeTeam','HRed', 'Home_avgRed')
#data_2324 = moyenne_Stats(data_2324, 'AwayTeam','ARed', 'Away_avgRed')
#data_2324 = moyenne_Stats(data_2324, 'HomeTeam','HFouls','Home_avgFouls')
#data_2324 = moyenne_Stats(data_2324, 'AwayTeam','AFouls','Away_avgFouls')
data_2324 = calculate_form(data_2324, 'HomeTeam', 'FullTimeResult', 'home_form')
data_2324 = calculate_form(data_2324, 'AwayTeam', 'FullTimeResult', 'away_form')

#avantageDomicile(data_2324)
#difference_buts(data_2324,moyenne_domcile(data_2324),moyenne_exterieru(data_2324))



    

    




#print(moy_buts_conceder_dom)
#print(data_2324)
features = ['Home_avgGoal','Away_avgGoal','Home_avgShot','Away_avgShot'
            , 'home_form','away_form', 'home_advantage','moyenne_domcile_buts','moyenne_exterieur_buts','difference_moyenne']


X = data_2324[features]
y_home = data_2324['HomeGoal']
y_away = data_2324['AwayGoal']



""""
# Séparation des données en jeu d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y_home, test_size=0.2, random_state=1)
W_train, W_test, Z_train, Z_test = train_test_split(X, y_away, test_size=0.2, random_state=1)

# Entraînement du modèle
model_home = RandomForestRegressor(n_estimators=100, min_samples_split=10, random_state=1)
model_home.fit(X_train, y_train)

model_away = RandomForestRegressor(n_estimators=100, min_samples_split=10, random_state=1)
model_away.fit(W_train,Z_train)

def predict_future_match(h_team, a_team, model_1, model_2, data):
    if h_team not in data['HomeTeam'].unique():
        #print(f"Erreur : {home_team} n'existe pas dans les données !")
        return None
    if a_team not in data['AwayTeam'].unique():
        #print(f"Erreur : {away_team} n'existe pas dans les données !")
        return None
    
    home_avg_goal = data[data['HomeTeam'] == h_team]['Home_avgGoal'].values[-1]
    away_avg_goal = data[data['AwayTeam'] == a_team]['Away_avgGoal'].values[-1]
    home_avg_shot = data[data['HomeTeam'] == h_team]['Home_avgShot'].values[-1]
    away_avg_shot = data[data['AwayTeam'] == a_team]['Away_avgShot'].values[-1]
    home_form = data[data['HomeTeam'] == h_team]['home_form'].values[-1]
    away_form = data[data['AwayTeam'] == a_team]['away_form'].values[-1]
    home_advantage = data[data['HomeTeam'] == h_team]['home_advantage'].values[-1]
    moyenne_domcile_buts = moyenne_domcile(data)[h_team]
    moyenne_extérieur_buts = moyenne_exterieru(data)[a_team]
    difference_moyenne = moyenne_domcile_buts - moyenne_extérieur_buts
    

    match_features = pd.DataFrame([[home_avg_goal, away_avg_goal, home_avg_shot, away_avg_shot,
                                    home_form, away_form, home_advantage, moyenne_domcile_buts,moyenne_extérieur_buts, difference_moyenne]],
                                  columns=features)
    print(match_features)
    prediction_buts_domicile = round(model_1.predict(match_features)[0])
    prediction_buts_extérieur = round(model_2.predict(match_features)[0])
    print(prediction_buts_domicile)
    print(prediction_buts_extérieur)
    if prediction_buts_domicile > prediction_buts_extérieur:
        return {prediction_buts_domicile : prediction_buts_extérieur }
    else:
        return {prediction_buts_extérieur : prediction_buts_domicile }
    


h_team = 'Arsenal'
a_team = 'Newcastle'
if h_team != a_team:
    predicted_result = predict_future_match(h_team, a_team, model_home, model_away, data_2324)
    print(f"Prédiction pour {h_team} vs {a_team} : {predicted_result}")
"""