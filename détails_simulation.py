import simpy
import random
from buts_match_equipe import buteurs_Dans_Match
from fetch_premier_league_players_data import data_joueur_predictions_buteurs



def match_process(env, home_team, away_team, prediction_buts_home, prediction_buts_away):
    # Initialisation des variables
    minute = 0
    score_home = 0
    score_away = 0
    buteurs_home = []
    buteurs_away = []
    minutes_prises = set()
    minutes_intervalles = [(1, 15), (15, 30), (30, 45), (45, 60), (60, 75), (75, 90)]
    probabilites_minutes = [0.15,0.15,0.20,0.25,0.20,0.15]
    
    while minute < 90:
        yield env.timeout(1)  # Fait avancer le temps de 1 minute
        minute += 1

        # Possession aléatoire basée sur les forces des équipes
        possession = random.choices([home_team, away_team], weights=[0.55, 0.45])[0]

        # Une attaque a lieu cette minute ?
        if random.random() < 0.2:  # Probabilité d'une attaque
            if possession == home_team and score_home < prediction_buts_home:
                score_home += 1
                buteur = buteurs_Dans_Match(data_joueur_predictions_buteurs,home_team,1)

                # Trouver une minute unique
                while True:
                    a, b = random.choices(minutes_intervalles, weights=probabilites_minutes)[0]
                    minute_but = random.randint(a, b)
                    minutes_prises.add(minute_but)
                    break  # On a trouvé une minute unique

                buteurs_home.append((buteur, minute_but))

            elif possession == away_team and score_away < prediction_buts_away:
                score_away += 1
                buteur = buteurs_Dans_Match(data_joueur_predictions_buteurs,away_team,1)

                # Trouver une minute unique
                while True:
                    a, b = random.choices(minutes_intervalles, weights=probabilites_minutes)[0]
                    minute_but = random.randint(a, b)
                    minutes_prises.add(minute_but)
                    break  # On a trouvé une minute unique

                buteurs_away.append((buteur, minute_but))    
    return score_home, score_away, buteurs_home, buteurs_away


home_team = "Manchester City"
away_team = "Luton"
prediction_buts_home = 4  
prediction_buts_away = 1  


env = simpy.Environment()


match_result = env.process(match_process(env, home_team, away_team, prediction_buts_home, prediction_buts_away))

env.run()


score_home, score_away, buteurs_home, buteurs_away = match_result.value

print(f"\n🔵 {home_team} {score_home} - {score_away} {away_team} 🔴")
print(f"⚽ Buteurs {home_team}: {buteurs_home}")
print(f"⚽ Buteurs {away_team}: {buteurs_away}")

possession = random.choices([home_team, away_team], weights=[0.55, 0.45])[0]
print(possession)