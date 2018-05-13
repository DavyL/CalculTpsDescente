#fichier principal projet Calcul Scientifique
#Python 3.5

#Un PDF décrivant certaines parties de ce programme, notamment la mise en équation du problème ainsi qu'un description de l'efficacité de certaines méthodes
#est disponible à l'adresse suivante :
# http://github.com/DavyL/CalculTpsDescente/blob/master/Temps_descente.pdf 

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

#IMPORTANT : l'option latex ignore l'option size

#On note:
#nombreDeSubdivision : le nombre de subidivision, noté N dans l'énoncé
#fonction : la fonction du toboggan
#pas : la taille d'un pas, noté delta_x dans l'énoncé
#listeDePoints : liste des x_i avec la notation de l'énoncé
#tempsDescenteListe : tableau contenant pour chaque fonction, le calcul du temps de descente en fonction du nombre de points de la subdivision
latex = 0
nombreDePointListe = []
tempsDescenteListe = []
tempsDescente = []
if( "latex" in args):
    latex = 1
    nombreDePointListe = [101, 501, 2001, 10001, 300001]

else:
    if( "size" not in args):
        nombreDePointListe.append(int(input("nombre de points "))) # il y a un point de plus que le nombre de subdivision
    else:
        flag = 0
        for arg in args: 
            if flag:
                nombreDePointListe.append(int(arg))
                flag = 0
            if arg == "size":
                flag = 1

#On crée une liste de fonctions, de derivées et de fonctions correspondant aux integrales resp, noté integrale

fonction = []
derive = []
integrale = []
rho = []

#Les parties lecture fonction et dérivation sont utilisées uniquement si l'option customest utilisée
#Elles sont rentrées a la main pour les fonctions demandées

##################
#LECTURE FONCTION#
##################
#Le programme demande à l'utilisateur d'entrer une fonction au bon format, par ex. : "1- x";"1 -sqrt(x)"
if(custom):
    print("La fonction doit être formattée pour python 3.5, la bibliothèque math est importée")
    fonctionLue = input("fonction qui à x associe: ")
    def lireFonction():
        fichier = open("Fonction.py","w")                  #On crée un fichier "Fonction.py" qui contient du code Python (en mode écriture)
              
        fichier.write("from math import *\n")              #On importe la bibliothèque math
        fichier.write("def fonctionPerso(x): \n")               #On définit la fonction
        fichier.write("\t return " + fonctionLue + "\n")   #La fonction renvoie la fonction lue
                                      
        fichier.close()                                    #On ferme le fichier

    lireFonction()

    from Fonction import fonctionPerso                           #On importe la fonction depuis le fichier crée précedemment
    
    fonction.append( lambda x: fonctionPerso(x))

    print("Afin d'utiliser la méthode du changement de variable, entrez la valeur de rho définie dans le PDF")
    print("Sinon, entrez la valeur 1")
    rho.append(int(input("rho = ")))

    #Si rho = 1, alors il n'y a pas de changement de variable, donc cela correspond à la méthode du point milieu

    assert (abs(fonction[0](0) - 1) <= 0.01), "Vérifier que la fonction vaut 1 en 0"       #On verifie que la fonction vérifie les conditions demandées   
    assert (abs(fonction[0](1)) <= 0.01), "Vérifier que la fonction vaut 0 en 1"

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
    
    derive.append( lambda x: derivCalc( fonction[0], x, 0.5 * pas))


fonction.append( lambda x: 1 - x)
fonction.append( lambda x: 1 - sqrt(x))
fonction.append( lambda x: 1 - ((x**(3/2))*(5-3*x))/2)
derive.append( lambda x: -1)
derive.append( lambda x: -1/(2*sqrt(x)))
derive.append( lambda x: (15/4)*(-1 * x**(1/2) + x**(3/2)))
rho.append(2)
rho.append(4)
rho.append(4)

#Dans la boucle suivante, on parcourt chaque tableau de fonction défini précedemment
for k in range(len(fonction)): 
    tempsDescenteListe = []
    print("\n Etude de la fonction " + str(k))
    integrale.append( lambda x: sqrt(1 + (derive[k](x))**2)/(sqrt(2*g*(fonction[k](0) - fonction[k](x)))))


    #integrale est la fonction à intégrer
    #Dans le calcul de la dérivée, on divise le pas par deux afin de rendre le calcul de la dérivée plus précis que celui de l'integrale
    #On définit la constante de "pesanteur" comme suit
    g = 10

    for nombreDePoint in nombreDePointListe:   
        print(nombreDePoint, nombreDePointListe)
        pas = 1 / (nombreDePoint - 1) 
        listeDePoint =[]
        tempsDescente = []
            
        #Les fonction ne sont pas nécéssairement définies en 0, on utilise donc une méthode ouverte
        #On étudie donc les fonction sur "l'ouvert" (0, 1) sur lequel on suppose les fonction définies

        for i in range (0, nombreDePoint ):
            xi = i*pas + 1/nombreDePoint
            listeDePoint.append(xi) 
        
        #méthode rect à gauche
        somme = 0
        listeRG = [0]

        for i in range (0, nombreDePoint-1):
            #on décale de 1 les valeurs dans la somme car i est l'indice dans la liste
            somme = somme + integrale[k] (listeDePoint[i])
        tempsDescente.append(pas * somme)
        print ("Temps de descente avec la méthode des rectangles à gauche=", tempsDescente[-1])

        #méthode rect à droite
        somme = 0 
        listeRD = [0]

        for i in range (1, nombreDePoint):
            somme = somme + integrale[k] (listeDePoint[i]) 
        tempsDescente.append(pas * somme) 

        print ("Temps de descente avec la méthode des rectangles à droite=", tempsDescente[-1])

        #méthode des trapèzes
        somme = 0 

        for i in range ( 1, nombreDePoint - 1):
            somme = somme + integrale[k] (listeDePoint[i])
        tempsDescente.append(pas*((integrale[k] (listeDePoint[0]) + integrale[k] (listeDePoint[nombreDePoint - 1])) / 2 + somme))

        print ("Temps de descente avec la méthode des trapèzes =", tempsDescente[-1])
        
        
        #méthode de Simpson
        if nombreDePoint%2 != 0:
            somme1 = 0
            somme2 = 0
            m = nombreDePoint // 2

            for i in range(1, m):
                somme1= somme1 + integrale[k](listeDePoint[2*i])
                somme2= somme2 + integrale[k](listeDePoint[2*i+1])
            tempsDescente.append((pas / 3) * (integrale[k](listeDePoint[0])+ 2 * somme1 + 4 * somme2 + integrale[k](listeDePoint[nombreDePoint-1]) ))
            print ("Temps de descente avec la méthode de Simpson = ", tempsDescente[-1])

        else:
            print("Le nombre de points de la subidivision n'est pas adapté à la méthode de Simpson")
        
        #Méthode point milieu avec changement de variable

        somme = 0
        try:
            for i in range(nombreDePoint):
                somme += integrale[k]( ((2*i + 1)/(2*nombreDePoint))**rho[k])*( ((2*i+1)/(2*nombreDePoint))**(rho[k] - 1))
        except ZeroDivisionError:
            print("La méthode du changement de variable ne peut être appliquée avec la fonction" + str(k) + "et une subdivision avec "+str(nombreDePoint) + "points.")
            somme = 0
        tempsDescente.append((rho[k]/nombreDePoint)*somme)
        print("Temps de descente avec le changement de variable = ", tempsDescente[-1])

        tempsDescenteListe.append(tempsDescente)
    ################
    #ECRITURE LATEX#
    ################
    if(latex):
        fichierLatex = open("tableau"+str(k)+".tex","w")                  #On crée un fichier "tableau.tex" qui contient du code LaTeX (en mode écriture)
              
        fichierLatex.write("\\begin{center}\n")                  #
        fichierLatex.write("\t \\begin{tabular}{ |l | c | c | c | c | r| }\n")               #
        fichierLatex.write("\t\t \\hline\n")   #
        fichierLatex.write("\t\t\t\t & Rect. \`a gauche \t& Rect. \`a droite \t& Trap\`eze \t& Simpson \t& Chgmt var. \\\\ \\hline\n") 
        for l in range(len(nombreDePointListe)):
            fichierLatex.write( "\t\t\tN = " + str(nombreDePointListe[l]) 
                                                            + "\t & " + str(tempsDescenteListe[l][0])
                                                            + "\t & " + str(tempsDescenteListe[l][1])
                                                            + "\t & " + str(tempsDescenteListe[l][2])
                                                            + "\t & " + str(tempsDescenteListe[l][3])
                                                            + "\t & " + str(tempsDescenteListe[l][4])  
                                                            + " \\\\ \\hline \n")
        fichierLatex.write("\t \\end{tabular}\n")
        fichierLatex.write("\\end{center}\n")
        fichierLatex.close() 

    ####################
    #AFFICHAGE FONCTION#
    ####################

    #Crée une fenêtre sur laquelle on affiche la courbe étudiée
    plt.figure(1)                                                                  
    plt.plot(listeDePoint, [fonction[k](i*pas) for i in range(nombreDePoint)], "ro")
    plt.ylabel("Fonction[" + str(k) + "]")
    
        
#On affiche les figures crées ci-dessus
plt.show()

