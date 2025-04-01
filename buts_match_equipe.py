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

#print(stats_Dans_Match(data_joueur_predictions_buteurs,'Manchester City',1,'Starting11Players','Gls_90'))
#SPlayer = (stats_Dans_Match(data_joueur_predictions_buteurs,'Manchester City',1,'Starting11Players','ProbOut'))
#BPlayer = (stats_Dans_Match(data_joueur_predictions_buteurs,'Manchester City',1,'BenchPlayers','ProbFinal'))

"""
def changement_de_joueur(data,team,SPlayer,BPlayer):
    Team_liste = []
    SPlayer_name = list(SPlayer.keys())[0]
    BPlayer_name = list(BPlayer.keys())[0]
    while SPlayer[SPlayer_name]['FirstPos'] not in (BPlayer[BPlayer_name]['FirstPos'], BPlayer[BPlayer_name]['SecondPos']):
        SPlayer = (stats_Dans_Match(data,team,1,'Starting11Players','ProbOut'))
        SPlayer_name = list(SPlayer.keys())[0]

    Joueur_change = []
    for i in range(len(data[team]['Starting11Players'])):
        if data[team]['Starting11Players'].loc[i,'Player'] == SPlayer_name:
            for j in range(len(data[team]['BenchPlayers'])):
                if data[team]['BenchPlayers'].loc[j,'Player'] == BPlayer_name:
                    Joueur_change.append(data[team]['Starting11Players'].loc[i])
                    data[team]['Starting11Players'].loc[i] = data[team]['BenchPlayers'].loc[j].copy()
                    data[team]['Starting11Players'].loc[i,'ProbOut'] = 0.0
                    data[team]['BenchPlayers'].drop(j,inplace=True)
                    break
    data[team]['Starting11Players'].reset_index(drop=True)
    data[team]['BenchPlayers'].reset_index(drop=True, inplace=True)
    Team_liste.append(data_joueur_predictions_buteurs[team])
    return Joueur_change, Team_liste"""
def stats_Joueur(team_liste,col,PlayersCol):
    JoueurTeam = []

    starting_players = team_liste[0][PlayersCol]
    JoueurTeam = starting_players.sort_values(col, ascending=False)
    players_list = JoueurTeam.to_dict('records')

    listWeight = [float(player[col]) for player in players_list]

    Buteur = random.choices(players_list, weights=listWeight, k=1)
    team_liste[0][PlayersCol] = JoueurTeam
    return Buteur[0]['Player'], team_liste

def changement_de_joueur(data, team, SPlayer, BPlayer):
    Team_liste = []
    SPlayer_name = SPlayer if isinstance(SPlayer, str) else list(SPlayer.keys())[0]
    BPlayer_name = BPlayer if isinstance(BPlayer, str) else list(BPlayer.keys())[0]
    
    Joueur_change = []
    for i in range(len(data[team]['Starting11Players'])):
        if data[team]['Starting11Players'].loc[i, 'Player'] == SPlayer_name:
            for j in range(len(data[team]['BenchPlayers'])):
                if data[team]['BenchPlayers'].loc[j, 'Player'] == BPlayer_name:
                    Joueur_change.append(data[team]['Starting11Players'].loc[i].copy())
                    data[team]['Starting11Players'].loc[i] = data[team]['BenchPlayers'].loc[j].copy()
                    data[team]['Starting11Players'].loc[i, 'ProbOut'] = 0.0
                    data[team]['BenchPlayers'] = data[team]['BenchPlayers'].drop(j)
                    break
    data[team]['Starting11Players'].reset_index(drop=True, inplace=True)
    data[team]['BenchPlayers'].reset_index(drop=True, inplace=True)
    Team_liste.append({
        'Starting11Players': data[team]['Starting11Players'],
        'BenchPlayers': data[team]['BenchPlayers']
    })
    
    return Joueur_change, Team_liste

