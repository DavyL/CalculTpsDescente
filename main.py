#fichier principal projet Calcul Scientifique
#Python 3.5

from math import *
import matplotlib.pyplot as plt

#On note:
#nombreDeSubdivision : le nombre de subidivision, noté N dans l'énoncé
#fonction : la fonction du toboggan
#pas : la taille d'un pas, noté delta_x dans l'énoncé
#listeDePoints : liste des x_i avec la notation de l'énoncé


nombreDePoint=int(input("nombre de points ")) # il y a un point de plus que le nombre de subdivision

#Les parties lecture fonction et dérivation ne sont pas utilisées ici
#Elles sont rentrées a la main pour les fonctions demandées


##################
#LECTURE FONCTION#
##################
#Le programme demande à l'utilisateur d'entrer une fonction au bon format, par ex. : "1- x";"1 -sqrt(x)"
print("La fonction doit être formattée pour python 3.5, la bibliothèque math est importée\n")
fonctionLue = input("fonction qui à x associe: ")
def lireFonction():
    fichier = open("Fonction.py","w")                  #On crée un fichier "Fonction.py" qui contient du code Python (en mode écriture)
          
    fichier.write("from math import *\n")              #On importe la bibliothèque math
    fichier.write("def fonction(x): \n")               #On définit la fonction
    fichier.write("\t return " + fonctionLue + "\n")   #La fonction renvoie la fonction lue
                                  
    fichier.close()                                    #On ferme le fichier

lireFonction()

from Fonction import fonction                           #On importe la fonction depuis le fichier crée précedemment

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

def deriv(f, x, h):
    if x == 0:
        return derivDroite(f, x, h)    
    elif x == 1:
        return derivGauche(f, x, h)                                                                    
    else:                                                                     
        return ( derivGauche(f, x, h) +  derivDroite(f, x, h))/2

                                                                                     
pas = 1 / (nombreDePoint - 1) 
listeDePoint =[]
                                                                                      
for i in range (0, nombreDePoint ):
    xi = i * pas 
    listeDePoint.append(xi) 

fonction1 = lambda x: 1 - x
fonction2 = lambda x: 1 - sqrt(x)
fonction3 = lambda x: 1 - ((x**(3/2))*(5-3*x))/2
derive1 = lambda x: -1
derive2 = lambda x: -1/(2*sqrt(x))
derive3 = lambda x: (15/4)*(-1 * x**(1/2) + x**(3/2))

#integrale est la fonction à intégrer
#Dans le calcul de la dérivée, on divise le pas par deux afin de rendre le calcul de la dérivée plus précis que celui de l'integrale
g = 10
integrale = lambda x: sqrt(1 + (deriv(fonction, x, 0.5 * pas))**2)/(sqrt(2*(g*fonction(0) - fonction(x))))

#méthode rect à gauche
somme = 0
listeRG = [0]

for i in range (0, nombreDePoint-1):
    #on décale de 1 les valeurs dans la somme car i est l'indice dans la liste
    somme = somme + integrale (listeDePoint[i])
    listeRG.append(pas * somme)
    tempsDeDescente = pas * somme

print ("tempsDeDescente avec la méthode des rectangles à gauche=", tempsDeDescente)

#méthode rect à droite
somme = 0 
listeRD = [0]

for i in range (1, nombreDePoint):
    somme = somme + integrale (listeDePoint[i]) 
    listeRD.append(pas * somme)
    tempsDeDescente = pas * somme 

print ("tempsDeDescente avec la méthode des rectangles à droite=", tempsDeDescente)

#méthode des trapèzes
somme = 0 
listeTrapeze = []
listeTrapeze.append( pas * 0.5 * integrale(listeDePoint[0])) 

for i in range ( 1, nombreDePoint - 1):
    somme = somme + integrale (listeDePoint[i])
    listeTrapeze.append(pas * somme)
listeTrapeze.append( pas * 0.5 * integrale(listeDePoint[nombreDePoint - 1]))
tempsDeDescente = pas*((integrale (listeDePoint[0]) + integrale (listeDePoint[nombreDePoint - 1])) / 2 + somme)

print ("tempsDeDescente avec la méthode des trapèzes =", tempsDeDescente)
#méthode de Simpson
if nombreDePoint%2 != 0:
    somme1 = 0
    somme2 = 0
    listeSimpson = []
    m = nombreDePoint // 2
    listeSimpson.append((pas * integrale(listeDePoint[0]))/6)

    for i in range(1, m):
        somme1= somme1 + integrale(listeDePoint[2*i])
        somme2= somme2 + integrale(listeDePoint[2*i+1])
    listeSimpson.append((pas * somme1)/3)
    listeSimpson.append((pas * somme2 * 2)/3)
    listeSimpson.append((pas * integrale(listeDePoint[nombreDePoint - 1]))/6)
    tempsDeDescente = (pas / 3) * (integrale(listeDePoint[0])+ 2 * somme1 + 4 * somme2 + integrale(listeDePoint[nombreDePoint-1]) )
    print ("tempsDeDescente avec la méthode de Simpson = ", tempsDeDescente)

else:
    print("Le nombre de points de la subidivision n'est pas adapté à la méthode de Simpson")
####################
#AFFICHAGE FONCTION#
####################
#C'est pas top mais je vois pas trop comment bien faire 😕
#Crée une première fenêtre sur laquelle on affiche le toboggan
plt.figure(1)                                                                  
plt.plot(listeDePoint, [fonction(i*pas) for i in range(nombreDePoint)], "ro")
plt.ylabel(fonctionLue)

#Crée une seconde figure sur laquelle on affiche trois graphes
#Chaque graphe correspond à la valeur de l'integrale de 0 à x<= 1
#En utilisant la méthode de calcul spécifiée
#f, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, sharey=True)
#ax1.plot(listeDePoint, listeRG)
#ax1.set_title("Rect. à gauche")
#ax2.plot(listeDePoint, listeRD)
#ax2.set_title("Rect. à Droite")
#ax3.scatter(listeDePoint, listeTrapeze)
#ax3.set_title("Méthode trapeze")
#ax4.scatter(listeDePoint, listeSimpson)
#ax4.set_title("Méthode de Simpson")
#On affiche les figures crées ci-dessus
plt.show()


