#fichier principal projet Calcul Scientifique
#Python 3.5

from math import *

#On note:
#nombreDeSubdivision : le nombre de subidivision, noté N dans l'énoncé
#fonction : la fonction du toboggan
#pas : la taille d'un pas, noté delta_x dans l'énoncé
#listeDePoints : liste des x_i avec la notation de l'énoncé


nombreDePoint=int(input("nombre de points ")) # il y a un point de plus que le nombre de subdivision

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

assert (fonction(0) == 1), "Vérifier que la fonction vaut 1 en 0"       #On verifie que la fonction vérifie les conditions demandées   
assert (fonction(1) == 0), "Vérifier que la fonction vaut 0 en 1"

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

print(deriv(fonction,1, (1/2)*pas))
listeDePoint =[]
for i in range (0, nombreDePoint ):
    xi = i * pas 
    listeDePoint.append(xi) 
#print (listeDePoint) 

#fonction = lambda x:1 - x

#integrale est la fonction à intégrer, le 3.9 correspond à la racine carrée de g, avec g = 9.81
#Dans le calcul de la dérivée, on divise le pas par deux afin de rendre le calcul de la dérivée plus précis que celui de l'integrale
integrale = lambda x: sqrt(1 + (deriv(fonction, x, 0.5 * pas))**2)/((3.9)*sqrt(2*(fonction(0) - fonction(x))))

#méthode rect à gauche
somme = 0 
for i in range (1, nombreDePoint - 1):
#on décale de 1 les valeurs dans la somme car i est l'indice dans la liste
    somme = somme + integrale (listeDePoint[i])
    tempsDeDescente = pas * somme
print ("tempsDeDescente avec la méthode des rectangles à gauche=", tempsDeDescente)


#méthode rect à droite
somme = 0 
for i in range (1, nombreDePoint):
    somme = somme + integrale (listeDePoint[i])
    tempsDeDescente = pas * somme
print ("tempsDeDescente avec la méthode des rectangles à droite=", tempsDeDescente)


#méthode des trapèzes
somme = 0 
for i in range ( 2, nombreDePoint - 2):
    somme = somme + integrale (listeDePoint[i])
    tempsDeDescente = pas*((integrale (listeDePoint[1]) + integrale (listeDePoint[nombreDePoint - 1])) / 2 + somme) 
print ("tempsDeDescente avec la méthode des trapèzes =", tempsDeDescente)


