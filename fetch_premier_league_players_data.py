import pandas as pd

data_joueur_stats = pd.read_csv('fichier csv/premier-player-23-24.csv')
def ajout_stats(data):
    data['PlayerID'] = data['Player'].astype("category").cat.codes
    data['TeamID'] = data['Team'].astype("category").cat.codes

    yellow_card_prob(data)
    for player_index in range(len(data)):
        
        data.loc[player_index,'Team'] = data.loc[player_index,'Team'].strip()
        data.loc[player_index,'GoalsPerGames'] = round(data.loc[player_index,'Gls']/data.loc[player_index,'MP'],2)
        data.loc[player_index,'Buts'] = 0
            
        if data.loc[player_index,'Pos'] == 'GK':
            data.loc[player_index,'CrdRPro'] = 0.0
            data.loc[player_index,'ProbChangement'] = 0.0
            data.loc[player_index,'FirstPos'] = 'GK'
        elif data.loc[player_index,'Pos'] == 'DF' or data.loc[player_index,'Pos'] == 'DF,MF' or data.loc[player_index,'Pos']== 'DF,FW':
            data.loc[player_index,'CrdRPro'] = 0.02
            data.loc[player_index,'FirstPos'] = 'DF'
        elif data.loc[player_index,'Pos'] == 'MF' or data.loc[player_index,'Pos'] == 'MF,DF' or data.loc[player_index,'Pos'] == 'MF,FW':
            data.loc[player_index,'CrdRPro'] = 0.015
            data.loc[player_index,'FirstPos'] = 'MF'
        elif data.loc[player_index,'Pos'] == 'FW' or data.loc[player_index,'Pos'] == 'FW,DF' or data.loc[player_index,'Pos'] == 'FW,MF':
            data.loc[player_index,'CrdRPro'] = 0.005
            data.loc[player_index,'FirstPos'] = 'FW'
            
    second_position(data)
    return data

def yellow_card_prob(data):
    for player_index in range(len(data)):
        if data.loc[player_index,'CrdY'] == 0 and data.loc[player_index,'Pos'] == 'GK':
            data.loc[player_index,'CrdYAvg'] = 0.0
        elif data.loc[player_index,'CrdY'] == 0:
            data.loc[player_index,'CrdYAvg'] = 0.04
        else:
            data.loc[player_index,'CrdYAvg'] = data.loc[player_index,'CrdY']/50
            
def second_position(data):
    for player_index in range(len(data)):
        if data.loc[player_index,'Pos'] == 'DF,MF' or data.loc[player_index,'Pos'] == 'FW,MF':
            data.loc[player_index,'SecondPos'] = 'MF'
        elif data.loc[player_index,'Pos'] == 'DF,FW' or data.loc[player_index,'Pos'] == 'MF,FW':
            data.loc[player_index,'SecondPos'] = 'FW'
        elif data.loc[player_index,'Pos'] == 'MF,DF' or data.loc[player_index,'Pos'] == 'FW,DF':
            data.loc[player_index,'SecondPos'] = 'DF'

def penalty_taker(data):
    penalty = 'Pénalty'
    takers_per_team = {}
    
    for team in data['Team'].unique():
        takers_per_team[team] ={penalty:[]}
        
    for player_index in range(len(data)):
        for player in takers_per_team:
            if data.loc[player_index,'Team'] == player and data.loc[player_index,'PKatt'] > 0:
                penalty_goals = data.loc[player_index, 'PK']
                player_name = data.loc[player_index, 'Player']
                takers_per_team[player][penalty].append({player_name: int(penalty_goals)})
                
    return takers_per_team

def find_top_scorer(data):
    top_scorers = {}
    
    for team, stats in data.items():
        penalty_info = stats['Pénalty']
        top_player = penalty_info[0]  
        for player_stat in penalty_info:
            _, goals = list(player_stat.items())[0]
            if goals > list(top_player.values())[0]:
                top_player = player_stat
        team_name = team
        player_name = list(top_player.keys())[0]
        top_scorers[team_name] = player_name
        
    return top_scorers

def valeur_takers(data):
    fk_takers_per_team = {'Manchester City': 'Kevin De Bruyne', 'Liverpool': 'Trent Alexander-Arnold', 'Arsenal': 'Martin Ødegaard', 'Chelsea': 'Cole Palmer', 
                   'Newcastle ': 'Kieran Trippier', 'Tottenham ': 'James Maddison', 'Manchester United': 'Bruno Fernandes', 'Aston Villa': 'Lucas Digne', 
                   'West Ham': 'James Ward-Prowse', 'Crystal Palace': 'Eberechi Eze', 'Fulham': 'Harry Wilson', 'Everton': 'Ashley Young',
                   'Brighton': 'Danny Welbeck', 'Bournemouth': 'Justin Kluivert', 'Wolves': 'Pablo Sarabia', 'Brentford': 'Bryan Mbeumo', 
                   'Nottingham Forest': 'Morgan Gibbs-White', 'Luton ': 'Alfie Doughty', 'Burnley': 'Josh Brownhill', 'Sheffield United': 'Gustavo Hamer'}
    
    for player_index in range(len(data)):
        if data.loc[player_index,'Player'] in top_scorers.values():
            data.loc[player_index,'PkTaker'] = 1
        else:
            data.loc[player_index,'PkTaker'] = 0
        if data.loc[player_index,'Player'] in fk_takers_per_team.values():
            data.loc[player_index,'FKTaker'] = 1
        else:
            data.loc[player_index,'FKTaker'] = 0

def data_team_effectif(data):
    starting_11_each_team  = {}
    bench_players = {}
    data_joueur = {}
    
    for team in data['Team'].unique():
        starting_11_each_team[team] = data[data['Team'] == team].sort_values(by = ['Starts'], ascending =False).head(11).reset_index(drop=True)
        bench_players[team] = data[data['Team'] == team ].sort_values(by = ['Starts'], ascending =False).tail(len(data[data['Team'] == team ])- len(starting_11_each_team[team])).reset_index(drop=True)

    features_players = ['Player','Team','Pos','PkTaker','FKTaker','Gls_90','Ast_90','xG_90','xAG_90','GoalsPerGames','CrdY','CrdYAvg','CrdRPro','FirstPos','SecondPos','MP']
    for team in data['Team'].unique():
        data_joueur[team] = {
            'Starting11Players' : starting_11_each_team[team][features_players],
            'BenchPlayers' : bench_players[team][features_players]
        }
        
    return data_joueur

data_joueur_stats = ajout_stats(data_joueur_stats)
top_scorers = find_top_scorer(penalty_taker(data_joueur_stats))
valeur_takers(data_joueur_stats)
data_joueur_predictions_buteurs = data_team_effectif(data_joueur_stats)

def probabilite_changement(data1,data2):
    for team in data1['Team'].unique():
        max_game_bench_players = data2[team]['BenchPlayers']['MP'].max()
        for player_index_bench in range(len(data2[team]['BenchPlayers'])):
            if data2[team]['BenchPlayers'].loc[player_index_bench,'FirstPos'] == 'FW' or data2[team]['BenchPlayers'].loc[player_index_bench,'SecondPos'] == 'FW':
                data2[team]['BenchPlayers'].loc[player_index_bench,'ProbPos'] = 0.65
            elif data2[team]['BenchPlayers'].loc[player_index_bench,'FirstPos'] == 'MF':
                data2[team]['BenchPlayers'].loc[player_index_bench,'ProbPos'] = 0.45
            elif data2[team]['BenchPlayers'].loc[player_index_bench,'FirstPos'] == 'DF':
                data2[team]['BenchPlayers'].loc[player_index_bench,'ProbPos'] = 0.20
            else:
                data2[team]['BenchPlayers'].loc[player_index_bench,'ProbPos'] = 0.0
                
            data2[team]['BenchPlayers'].loc[player_index_bench,'ProbMP'] = round(data2[team]['BenchPlayers'].loc[player_index_bench,'MP'] / max_game_bench_players,2)
            data2[team]['BenchPlayers'].loc[player_index_bench,'ProbFinal'] = round(data2[team]['BenchPlayers'].loc[player_index_bench,'ProbMP'] * data2[team]['BenchPlayers'].loc[player_index_bench,'ProbPos'],2)
            
            if data2[team]['BenchPlayers'].loc[player_index_bench,'MP'] < 10:
                data2[team]['BenchPlayers'].loc[player_index_bench,'ProbFinal'] = 0

    probabilite_changement_starter(data1,data2)
    
def probabilite_changement_starter(data1,data2):
    for team in data1['Team'].unique():
        for player_index_starter in range(len(data2[team]['Starting11Players'])):
            if data2[team]['Starting11Players'].loc[player_index_starter,'FirstPos'] == 'FW' or data2[team]['Starting11Players'].loc[player_index_starter,'SecondPos'] == 'FW':
                data2[team]['Starting11Players'].loc[player_index_starter,'ProbOut'] = 0.60
            elif data2[team]['Starting11Players'].loc[player_index_starter,'FirstPos'] == 'MF':
                data2[team]['Starting11Players'].loc[player_index_starter,'ProbOut'] = 0.50
            elif data2[team]['Starting11Players'].loc[player_index_starter,'FirstPos'] == 'DF':
                data2[team]['Starting11Players'].loc[player_index_starter,'ProbOut'] = 0.30
            else:
                data2[team]['Starting11Players'].loc[player_index_starter,'ProbOut'] = 0.0

probabilite_changement(data_joueur_stats, data_joueur_predictions_buteurs)

