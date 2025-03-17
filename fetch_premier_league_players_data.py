import pandas as pd

data_joueur_stats = pd.read_csv('premier-player-23-24.csv')

for i in range(len(data_joueur_stats)):
    data_joueur_stats.loc[i,'GoalsPerGames'] = round(data_joueur_stats.loc[i,'Gls']/data_joueur_stats.loc[i,'MP'],2)
    
TakersPerTeam = {}

for i in data_joueur_stats['Team'].unique():
    TakersPerTeam[i] ={'Pénalty':[]}
    
#print(TakersPerTeam)
    
for j in range(len(data_joueur_stats)):
    for k in TakersPerTeam:
        if data_joueur_stats.loc[j,'Team'] ==k:
            if data_joueur_stats.loc[j,'PKatt'] > 0:
                penalty_goals = data_joueur_stats.loc[j, 'PK']
                player_name = data_joueur_stats.loc[j, 'Player']
                TakersPerTeam[k]['Pénalty'].append({player_name: int(penalty_goals)})

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

top_scorers = find_top_scorer(TakersPerTeam)

print(top_scorers)

#print(data_joueur_stats)