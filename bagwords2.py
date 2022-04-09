##----------------------------------------------
## Construction d'une matrice documents-termes
## Atelier transversal 11
## Version: 1.0
## Auteur: Pierre Chauvet
##----------------------------------------------
import re
import csv
import os
from calculOdds import constructListeGenre

# Ensemble (Set) de mots "vides", i.e. mots à supprimer
MOTS_VIDES = {"LE", "LA", "LES", "DE", "DU", "DES", "AU", "AUX",
"QUI", "QUE", "QUOI", "DONT", "OU",
"MAIS", "ET", "DONC", "NI", "CAR", "NE", "LÀ",
"JE", "TU", "IL", "ELLE", "ON", "NOUS", "VOUS", "ILS", "ELLES",
"MON", "MA", "TE", "TA", "SON", "SA", "MES", "TES", "SES", "UN", "UNE",
"NOTRE", "VOTRE", "LEUR", "NOTRES", "VOTRES", "LEURS", "NOS", "VOS",
"MIEN", "TIEN", "SIEN", "MIENNE", "TIENNE", "SIENNE",
"MIENS", "TIENS", "SIENS", "MIENNES", "TIENNES", "SIENNES",
"POUR", "PAR", "EN", "SE", "CE", "ÇA", "CES", "CET", "CETTE", "PAS", "DANS",
"TOUT", "TOUS", "TOUTE", "TOUTES", "QUAND","PENDANT",
"QU", "QUEL", "QUELLE", "QUELS", "QUELLES", "NE","SUR","EST","SONT","A",
"PLAIRE","ES","SUIS","SOMMES","ETES","ONT","AI","OU","PEUT","PEUVENT","FAIT",
"FAIS","FONT","VAIS","VA","VONT","HOMME","LUI","MONDE","AUSSI","ALORS","DEUX",
"TROIS","DEPUIS","SANS","AVEC","COMME","AUTRE","BIEN"}

# Dictionnaire (mapping) des caractères à remplacer
CAR_REMPLACE={"Ç":"C","É":"E","È":"E","Ê":"E","Ë":"E","À":"A","Â":"A",
              "Û":"U","Ù":"U","Ô":"O","Î":"I","Ï":"I","Œ":"OE"}

def captureTermes(filename, table_accents=None, dict_lemmes=None) :
    """ Construit la liste des termes (et de leur fréquence) du texte contenu
        dans le fichier passé en paramètre """
    # Lecture du texte et construction de la liste des mots avant traitement
    fo=open(filename,"r")
    liste=re.split("\s*[-:;,().«!…?'’\"\r\n\s]\s*",fo.read())
    fo.close()
    # Construction dictionnaire terme:fréquence
    termesfreq=dict()
    for mot in liste :
        #mot=mot.strip()
        if len(mot)>1 : # Ne retient que les mots de longueur>1
            mot=mot.upper() # Transforme le mot en majuscules
            if not mot in MOTS_VIDES : # Ne retient que les mots qui ne sont pas dans MOTS_VIDES
                if table_accents!=None : mot=mot.translate(table_accents) # Enlève les accents
                if dict_lemmes!=None :
                    if mot in dict_lemmes : mot=dict_lemmes[mot]
                if not mot in termesfreq : 
                    termesfreq[mot]=1
                else:
                    termesfreq[mot]+=1
    return termesfreq

def construireDicoLemmes(csvname) :
    """ Construit le dictionnaire de lemmes à partir du fichier csv passé en paramètres """
    dicoLemmes=dict()
    with open(csvname,"r") as fo:
        reader=csv.reader(fo, delimiter=';')
        for ligne in reader:
            dicoLemmes[ligne[0]]=ligne[1]
    return dicoLemmes

def construireDocumentsTermes(basename, table_accents=None, dict_lemmes=None) :
    """ Construit la matrice documents-termes.
        basename : nom du répertoire qui contient les sous-répertoires avec les textes;
        table_accents (optionnel) : transforme les caractères accentués en caractères simples;
        dict_lemmes (optionnel) : dictionnaire des lemmes utilisé pour la lemmatisation;
    """
    ensemble_termes=set() # Ensemble des termes qui serviront pour la matrice
    liste_termesfreq=list() # Liste des dico retournés pour chaque document analysé
    # Récupère tous les sous-répertoires (un sous-répertoire = une classe)
    reps=filter(os.path.isdir, [os.path.join(basename, f) for f in os.listdir(basename)])
    for rep in reps:
        # Dans chaque sous-répertoire, analyse de tous les fichiers
        nom_classe=os.path.basename(rep).upper() # Nom de la classe
        print(nom_classe)
        filenames = filter(os.path.isfile, [os.path.join(rep, f) for f in os.listdir(rep)])
        for fname in filenames :
            termesfreq=captureTermes(fname, table_accents, dict_lemmes)
            ensemble_termes.update(termesfreq.keys())
            liste_termesfreq.append([termesfreq,nom_classe])
    dico_termes = dict.fromkeys(sorted(ensemble_termes),0)
    for i, key in enumerate(dico_termes):  # iterates on the keys
        dico_termes[key] = i
    del ensemble_termes
    print("Nombres documents",len(liste_termesfreq))
    print("Nombres mots",len(dico_termes))
    # Génère la matrice documents-termes
    lcol=len(dico_termes)
    matrice=[[0 for j in range(lcol+1)] for i in range(len(liste_termesfreq))]
    for i in range(len(liste_termesfreq)) :
        termesfreq=liste_termesfreq[i][0]
        for terme in termesfreq.keys() :
            matrice[i][dico_termes[terme]]=termesfreq[terme]
        matrice[i][lcol]=liste_termesfreq[i][1]
    return dico_termes , matrice 



def ecrireDocumentsTermes(filename, termes, matrice) :
    """ Ecrit la matrice documents-termes dans un fichier csv.
        filename : nom du fichier csv;
        termes : liste des termes (entêtes de colonnes); 
        matrice : matrice documents-termes (fréquence de chaque termes dans chaque document);
    """
    import csv
    termes.append("CLASSE")
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file,delimiter=';')
        writer.writerow(termes)
        writer.writerows(matrice)
    print("Matrice Documents-Termes sauvée dans :",filename)

def chargerDocumentsTermes(nomfichier) :
    assert isinstance(nomfichier,str)
    matrice=[]
    with open(nomfichier,newline='') as fo:
        reader=csv.reader(fo, delimiter=';')
        for ligne in reader:
            matrice.append(ligne)
    return matrice    

def findGenre(termesfreq,dicoGenre):
    listeScoreGenre = [0,0,0,0]
    for termes in termesfreq:
        for i in range(4):
            for dicoTerm in dicoGenre[i]:
                if termes == dicoTerm:
                    listeScoreGenre[i] += termesfreq[termes]*dicoGenre[i][termes]
    return listeScoreGenre

def afficherPourcentage(listeScore):
    total = 0
    for i in listeScore:
        total += i
    print(f"         SF : {listeScore[0]*100//total}%")
    print(f"Fantastique : {listeScore[1]*100//total}%")
    print(f"   Policier : {listeScore[2]*100//total}%")
    print(f"    Fantasy : {listeScore[3]*100//total}%")

###### Programme principal ######
if __name__=="__main__":
    ## Quelques paramètres du programme
    REP_BASE_TEXTE="Textes"
    TEST_TEXTE = "Dune.txt" #"Textes\\Fantastique\\eternels.txt"
    FICHIER_LEMMES="Lemmas.csv"
    FICHIER_MAT_DOC_TERMES="matrice.csv"
    dicoLemmes=construireDicoLemmes(FICHIER_LEMMES) # Construction du dictionnaire des lemmes
    tableAccents=str.maketrans(CAR_REMPLACE) # Construction de la table de transformation des caractères accentués en caractères simples
    
    ## Analyse du résumé de "Dune" (pour tester)
    dicoGenre = constructListeGenre("matrice.csv")
    termesfreq=captureTermes(TEST_TEXTE, tableAccents, dicoLemmes) # Test de la fonction captureTerme() sur le résumé du roman "Dune"

    print("Nombre de termes :",len(termesfreq))
    #print("Dictionnaire :\n",termesfreq)

    ## Construction et sauvegarde de la matrice documents-termes sur l'ensemble du corpus
    dico_termes , matrice=construireDocumentsTermes(REP_BASE_TEXTE, table_accents=tableAccents, dict_lemmes=dicoLemmes)
    ecrireDocumentsTermes(FICHIER_MAT_DOC_TERMES, list(dico_termes.keys()), matrice)

    ## Lecture de la matrice documents-termes (pour vérifier)
    matrice=chargerDocumentsTermes(FICHIER_MAT_DOC_TERMES)

    #~~~~ Test ~~~~#
    print(f"Texte : {TEST_TEXTE} : ")
    listeScore = findGenre(termesfreq,dicoGenre)
    afficherPourcentage(listeScore)