from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier

def train_models(data, features, team_categorie):
    X = data[features]
    y_home = data[team_categorie]
    x_train, x_test, y_train, y_test = train_test_split(X, y_home, test_size=0.2, random_state=1)
    if team_categorie == 'HomeGoal' or team_categorie == 'AwayGoal' or team_categorie == 'HYellow' or team_categorie == 'AYellow' or team_categorie == 'HRed' or team_categorie == 'ARed':
        model = RandomForestClassifier(n_estimators=500, max_depth=7, random_state=1)
        model.fit(x_train, y_train)    
    else:
        model = RandomForestRegressor(n_estimators=1500, max_depth=15, min_samples_split=10, random_state=1)
        model.fit(x_train, y_train)

    return model
