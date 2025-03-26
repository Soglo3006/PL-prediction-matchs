import random
from buts_match_equipe import stats_Dans_Match
from fetch_premier_league_players_data import data_joueur_predictions_buteurs
import simpy

def match_process(env, home_team, away_team, prediction_buts_home, prediction_buts_away, HomePossesion, AwayPossesion):
    minute = 0
    score_home = 0
    score_away = 0
    buteurs_home = []
    buteurs_away = []
    passeur_home = []
    passeur_away = []
    minutes_prises = set()
    minutes_intervalles = [(1, 15), (15, 30), (30, 45), (45, 60), (60, 75), (75, 90)]
    probabilites_minutes = [0.15,0.15,0.20,0.25,0.20,0.15]
    
    while minute < 90:
        yield env.timeout(1)  
        minute += 1
        possession = random.choices([home_team, away_team], weights=[HomePossesion/100,AwayPossesion/100])[0]
        if random.random() < 0.2:  
            if possession == home_team and score_home < prediction_buts_home:
                score_home += 1
                buteur = stats_Dans_Match(data_joueur_predictions_buteurs,home_team,1,'Gls_90')
                passeur = stats_Dans_Match(data_joueur_predictions_buteurs,home_team,1,'Ast_90')
                while True:
                    a, b = random.choices(minutes_intervalles, weights=probabilites_minutes)[0]
                    minute_but = random.randint(a, b)
                    minutes_prises.add(minute_but)
                    break  
                buteurs_home.append((buteur, minute_but))
                passeur_home.append((passeur, minute_but))
            elif possession == away_team and score_away < prediction_buts_away:
                score_away += 1
                buteur = stats_Dans_Match(data_joueur_predictions_buteurs,away_team,1,'Gls_90')
                passeur = stats_Dans_Match(data_joueur_predictions_buteurs,away_team,1,'Ast_90')
                while True:
                    a, b = random.choices(minutes_intervalles, weights=probabilites_minutes)[0]
                    minute_but = random.randint(a, b)
                    minutes_prises.add(minute_but)
                    break 
                buteurs_away.append((buteur, minute_but))
                passeur_away.append((passeur, minute_but))
    buteurs_home = sorted(buteurs_home,key =lambda x:x[1])
    buteurs_away = sorted(buteurs_away,key = lambda x:x[1])
    passeur_home = sorted(passeur_home,key = lambda x:x[1])
    passeur_away = sorted(passeur_away,key = lambda x:x[1])
    return buteurs_home, buteurs_away, passeur_home, passeur_away


def simulate_match(h_team, a_team, prediction_buts_domicile, prediction_buts_extérieur, home_possession, away_possession):
    env = simpy.Environment()
    match_result = env.process(match_process(env, h_team, a_team, prediction_buts_domicile, prediction_buts_extérieur, home_possession, away_possession))
    
    env.run()
    buteurs_home,buteurs_away,passeur_home, passeur_away = match_result.value 

    return buteurs_home,buteurs_away,passeur_home,passeur_away

#2 Ajout de carton jaunes sur les joueurs
#3 Ajoute de remplacant dans la simulation