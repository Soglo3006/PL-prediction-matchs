from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingRegressor
from fetch_premier_league_data import data_2324
from features import features_match, features_possession,features_tirs,features_tirsCadre

def train_models(data, features, teamCategorie):
    X = data[features]
    y_home = data[teamCategorie]
    X_train, X_test, y_train, y_test = train_test_split(X, y_home, test_size=0.2, random_state=1)
    if teamCategorie == 'HomeGoal' or teamCategorie == 'AwayGoal':
        model = RandomForestClassifier(n_estimators=500, max_depth=7, random_state=1)
        model.fit(X_train, y_train)
    elif teamCategorie == 'HomePossesion' or teamCategorie == 'HomeShots' or teamCategorie == 'AwayShots' or teamCategorie == 'HomeShotTarget' or teamCategorie == 'AwayShotTarget':
        model = RandomForestRegressor(n_estimators=1500, max_depth=15, min_samples_split=10, random_state=1)
        model.fit(X_train, y_train)

    return model

model_home = train_models(data_2324, features_match, 'HomeGoal')
model_away = train_models(data_2324, features_match, 'AwayGoal')
model_possession = train_models(data_2324,features_possession, 'HomePossesion')
model_tirsH = train_models(data_2324,features_tirs,'HomeShots')
model_tirsA = train_models(data_2324,features_tirs,'AwayShots')
model_tirsCadreH = train_models(data_2324,features_tirsCadre,'HomeShotTarget')
model_tirsCadreA = train_models(data_2324,features_tirsCadre,'AwayShotTarget')