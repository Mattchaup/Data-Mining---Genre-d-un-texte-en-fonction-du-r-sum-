def OpenFile(name):
    listeTotal = []
    with open(name,"r") as doss:
        listeMot = doss.readlines()
        for raw in listeMot:
            newRaw = raw.split(";")
            listeTotal.append(newRaw)
    listeMot = listeTotal[0]
    listeScore = listeTotal[1:]
    return listeMot,listeScore

def findCommonWord(listeMot,listeScore,genre):
    dico = [0 for i in range (len(listeMot)-1)]
    for i in range (0,len(listeScore)-1):
        if listeScore[i][-1][:-1] == genre:
            for j in range(len(listeScore[i][:-1])):
                dico[j] += int(listeScore[i][j])
    return dico

def bestWord(mot,score):
    dico = {}
    for i in range(50):
        j = score.index(max(score))
        #print(f"{i+1} - {mot[j]} : {score[j]}")
        dico.update({mot[j]:score[j]})
        del mot[j]
        del score[j]
    return dico

def constructListeGenre(name):
    genre = ['SF','FANTASTIQUE','POLICIER','FANTASY']
    listeGenre = []
    for g in genre:
        listeMot,listeScore = OpenFile(name)
        dico = findCommonWord(listeMot,listeScore,g)
        listeGenre.append(bestWord(listeMot, dico))
    return listeGenre

"""
listeGenre = constructListeGenre("matrice.csv")
for i in listeGenre:
    print("\n\n")
    for j in i:
        print(j,i[j])
"""