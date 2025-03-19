import pandas as pd

data_joueur_stats = pd.read_csv('premier-player-23-24.csv')

for i in range(len(data_joueur_stats)):
    data_joueur_stats.loc[i,'Team'] = data_joueur_stats.loc[i,'Team'].strip()

for i in range(len(data_joueur_stats)):
    data_joueur_stats.loc[i,'GoalsPerGames'] = round(data_joueur_stats.loc[i,'Gls']/data_joueur_stats.loc[i,'MP'],2)

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

top_scorers = find_top_scorer(penalty_taker(data_joueur_stats))

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
            
valeur_takers(data_joueur_stats)

def data_team_effectif(data):
    Starting11EachTeam  = {}
    BenchPlayers = {}
    dataJoueur = {}
    for i in data['Team'].unique():
        Starting11EachTeam[i] = data[data['Team']==i].sort_values(by = ['Starts'], ascending =False).head(11)
        BenchPlayers[i] = data[data['Team'] == i ].sort_values(by = ['Starts'], ascending =False).tail(len(data[data['Team'] == i ])- len(Starting11EachTeam[i]))

    features_players = ['Player','Team','Pos','Gls','Ast','PkTaker','FKTaker','Gls_90','npxG','xG_90']
    for i in data['Team'].unique():
        dataJoueur[i] = {
            'Starting11Players' : Starting11EachTeam[i][features_players],
            'BenchPlayers' : BenchPlayers[i][features_players]
        }
    return dataJoueur

print(data_team_effectif(data_joueur_stats))
#data_joueur_predictions_buteurs = data_joueur_stats[features_players]