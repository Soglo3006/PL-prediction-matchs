import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
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
data_2324 = moyenne_Stats(data_2324, 'HomeTeam','HFouls','Home_avgFouls')
data_2324 = moyenne_Stats(data_2324, 'AwayTeam','AFouls','Away_avgFouls')

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

features = ['Home_avgGoal','Away_avgGoal','Home_avgShot','Away_avgShot', 'home_form','away_form']


X = data_2324[features]
y = data_2324['FullTimeResult']

# Séparation des données en jeu d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

# Entraînement du modèle
model = RandomForestClassifier(n_estimators=100, min_samples_split=10, random_state=1)
model.fit(X_train, y_train)

def predict_future_match(home_team, away_team, model, data):
    if home_team not in data['HomeTeam'].unique():
        #print(f"Erreur : {home_team} n'existe pas dans les données !")
        return None
    if away_team not in data['AwayTeam'].unique():
        #print(f"Erreur : {away_team} n'existe pas dans les données !")
        return None
    
    home_avg_goal = data[data['HomeTeam'] == home_team]['Home_avgGoal'].values[-1]
    away_avg_goal = data[data['AwayTeam'] == away_team]['Away_avgGoal'].values[-1]
    home_avg_shot = data[data['HomeTeam'] == home_team]['Home_avgShot'].values[-1]
    away_avg_shot = data[data['AwayTeam'] == away_team]['Away_avgShot'].values[-1]
    home_form = data[data['HomeTeam'] == home_team]['home_form'].values[-1]
    away_form = data[data['AwayTeam'] == away_team]['away_form'].values[-1]

    match_features = pd.DataFrame([[home_avg_goal, away_avg_goal, home_avg_shot, away_avg_shot, home_form, away_form]],
                                  columns=features)

    prediction = model.predict(match_features)[0]
    if prediction == 'H':
        return home_team
    elif prediction == 'A':
        return away_team

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

#avantageDomicile(data_2324)
#print(data_2324)

def moyenne_domcile(data):
    Équipe_domicile= {}

    for i in data['HomeTeam'].unique():
        Équipe_domicile[i] = 0
    for y in range(len(data)):
        for j in Équipe_domicile:
            if data.loc[y,'HomeTeam'] == j:
                Équipe_domicile[j] += int(data.loc[y,'HomeGoal'])
    moyenne_buts_domicile = dict(sorted(Équipe_domicile.items()))
    for moy in moyenne_buts_domicile:
        moyenne_buts_domicile[moy] = round(moyenne_buts_domicile[moy]/19,2)
    return moyenne_buts_domicile
        
        
#print(moyenne_domcile(data_2324))

def moyenne_exterieru(data):
    Équipe_extérieur = {}
    for i in data['AwayTeam'].unique():
        Équipe_extérieur[i] = 0
    for y in range(len(data)):
        for j in Équipe_extérieur:
            if data.loc[y,'AwayTeam'] == j:
                Équipe_extérieur[j] += int(data.loc[y,'AwayGoal'])
    moyenne_buts_extérieur = dict(sorted(Équipe_extérieur.items()))
    for moy in moyenne_buts_extérieur :
        moyenne_buts_extérieur[moy] = round(moyenne_buts_extérieur[moy]/19,2)
    return moyenne_buts_extérieur
        
        
#print(moyenne_exterieru(data_2324))

def difference_buts(data, moyenne_dom, moyenne_ext):
    dom = moyenne_dom
    ext = moyenne_ext
    for i in range(len(data)):
        if dom[data.loc[i,'HomeTeam']]> ext[data.loc[i,'AwayTeam']] : 
            data.loc[i,'difference'] = dom[data.loc[i,'HomeTeam']] - ext[data.loc[i,'AwayTeam']]
            data.loc[i,'difference_nom'] = data.loc[i,'HomeTeam']
        else:
            data.loc[i,'difference'] = ext[data.loc[i,'AwayTeam']] - dom[data.loc[i,'HomeTeam']]
            data.loc[i,'difference_nom'] = data.loc[i,'AwayTeam']

difference_buts(data_2324,moyenne_domcile(data_2324),moyenne_exterieru(data_2324))
print(data_2324)


# Exemple de prédiction
#home_team = str(random.choice(data_2324['HomeTeam'].unique()))
#away_team = str(random.choice(data_2324['AwayTeam'].unique()))
#if home_team != away_team:
#    predicted_result = predict_future_match(home_team, away_team, model, data_2324)
#    print(f"Prédiction pour {home_team} vs {away_team} : {predicted_result}")

