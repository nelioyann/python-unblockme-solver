# 15/03/19
# Projet Unblock Me, IA

# Etat initial
# [	[0, 0, 0, 0],
#   [0, 0, 0, 0],
#   [0, 0, 0, 0],
#   [0, 0, 0, 0]
#             ]
matrice = [	[0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
            ]
etat_final = [	[0, 0, 0, 0],
               [0, 0, 1, 1],
               [0, 0, 0, 0],
               [0, 0, 0, 0]
               ]


def est_final(matrice):
    return (matrice[1][2:4] == [1, 1])


def show_board(matrice):
    for ligne in matrice:
        print(ligne)
    print("---------------------------")

# Bloque à déplacer


class Blocs:
    codage = 0  # valeur qui represente l'instance du bloc dans la matrice
    # Initialisation d'une instance composee de 2 petits blocs

    def __init__(self, first_bloc, second_bloc):
        self.first_bloc = first_bloc
        self.second_bloc = second_bloc
        self.fullbloc = first_bloc + second_bloc
        Blocs.codage += 1
        self.codage = Blocs.codage
        # # Afficher la matrice
        # show_board(matrice)

    def move_down(self):
        f_line, f_col, s_line, s_col = self.fullbloc
        # Le deuxieme bloc devient le premier
        self.first_bloc = [s_line, s_col]
        # Le bloc en dessous devient le deuxieme
        self.second_bloc = [s_line+1, s_col]
        # Mise a jour du bloc complet
        self.fullbloc = self.first_bloc + self.second_bloc
        # Retirer le premier bloc de la matrice et laisser une case vide
        matrice[f_line][f_col] = 0
        # Rajouter le bloc a sa nouvelle position
        matrice[s_line+1][s_col] = self.codage
        # Afficher la matrice
        print("Deplacement vers le bas du bloc", self.codage)
        show_board(matrice)

    def move_up(self):
        f_line, f_col, s_line, s_col = self.fullbloc
        # L'ancien 1er bloc devient le nouveau 2eme bloc
        self.second_bloc = [f_line, f_col]
        # L'ancien 2e bloc se place au dessus du nouveau 2eme bloc
        self.first_bloc = [f_line-1, f_col]
        # Mise a jour du bloc complet
        self.fullbloc = self.first_bloc + self.second_bloc
        # Retirer l'ancien second bloc de la matrice et laisser une case vide
        matrice[s_line][s_col] = 0
        # Rajouter le nouveau 1er bloc a sa nouvelle position
        matrice[f_line-1][f_col] = self.codage
        # Afficher la matrice
        print("Deplacement vers le haut du bloc", self.codage)
        show_board(matrice)

    def move_right(self):
        f_line, f_col, s_line, s_col = self.fullbloc
        # Le deuxieme bloc devient le premier
        self.first_bloc = [s_line, s_col]
        # Le bloc a droite devient le deuxieme
        self.second_bloc = [s_line, s_col+1]
        # Mise a jour du bloc complet
        self.fullbloc = self.first_bloc + self.second_bloc
        # Retirer le premier bloc de la matrice et laisser une case vide
        matrice[f_line][f_col] = 0
        # Rajouter le bloc a sa nouvelle position
        matrice[s_line][s_col+1] = self.codage
        # Afficher la matrice
        print("Deplacement vers la droite du bloc", self.codage)
        show_board(matrice)

    def move_left(self):
        f_line, f_col, s_line, s_col = self.fullbloc
        # L'ancien 1er bloc devient le nouveau 2eme bloc
        self.second_bloc = [f_line, f_col]
        # L'ancien 2e bloc se place au dessus du nouveau 2eme bloc
        self.first_bloc = [f_line, f_col-1]
        # Mise a jour du bloc complet
        self.fullbloc = self.first_bloc + self.second_bloc
        # Retirer l'ancien second bloc de la matrice et laisser une case vide
        matrice[s_line][s_col] = 0
        # Rajouter le nouveau 1er bloc a sa nouvelle position
        matrice[f_line][f_col-1] = self.codage
        # Afficher la matrice
        print("Deplacement vers la gauche du bloc", self.codage)
        show_board(matrice)

    def precond_down(self):
        # Verifier que le bloc en dessous du 2eme bloc est un 0
        f_line, f_col, s_line, s_col = self.fullbloc
        if (s_line == len(matrice) - 1) or (f_col != s_col):
            print("Out of range", len(matrice))
            return False
        else:
            if matrice[s_line+1][s_col] == 0:
                return True
            else:
                return False

    def precond_right(self):
        # Verifier que le bloc qui suit le 2eme bloc est un 0
        f_line, f_col, s_line, s_col = self.fullbloc
        if (s_col == len(matrice) - 1) or (f_line != s_line):
            print("Out of range", len(matrice))
            return False
        else:
            if matrice[s_line][s_col+1] == 0:
                return True
            else:
                return False

    def precond_up(self):
        # Verifier que le bloc avant le 1er bloc est un 0
        f_line, f_col, s_line, s_col = self.fullbloc
        if (f_line == 0) or (f_col != s_col):
            print("Out of range", len(matrice))
            return False
        else:
            if matrice[f_line-1][f_col] == 0:
                return True
            else:
                return False

    def precond_left(self):
        # Verifier que le bloc avant le 1er bloc est un 0
        f_line, f_col, s_line, s_col = self.fullbloc
        if (f_col == 0) or (f_line != s_line):
            print("Out of range", len(matrice))
            return False
        else:
            if matrice[f_line][f_col-1] == 0:
                return True
            else:
                return False
    # Rajouter le nouveau bloc sur le plateau

    def add_to_board(self):
        # separer les lignes/colonnes
        f_line, f_col, s_line, s_col = self.fullbloc
        matrice[f_line][f_col] = self.codage
        matrice[s_line][s_col] = self.codage
        # Afficher la matrice
        print("Ajout du bloc", self.codage)
        show_board(matrice)


# Obstables
bloc_1 = Blocs([1, 0], [1, 1])
# bloc_2 = Blocs([2, 1], [2, 2])
bloc_2 = Blocs([0, 2], [1, 2])


# show_board(matrice)
Blocs.add_to_board(bloc_1)
Blocs.add_to_board(bloc_2)
# Blocs.add_to_board(bloc_3)
# print(bloc_1.__dict__)
# show_board(matrice)
# print(Blocs.precond_down(bloc_2))
Blocs.move_down(bloc_2)
# print(Blocs.precond_down(bloc_2))
Blocs.move_down(bloc_2)
print(Blocs.precond_right(bloc_1))
Blocs.move_right(bloc_1)
print(Blocs.precond_right(bloc_1))
Blocs.move_right(bloc_1)
print(Blocs.precond_left(bloc_1))
Blocs.move_left(bloc_1)
print(Blocs.precond_left(bloc_1))
Blocs.move_left(bloc_1)
print(Blocs.precond_left(bloc_1))
print(Blocs.precond_down(bloc_2))
