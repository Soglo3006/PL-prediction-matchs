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


def buts_minutes(butsEquipe):
    minutes = [ (0,15), (15,30),(30,45),(45,60),(60,75),(75,90)]
    probMinutes = [0.10,0.15,0.20,0.25,0.20,0.10]
    minutes_set = set()
    while len(minutes_set) < len(butsEquipe):
        a,b = random.choices(minutes,weights= probMinutes)[0]
        minutes_set.add(random.randint(a,b))
    ButsMinutesEquipe = sorted(minutes_set)
    for i in range (len(butsEquipe)):
        butsEquipe[i] = {butsEquipe[i] : ButsMinutesEquipe[i]}
    return butsEquipe
