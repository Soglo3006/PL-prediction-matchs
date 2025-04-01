import random
from buts_match_equipe import stats_Joueur, changement_de_joueur
from fetch_premier_league_players_data import data_joueur_predictions_buteurs
import simpy

def match_process(env, home_team, away_team, prediction_buts_home, prediction_buts_away, HomePossesion, AwayPossesion,Hfouls,Afouls,HYellow,AYellow,HRed,ARed,data):
    minute = 0
    minutes_changement = 0
    score_home = 0
    score_away = 0
    home_team_liste = []
    away_team_liste = []
    home_team_liste.append(data[home_team])
    away_team_liste.append(data[away_team])
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
    probabilites_minutes_changement = [0.05,0.10,0.20]
    nb_remplacant_max = 3
    Joueur_remplacer = []
    
    while minute < 90:
        yield env.timeout(1)  
        minute += 1
        minutes_changement += 1
        totalFouls = Hfouls + Afouls
        totalPossesion = HomePossesion + AwayPossesion
        possession = random.choices([home_team, away_team], weights=[HomePossesion/totalPossesion,AwayPossesion/totalPossesion])[0]
        fautes = random.choices([home_team, away_team], weights=[Hfouls/(totalFouls),Afouls/totalFouls])[0]
        if minutes_changement> 45 and nb_remplacant_max >0:
            if random.random() < 0.07:
                SPlayer, home_team_liste = stats_Joueur(home_team_liste,'ProbOut','Starting11Players')
                BPlayer, home_team_liste = stats_Joueur(home_team_liste,'ProbFinal','BenchPlayers')
                resultat,updateteam  = changement_de_joueur(data,home_team,SPlayer,BPlayer)
                home_team_liste = updateteam
                resultat = resultat[0]['Player']
                #a,b = random.choices(minutes_intervalles[3:6],weights=probabilites_minutes_changement)[0]
                #minutes_changement = random.randint(a,b)
                Joueur_remplacer.append((resultat,minutes_changement))
                #print(home_team_liste)
                nb_remplacant_max -= 1
                #print(data_joueur_predictions_buteurs[home_team])
                

        if fautes == home_team:
            if random.random() < HYellow/Hfouls and yellow_home < HYellow:
                yellow_home += 1
                Joueur_carton_jaune,Home_team_liste = stats_Joueur(Home_team_liste,'CrdYAvg','Starting11Players')
                a,b = random.choices(minutes_intervalles,weights=probabilites_minutes)[0]
                minutes_fautes = random.randint(a, b)
                yellow_home_players.append((Joueur_carton_jaune,minute))
                
                
            if random.random() < HRed/Hfouls and red_home < ARed:
                red_home += 1
                Joueur_carton_rouge,home_team_liste = stats_Joueur(home_team_liste,'CrdRAvg','Starting11Players')
                a,b = random.choices(minutes_intervalles,weights=probabilites_minutes)[0]
                minutes_fautes = random.randint(a, b)
                red_home_players.append((Joueur_carton_rouge,minute))
        else:
            if random.random() < AYellow/Afouls and yellow_away < AYellow:
                yellow_away += 1
                Joueur_carton_jaune,away_team_liste = stats_Joueur(away_team_liste,'CrdYAvg','Starting11Players')
                a,b = random.choices(minutes_intervalles,weights=probabilites_minutes)[0]
                minutes_fautes = random.randint(a, b)
                yellow_away_players.append((Joueur_carton_jaune,minute))
                
            if random.random() < ARed/Afouls and red_away < ARed:
                red_away += 1
                Joueur_carton_rouge,away_team_liste = stats_Joueur(away_team_liste,'CrdRAvg','Starting11Players')
                a, b = random.choices(minutes_intervalles, weights=probabilites_minutes)[0]
                minutes_fautes = random.randint(a, b)
                red_away_players.append((Joueur_carton_rouge,minute))
        
        if random.random() < 0.2:  
            if possession == home_team and score_home < prediction_buts_home:
                score_home += 1
                print(score_home)
                print(home_team_liste)
                buteur,home_team_liste = stats_Joueur(home_team_liste,'Gls_90','Starting11Players')
                passeur,home_team_liste = stats_Joueur(home_team_liste,'Ast_90','Starting11Players')
                a, b = random.choices(minutes_intervalles, weights=probabilites_minutes, k=1)[0]
                minute_but = random.randint(a, b)
                minutes_prises.add(minute)
                while passeur == buteur:
                    passeur = passeur,home_team_liste = stats_Joueur(home_team_liste,'Ast_90','Starting11Players')
                buteurs_home.append((buteur, minute))
                passeur_home.append((passeur, minute))
            elif possession == away_team and score_away < prediction_buts_away:
                score_away += 1
                buteur,away_team_liste = stats_Joueur(away_team_liste,'Gls_90','Starting11Players')
                passeur,away_team_liste = stats_Joueur(away_team_liste,'Ast_90','Starting11Players')
                a, b = random.choices(minutes_intervalles, weights=probabilites_minutes, k=1)[0]
                minute_but = random.randint(a, b)
                minutes_prises.add(minute)
                while passeur == buteur:
                    passeur,away_team_liste = stats_Joueur(away_team_liste,'Ast_90','Starting11Players')
                buteurs_away.append((buteur, minute))
                passeur_away.append((passeur, minute))
    buteurs_home = sorted(buteurs_home,key =lambda x:x[1])
    buteurs_away = sorted(buteurs_away,key = lambda x:x[1])
    passeur_home = sorted(passeur_home,key = lambda x:x[1])
    passeur_away = sorted(passeur_away,key = lambda x:x[1])
    yellow_home_players = sorted(yellow_home_players, key = lambda x:x[1])
    yellow_away_players = sorted(yellow_away_players, key = lambda x:x[1])
    red_home_players = sorted(red_home_players, key = lambda x:x[1])
    red_away_players = sorted(red_away_players, key = lambda x:x[1])
    print(Joueur_remplacer)
    
    return buteurs_home, buteurs_away, passeur_home, passeur_away, yellow_home_players, yellow_away_players, red_home_players, red_away_players





def simulate_match(h_team, a_team, prediction_buts_domicile, prediction_buts_extérieur, home_possession, away_possession,Hfouls,Afouls,HYellow,AYellow,HRed,ARed,data):
    env = simpy.Environment()
    match_result = env.process(match_process(env, h_team, a_team, prediction_buts_domicile, prediction_buts_extérieur, home_possession, away_possession,Hfouls,Afouls,HYellow,AYellow,HRed,ARed,data))
    
    env.run()
    buteurs_home,buteurs_away,passeur_home, passeur_away, yellow_home_players, yellow_away_players, red_home_players, red_away_players   = match_result.value 

    return buteurs_home,buteurs_away,passeur_home,passeur_away, yellow_home_players, yellow_away_players, red_home_players, red_away_players 

#3 Ajoute de remplacant dans la simulation (#Arranger les minutes dans la fonction pour la simulation)


print(simulate_match('Manchester City','Wolves',3,0,60,40,6,13,0,1,0,0,data_joueur_predictions_buteurs))

