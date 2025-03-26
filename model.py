from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingRegressor

def train_models(data, features, teamCategorie):
    X = data[features]
    y_home = data[teamCategorie]
    X_train, X_test, y_train, y_test = train_test_split(X, y_home, test_size=0.2, random_state=1)
    if teamCategorie == 'HomeGoal' or teamCategorie == 'AwayGoal' or teamCategorie == 'HYellow' or teamCategorie == 'AYellow' or teamCategorie == 'HRed' or teamCategorie == 'ARed':
        model = RandomForestClassifier(n_estimators=500, max_depth=7, random_state=1)
        model.fit(X_train, y_train)    
    else:
        model = RandomForestRegressor(n_estimators=1500, max_depth=15, min_samples_split=10, random_state=1)
        model.fit(X_train, y_train)

    return model
