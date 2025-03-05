import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

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



features = ['Home_avgGoal','Away_avgGoal','Home_avgShot','Away_avgShot','Home_avgCorner',
            'Away_avgCorner','home_form','away_form','Home_avgFouls','Away_avgFouls',
            'home_code','away_code','goal_diff']

X = data_2324[features]
y = data_2324['FullTimeResult']

# Séparation des données en jeu d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

# Entraînement du modèle
model = RandomForestClassifier(n_estimators=100, min_samples_split=10, random_state=1)
model.fit(X_train, y_train)

# Prédictions et évaluation du modèle
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred)

#print(f"Accuracy: {accuracy:.2f}")
#print("Matrice de confusion:\n", conf_matrix)
#print("Rapport de classification:\n", class_report)

def predict_future_match(home_team, away_team, model, data):
    home_code = data[data['HomeTeam'] == home_team]['home_code'].values[0]
    away_code = data[data['AwayTeam'] == away_team]['away_code'].values[0]
    
    match_features = data[features].iloc[-1:].copy()
    match_features['home_code'] = home_code
    match_features['away_code'] = away_code
    
    prediction = model.predict(match_features)[0]
    return prediction

# Exemple de prédiction
home_team = 'Everton'
away_team = 'Chelsea'
predicted_result = predict_future_match(home_team, away_team, model, data_2324)
print(f"Prédiction pour {home_team} vs {away_team} : {predicted_result}")

