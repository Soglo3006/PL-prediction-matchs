import random 
from fetch_premier_league_players_data import data_joueur_predictions_buteurs

def stats_Dans_Match(data2,team, Stats,Col):
    if Stats == 0:
        return []
    else:
        JoueurTeam = []
        for i in range(len(data2[team]['Starting11Players'])):
            if data2[team]['Starting11Players'].loc[i,'Team'] == team:
                JoueurTeam.append(data2[team]['Starting11Players'].iloc[i])
        JoueurTeam = sorted(JoueurTeam, key=lambda x:x[Col], reverse=True)
        listWeight = []
        for j in JoueurTeam:
            listWeight.append(float(j[Col]))
        Buteur = random.choices(JoueurTeam, weights= listWeight, k= Stats)
        Buteur[0] = Buteur[0]['Player']
        
    return Buteur


print(stats_Dans_Match(data_joueur_predictions_buteurs,'Manchester City',1,'CrdYAvg'))