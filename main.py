# 15/03/19
# Projet Unblock Me, IA
# Algorithme recherche_en_largeur
# Début
#   ouverts = { état initial } ; fermés = vide ; succès = faux
#   Tant que (ouverts non vide) et (non succès) faire
#       n = noeud_choisi(ouverts)
#       Si est_final(n) Alors succès=vrai
#       Sinon ouverts = ouverts privé de n
#           fermés = fermés + n
#           Pour chaque successeurs s de n faire
#               Si (s n’est ni dans ouverts ni dans fermés) Alors
#                   ouverts = ouverts + s
#                   père(s) = n
#               Fin si
#           Fin pour
#       Fin si
#   Fin TQ
# Fin
from functools import partial

empty_board = [	[0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
                ]
etat_final = [[0, 0, 0, 0],
              [0, 0, 1, 1],
              [0, 0, 0, 0],
              [0, 0, 0, 0]
              ]


def est_final(e):
    return (e[1][2:4] == [1, 1])


def show_board(e):
    for ligne in e:
        print(ligne)
    print("---------------------------")

# Bloque à déplacer


class Blocs:
    codage = 0  # valeur qui represente l'instance du bloc dans la matrice
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

        # Deplacement vers le bas du bloc self dans l'etat e
    def move_down(self, e):
                # Enumeration des differentes coordonnees du bloc
        f_line, f_col, s_line, s_col = self.fullbloc
        # Le deuxieme bloc devient le premier
        self.first_bloc = [s_line, s_col]
        # Le bloc en dessous devient le deuxieme
        self.second_bloc = [s_line+1, s_col]
        # Mise a jour du bloc complet
        self.fullbloc = self.first_bloc + self.second_bloc
        # Retirer le premier bloc de la matrice et laisser une case vide
        e[f_line][f_col] = 0
        # Rajouter le bloc a sa nouvelle position
        e[s_line+1][s_col] = self.codage
        #print("Deplacement vers le bas du bloc", self.codage)
        return (e)

    def move_up(self, e):
        f_line, f_col, s_line, s_col = self.fullbloc
        # L'ancien 1er bloc devient le nouveau 2eme bloc
        self.second_bloc = [f_line, f_col]
        # L'ancien 2e bloc se place au dessus du nouveau 2eme bloc
        self.first_bloc = [f_line-1, f_col]
        # Mise a jour du bloc complet
        self.fullbloc = self.first_bloc + self.second_bloc
        # Retirer l'ancien second bloc de la matrice et laisser une case vide
        e[s_line][s_col] = 0
        # Rajouter le nouveau 1er bloc a sa nouvelle position
        e[f_line-1][f_col] = self.codage
        # Afficher la matrice
        #print("Deplacement vers le haut du bloc", self.codage)
        return (e)

    def move_right(self, e):
        f_line, f_col, s_line, s_col = self.fullbloc
        # Le deuxieme bloc devient le premier
        self.first_bloc = [s_line, s_col]
        # Le bloc a droite devient le deuxieme
        self.second_bloc = [s_line, s_col+1]
        # Mise a jour du bloc complet
        self.fullbloc = self.first_bloc + self.second_bloc
        # Retirer le premier bloc de la matrice et laisser une case vide
        e[f_line][f_col] = 0
        # Rajouter le bloc a sa nouvelle position
        e[s_line][s_col+1] = self.codage
        # Afficher la matrice
        #print("Deplacement vers la droite du bloc", self.codage)
        return (e)

    def move_left(self, e):
        f_line, f_col, s_line, s_col = self.fullbloc
        # L'ancien 1er bloc devient le nouveau 2eme bloc
        self.second_bloc = [f_line, f_col]
        # L'ancien 2e bloc se place au dessus du nouveau 2eme bloc
        self.first_bloc = [f_line, f_col-1]
        # Mise a jour du bloc complet
        self.fullbloc = self.first_bloc + self.second_bloc
        # Retirer l'ancien second bloc de la matrice et laisser une case vide
        e[s_line][s_col] = 0
        # Rajouter le nouveau 1er bloc a sa nouvelle position
        e[f_line][f_col-1] = self.codage
        # Afficher la matrice
        #print("Deplacement vers la gauche du bloc", self.codage)
        return (e)

    def precond_down(self, e):
        # Verifier que le bloc en dessous du 2eme bloc est un 0
        _, f_col, s_line, s_col = self.fullbloc
        if (s_line == len(e) - 1) or (f_col != s_col):
            #print("Deplacement vers le bas impossible du bloc", self.codage)
            return False
        else:
            if e[s_line+1][s_col] == 0:
                #print("Deplacement vers le bas possible du bloc", self.codage)
                return True
            else:
                #print("Deplacement vers le bas impossible du bloc", self.codage)
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
        if (f_col == 0) or (f_line != s_line):
            #print("Deplacement vers la gauche impossible du bloc", self.codage)
            return False
        else:
            if e[f_line][f_col-1] == 0:
                #print("Deplacement vers la gauche possible du bloc", self.codage)
                return True
            else:
                #print("Deplacement vers la gauche impossible du bloc", self.codage)
                return False
    # Rajouter le nouveau bloc sur le plateau

    def add_to_board(self, matrice):
        # separer les lignes/colonnes
        f_line, f_col, s_line, s_col = self.fullbloc
        matrice[f_line][f_col] = self.codage
        matrice[s_line][s_col] = self.codage
        # Afficher la matrice
        print("Ajout du bloc", self.codage)
        show_board(matrice)


# Matrice?board
# getattr(Board, "bloctest")
# Obstables
bloc_1 = Blocs([1, 0], [1, 1])
bloc_2 = Blocs([0, 2], [1, 2])
bloc_3 = Blocs([2, 2], [2, 3])
bloc_4 = Blocs([3, 1], [3, 2])


def copie_matrice(m):
    return [
        [m[0][0], m[0][1], m[0][2], m[0][3]],
        [m[1][0], m[1][1], m[1][2], m[1][3]],
        [m[2][0], m[2][1], m[2][2], m[2][3]],
        [m[3][0], m[3][1], m[3][2], m[3][3]]
    ]


# ---------------------------------TEST---------------------------------
# Initialisation
etat_initial = copie_matrice(empty_board)
Blocs.add_to_board(bloc_1, etat_initial)
Blocs.add_to_board(bloc_2, etat_initial)
Blocs.add_to_board(bloc_3, etat_initial)
Blocs.add_to_board(bloc_4, etat_initial)


# Renvoie les mouvements possibles de chaque bloc
def possible_moves(e):
    moves_list = []
    for bloc in [bloc_1, bloc_2, bloc_3, bloc_4]:
        if (Blocs.precond_down(bloc, e)):
            moves_list.append("down_"+str(bloc.codage))
        if (Blocs.precond_left(bloc, e)):
            moves_list.append("left_"+str(bloc.codage))
        if (Blocs.precond_right(bloc, e)):
            moves_list.append("right_"+str(bloc.codage))
        if (Blocs.precond_up(bloc, e)):
            moves_list.append("up_"+str(bloc.codage))
    return moves_list

# DEplacement des blocs
# precond_left3 = Blocs.precond_left(bloc_3, etat_initial)


print(possible_moves(etat_initial))
show_board(etat_initial)
Blocs.move_left(bloc_3, etat_initial)
print(possible_moves(etat_initial))
show_board(etat_initial)
Blocs.move_left(bloc_3, etat_initial)
print(possible_moves(etat_initial))
show_board(etat_initial)
Blocs.move_left(bloc_4, etat_initial)
print(possible_moves(etat_initial))
show_board(etat_initial)


# show_board(left_3(etat_initial))
# show_board(left_3(etat_initial))
# show_board(down_2(etat_initial))
# show_board(right_1(etat_initial))
# show_board(right_1(etat_initial))


# Operateurs disponibles
# operateurs_disponibles = [
#     nouvel_operateur("down_1", precond, down_1),
#     nouvel_operateur("down_2", precond, down_2),
#     nouvel_operateur("down_3", precond, down_3),
#     nouvel_operateur("up_1", precond, up_1),
#     nouvel_operateur("up_2", precond, up_2),
#     nouvel_operateur("up_3", precond, up_3),
#     nouvel_operateur("left_1", precond, left_1),
#     nouvel_operateur("left_2", precond, left_2),
#     nouvel_operateur("left_3", precond, left_3),
#     nouvel_operateur("right_1", precond, right_1),
#     nouvel_operateur("right_2", precond, right_2),
#     nouvel_operateur("right_3", precond, right_3),
# ]
