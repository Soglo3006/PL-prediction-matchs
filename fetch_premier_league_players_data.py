import pandas as pd

data_joueur_stats = pd.read_csv('fichier csv/premier-player-23-24.csv')

def AjoutStats(data):
    data['PlayerID'] = data['Player'].astype("category").cat.codes
    data['TeamID'] = data['Team'].astype("category").cat.codes

    for i in range(len(data)):
        data.loc[i,'Team'] = data.loc[i,'Team'].strip()
        data.loc[i,'GoalsPerGames'] = round(data.loc[i,'Gls']/data.loc[i,'MP'],2)
        data.loc[i,'Buts'] = 0
        if data.loc[i,'CrdY'] == 0.0 and data.loc[i,'Pos'] == 'GK':
            data.loc[i,'CrdYAvg'] = 0.0
        elif data.loc[i,'CrdY'] == 0.0:
            data.loc[i,'CrdYAvg'] = 0.04
        else:
            data.loc[i,'CrdYAvg'] = data.loc[i,'CrdY']/50
            
        if data.loc[i,'Pos'] == 'GK':
            data.loc[i,'CrdRPro'] = 0.0
            data.loc[i,'ProbChangement'] = 0.0
            data.loc[i,'FirstPos'] = 'GK'
        elif data.loc[i,'Pos'] == 'DF' or data.loc[i,'Pos'] == 'DF,MF' or data.loc[i,'Pos']== 'DF,FW':
            data.loc[i,'CrdRPro'] = 0.02
            data.loc[i,'FirstPos'] = 'DF'
        elif data.loc[i,'Pos'] == 'MF' or data.loc[i,'Pos'] == 'MF,DF' or data.loc[i,'Pos'] == 'MF,FW':
            data.loc[i,'CrdRPro'] = 0.015
            data.loc[i,'FirstPos'] = 'MF'
        elif data.loc[i,'Pos'] == 'FW' or data.loc[i,'Pos'] == 'FW,DF' or data.loc[i,'Pos'] == 'FW,MF':
            data.loc[i,'CrdRPro'] = 0.005
            data.loc[i,'FirstPos'] = 'FW'
            
        if data.loc[i,'Pos'] == 'DF,MF' or data.loc[i,'Pos'] == 'FW,MF':
            data.loc[i,'SecondPos'] = 'MF'
        elif data.loc[i,'Pos'] == 'DF,FW' or data.loc[i,'Pos'] == 'MF,FW':
            data.loc[i,'SecondPos'] = 'FW'
        elif data.loc[i,'Pos'] == 'MF,DF' or data.loc[i,'Pos'] == 'FW,DF':
            data.loc[i,'SecondPos'] = 'DF'
    return data

def penalty_taker(data):
    TakersPerTeam = {}
    for i in data['Team'].unique():
        TakersPerTeam[i] ={'Pénalty':[]}
        
    for j in range(len(data)):
        for k in TakersPerTeam:
            if data.loc[j,'Team'] ==k and data.loc[j,'PKatt'] > 0:
                penalty_goals = data.loc[j, 'PK']
                player_name = data.loc[j, 'Player']
                TakersPerTeam[k]['Pénalty'].append({player_name: int(penalty_goals)})
    return TakersPerTeam

def find_top_scorer(data):
    top_scorers = {}
    for team, stats in data.items():
        penalty_info = stats['Pénalty']
        top_player = penalty_info[0]  
        for player_stat in penalty_info:
            player, goals = list(player_stat.items())[0]
            if goals > list(top_player.values())[0]:
                top_player = player_stat
        team_name = team
        player_name = list(top_player.keys())[0]
        top_scorers[team_name] = player_name
    return top_scorers


def valeur_takers(data):
    FKTakersPerTeam = {'Manchester City': 'Kevin De Bruyne', 'Liverpool': 'Trent Alexander-Arnold', 'Arsenal': 'Martin Ødegaard', 'Chelsea': 'Cole Palmer', 
                   'Newcastle ': 'Kieran Trippier', 'Tottenham ': 'James Maddison', 'Manchester United': 'Bruno Fernandes', 'Aston Villa': 'Lucas Digne', 
                   'West Ham': 'James Ward-Prowse', 'Crystal Palace': 'Eberechi Eze', 'Fulham': 'Harry Wilson', 'Everton': 'Ashley Young',
                   'Brighton': 'Danny Welbeck', 'Bournemouth': 'Justin Kluivert', 'Wolves': 'Pablo Sarabia', 'Brentford': 'Bryan Mbeumo', 
                   'Nottingham Forest': 'Morgan Gibbs-White', 'Luton ': 'Alfie Doughty', 'Burnley': 'Josh Brownhill', 'Sheffield United': 'Gustavo Hamer'}
    for j in range(len(data)):
        if data.loc[j,'Player'] in top_scorers.values():
            data.loc[j,'PkTaker'] = 1
        else:
            data.loc[j,'PkTaker'] = 0
        if data.loc[j,'Player'] in FKTakersPerTeam.values():
            data.loc[j,'FKTaker'] = 1
        else:
            data.loc[j,'FKTaker'] = 0


def data_team_effectif(data):
    Starting11EachTeam  = {}
    BenchPlayers = {}
    dataJoueur = {}
    for i in data['Team'].unique():
        Starting11EachTeam[i] = data[data['Team']==i].sort_values(by = ['Starts'], ascending =False).head(11).reset_index(drop=True)
        BenchPlayers[i] = data[data['Team'] == i ].sort_values(by = ['Starts'], ascending =False).tail(len(data[data['Team'] == i ])- len(Starting11EachTeam[i])).reset_index(drop=True)

    features_players = ['Player','Team','Pos','PkTaker','FKTaker','Gls_90','Ast_90','xG_90','xAG_90','GoalsPerGames','CrdY','CrdYAvg','CrdRPro','FirstPos','SecondPos','MP']
    for i in data['Team'].unique():
        dataJoueur[i] = {
            'Starting11Players' : Starting11EachTeam[i][features_players],
            'BenchPlayers' : BenchPlayers[i][features_players]
        }
    return dataJoueur



#print(data_joueur_stats.loc[0:21,['Player','Team','Pos','Gls_90','Ast_90','xG_90','xAG_90','CrdY']])
data_joueur_stats = AjoutStats(data_joueur_stats)
top_scorers = find_top_scorer(penalty_taker(data_joueur_stats))
valeur_takers(data_joueur_stats)
data_joueur_predictions_buteurs = data_team_effectif(data_joueur_stats)

def probabilité_changement(data1,data2):
    for k in data1['Team'].unique():
        max_game_benchPlayers = data2[k]['BenchPlayers']['MP'].max()
        for i in range(len(data2[k]['BenchPlayers'])):
            if data2[k]['BenchPlayers'].loc[i,'FirstPos'] == 'FW' or data2[k]['BenchPlayers'].loc[i,'SecondPos'] == 'FW':
                data2[k]['BenchPlayers'].loc[i,'ProbPos'] = 0.65
            elif data2[k]['BenchPlayers'].loc[i,'FirstPos'] == 'MF':
                data2[k]['BenchPlayers'].loc[i,'ProbPos'] = 0.45
            elif data2[k]['BenchPlayers'].loc[i,'FirstPos'] == 'DF':
                data2[k]['BenchPlayers'].loc[i,'ProbPos'] = 0.20
            else:
                data2[k]['BenchPlayers'].loc[i,'ProbPos'] = 0.0
                
            data2[k]['BenchPlayers'].loc[i,'ProbMP'] = round(data2[k]['BenchPlayers'].loc[i,'MP'] / max_game_benchPlayers,2)

            data2[k]['BenchPlayers'].loc[i,'ProbFinal'] = round(data2[k]['BenchPlayers'].loc[i,'ProbMP'] * data2[k]['BenchPlayers'].loc[i,'ProbPos'],2)
            
            if data2[k]['BenchPlayers'].loc[i,'MP'] < 10:
                data2[k]['BenchPlayers'].loc[i,'ProbFinal'] = 0

        for i in range(len(data2[k]['Starting11Players'])):
            if data2[k]['Starting11Players'].loc[i,'FirstPos'] == 'FW' or data2[k]['Starting11Players'].loc[i,'SecondPos'] == 'FW':
                data2[k]['Starting11Players'].loc[i,'ProbOut'] = 0.60
            elif data2[k]['Starting11Players'].loc[i,'FirstPos'] == 'MF':
                data2[k]['Starting11Players'].loc[i,'ProbOut'] = 0.50
            elif data2[k]['Starting11Players'].loc[i,'FirstPos'] == 'DF':
                data2[k]['Starting11Players'].loc[i,'ProbOut'] = 0.30
            else:
                data2[k]['Starting11Players'].loc[i,'ProbOut'] = 0.0

probabilité_changement(data_joueur_stats, data_joueur_predictions_buteurs)
print(data_joueur_predictions_buteurs['Manchester City'])