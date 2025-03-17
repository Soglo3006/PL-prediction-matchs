import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import random
import numpy as np
from xgboost import XGBRegressor

# Charger les données depuis un fichier CSV
data_2324 = pd.read_csv('season-2324.csv')
data_2223 = pd.read_csv('season-2223.csv')


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


def moyenne_stats_buts(data,dictionnaire,équipe,but,newCol):
    for i in data[équipe].unique():
        dictionnaire[i] = 0
        dictionnaire = dict(sorted(dictionnaire.items()))
    for y in range(len(data)):
        for j in dictionnaire:
            if data.loc[y,équipe] == j:
                dictionnaire[j] += int(data.loc[y,but])
    for moy in dictionnaire:
        dictionnaire[moy] = round(dictionnaire[moy]/19,2)
    for k in range(len(data)):
        for nom_équipe in dictionnaire:
            if nom_équipe == data.loc[k,équipe]:
                data.loc[k,newCol] = dictionnaire[nom_équipe]
    return dictionnaire
def difference_buts(data, moyenne_dom, moyenne_ext, newCol, newCol2):
    dom = moyenne_dom
    ext = moyenne_ext
    for i in range(len(data)):
        if dom[data.loc[i,'HomeTeam']]> ext[data.loc[i,'AwayTeam']] : 
            data.loc[i,newCol] = dom[data.loc[i,'HomeTeam']] - ext[data.loc[i,'AwayTeam']]
            data.loc[i,newCol2] = data.loc[i,'HomeTeam']
        else:
            data.loc[i,newCol] = ext[data.loc[i,'AwayTeam']] - dom[data.loc[i,'HomeTeam']]
            data.loc[i,newCol2] = data.loc[i,'AwayTeam']

data_2324 = moyenne_Stats(data_2324, 'HomeTeam','HomeGoal', 'Home_avgGoal')
data_2324 = moyenne_Stats(data_2324, 'AwayTeam','AwayGoal', 'Away_avgGoal')
data_2324 = moyenne_Stats(data_2324, 'HomeTeam','HomeShots', 'Home_avgShot')
data_2324 = moyenne_Stats(data_2324, 'AwayTeam','AwayShots', 'Away_avgShot')
data_2324 = moyenne_Stats(data_2324, 'HomeTeam','HomeShotTarget', 'Home_avgShot_Target')
data_2324 = moyenne_Stats(data_2324, 'AwayTeam','AwayShotTarget', 'Away_avgShot_Target')
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

Équipe_domicile= {}
Équipe_extérieur = {}
moy_buts_conceder_dom = {}
moy_buts_conceder_ext = {}
moyenne_dom_but = moyenne_stats_buts(data_2324,Équipe_domicile,'HomeTeam','HomeGoal','moyenne_domcile_buts')
moyenne_ext_but = moyenne_stats_buts(data_2324,Équipe_extérieur,'AwayTeam','AwayGoal','moyenne_exterieur_buts')
moyenne_con_but_dom = moyenne_stats_buts(data_2324,moy_buts_conceder_dom,'HomeTeam','AwayGoal','moyenne_conceder_dom')
moyenne_con_but_ext = moyenne_stats_buts(data_2324,moy_buts_conceder_ext,'AwayTeam','HomeGoal','moyenne_conceder_ext')