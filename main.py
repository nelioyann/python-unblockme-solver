# 15/03/19
# Projet Unblock Me, IA

from functools import partial
from resolution import recherche_en_profondeur_lim_mem, recherche_en_profondeur_limitee, nouvel_operateur, recherche_en_profondeur_memoire, recherche_en_largeur

empty_board = [	[0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
                ]


def est_final(e):
    if (e[1][2:4] == [1, 1]) or (e[1] == [0, 1, 1, 0]) or (e[1] == [1, 1, 0, 0]):
        return (True)
    else:
        return(False)


def show_board(e):
    for ligne in e:
        print(ligne)
    print("---------------------------")


def copie_matrice(m):
    return [
        [m[0][0], m[0][1], m[0][2], m[0][3]],
        [m[1][0], m[1][1], m[1][2], m[1][3]],
        [m[2][0], m[2][1], m[2][2], m[2][3]],
        [m[3][0], m[3][1], m[3][2], m[3][3]]
    ]
# Bloque à déplacer


class Blocs:
    codage = 0  # valeur qui represente l'instance du bloc dans la matrice
    obstacles = []  # liste de toutes les instances
    # Initialisation d'une instance composee de 2 petits blocs
    # Chaque petit bloc est une liste de coordonnees (x,y)

    def __init__(self, first_bloc, second_bloc):
        # First Bloc est le bloc au plus a gauche/en haut a l'interieur de la matrice
        # Second Bloc est le bloc au plus a droite/en bas a l'interieur de la matrice
        self.first_bloc = first_bloc
        self.second_bloc = second_bloc
        self.fullbloc = first_bloc + second_bloc
        Blocs.codage += 1
        # Codage est la valeur qui sera utilise pour RPZ le bloc a l'interieur de la matrice
        self.codage = Blocs.codage
        Blocs.obstacles.append(self)

        # Deplacement vers le bas du bloc self dans l'etat e
    def move_down(self, e):  # * RAS
        # Enumeration des differentes coordonnees du bloc
        s_line, s_col = self.second_bloc
        # L'ancien deuxieme bloc devient le nouveau premier bloc
        self.first_bloc = [s_line, s_col]
        # Le bloc en dessous devient le nouveau deuxieme bloc
        self.second_bloc = [s_line+1, s_col]
        # Mise a jour du bloc complet
        self.fullbloc = self.first_bloc + self.second_bloc
        print("Deplacement vers le bas du bloc", self.codage)
        print("Etat à instant t: ")
        board = copie_matrice(empty_board)
        fill_board(Blocs.obstacles, board)
        return (board)

    def move_up(self, e):
        f_line, f_col = self.first_bloc
        # L'ancien 1er bloc devient le nouveau 2eme bloc
        self.second_bloc = [f_line, f_col]
        # L'ancien 2e bloc se place au dessus du nouveau 2eme bloc
        self.first_bloc = [f_line-1, f_col]
        # Mise a jour du bloc complet
        self.fullbloc = self.first_bloc + self.second_bloc
        # Afficher la matrice
        print("Deplacement vers le haut du bloc", self.codage)
        print("Etat à instant t: ")
        board = copie_matrice(empty_board)
        fill_board(Blocs.obstacles, board)
        return (board)

    def move_right(self, e):
        s_line, s_col = self.second_bloc
        # L'ancien deuxieme bloc devient le nouveau premier
        self.first_bloc = [s_line, s_col]
        # Le bloc a droite devient le deuxieme
        self.second_bloc = [s_line, s_col+1]
        # Mise a jour du bloc complet
        self.fullbloc = self.first_bloc + self.second_bloc
        print("Deplacement vers la droite du bloc", self.codage)
        print("Etat à instant t: ")
        board = copie_matrice(empty_board)
        fill_board(Blocs.obstacles, board)
        return (board)

    def move_left(self, e):
        f_line, f_col = self.first_bloc
        # L'ancien 1er bloc devient le nouveau 2eme bloc
        self.second_bloc = [f_line, f_col]
        # L'ancien 2e bloc se place au dessus du nouveau 2eme bloc
        self.first_bloc = [f_line, f_col-1]
        # Mise a jour du bloc complet
        self.fullbloc = self.first_bloc + self.second_bloc
        # Afficher la matrice
        print("Deplacement vers la gauche du bloc", self.codage)
        print("Etat à instant t: ")
        board = copie_matrice(empty_board)
        fill_board(Blocs.obstacles, board)
        return (board)

    def precond_down(self, e):
        # Verifier que le bloc en dessous du 2eme bloc est un 0
        _, f_col, s_line, s_col = self.fullbloc
        if (s_line == len(e) - 1) or (f_col != s_col):
            #print("Deplacement vers le bas impossible du bloc", self.codage)
            return False
        else:
            if e[s_line+1][s_col] == 0:
                return True
            else:
                return False

    def precond_right(self, e):
        # Verifier que le bloc qui suit le 2eme bloc est un 0
        f_line, _, s_line, s_col = self.fullbloc
        if (s_col == len(e) - 1) or (f_line != s_line):
            #print("Deplacement vers la droite impossible du bloc(orientation)", self.codage)
            return False
        else:
            if e[s_line][s_col+1] == 0:
                #print("Deplacement vers la droite possible du bloc", self.codage)
                return True
            else:
                #print("Deplacement vers la droite impossible du bloc(pas vide)", self.codage)
                return False

    def precond_up(self, e):
        # Verifier que le bloc avant le 1er bloc est un 0
        f_line, f_col, _, s_col = self.fullbloc
        if (f_line == 0) or (f_col != s_col):
            #print("Deplacement vers le haut impossible du bloc", self.codage)
            return False
        else:
            if e[f_line-1][f_col] == 0:
                #print("Deplacement vers le haut possible du bloc", self.codage)
                return True
            else:
                #print("Deplacement vers le haut impossible du bloc", self.codage)
                return False

    def precond_left(self, e):
        # Verifier que le bloc avant le 1er bloc est un 0
        f_line, f_col, s_line, _ = self.fullbloc
        # Si le premier bloc est contre les bords ou si le bloc n'est pas horizontal
        if (f_col == 0) or (f_line != s_line):
            return False
        else:
            # Si la case a gauche est vide
            if e[f_line][f_col-1] == 0:
                #print("Deplacement vers la gauche possible du bloc", self.codage)
                return True
            # Si la case de gauche est occupee
            else:
                #print("Deplacement vers la gauche impossible du bloc", self.codage)
                return False

    # Rajouter le nouveau bloc sur le plateau
    def add_to_board(self, matrice):
        # separer les lignes/colonnes
        f_line, f_col, s_line, s_col = self.fullbloc
        matrice[f_line][f_col] = self.codage
        matrice[s_line][s_col] = self.codage


# Matrice?board
# getattr(Board, "bloctest")
# * Obstables
Blocs([1, 0], [1, 1])
Blocs([0, 2], [0, 3])
Blocs([1, 2], [2, 2])
Blocs([1, 3], [2, 3])


# ---------------------------------TEST---------------------------------
# Initialisation
etat_initial = copie_matrice(empty_board)
# Rajout des blocs dans la matrice


def fill_board(obstacles, matrice):
    for bloc in obstacles:
        Blocs.add_to_board(bloc, matrice)
    show_board(matrice)


fill_board(Blocs.obstacles, etat_initial)

# Operateurs disponibles
operateurs_disponibles = []
for bloc in Blocs.obstacles:
    # nom prrecond effet
    op = nouvel_operateur(
        "move down bloc"+str(bloc.codage), partial(Blocs.precond_down, bloc), partial(Blocs.move_down, bloc))
    operateurs_disponibles.append(op)
    op = nouvel_operateur(
        "move up bloc"+str(bloc.codage), partial(Blocs.precond_up, bloc), partial(Blocs.move_up, bloc))
    operateurs_disponibles.append(op)
    op = nouvel_operateur(
        "move left bloc"+str(bloc.codage), partial(Blocs.precond_left, bloc), partial(Blocs.move_left, bloc))
    operateurs_disponibles.append(op)
    op = nouvel_operateur(
        "move right bloc"+str(bloc.codage), partial(Blocs.precond_right, bloc), partial(Blocs.move_right, bloc))
    operateurs_disponibles.append(op)


# print(recherche_en_profondeur_limitee(
#     etat_initial, est_final, operateurs_disponibles, 5))
# print(recherche_en_profondeur_lim_mem(
#     etat_initial, est_final, operateurs_disponibles, 7, []))
print(recherche_en_largeur(
    etat_initial, est_final, operateurs_disponibles, [], False))
