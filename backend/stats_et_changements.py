import random 
from fetch_premier_league_players_data import data_joueur_predictions_buteurs

def select_event_player(team_list, col, players_col):
    joueur_team = []

    starting_players = team_list[0][players_col]
    joueur_team = starting_players.sort_values(col, ascending=False)
    players_list = joueur_team.to_dict('records')

    list_weight = [float(player[col]) for player in players_list]

    if sum(list_weight) == 0:
        list_weight = [1.0] * len(players_list)

    joueur = random.choices(players_list, weights=list_weight, k=1)
    joueur = joueur[0]['Player']
    team_list[0][players_col] = joueur_team
    
    if col == 'CrdRPro':
        for index in range(len(team_list[0][players_col])):
            if team_list[0][players_col].loc[index, 'Player'] == joueur:
                team_list[0][players_col].drop(index, inplace=True)
                team_list[0][players_col].reset_index(drop=True, inplace=True)
                break
    if col == 'CrdYAvg':
        for index in range(len(team_list[0][players_col])):
            if team_list[0][players_col].loc[index, 'Player'] == joueur:
                team_list[0][players_col].loc[index,'CrdYAvg'] = 0.01
                team_list[0][players_col].reset_index(drop=True, inplace=True)
                break

    return joueur, team_list

def changement_de_joueur(data, team, starter_player, bench_player):
    team_liste = []
    joueur_change = []
    
    starter_player_name = starter_player if isinstance(starter_player, str) else list(starter_player.keys())[0]
    bench_player_name = bench_player if isinstance(bench_player, str) else list(bench_player.keys())[0]
    
    for starters in range(len(data[team]['Starting11Players'])):
        if data[team]['Starting11Players'].loc[starters, 'Player'] == starter_player_name:
            for backups in range(len(data[team]['BenchPlayers'])):
                if data[team]['BenchPlayers'].loc[backups, 'Player'] == bench_player_name:
                    joueur_change.append(data[team]['Starting11Players'].loc[starters].copy())
                    data[team]['Starting11Players'].loc[starters] = data[team]['BenchPlayers'].loc[backups].copy()
                    data[team]['Starting11Players'].loc[starters, 'ProbOut'] = 0.0
                    data[team]['BenchPlayers'] = data[team]['BenchPlayers'].drop(backups)
                    break

    data[team]['Starting11Players'].reset_index(drop=True, inplace=True)
    data[team]['BenchPlayers'].reset_index(drop=True, inplace=True)

    team_liste.append({
        'Starting11Players': data[team]['Starting11Players'],
        'BenchPlayers': data[team]['BenchPlayers']
    })
    
    return joueur_change, team_liste

