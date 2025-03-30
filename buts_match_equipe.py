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
            Buteur = Buteur[0]
    return Buteur

#print(stats_Dans_Match(data_joueur_predictions_buteurs,'Manchester City',1,'Starting11Players','Gls_90'))
SPlayer = (stats_Dans_Match(data_joueur_predictions_buteurs,'Manchester City',1,'Starting11Players','ProbOut'))
BPlayer = (stats_Dans_Match(data_joueur_predictions_buteurs,'Manchester City',1,'BenchPlayers','ProbFinal'))

SPlayer_name = list(SPlayer.keys())[0]

BPlayer_name = list(BPlayer.keys())[0]
while SPlayer[SPlayer_name]['FirstPos'] not in (BPlayer[BPlayer_name]['FirstPos'], BPlayer[BPlayer_name]['SecondPos']):
    SPlayer = (stats_Dans_Match(data_joueur_predictions_buteurs,'Manchester City',1,'Starting11Players','ProbOut'))
    SPlayer_name = list(SPlayer.keys())[0]

Joueur_change = []
for i in range(len(data_joueur_predictions_buteurs['Manchester City']['Starting11Players'])):
    if data_joueur_predictions_buteurs['Manchester City']['Starting11Players'].loc[i,'Player'] == SPlayer_name:
        for j in range(len(data_joueur_predictions_buteurs['Manchester City']['BenchPlayers'])):
            if data_joueur_predictions_buteurs['Manchester City']['BenchPlayers'].loc[j,'Player'] == BPlayer_name:
                Joueur_change.append(data_joueur_predictions_buteurs['Manchester City']['Starting11Players'].loc[i])
                data_joueur_predictions_buteurs['Manchester City']['Starting11Players'].loc[i] = data_joueur_predictions_buteurs['Manchester City']['BenchPlayers'].loc[j].copy()
                data_joueur_predictions_buteurs['Manchester City']['BenchPlayers'].drop(j,inplace=True)
                break
print(SPlayer)
print(BPlayer)
print(data_joueur_predictions_buteurs['Manchester City'])
print(Joueur_change)



    