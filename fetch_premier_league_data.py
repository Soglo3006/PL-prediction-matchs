import pandas as pd

data_2324 = pd.read_csv('fichier csv/season-2324.csv')
match_2324 = pd.read_csv('fichier csv/matches-23-24.csv')

def moyenne_stats(data,h_team,a_team,h_categore,a_categorie,home_new_col,away_new_col):
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
                data.loc[z,home_new_col] = equipe[a]
            elif a == data.loc[z,a_team]:
                data.loc[z,away_new_col] = equipe[a]
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

def avantage_domicile(data):
    equipe_victoires_domicile = {}
    for i in data['HomeTeam'].unique():
        equipe_victoires_domicile[i] = 0
    for y in range(len(data)):
        if data.loc[y,'FullTimeResult'] == 'H':
            equipe_victoires_domicile[data.loc[y,'HomeTeam']] += 1
    for j in equipe_victoires_domicile:
        equipe_victoires_domicile[j] = round(equipe_victoires_domicile[j]/19,2)
    porucentage_victoire = dict(sorted(equipe_victoires_domicile.items()))
    for i in range(len(data)):
        if porucentage_victoire[data.loc[i,'HomeTeam']] > porucentage_victoire[data_2324.loc[i,'AwayTeam']]:
            data.loc[i,'home_advantage'] = 1
        else:
            data.loc[i,'home_advantage'] = 0


def moyenne_stats_buts(data,equipe,but,new_col):
    stats_equipe = {}
    for i in data[equipe].unique():
        stats_equipe[i] = 0
        stats_equipe = dict(sorted(stats_equipe.items()))
    for y in range(len(data)):
        for j in stats_equipe:
            if data.loc[y,equipe] == j:
                stats_equipe[j] += int(data.loc[y,but])
    for moy in stats_equipe:
        stats_equipe[moy] = round(stats_equipe[moy]/19,2)
    for k in range(len(data)):
        for nom_equipe in stats_equipe:
            if nom_equipe == data.loc[k,equipe]:
                data.loc[k,new_col] = stats_equipe[nom_equipe]
    return stats_equipe
def difference_buts(data, moyenne_dom, moyenne_ext, new_col, new_col2):
    dom = moyenne_dom
    ext = moyenne_ext
    for i in range(len(data)):
        if dom[data.loc[i,'HomeTeam']]> ext[data.loc[i,'AwayTeam']] : 
            data.loc[i,new_col] = dom[data.loc[i,'HomeTeam']] - ext[data.loc[i,'AwayTeam']]
            data.loc[i,new_col2] = data.loc[i,'HomeTeam']
        else:
            data.loc[i,new_col] = ext[data.loc[i,'AwayTeam']] - dom[data.loc[i,'HomeTeam']]
            data.loc[i,new_col2] = data.loc[i,'AwayTeam']

def format_date(match_df):
    for i in range(len(match_df)):
        date = match_df.loc[i, 'Date']
        annee = date[2:4] 
        mois = date[5:7]  
        jour = date[8:10]  
        match_df.loc[i, 'Date'] = f"{jour}/{mois}/{annee}"

    match_df['Date'] = pd.to_datetime(match_df['Date'], format='%d/%m/%y')
    match_df = match_df.sort_values(by='Date').reset_index(drop=True)
    match_df['Date'] = match_df['Date'].dt.strftime('%d/%m/%y')

    return match_df

def correct_team_names(match_df):
    corrections = {
        'Luton Town': 'Luton',
        'Newcastle Utd': 'Newcastle',
        'Sheffield Utd': 'Sheffield United',
        'Manchester Utd': 'Manchester United',
        "Nott'ham Forest": 'Nottingham Forest'
    }
    match_df['Opponent'] = match_df['Opponent'].replace(corrections)

    return match_df

def team_stats(match_df, data_df,new_col1, new_col2,new_col3,new_col4):
    for k in range(len(match_df)):
        for h in range(len(data_df)):
            if match_df.loc[k, 'Date'] == data_df.loc[h, 'Date']:
                if match_df.loc[k, 'Opponent'] == data_df.loc[h, 'HomeTeam']:
                    data_df.loc[h, new_col2] = 100 - match_df.loc[k, 'Poss']
                    data_df.loc[h, new_col1] = 100 - data_df.loc[h, new_col2]
                    data_df.loc[h,new_col3] = match_df.loc[k,'xGA']
                    data_df.loc[h,new_col4] = match_df.loc[k,'xG']

    return data_df


match_2324 = format_date(match_2324)
match_2324 = correct_team_names(match_2324)

moyenne_stats(data_2324,'HomeTeam','AwayTeam','HomeGoal','AwayGoal','Home_avgGoal','Away_avgGoal')
moyenne_stats(data_2324,'HomeTeam','AwayTeam','HomeShots','AwayShots','Home_avgShot','Away_avgShot')
moyenne_stats(data_2324,'HomeTeam','AwayTeam','HomeShotTarget','AwayShotTarget','Home_avgShot_Target','Away_avgShot_Target')
moyenne_stats(data_2324,'HomeTeam','AwayTeam','HCorners','ACorners','Home_avgCorner','Away_avgCorner')
moyenne_stats(data_2324,'HomeTeam','AwayTeam','HYellow','AYellow','Home_avgYellow','Away_avgYellow')
moyenne_stats(data_2324,'HomeTeam','AwayTeam','HRed','ARed','Home_avgRed','Away_avgRed')
moyenne_stats(data_2324,'HomeTeam','AwayTeam','HFouls','AFouls','Home_avgFouls','Away_avgFouls')
team_stats(match_2324, data_2324,'AwayPossesion', 'HomePossesion','Home_xG','Away_xG')

data_2324 = calculate_form(data_2324, 'HomeTeam', 'FullTimeResult', 'home_form')
data_2324 = calculate_form(data_2324, 'AwayTeam', 'FullTimeResult', 'away_form')

moyenne_dom_but = moyenne_stats_buts(data_2324,'HomeTeam','HomeGoal','moyenne_domcile_buts')
moyenne_ext_but = moyenne_stats_buts(data_2324,'AwayTeam','AwayGoal','moyenne_exterieur_buts')
moyenne_con_but_dom = moyenne_stats_buts(data_2324,'HomeTeam','AwayGoal','moyenne_conceder_dom')
moyenne_con_but_ext = moyenne_stats_buts(data_2324,'AwayTeam','HomeGoal','moyenne_conceder_ext')

moyenne_stats(data_2324,'HomeTeam','AwayTeam','HomePossesion','AwayPossesion','Home_avgPos','Away_avgPos')

