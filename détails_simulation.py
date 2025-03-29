import random
from buts_match_equipe import stats_Dans_Match
from fetch_premier_league_players_data import data_joueur_predictions_buteurs
import simpy

def match_process(env, home_team, away_team, prediction_buts_home, prediction_buts_away, HomePossesion, AwayPossesion,Hfouls,Afouls,HYellow,AYellow,HRed,ARed):
    minute = 0
    score_home = 0
    score_away = 0
    buteurs_home = []
    buteurs_away = []
    passeur_home = []
    passeur_away = []
    yellow_home = 0
    yellow_away = 0
    red_home = 0
    red_away = 0
    red_home_players = []
    red_away_players = []
    yellow_home_players = []
    yellow_away_players = []
    minutes_prises = set()
    minutes_intervalles = [(1, 15), (15, 30), (30, 45), (45, 60), (60, 75), (75, 90)]
    probabilites_minutes = [0.15,0.15,0.20,0.25,0.20,0.15]
    
    while minute < 90:
        yield env.timeout(1)  
        minute += 1
        totalFouls = Hfouls + Afouls
        totalPossesion = HomePossesion + AwayPossesion
        possession = random.choices([home_team, away_team], weights=[HomePossesion/totalPossesion,AwayPossesion/totalPossesion])[0]
        fautes = random.choices([home_team, away_team], weights=[Hfouls/(totalFouls),Afouls/totalFouls])[0]
        if fautes == home_team:
            if random.random() < HYellow/Hfouls and yellow_home < HYellow:
                yellow_home += 1
                Joueur_carton_jaune = stats_Dans_Match(data_joueur_predictions_buteurs,home_team,1,'CrdYAvg')
                a,b = random.choices(minutes_intervalles,weights=probabilites_minutes)[0]
                minutes_fautes = random.randint(a, b)
                yellow_home_players.append((Joueur_carton_jaune,minutes_fautes))
                
                
            if random.random() < HRed/Hfouls and red_home < ARed:
                red_home += 1
                Joueur_carton_rouge = stats_Dans_Match(data_joueur_predictions_buteurs,home_team,1,'CrdRAvg')
                a,b = random.choices(minutes_intervalles,weights=probabilites_minutes)[0]
                minutes_fautes = random.randint(a, b)
                red_home_players.append((Joueur_carton_rouge,minutes_fautes))
        else:
            if random.random() < AYellow/Afouls and yellow_away < AYellow:
                yellow_away += 1
                Joueur_carton_jaune = stats_Dans_Match(data_joueur_predictions_buteurs,away_team,1,'CrdYAvg')
                a,b = random.choices(minutes_intervalles,weights=probabilites_minutes)[0]
                minutes_fautes = random.randint(a, b)
                yellow_away_players.append((Joueur_carton_jaune,minutes_fautes))
                
            if random.random() < ARed/Afouls and red_away < ARed:
                red_away += 1
                Joueur_carton_rouge = stats_Dans_Match(data_joueur_predictions_buteurs,away_team,1,'CrdRAvg')
                a, b = random.choices(minutes_intervalles, weights=probabilites_minutes)[0]
                minutes_fautes = random.randint(a, b)
                red_away_players.append((Joueur_carton_rouge,minutes_fautes))
        
        if random.random() < 0.2:  
            if possession == home_team and score_home < prediction_buts_home:
                score_home += 1
                buteur = stats_Dans_Match(data_joueur_predictions_buteurs,home_team,1,'Gls_90')
                passeur = stats_Dans_Match(data_joueur_predictions_buteurs,home_team,1,'Ast_90')
                a, b = random.choices(minutes_intervalles, weights=probabilites_minutes, k=1)[0]
                minute_but = random.randint(a, b)
                minutes_prises.add(minute_but)

                while passeur == buteur:
                    passeur = stats_Dans_Match(data_joueur_predictions_buteurs, home_team, 1, 'Ast_90')
                buteurs_home.append((buteur, minute_but))
                passeur_home.append((passeur, minute_but))
            elif possession == away_team and score_away < prediction_buts_away:
                score_away += 1
                buteur = stats_Dans_Match(data_joueur_predictions_buteurs,away_team,1,'Gls_90')
                passeur = stats_Dans_Match(data_joueur_predictions_buteurs,away_team,1,'Ast_90')
                a, b = random.choices(minutes_intervalles, weights=probabilites_minutes, k=1)[0]
                minute_but = random.randint(a, b)
                minutes_prises.add(minute_but)
                while passeur == buteur:
                    passeur = stats_Dans_Match(data_joueur_predictions_buteurs, away_team, 1, 'Ast_90')
                buteurs_away.append((buteur, minute_but))
                passeur_away.append((passeur, minute_but))
    buteurs_home = sorted(buteurs_home,key =lambda x:x[1])
    buteurs_away = sorted(buteurs_away,key = lambda x:x[1])
    passeur_home = sorted(passeur_home,key = lambda x:x[1])
    passeur_away = sorted(passeur_away,key = lambda x:x[1])
    yellow_home_players = sorted(yellow_home_players, key = lambda x:x[1])
    yellow_away_players = sorted(yellow_away_players, key = lambda x:x[1])
    red_home_players = sorted(red_home_players, key = lambda x:x[1])
    red_away_players = sorted(red_away_players, key = lambda x:x[1])
    
    return buteurs_home, buteurs_away, passeur_home, passeur_away, yellow_home_players, yellow_away_players, red_home_players, red_away_players





def simulate_match(h_team, a_team, prediction_buts_domicile, prediction_buts_extérieur, home_possession, away_possession,Hfouls,Afouls,HYellow,AYellow,HRed,ARed):
    env = simpy.Environment()
    match_result = env.process(match_process(env, h_team, a_team, prediction_buts_domicile, prediction_buts_extérieur, home_possession, away_possession,Hfouls,Afouls,HYellow,AYellow,HRed,ARed))
    
    env.run()
    buteurs_home,buteurs_away,passeur_home, passeur_away, yellow_home_players, yellow_away_players, red_home_players, red_away_players   = match_result.value 

    return buteurs_home,buteurs_away,passeur_home,passeur_away, yellow_home_players, yellow_away_players, red_home_players, red_away_players 

#2 Ajout de carton jaunes sur les joueurs
#3 Ajoute de remplacant dans la simulation

