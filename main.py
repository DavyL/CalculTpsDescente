#fichier principal projet Calcul Scientifique
#Python 3.5

##########
#EXEMPLES#
##########

# > python3 main.py size 420 
# > python3 main.py custom size 10000
# > python3 main.py custom

from math import *
import matplotlib.pyplot as plt
import sys

args = sys.argv
if( "custom" in args):
    custom = 1
else:
    custom = 0

#Le programme peut lire des arguments passés depuis la ligne de commande
# custom : pour lire une fonction qui n'est pas écrites à la main dans le code source
# latex  : pour avoir en sortie du programme un fichier .tex contenant un résumé de l'étude des fonctions
# size [int]: pour définir la taille de la subdivision lors de l'execution

#On note:
#nombreDeSubdivision : le nombre de subidivision, noté N dans l'énoncé
#fonction : la fonction du toboggan
#pas : la taille d'un pas, noté delta_x dans l'énoncé
#listeDePoints : liste des x_i avec la notation de l'énoncé

if( "size" not in args):
    nombreDePoint=int(input("nombre de points ")) # il y a un point de plus que le nombre de subdivision
else:
    flag = 0
    for arg in args: 
        if flag:
            nombreDePoint = int(arg)
            flag = 0
        if arg == "size":
            flag = 1

                                                                                     
pas = 1 / (nombreDePoint - 1) 
listeDePoint =[]
    
#Les fonction ne sont pas nécéssairement définies en 0, on utilise donc une méthode ouverte
#On étudie donc les fonction sur l'ouvert (0, 1) sur lequel on suppose les fonction définies

for i in range (0, nombreDePoint ):
    xi = i*pas + 1/nombreDePoint
    listeDePoint.append(xi) 
#On crée une liste de fonctions, de derivées et de fonctions correspondant aux integrales resp, noté integrale

fonction = []
derive = []
integrale = []

#Les parties lecture fonction et dérivation sont utilisées uniquement si l'option customest utilisée
#Elles sont rentrées a la main pour les fonctions demandées

##################
#LECTURE FONCTION#
##################
#Le programme demande à l'utilisateur d'entrer une fonction au bon format, par ex. : "1- x";"1 -sqrt(x)"
if(custom):
    print("La fonction doit être formattée pour python 3.5, la bibliothèque math est importée\n")
    fonctionLue = input("fonction qui à x associe: ")
    def lireFonction():
        fichier = open("Fonction.py","w")                  #On crée un fichier "Fonction.py" qui contient du code Python (en mode écriture)
              
        fichier.write("from math import *\n")              #On importe la bibliothèque math
        fichier.write("def fonction(x): \n")               #On définit la fonction
        fichier.write("\t return " + fonctionLue + "\n")   #La fonction renvoie la fonction lue
                                      
        fichier.close()                                    #On ferme le fichier

    lireFonction()

    from Fonction import fonctionPerso                           #On importe la fonction depuis le fichier crée précedemment
    
    fonction.append( lambda x: fonctionPerso(x))

    assert (abs(fonction(0) - 1) <= 0.01), "Vérifier que la fonction vaut 1 en 0"       #On verifie que la fonction vérifie les conditions demandées   
    assert (abs(fonction(1)) <= 0.01), "Vérifier que la fonction vaut 0 en 1"

    #Les fonctions étudiées sont décroissantes de 0 à 1 donc la dérivée à gauche n'est pas nécéssairement définie
    #On va donc dériver à droite en 0 et de même, on va dériver en gauche en 1
    #Sur les autres points afin de gagner en précision, on calculera la moyenne de la dérivée à gauche et à droite
    #Il faut donc définir les trois dérivées
    def derivGauche(f, x, h):
        return (f(x) - f(x - h))/h

    def derivDroite(f, x, h):
        return (f(x + h) - f(x))/h

    def derivCalc(f, x, h):
        if x == 0:
            return derivDroite(f, x, h)    
        elif x == 1:
            return derivGauche(f, x, h)                                                                    
        else:                                                                     
            return ( derivGauche(f, x, h) +  derivDroite(f, x, h))/2
    
    deriv.append( lambda x: derivCalc( fonction[0], x, 0.5 * pas))


fonction.append( lambda x: 1 - x)
fonction.append( lambda x: 1 - sqrt(x))
fonction.append( lambda x: 1 - ((x**(3/2))*(5-3*x))/2)
derive.append( lambda x: -1)
derive.append( lambda x: -1/(2*sqrt(x)))
derive.append( lambda x: (15/4)*(-1 * x**(1/2) + x**(3/2)))

#integrale est la fonction à intégrer
#Dans le calcul de la dérivée, on divise le pas par deux afin de rendre le calcul de la dérivée plus précis que celui de l'integrale
g = 10

#Dans la boucle suivante, on parcourt chaque tableau de fonction défini précedemment
for k in range(len(fonction)):
    print("\n Etude de la fonction " + str(k))
    integrale.append( lambda x: sqrt(1 + (derive[k](x))**2)/(sqrt(2*g*(fonction[k](0) - fonction[k](x)))))

    #integrale = lambda x: sqrt(1 + (deriv(fonction, x, 0.5 * pas))**2)/(sqrt(2*(g*fonction(0) - fonction(x))))

    #méthode rect à gauche
    somme = 0
    listeRG = [0]

    for i in range (0, nombreDePoint-1):
        #on décale de 1 les valeurs dans la somme car i est l'indice dans la liste
        somme = somme + integrale[k] (listeDePoint[i])
        tempsDeDescente = pas * somme

    print ("tempsDeDescente avec la méthode des rectangles à gauche=", tempsDeDescente)

    #méthode rect à droite
    somme = 0 
    listeRD = [0]

    for i in range (1, nombreDePoint):
        somme = somme + integrale[k] (listeDePoint[i]) 
        tempsDeDescente = pas * somme 

    print ("tempsDeDescente avec la méthode des rectangles à droite=", tempsDeDescente)

    #méthode des trapèzes
    somme = 0 

    for i in range ( 1, nombreDePoint - 1):
        somme = somme + integrale[k] (listeDePoint[i])
    tempsDeDescente = pas*((integrale[k] (listeDePoint[0]) + integrale[k] (listeDePoint[nombreDePoint - 1])) / 2 + somme)

    print ("tempsDeDescente avec la méthode des trapèzes =", tempsDeDescente)
    #méthode de Simpson
    if nombreDePoint%2 != 0:
        somme1 = 0
        somme2 = 0
        m = nombreDePoint // 2

        for i in range(1, m):
            somme1= somme1 + integrale[k](listeDePoint[2*i])
            somme2= somme2 + integrale[k](listeDePoint[2*i+1])
        tempsDeDescente = (pas / 3) * (integrale[k](listeDePoint[0])+ 2 * somme1 + 4 * somme2 + integrale[k](listeDePoint[nombreDePoint-1]) )
        print ("tempsDeDescente avec la méthode de Simpson = ", tempsDeDescente)

    else:
        print("Le nombre de points de la subidivision n'est pas adapté à la méthode de Simpson")
    ####################
    #AFFICHAGE FONCTION#
    ####################

    #Crée une fenêtre sur laquelle on affiche la courbe étudiée
    plt.figure(1)                                                                  
    plt.plot(listeDePoint, [fonction[k](i*pas) for i in range(nombreDePoint)], "ro")
    plt.ylabel("Fonction[" + str(k) + "]")

#On affiche les figures crées ci-dessus
plt.show()


