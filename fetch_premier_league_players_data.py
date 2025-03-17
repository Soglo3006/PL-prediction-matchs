import panda as pd

data_joueur_stats = pd.read_csv('premier-player-23-24.csv')

for i in range(len(data_joueur_stats)):
    data_joueur_stats.loc[i,'GoalsPerGames'] = round(data_joueur_stats.loc[i,'Gls']/data_joueur_stats.loc[i,'MP'],2)
    
print(data_joueur_stats)