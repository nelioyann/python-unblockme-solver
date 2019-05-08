# 15/03/19
# 10/04/19
# ? Changement de la nature des etats
# ** Etat = [[],[],[],[]]

# Projet Unblock Me, IA, resolution
import time
from os import system
from functools import partial
from resolution import *
from termcolor import colored, cprint

# ---------------------------------FONCTIONS---------------------------------
# Construction de la grille de jeu en fonction de la taille souhaitee
def make_board(size):
    board = []
    line = []
    # On cree une ligne qui contiendra size elements
    for _ in range(size):
        line.append('●')
    # On cree une matrice qui contiendra size ligne
    for _ in range(size):
        board.append(line)
    return board

# Verifie si un etat correspond a une fin de partie, depend de la taille du plateau
def est_final(board_size, e):
    # Si le bloc directeur se trouve contre la paroi droite
    if (e[0] == [1, board_size-2, 1, board_size-1]):  
        return (True)
    else:
        return(False)

# Affiche le plateau en assignant une couleur a chaque bloc
def show(plateau):
    # Palette de couleur utilisee pour differencier les blocs
    palette = ["red", "yellow", "blue", "green", "grey", "magenta", "cyan", "white"] 
    print("- -" + " -"*len(plateau)) 
    for line in plateau:
        print("|", end=" ")
        for element in line:
            if element == "●":
                print(" ", end=" ")
            else: # Si l'element est un chiffre
                cprint("●", palette[element], attrs=['bold'], end=" ")
        print("|")
    print("- -" + " -"*len(plateau))

# Renvoie une copie de e
def copie(e):
    copied = []
    for bloc in e:
        coord_list = []
        for coord in bloc:
            coord_list.append(coord)
        copied.append(coord_list)
    return(copied)

# Construit un plateau a partir d'un etat et d'une grille vide
def fill_board(etat):
    board = copie(empty_board)
    for index, bloc in enumerate(etat):
        # Decomposition des coordonnees
        f_line, f_col, s_line, s_col = bloc
        # Ajouts du marqueur(index) du bloc dans la grille
        board[f_line][f_col] = index
        board[s_line][s_col] = index
    return board

# Affiche sequentiellement les plateau menants a la solution
def show_result(solution, e):
    states = [] # Liste des etats, permets de voir s'il y'a des mouvements repetitifs
    if solution != None:
        system("cls")
        show(fill_board(e))
        print("Etat Initial")
        # input()
        time.sleep(2)
        for mouvement in solution:
            system("cls")
            e = mouvement(e) # Produit un nouvel etat
            states.append(e)
            show(fill_board(e)) # Affiche le plateau
            time.sleep(0.5)
        print(f"Temps mis: {(end - start)*1000} ms")
        print(f"Solution en {len(solution)} coups")
        reps = False
        for etat in states:
            if states.count(etat) != 1:
                reps = True
                
        if reps:
            print(f"Au moins un etat se repete")
    else:
        print("Pas de solution")

# Constructions des operateurs disponibles pour les blocs initialises
def make_operateurs(blocs):
    operateurs = [] # Liste des operateurs disponibles
    for bloc in blocs:
        op = nouvel_operateur("move down bloc n°"+str(bloc.codage), partial(Blocs.precond_down, bloc), partial(Blocs.move_down, bloc))
        operateurs.append(op)
        op = nouvel_operateur("move up bloc n°"+str(bloc.codage), partial(Blocs.precond_up, bloc), partial(Blocs.move_up, bloc))
        operateurs.append(op)
        op = nouvel_operateur("move left bloc n°"+str(bloc.codage), partial(Blocs.precond_left, bloc), partial(Blocs.move_left, bloc))
        operateurs.append(op)
        op = nouvel_operateur("move right bloc n°"+str(bloc.codage), partial(Blocs.precond_right, bloc), partial(Blocs.move_right, bloc))
        operateurs.append(op)
    return operateurs
# --------------------------------- Operations sur les blocs---------------------------------

class Blocs:
    codage = 0  # valeur qui represente l'index du bloc
    obstacles = []  # liste de toutes les instances
    initial = []  # liste des coordonees de chaque bloc de l'etat initial

    # Initialisation d'une bloc depend des coords (x1,y1,x2,y2) de ses 2 petits blocs
    def __init__(self, bloc_coord):
        self.codage = Blocs.codage  # Codage est le label associe au bloc
        Blocs.codage += 1
        # ajout de l'instance actuelle a la liste d'obstacles
        Blocs.obstacles.append(self)
        # ajout des coordonnees de l'instance a la liste de coordonnees initiale
        Blocs.initial.append(bloc_coord)

    # ---------------------------------Deplacements des blocs ---------------------------------
    def move_down(self, e):  # Deplacement vers le bas d'un bloc (self) pour un etat e
        # Decomposition des coordonnees du second petit bloc
        _, _, s_line, s_col = e[self.codage]
        # Incrementation de la position, une ligne vers le bas
        new_coords = [s_line, s_col, s_line+1, s_col]
        # print("Deplacement vers le bas du bloc: ", self.codage)
        nouvel_etat = copie(e)
        # Remplace les anciennes coordonnees par les nouvelles
        nouvel_etat[self.codage] = new_coords
        return (nouvel_etat)

    def move_up(self, e):  # Deplacement vers le haut d'un bloc (self) pour un etat e
        # Decomposition des coordonnees du premier petit bloc
        f_line, f_col, _, _ = e[self.codage]
        # Decrementation de la position, une ligne vers le haut
        new_coords = [f_line-1, f_col, f_line, f_col]
        # print("Deplacement vers le haut du bloc: ", self.codage)
        nouvel_etat = copie(e)
        # Remplace les anciennes coordonnees par les nouvelles
        nouvel_etat[self.codage] = new_coords
        return (nouvel_etat)

    def move_right(self, e):  # Deplacement vers le haut d'un bloc (self) pour un etat e
        # Decomposition des coordonnees du second petit bloc
        _, _, s_line, s_col = e[self.codage]
        # Incrementation de la position, une colonne vers la droite
        new_coords = [s_line, s_col, s_line, s_col+1]
        # print("Deplacement vers la droite du bloc: ", self.codage)
        nouvel_etat = copie(e)
        # Remplace les anciennes coordonnees par les nouvelles
        nouvel_etat[self.codage] = new_coords
        return (nouvel_etat)

    def move_left(self, e):  # Deplacement vers le bas du bloc pour un etat e
        # Decomposition des coordonnees du premier petit bloc
        f_line, f_col, _, _ = e[self.codage]
        # Decrementation de la position, une colonne vers la gauche
        new_coords = [f_line, f_col-1, f_line, f_col]
        # print("Deplacement vers la gauche du bloc: ", self.codage)
        nouvel_etat = copie(e)
        # Remplace les anciennes coordonnees par les nouvelles
        nouvel_etat[self.codage] = new_coords
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
# Creation de la grille de jeu
empty_board = make_board(5)

# Initialisation des blocs
Blocs([1, 0, 1, 1])
Blocs([2, 0, 3, 0])
Blocs([1, 2, 2, 2])
Blocs([4, 1, 4, 2])
Blocs([2, 3, 2, 4])
Blocs([0, 4, 1, 4])

# Creation des operateurs pour les blocs initialises
operateurs_disponibles = make_operateurs(Blocs.obstacles)

# Initialisation du Timer
start = time.time() 

# Lancement de la resolution
# solution = recherche_en_profondeur_memoire(Blocs.initial, partial(est_final, len(empty_board)), operateurs_disponibles, [])
# solution = recherche_en_profondeur_limitee(Blocs.initial, partial(est_final, len(empty_board)), operateurs_disponibles, 14)
solution = recherche_en_largeur(Blocs.initial, partial(est_final, len(empty_board)), operateurs_disponibles, [], False)

# Arret du Timer
end = time.time()   

# Affichage graphique de la solution
show_result(solution, Blocs.initial)

