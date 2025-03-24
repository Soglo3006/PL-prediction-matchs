import pandas as pd

data_2324 = pd.read_csv('season-2324.csv')
match_2324 = pd.read_csv('matches-23-24.csv')

def moyenne_stats(data,h_team,a_team,h_categore,a_categorie,h_newCol,a_newCol ):
    equipe = {}
    for i in data[h_team].unique():
        equipe[i] = 0 
        equipe = dict(sorted(equipe.items()))
    for y in range(len(data)):
        for j in equipe:
            if data.loc[y,h_team] == j :
                equipe[j] += int(data.loc[y,h_categore])
            elif data.loc[y,a_team] == j:
                equipe[j] += int(data.loc[y,a_categorie])
    for k in equipe:
        equipe[k] = round(equipe[k]/38,2)
    for z in range(len(data)):
        for a in equipe:
            if a == data.loc[z,h_team]:
                data.loc[z,h_newCol] = equipe[a]
            elif a == data.loc[z,a_team]:
                data.loc[z,a_newCol] = equipe[a]
    return equipe

def calculate_form(data, team_col, result_col, new_col):
    form_list = []
    for i in range(len(data)):
        team = data.loc[i, team_col]
        past_matches = data.loc[:i-1]
        team_matches = past_matches[past_matches[team_col] == team]
        
        form_score = 0
        if len(team_matches) > 0:
            last_five = team_matches.tail(5)
            for result in last_five[result_col]:
                if result == 'H':
                    form_score += 1
                elif result == 'A':
                    form_score -= 1
        
        form_list.append(form_score)
    
    data[new_col] = form_list
    return data

def avantageDomicile(data):
    Équipe_victoires_domicile = {}
    for i in data['HomeTeam'].unique():
        Équipe_victoires_domicile[i] = 0
    for y in range(len(data)):
        if data.loc[y,'FullTimeResult'] == 'H':
            Équipe_victoires_domicile[data.loc[y,'HomeTeam']] += 1
    for j in Équipe_victoires_domicile:
        Équipe_victoires_domicile[j] = round(Équipe_victoires_domicile[j]/19,2)
    porucentage_victoire = dict(sorted(Équipe_victoires_domicile.items()))
    for i in range(len(data)):
        if porucentage_victoire[data.loc[i,'HomeTeam']] > porucentage_victoire[data_2324.loc[i,'AwayTeam']]:
            data.loc[i,'home_advantage'] = 1
        else:
            data.loc[i,'home_advantage'] = 0


def moyenne_stats_buts(data,équipe,but,newCol):
    statsEquipe = {}
    for i in data[équipe].unique():
        statsEquipe[i] = 0
        statsEquipe = dict(sorted(statsEquipe.items()))
    for y in range(len(data)):
        for j in statsEquipe:
            if data.loc[y,équipe] == j:
                statsEquipe[j] += int(data.loc[y,but])
    for moy in statsEquipe:
        statsEquipe[moy] = round(statsEquipe[moy]/19,2)
    for k in range(len(data)):
        for nom_équipe in statsEquipe:
            if nom_équipe == data.loc[k,équipe]:
                data.loc[k,newCol] = statsEquipe[nom_équipe]
    return statsEquipe
def difference_buts(data, moyenne_dom, moyenne_ext, newCol, newCol2):
    dom = moyenne_dom
    ext = moyenne_ext
    for i in range(len(data)):
        if dom[data.loc[i,'HomeTeam']]> ext[data.loc[i,'AwayTeam']] : 
            data.loc[i,newCol] = dom[data.loc[i,'HomeTeam']] - ext[data.loc[i,'AwayTeam']]
            data.loc[i,newCol2] = data.loc[i,'HomeTeam']
        else:
            data.loc[i,newCol] = ext[data.loc[i,'AwayTeam']] - dom[data.loc[i,'HomeTeam']]
            data.loc[i,newCol2] = data.loc[i,'AwayTeam']
                

#data_2324 = moyenne_Stats(data_2324, 'HomeTeam','HYellow', 'Home_avgYellow')
#data_2324 = moyenne_Stats(data_2324, 'AwayTeam','AYellow', 'Away_avgYellow')
#data_2324 = moyenne_Stats(data_2324, 'HomeTeam','HRed', 'Home_avgRed')
#data_2324 = moyenne_Stats(data_2324, 'AwayTeam','ARed', 'Away_avgRed')
#data_2324 = moyenne_Stats(data_2324, 'HomeTeam','HFouls','Home_avgFouls')
#data_2324 = moyenne_Stats(data_2324, 'AwayTeam','AFouls','Away_avgFouls')
moyenne_stats(data_2324,'HomeTeam','AwayTeam','HomeGoal','AwayGoal','Home_avgGoal','Away_avgGoal')
moyenne_stats(data_2324,'HomeTeam','AwayTeam','HomeShots','AwayShots','Home_avgShot','Away_avgShot')
moyenne_stats(data_2324,'HomeTeam','AwayTeam','HomeShotTarget','AwayShotTarget','Home_avgShot_Target','Away_avgShot_Target')
moyenne_stats(data_2324,'HomeTeam','AwayTeam','HCorners','ACorners','Home_avgCorner','Away_avgCorner')

data_2324 = calculate_form(data_2324, 'HomeTeam', 'FullTimeResult', 'home_form')
data_2324 = calculate_form(data_2324, 'AwayTeam', 'FullTimeResult', 'away_form')

moyenne_dom_but = moyenne_stats_buts(data_2324,'HomeTeam','HomeGoal','moyenne_domcile_buts')
moyenne_ext_but = moyenne_stats_buts(data_2324,'AwayTeam','AwayGoal','moyenne_exterieur_buts')
moyenne_con_but_dom = moyenne_stats_buts(data_2324,'HomeTeam','AwayGoal','moyenne_conceder_dom')
moyenne_con_but_ext = moyenne_stats_buts(data_2324,'AwayTeam','HomeGoal','moyenne_conceder_ext')



def changerDate(data):
    for i in range(len(data)):
        date = data.loc[i, 'Date']
        annee = date[2:4] 
        mois = date[5:7]  
        jour = date[8:10]  

        data.loc[i, 'Date'] = f"{jour}/{mois}/{annee}"

    data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%y')

    data = data.sort_values(by='Date').reset_index(drop=True)

    data['Date'] = data['Date'].dt.strftime('%d/%m/%y')

changerDate(match_2324)

def modifierNom(data):
    for j in data['Opponent'].unique():
        if j == 'Luton Town':
            data.loc[data['Opponent'] == j, 'Opponent'] = 'Luton'
        elif j == 'Newcastle Utd':
            data.loc[data['Opponent'] == j, 'Opponent'] = 'Newcastle'
        elif j == 'Sheffield Utd':
            data.loc[data['Opponent'] == j, 'Opponent'] = 'Sheffield United'
        elif j == 'Manchester Utd':
            data.loc[data['Opponent'] == j, 'Opponent'] = 'Manchester United'
        elif j == "Nott'ham Forest":
            data.loc[data['Opponent'] == j, 'Opponent'] = 'Nottingham Forest'
            
modifierNom(match_2324)
        
for k in range (len(match_2324)):
    for h in range(len(data_2324)):
        if match_2324.loc[k,'Date'] == data_2324.loc[h,'Date']:
            if match_2324.loc[k,'Opponent'] == data_2324.loc[h,'HomeTeam']:
                data_2324.loc[h,'AwayPossesion'] = 100-match_2324.loc[k,'Poss']
                data_2324.loc[h,'HomePossesion'] = 100 - data_2324.loc[h,'AwayPossesion']

print(data_2324[0:21])
