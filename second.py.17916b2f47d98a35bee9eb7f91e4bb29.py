# 15/03/19
# 10/04/19
# ? Changement de la nature des etats
# ** Etat = [[],[],[],[]]

# Projet Unblock Me, IA

from functools import partial
from resolution import recherche_en_profondeur_lim_mem, recherche_en_profondeur_limitee, nouvel_operateur, recherche_en_profondeur_memoire, recherche_en_largeur

empty_board = [	['x', 'x', 'x', 'x'],
                ['x', 'x', 'x', 'x'],
                ['x', 'x', 'x', 'x'],
                ['x', 'x', 'x', 'x']
                ]


def est_final(e):
    if (e[0] == [1, 2, 1, 3]):
        return (True)
    else:
        return(False)


# def show_board(e):
#     print(" - - - -")
#     for l in e:
#         print(f"|{l[0]} {l[1]} {l[2]} {l[3]} {l[4]}|")
#         # print(" _ _ _ _")
#     print(" - - - -")
def show_board(e):
    print(" - - - -")
    for l in e:
        print(f"|{l[0]} {l[1]} {l[2]} {l[3]}|")
        # print(" _ _ _ _")
    print(" - - - -")


def copie(matrice):
    copied = []
    for bloc in matrice:
        coord_list = []
        for coord in bloc:
            coord_list.append(coord)
        copied.append(coord_list)
    return(copied)


def copie_etat(m):
    return [
        [m[0][0], m[0][1], m[0][2], m[0][3]],
        [m[1][0], m[1][1], m[1][2], m[1][3]],
        [m[2][0], m[2][1], m[2][2], m[2][3]],
        [m[3][0], m[3][1], m[3][2], m[3][3]],
        [m[4][0], m[4][1], m[4][2], m[4][3]]
    ]


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
    initial = []
    # Initialisation d'une instance composee de 2 petits blocs
    # Chaque petit bloc est une liste de coordonnees (x,y)

    def __init__(self, bloc_coord):
        # Codage est la valeur qui sera utilise pour RPZ le bloc a l'interieur de la matrice
        self.codage = Blocs.codage
        Blocs.codage += 1
        Blocs.obstacles.append(self)
        Blocs.initial.append(bloc_coord)

        # Deplacement vers le bas du bloc self dans l'etat e
    def move_down(self, e):  # * RAS
        # Enumeration coordonnees du second carre
        _, _, s_line, s_col = e[self.codage]
        new_bloc = [s_line, s_col, s_line+1, s_col]
        print("Deplacement vers le bas du bloc", self.codage)
        nouvel_etat = copie_etat(e)
        nouvel_etat[self.codage] = new_bloc
        return (nouvel_etat)

    def move_up(self, e):
        f_line, f_col, _, _ = e[self.codage]
        new_bloc = [f_line-1, f_col, f_line, f_col]
        print("Deplacement vers le haut du bloc", self.codage)
        nouvel_etat = copie_etat(e)
        nouvel_etat[self.codage] = new_bloc
        return (nouvel_etat)

    def move_right(self, e):
        _, _, s_line, s_col = e[self.codage]
        new_bloc = [s_line, s_col, s_line, s_col+1]
        print("Deplacement vers la droite du bloc", self.codage)
        nouvel_etat = copie_etat(e)
        nouvel_etat[self.codage] = new_bloc
        return (nouvel_etat)

    def move_left(self, e):
        f_line, f_col, _, _ = e[self.codage]
        new_bloc = [f_line, f_col-1, f_line, f_col]
        print("Deplacement vers la gauche du bloc", self.codage)
        nouvel_etat = copie_etat(e)
        nouvel_etat[self.codage] = new_bloc
        return (nouvel_etat)

    def precond_down(self, e):
        print("codage", self.codage)
        print("e", e)
        # Verifier que le bloc en dessous du 2eme bloc est un 0
        _, f_col, s_line, s_col = e[self.codage]
        # Si le bloc est contre un bord ou s'il n'est pas vertical
        if (s_line == len(empty_board) - 1) or (f_col != s_col):
            #print("Deplacement vers le bas impossible du bloc", self.codage)
            return False
        else:
            for bloc in e:
                for carre in [bloc[:2], bloc[2:]]:
                    if carre == [s_line+1, s_col]:
                        return False
            # Si aucun des bloc de l'etat n'occupe l'espace que l'on souhaite occupe
            return True

    def precond_right(self, e):
        # Verifier que le bloc qui suit le 2eme bloc est un 0
        f_line, _, s_line, s_col = e[self.codage]
        if (s_col == len(empty_board) - 1) or (f_line != s_line):
            return False
        else:
            for bloc in e:
                for carre in [bloc[:2], bloc[2:]]:
                    if carre == [s_line, s_col+1]:
                        return False
            # Si aucun des bloc de l'etat n'occupe l'espace que l'on souhaite occupe
            return True

    def precond_up(self, e):
        # Verifier que le bloc avant le 1er bloc est un 0
        f_line, f_col, _, s_col = e[self.codage]
        if (f_line == 0) or (f_col != s_col):
            return False
        else:
            for bloc in e:
                for carre in [bloc[:2], bloc[2:]]:
                    if carre == [f_line-1, f_col]:
                        return False
            # Si aucun des bloc de l'etat n'occupe l'espace que l'on souhaite occupe
            return True

    def precond_left(self, e):
        # Verifier que le bloc avant le 1er bloc est un 0
        f_line, f_col, s_line, _ = e[self.codage]
        if (f_col == 0) or (f_line != s_line):
            return False
        else:
            for bloc in e:
                for carre in [bloc[:2], bloc[2:]]:
                    if carre == [f_line, f_col-1]:
                        return False
            # Si aucun des bloc de l'etat n'occupe l'espace que l'on souhaite occupe
            return True


def fill_board(etat):
    instance = copie_matrice(empty_board)
    for index, bloc in enumerate(etat):
        f_line, f_col, s_line, s_col = bloc
        instance[f_line][f_col] = index
        instance[s_line][s_col] = index
    show_board(instance)


# Matrice?board
# getattr(Board, "bloctest")


# for bloc in Blocs.obstacles:
#     print(f"Bloc n-{bloc.codage}")
#     print(Blocs.precond_up(bloc, etat_futur))
#     print()
# etatfutur = []
# ---------------------------------TEST---------------------------------
# Initialisation
# * Obstables
Blocs([1, 0, 1, 1])
Blocs([0, 2, 0, 3])
Blocs([1, 2, 2, 2])
Blocs([1, 3, 2, 3])
Blocs([3, 2, 3, 3])

etat_initial = Blocs.initial
# fill_board(etat_initial)

# Rajout des blocs dans la matrice

# etat_futur = Blocs.move_down(Blocs.obstacles[3], etat_futur)
# fill_board(etat_futur, etat_initial)
# fill_board(etat_futur)
# print(etat_futur)
# etat_futur = Blocs.move_left(Blocs.obstacles[1], etat_futur)
# print(etat_futur)
# fill_board(etat_futur)
# etat_futur = Blocs.move_left(Blocs.obstacles[1], etat_futur)
# print(etat_futur)
# fill_board(etat_futur)
# fill_board(etat_futur, etat_initial)


# Operateurs disponibles
operateurs_disponibles = []
for bloc in Blocs.obstacles:
    # nom prrecond effet
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


print(recherche_en_profondeur_limitee(
    etat_initial, est_final, operateurs_disponibles, 7))
# fill_board(etat_initial)
# print(recherche_en_profondeur_lim_mem(
#     etat_initial, est_final, operateurs_disponibles, 7, []))
# print(recherche_en_largeur(
#     etat_initial, est_final, operateurs_disponibles, [], False))
