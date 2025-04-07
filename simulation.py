import random
from stats_et_changements import select_event_player, changement_de_joueur
from fetch_premier_league_players_data import data_joueur_predictions_buteurs

def minutes_stats(stats,probabilites,intervale_x,intervale_y):
    minutes_intervalles = [(1, 15), (15, 30), (30, 45), (45, 60), (60, 75), (75, 90)]
    minutes_stats = set()
    for _ in range(stats):
        a,b = random.choices(minutes_intervalles[intervale_x:intervale_y],weights= probabilites)[0]
        minutes_stats.add(random.randint(a,b))
        
    return minutes_stats

def process_goal(minute, buteur_team, passeur_team, prediction_buts_team, team_liste):
    if len(buteur_team) < prediction_buts_team:
        buteur, team_liste = select_event_player(team_liste, 'Gls_90', 'Starting11Players')
        passeur, team_liste = select_event_player(team_liste, 'Ast_90', 'Starting11Players')
        while passeur == buteur:
            passeur, team_liste = select_event_player(team_liste, 'Ast_90', 'Starting11Players')
        buteur_team.append((buteur, minute))
        passeur_team.append((passeur, minute))
    return buteur_team, passeur_team, team_liste

def process_yellow_card(minute, yellow_team_players, cartons_jaunes_team, team_liste):
    if len(yellow_team_players) < cartons_jaunes_team:
        joueur, team_liste = select_event_player(team_liste, 'CrdYAvg', 'Starting11Players')
        yellow_team_players.append((joueur, minute))
    return yellow_team_players, team_liste

def process_red_card(minute, red_team_players, cartons_rouges_team, team_liste):
    if len(red_team_players) < cartons_rouges_team:
        joueur, team_liste = select_event_player(team_liste, 'CrdRPro', 'Starting11Players')
        red_team_players.append((joueur, minute))
    return red_team_players, team_liste

def process_substitution(minute, joueur_remplacer_team, remplacant_nb, team_liste, team, joueur_rentre_team):
    if len(joueur_remplacer_team) < remplacant_nb:
        starting_player, team_liste = select_event_player(team_liste, 'ProbOut', 'Starting11Players')
        bench_player, team_liste = select_event_player(team_liste, 'ProbFinal', 'BenchPlayers')
        resultat, updated_team = changement_de_joueur(data_joueur_predictions_buteurs, team, starting_player, bench_player)
        team_liste = updated_team
        resultat = resultat[0]['Player']
        joueur_remplacer_team.append((starting_player, minute))
        joueur_rentre_team.append((bench_player, minute))
    return joueur_remplacer_team, joueur_rentre_team, team_liste


def match_process(prediction_buts_team, team_liste,cartons_jaunes_team,cartons_rouges_team,remplacant_nb,team,
                  buteur_team,passeur_team,minutes_buts, minutes_changements, minutes_fautes_cartons_jaunes,
                  minutes_fautes_carton_rouge,minutes_stats_team):
    
    yellow_team_players = []
    red_team_players = []
    joueur_remplacer_team = []
    joueur_rentre_team = []
    
    for minute_match in minutes_stats_team:
        for minute_but in minutes_buts:
            if minute_match == minute_but :
                buteur_team, passeur_team, team_liste = process_goal(minute_match, buteur_team, passeur_team, prediction_buts_team, team_liste)

        for minute_carton_jaune in minutes_fautes_cartons_jaunes: 
            if minute_match == minute_carton_jaune:
                yellow_team_players, team_liste = process_yellow_card(minute_match, yellow_team_players, cartons_jaunes_team, team_liste)


        for minute_carton_rouge in minutes_fautes_carton_rouge :
            if minute_match == minute_carton_rouge:
                red_team_players, team_liste = process_red_card(minute_match, red_team_players, cartons_rouges_team, team_liste)


        for minute_changement in minutes_changements:
            if minute_match == minute_changement:
                joueur_remplacer_team, joueur_rentre_team, team_liste = process_substitution(minute_match, joueur_remplacer_team, remplacant_nb, team_liste, team, joueur_rentre_team)


    return buteur_team, passeur_team, yellow_team_players, red_team_players, joueur_remplacer_team, joueur_rentre_team

def simulate_match(team,prediction_buts_team,team_yellow,team_red):
    team_liste = []
    buteurs_team = []
    passeur_team = []
    nb_remplacant_max_team = random.randint(0,4)
    probabilites_minutes = [0.15,0.15,0.20,0.25,0.20,0.15]
    probabilites_minutes_changement = [0.05,0.10,0.20]
    carton_jaunes_team = team_yellow
    carton_rouges_team = team_red
    team_liste.append(data_joueur_predictions_buteurs[team])

    minutes_buts_team = []
    minutes_changement_team = []
    minutes_stats_team = []
    minutes_fautes_cartons_jaunes_team = []
    minutes_fautes_cartons_rouges_team = []

    minutes_buts_team = minutes_stats(prediction_buts_team,probabilites_minutes,0,6)
    minutes_changement_team = minutes_stats(nb_remplacant_max_team,probabilites_minutes_changement,3,6)
    minutes_fautes_cartons_jaunes_team = minutes_stats(carton_jaunes_team,probabilites_minutes,0,6)
    minutes_fautes_cartons_rouges_team = minutes_stats(carton_rouges_team,probabilites_minutes,0,6)

    minutes_stats_team = sorted(set(minutes_buts_team | minutes_changement_team | minutes_fautes_cartons_jaunes_team | minutes_fautes_cartons_rouges_team))

    buteurs_team, passeur_team,yellow_team,red_team,joueur_remplacer_team,joueur_rentre_team = (match_process(prediction_buts_team,team_liste,carton_jaunes_team,carton_rouges_team,nb_remplacant_max_team,
                    team,buteurs_team,passeur_team,minutes_buts_team, minutes_changement_team, minutes_fautes_cartons_jaunes_team,
                    minutes_fautes_cartons_rouges_team,minutes_stats_team))
    
    return buteurs_team, passeur_team,yellow_team,red_team,joueur_remplacer_team,joueur_rentre_team
    
