import random
from buts_match_equipe import buteurs_Dans_Match
from fetch_premier_league_players_data import data_joueur_predictions_buteurs

def match_process(env, home_team, away_team, prediction_buts_home, prediction_buts_away):
    minute = 0
    score_home = 0
    score_away = 0
    buteurs_home = []
    buteurs_away = []
    minutes_prises = set()
    minutes_intervalles = [(1, 15), (15, 30), (30, 45), (45, 60), (60, 75), (75, 90)]
    probabilites_minutes = [0.15,0.15,0.20,0.25,0.20,0.15]
    
    while minute < 90:
        yield env.timeout(1)  
        minute += 1
        possession = random.choices([home_team, away_team], weights=[0.65, 0.35])[0]
        if random.random() < 0.2:  
            if possession == home_team and score_home < prediction_buts_home:
                score_home += 1
                buteur = buteurs_Dans_Match(data_joueur_predictions_buteurs,home_team,1)
                while True:
                    a, b = random.choices(minutes_intervalles, weights=probabilites_minutes)[0]
                    minute_but = random.randint(a, b)
                    minutes_prises.add(minute_but)
                    break  
                buteurs_home.append((buteur, minute_but))
            elif possession == away_team and score_away < prediction_buts_away:
                score_away += 1
                buteur = buteurs_Dans_Match(data_joueur_predictions_buteurs,away_team,1)
                while True:
                    a, b = random.choices(minutes_intervalles, weights=probabilites_minutes)[0]
                    minute_but = random.randint(a, b)
                    minutes_prises.add(minute_but)
                    break 
                buteurs_away.append((buteur, minute_but))
    buteurs_home = sorted(buteurs_home,key =lambda x:x[1])
    buteurs_away = sorted(buteurs_away,key = lambda x:x[1])
    return buteurs_home, buteurs_away
