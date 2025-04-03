import pandas as pd

data_2324 = pd.read_csv('fichier csv/season-2324.csv')
match_2324 = pd.read_csv('fichier csv/matches-23-24.csv')

def moyenne_stats(data,h_team,a_team,h_categore,a_categorie,home_new_col,away_new_col):
    teams = {}
    
    for team_name in data[h_team].unique():
        teams[team_name] = 0 
        teams = dict(sorted(teams.items()))
        
    for match_index in range(len(data)):
        for team in teams:
            if data.loc[match_index,h_team] == team :
                teams[team] += int(data.loc[match_index,h_categore])
            elif data.loc[match_index,a_team] == team:
                teams[team] += int(data.loc[match_index,a_categorie])
                
    for team in teams:
        teams[team] = round(teams[team]/38,2)
        
    for match_index in range(len(data)):
        for a in teams:
            if a == data.loc[match_index,h_team]:
                data.loc[match_index,home_new_col] = teams[a]
            elif a == data.loc[match_index,a_team]:
                data.loc[match_index,away_new_col] = teams[a]
                
    return teams

def calculate_form(data, team_col, result_col, new_col):
    form_list = []
    
    for match_index in range(len(data)):
        team = data.loc[match_index, team_col]
        past_matches = data.loc[:match_index-1]
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
    home_team_wins = {}
    
    for team_name in data['HomeTeam'].unique():
        home_team_wins[team_name] = 0
        
    for match_index in range(len(data)):
        if data.loc[match_index,'FullTimeResult'] == 'H':
            home_team_wins[data.loc[match_index,'HomeTeam']] += 1
            
    for team in home_team_wins:
        home_team_wins[team] = round(home_team_wins[team]/19,2)
    win_percentage = dict(sorted(home_team_wins.items()))
    
    for match_index in range(len(data)):
        if win_percentage[data.loc[match_index,'HomeTeam']] > win_percentage[data_2324.loc[match_index,'AwayTeam']]:
            data.loc[match_index,'home_advantage'] = 1
        else:
            data.loc[match_index,'home_advantage'] = 0

def moyenne_stats_buts(data,equipe,goal,new_col):
    team_stats = {}
    
    for team_name in data[equipe].unique():
        team_stats[team_name] = 0
        team_stats = dict(sorted(team_stats.items()))
        
    for match_index in range(len(data)):
        for j in team_stats:
            if data.loc[match_index,equipe] == j:
                team_stats[j] += int(data.loc[match_index,goal])
                
    for moy in team_stats:
        team_stats[moy] = round(team_stats[moy]/19,2)
        
    for match_index in range(len(data)):
        for nom_equipe in team_stats:
            if nom_equipe == data.loc[match_index,equipe]:
                data.loc[match_index,new_col] = team_stats[nom_equipe]
                
    return team_stats
def difference_buts(data, home_average, away_average, new_col, new_col2):
    home = home_average
    away = away_average
    
    for match_index in range(len(data)):
        if home[data.loc[match_index,'HomeTeam']]> away[data.loc[match_index,'AwayTeam']] : 
            data.loc[match_index,new_col] = home[data.loc[match_index,'HomeTeam']] - away[data.loc[match_index,'AwayTeam']]
            data.loc[match_index,new_col2] = data.loc[match_index,'HomeTeam']
        else:
            data.loc[match_index,new_col] = away[data.loc[match_index,'AwayTeam']] - home[data.loc[match_index,'HomeTeam']]
            data.loc[match_index,new_col2] = data.loc[match_index,'AwayTeam']

def format_date(match_df):
    for match_index in range(len(match_df)):
        date = match_df.loc[match_index, 'Date']
        year = date[2:4] 
        month = date[5:7]  
        day = date[8:10]  
        match_df.loc[match_index, 'Date'] = f"{day}/{month}/{year}"

    match_df['Date'] = pd.to_datetime(match_df['Date'], format='%d/%m/%y')
    match_df = match_df.sort_values(by='Date').reset_index(drop=True)
    match_df['Date'] = match_df['Date'].dt.strftime('%d/%m/%y')

    return match_df

def correct_team_names(match_df):
    fixing_name = {
        'Luton Town': 'Luton',
        'Newcastle Utd': 'Newcastle',
        'Sheffield Utd': 'Sheffield United',
        'Manchester Utd': 'Manchester United',
        "Nott'ham Forest": 'Nottingham Forest'
    }
    
    match_df['Opponent'] = match_df['Opponent'].replace(fixing_name)

    return match_df

def team_stats(match_df, data_df,new_col1, new_col2,new_col3,new_col4):
    for match_index in range(len(match_df)):
        for match_index_in_data in range(len(data_df)):
            if match_df.loc[match_index, 'Date'] == data_df.loc[match_index_in_data, 'Date']:
                if match_df.loc[match_index, 'Opponent'] == data_df.loc[match_index_in_data, 'HomeTeam']:
                    data_df.loc[match_index_in_data, new_col2] = 100 - match_df.loc[match_index, 'Poss']
                    data_df.loc[match_index_in_data, new_col1] = 100 - data_df.loc[match_index_in_data, new_col2]
                    data_df.loc[match_index_in_data,new_col3] = match_df.loc[match_index,'xGA']
                    data_df.loc[match_index_in_data,new_col4] = match_df.loc[match_index,'xG']

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

