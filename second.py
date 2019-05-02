# 15/03/19
# 10/04/19
# ? Changement de la nature des etats
# ** Etat = [[],[],[],[]]

# Projet Unblock Me, IA
import time
from functools import partial
from resolution import recherche_en_profondeur_lim_mem, recherche_en_profondeur, recherche_en_profondeur_limitee, nouvel_operateur, recherche_en_profondeur_memoire, recherche_en_largeur


# ---------------------------------VARS---------------------------------
# Representation de la grille de jeu vide
#! Grille 4x4, creation dynamic ?
empty_board = [	['x', 'x', 'x', 'x'],
                ['x', 'x', 'x', 'x'],
                ['x', 'x', 'x', 'x'],
                ['x', 'x', 'x', 'x']
                ]

operateurs_disponibles = []
# ---------------------------------FONCTIONS---------------------------------
# Verifie si un etat correspond a une fin de partie
def est_final(e):
    # Si le bloc principal se trouve en position de fin de partie
    if (e[0] == [1, 2, 1, 3]):
        return (True)
    else:
        return(False)

#! Affiche un plateau de jeu
def show(matrice):
    print("- -" + " -"*len(matrice))
    for bloc in matrice:
        ligne = " "
        for element in bloc:
            ligne += str(element) + " "
        print(f"|{ligne}|")
    print("- -" + " -"*len(matrice))


def copie(matrice):
    copied = []
    for bloc in matrice:
        coord_list = []
        for coord in bloc:
            coord_list.append(coord)
        copied.append(coord_list)
    return(copied)

# * Construction du plateau a partir d'un etat et d'une grille vide
def fill_board(etat):
    instance = copie(empty_board)
    for index, bloc in enumerate(etat):
        # Decomposition des coordonnees
        f_line, f_col, s_line, s_col = bloc
        # Ajouts du marqueur(index) du bloc dans la grille
        instance[f_line][f_col] = index
        instance[s_line][s_col] = index
    # Affichage du plateau nouvellement forme
    show(instance)

def show_result(solution, e):
    if solution != None:
        print(f"\n__SOLUTION en {len(solution)} coups__\n")
        fill_board(e)
        for mouvement in solution:
            e = mouvement(e)
            fill_board(e)
        print(f"Temps mis: {end - start}s")
    else:
        print("Pas de solution")
        print(end - start)

# --------------------------------- Operations sur les blocs---------------------------------
class Blocs:
    codage = 0  # valeur qui represente l'instance du bloc dans la matrice
    obstacles = []  # liste de toutes les instances
    initial = [] # liste des coordonees de chaque bloc de l'etat initial

    # Initialisation d'une bloc depend des coords (x1,y1,x2,y2) de ses 2 petits blocs
    def __init__(self, bloc_coord):
        self.codage = Blocs.codage # Codage est le label associe au bloc
        Blocs.codage += 1
        Blocs.obstacles.append(self) # ajout de l'instance actuelle a la liste d'obstacles
        Blocs.initial.append(bloc_coord) # ajout des coordonnes de l'instance a la liste de coordonnees

    # ---------------------------------Deplacements des blocs ---------------------------------
    def move_down(self, e):  # Deplacement vers le bas d'un bloc (self) pour un etat e
        _, _, s_line, s_col = e[self.codage] # Decomposition des coordonnees du second petit bloc
        new_coords = [s_line, s_col, s_line+1, s_col] # Incrementation de la position, une ligne vers le bas
        print("Deplacement vers le bas du bloc: ", self.codage)
        nouvel_etat = copie(e)
        nouvel_etat[self.codage] = new_coords # Remplace les anciennes coordonnees par les nouvelles
        return (nouvel_etat)

    def move_up(self, e): # Deplacement vers le haut d'un bloc (self) pour un etat e
        f_line, f_col, _, _ = e[self.codage] # Decomposition des coordonnees du premier petit bloc
        new_coords = [f_line-1, f_col, f_line, f_col] # Decrementation de la position, une ligne vers le haut
        print("Deplacement vers le haut du bloc: ", self.codage)
        nouvel_etat = copie(e)
        nouvel_etat[self.codage] = new_coords # Remplace les anciennes coordonnees par les nouvelles
        return (nouvel_etat)

    def move_right(self, e): # Deplacement vers le haut d'un bloc (self) pour un etat e
        _, _, s_line, s_col = e[self.codage] # Decomposition des coordonnees du second petit bloc
        new_coords = [s_line, s_col, s_line, s_col+1] # Incrementation de la position, une colonne vers la droite
        print("Deplacement vers la droite du bloc: ", self.codage)
        nouvel_etat = copie(e)
        nouvel_etat[self.codage] = new_coords # Remplace les anciennes coordonnees par les nouvelles
        return (nouvel_etat)

    def move_left(self, e): # Deplacement vers le bas du bloc pour un etat e
        f_line, f_col, _, _ = e[self.codage] # Decomposition des coordonnees du premier petit bloc
        new_coords = [f_line, f_col-1, f_line, f_col] # Decrementation de la position, une colonne vers la gauche
        print("Deplacement vers la gauche du bloc: ", self.codage)
        nouvel_etat = copie(e)
        nouvel_etat[self.codage] = new_coords # Remplace les anciennes coordonnees par les nouvelles
        return (nouvel_etat)

    # ---------------------------------Preconditions---------------------------------
    def precond_down(self, e):
        _, f_col, s_line, s_col = e[self.codage]
        # Si le bloc est contre un bord ou s'il n'est pas vertical
        if (s_line == len(empty_board) - 1) or (f_col != s_col):
            return False
        else:
            for coords in e:
                for bloc in [coords[:2], coords[2:]]:
                    if bloc == [s_line+1, s_col]:
                        return False
            # Si aucun des bloc de l'etat n'occupe l'espace que l'on souhaite occupe
            return True

    def precond_right(self, e):
        f_line, _, s_line, s_col = e[self.codage]
        if (s_col == len(empty_board) - 1) or (f_line != s_line):
            return False
        else:
            for coords in e:
                for bloc in [coords[:2], coords[2:]]:
                    if bloc == [s_line, s_col+1]:
                        return False
            # Si aucun des bloc de l'etat n'occupe l'espace que l'on souhaite occupe
            return True

    def precond_up(self, e):
        f_line, f_col, _, s_col = e[self.codage]
        if (f_line == 0) or (f_col != s_col):
            return False
        else:
            for coords in e:
                for bloc in [coords[:2], coords[2:]]:
                    if bloc == [f_line-1, f_col]:
                        return False
            # Si aucun des bloc de l'etat n'occupe l'espace que l'on souhaite occupe
            return True

    def precond_left(self, e):
        f_line, f_col, s_line, _ = e[self.codage]
        if (f_col == 0) or (f_line != s_line):
            return False
        else:
            for coords in e:
                for bloc in [coords[:2], coords[2:]]:
                    if bloc == [f_line, f_col-1]:
                        return False
            # Si aucun des bloc de l'etat n'occupe l'espace que l'on souhaite occupe
            return True


# ---------------------------------TEST---------------------------------

# * Initialisation des blocs
Blocs([1, 0, 1, 1])
Blocs([0, 2, 1, 2])
Blocs([0, 3, 1, 3])
Blocs([2, 1, 2, 2])
Blocs([3, 1, 3, 2])


# * des operateurs disponibles pour les blocs initialises

for bloc in Blocs.obstacles:
    op = nouvel_operateur(
        "move down bloc n°"+str(bloc.codage), partial(Blocs.precond_down, bloc), partial(Blocs.move_down, bloc))
    operateurs_disponibles.append(op)
    op = nouvel_operateur(
        "move up bloc n°"+str(bloc.codage), partial(Blocs.precond_up, bloc), partial(Blocs.move_up, bloc))
    operateurs_disponibles.append(op)
    op = nouvel_operateur(
        "move left bloc n°"+str(bloc.codage), partial(Blocs.precond_left, bloc), partial(Blocs.move_left, bloc))
    operateurs_disponibles.append(op)
    op = nouvel_operateur(
        "move right bloc n°"+str(bloc.codage), partial(Blocs.precond_right, bloc), partial(Blocs.move_right, bloc))
    operateurs_disponibles.append(op)


start = time.time() # Initialisation du Timer

# recherche_en_profondeur_lim_mem
# recherche_en_profondeur_limitee
# recherche_en_profondeur_memoire
# recherche_en_largeur

# Executions de la resolution
solution = recherche_en_profondeur_limitee(
    Blocs.initial, est_final, operateurs_disponibles, 8)
# solution = (recherche_en_profondeur_lim_mem(
#     Blocs.initial, est_final, operateurs_disponibles, 4, []))
# solution = (recherche_en_profondeur_memoire(
#     Blocs.initial, est_final, operateurs_disponibles, []))
# solution = recherche_en_largeur(Blocs.initial, est_final, operateurs_disponibles, [], False)

end = time.time() # Arret du Timer


show_result(solution, Blocs.initial)
