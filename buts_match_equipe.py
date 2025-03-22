import random 

def buteurs_Dans_Match(data2,team, Buts):
    if Buts == 0:
        return []
    else:
        JoueurTeam = []
        for i in range(len(data2[team]['Starting11Players'])):
            if data2[team]['Starting11Players'].loc[i,'Team'] == team:
                JoueurTeam.append(data2[team]['Starting11Players'].iloc[i])
        JoueurTeam = sorted(JoueurTeam, key=lambda x:x['Gls_90'], reverse=True)
        listWeight = []
        for j in JoueurTeam:
            listWeight.append(float(j['Gls_90']))
        Buteur = random.choices(JoueurTeam, weights= listWeight, k= Buts)
        for z in range(len(Buteur)):
            Buteur[z] = Buteur[z]['Player']
        
    return Buteur
