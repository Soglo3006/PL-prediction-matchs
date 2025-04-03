import random
from stats_et_changements import stats_joueur, changement_de_joueur
from fetch_premier_league_players_data import data_joueur_predictions_buteurs

def minutes_stats(stats,probabilites,intervale_x,intervale_y,liste):
    minutes_intervalles = [(1, 15), (15, 30), (30, 45), (45, 60), (60, 75), (75, 90)]
    for _ in range(stats):
        a,b = random.choices(minutes_intervalles[intervale_x:intervale_y],weights= probabilites)[0]
        liste.append(random.randint(a,b))
    return liste

def match_process(prediction_buts_team, team_liste,cartons_jaunes_team,cartons_rouges_team,remplacant_nb,team,
                  buteur_team,passeur_team,yellow_team,red_team,Joueur_remplacer_team,Joueur_rentre_team, minutes_buts, minutes_changement, minutes_fautes_cartons_jaunes,
                  minutes_fautes_carton_rouge,minutes_stats):
    for i in minutes_stats:
        for j in minutes_buts:
            if i == j and len(buteur_team) < prediction_buts_team:
                buteur,team_liste = stats_joueur(team_liste,'Gls_90','Starting11Players')
                passeur,team_liste = stats_joueur(team_liste,'Ast_90','Starting11Players')
                while passeur == buteur:
                    passeur = passeur,team_liste = stats_joueur(team_liste,'Ast_90','Starting11Players')
                buteur_team.append((buteur, i))
                passeur_team.append((passeur, i))
        for z in minutes_fautes_cartons_jaunes: 
            if i == z and len(yellow_team) < cartons_jaunes_team:
                joueur_carton_jaune,team_liste = stats_joueur(team_liste,'CrdYAvg','Starting11Players')
                yellow_team.append((joueur_carton_jaune,z))
                
        for l in minutes_fautes_carton_rouge :
            if i == l and len(red_team) < cartons_rouges_team :
                joueur_carton_rouge,team_liste = stats_joueur(team_liste,'CrdRPro','Starting11Players')
                red_team.append((joueur_carton_rouge,l))
                print(team_liste)
        for k in minutes_changement:
            if i == k and len(Joueur_remplacer_team) < remplacant_nb :
                starting_player, team_liste = stats_joueur(team_liste,'ProbOut','Starting11Players')
                bench_player, team_liste = stats_joueur(team_liste,'ProbFinal','BenchPlayers')
                resultat,updateteam  = changement_de_joueur(data_joueur_predictions_buteurs,team,starting_player,bench_player)
                team_liste = updateteam
                resultat = resultat[0]['Player']
                Joueur_remplacer_team.append((starting_player,k))
                Joueur_rentre_team.append((bench_player,k))
    return buteur_team, passeur_team, yellow_team, red_team, Joueur_remplacer_team, Joueur_rentre_team

def simulate_match(home_team,away_team,prediction_buts_domicile, prediction_buts_exterieur,home_yellow,away_yellow,home_red,away_red):
    home_team_liste = []
    away_team_liste = []
    buteurs_home = []
    buteurs_away = []
    passeur_home = []
    passeur_away = []
    red_home_players = []
    red_away_players = []
    yellow_home_players = []
    yellow_away_players = []
    joueur_remplacer_home = []
    joueur_rentre_home = []
    joueur_remplacer_away = []
    joueur_rentre_away = []
    nb_remplacant_max = 2
    probabilites_minutes = [0.15,0.15,0.20,0.25,0.20,0.15]
    probabilites_minutes_changement = [0.05,0.10,0.20]
    carton_jaunes_home = home_yellow
    carton_rouges_home = home_red
    carton_jaunes_away = away_yellow
    carton_rouges_away = away_red
    home_team_liste.append(data_joueur_predictions_buteurs[home_team])
    away_team_liste.append(data_joueur_predictions_buteurs[away_team])

    minutes_buts_home = []
    minutes_changement_home = []
    minutes_stats_home = []
    minutes_fautes_cartons_jaunes_home = []
    minutes_fautes_cartons_rouges_home = []

    minutes_buts_away = []
    minutes_changement_away = []
    minutes_stats_away = []
    minutes_fautes_cartons_jaunes_away = []
    minutes_fautes_cartons_rouges_away = []

    minutes_buts_home = minutes_stats(prediction_buts_domicile,probabilites_minutes,0,6,minutes_buts_home)
    minutes_changement_home = minutes_stats(nb_remplacant_max,probabilites_minutes_changement,3,6,minutes_changement_home)
    minutes_fautes_cartons_jaunes_home = minutes_stats(carton_jaunes_home,probabilites_minutes,0,6,minutes_fautes_cartons_jaunes_home)
    minutes_fautes_cartons_rouges_home = minutes_stats(carton_rouges_home,probabilites_minutes,0,6,minutes_fautes_cartons_rouges_home)

    minutes_buts_away = minutes_stats(prediction_buts_exterieur,probabilites_minutes,0,6,minutes_buts_away)
    minutes_changement_away = minutes_stats(nb_remplacant_max,probabilites_minutes_changement,3,6,minutes_changement_away)
    minutes_fautes_cartons_jaunes_away = minutes_stats(carton_jaunes_away,probabilites_minutes,0,6,minutes_fautes_cartons_jaunes_away)
    minutes_fautes_cartons_rouges_away = minutes_stats(carton_rouges_away,probabilites_minutes,0,6,minutes_fautes_cartons_rouges_away)

    minutes_stats_home = sorted(set(minutes_buts_home + minutes_changement_home + minutes_fautes_cartons_jaunes_home + minutes_fautes_cartons_rouges_home))
    minutes_stats_away = sorted(set(minutes_buts_away + minutes_changement_away + minutes_fautes_cartons_jaunes_away + minutes_fautes_cartons_rouges_away))

    buteurs_home, passeur_home,yellow_home,red_home,joueur_remplacer_home,joueur_rentre_home = (match_process(prediction_buts_domicile,home_team_liste,carton_jaunes_home,carton_rouges_home,nb_remplacant_max,
                    home_team,buteurs_home,passeur_home,yellow_home_players,red_home_players,joueur_remplacer_home,joueur_rentre_home,
                    minutes_buts_home, minutes_changement_home, minutes_fautes_cartons_jaunes_home,
                    minutes_fautes_cartons_rouges_home,minutes_stats_home))
    
    buteurs_away, passeur_away , yellow_away, red_away, joueur_remplacer_away, joueur_rentre_away = (match_process(prediction_buts_exterieur,away_team_liste,carton_jaunes_away,carton_rouges_away,nb_remplacant_max,
                    away_team,buteurs_away,passeur_away,yellow_away_players,red_away_players,joueur_remplacer_away,joueur_rentre_away,
                    minutes_buts_away,minutes_changement_away,minutes_fautes_cartons_jaunes_away,minutes_fautes_cartons_rouges_away,minutes_stats_away))
    
    return buteurs_home, buteurs_away , passeur_home , passeur_away , yellow_home, yellow_away, red_home, red_away, joueur_remplacer_home, joueur_remplacer_away, joueur_rentre_home, joueur_rentre_away
    
