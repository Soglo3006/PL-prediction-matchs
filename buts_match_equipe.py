import random 
from fetch_premier_league_players_data import data_joueur_predictions_buteurs
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

