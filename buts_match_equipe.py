import random 
from fetch_premier_league_players_data import data_joueur_predictions_buteurs

def stats_Dans_Match(data2,team, Stats,nameCol,Col):
    if Stats == 0:
        return []
    else:
        JoueurTeam = []
        for i in range(len(data2[team][nameCol])):
            if data2[team][nameCol].loc[i,'Team'] == team:
                JoueurTeam.append(data2[team][nameCol].iloc[i])
        JoueurTeam = sorted(JoueurTeam, key=lambda x:x[Col], reverse=True)
        listWeight = []
        for j in JoueurTeam:
            listWeight.append(float(j[Col]))
        Buteur = random.choices(JoueurTeam, weights= listWeight, k= Stats)
        if Col == 'ProbOut' or Col == 'ProbFinal':
            Buteur = {j['Player']: {'FirstPos': j['FirstPos'], 'SecondPos': j['SecondPos']} for j in Buteur}
        else:
            Buteur = Buteur[0]['Player']
    return Buteur

print(stats_Dans_Match(data_joueur_predictions_buteurs,'Manchester City',1,'Starting11Players','Gls_90'))
print(stats_Dans_Match(data_joueur_predictions_buteurs,'Manchester City',1,'Starting11Players','ProbOut'))
print(stats_Dans_Match(data_joueur_predictions_buteurs,'Manchester City',1,'BenchPlayers','ProbFinal'))
