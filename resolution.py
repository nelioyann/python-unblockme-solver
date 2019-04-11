from random import shuffle

# construction d'un nouvel opérateur

empty_board = [	['x', 'x', 'x', 'x'],
                ['x', 'x', 'x', 'x'],
                ['x', 'x', 'x', 'x'],
                ['x', 'x', 'x', 'x']
                ]


# def copie_matrice(m):
#     return [
#         [m[0][0], m[0][1], m[0][2], m[0][3], m[0][4]],
#         [m[1][0], m[1][1], m[1][2], m[1][3], m[1][4]],
#         [m[2][0], m[2][1], m[2][2], m[2][3], m[2][4]],
#         [m[3][0], m[3][1], m[3][2], m[3][3], m[3][4]],
#         [m[4][0], m[4][1], m[4][2], m[4][3], m[4][4]]
#     ]
def copie_matrice(m):
    return [
        [m[0][0], m[0][1], m[0][2], m[0][3]],
        [m[1][0], m[1][1], m[1][2], m[1][3]],
        [m[2][0], m[2][1], m[2][2], m[2][3]],
        [m[3][0], m[3][1], m[3][2], m[3][3]]
    ]


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


def fill_board(etat):
    instance = copie_matrice(empty_board)
    for index, bloc in enumerate(etat):
        f_line, f_col, s_line, s_col = bloc
        instance[f_line][f_col] = index
        instance[s_line][s_col] = index
    show_board(instance)


def nouvel_operateur(nom, precond, effet):
    return (nom, precond, effet)

# accès aux éléments d'un opérateur


def nom_operateur(o):
    return o[0]


def precond_operateur(o):
    return o[1]


def action_operateur(o):
    return o[2]

# est-ce qu'un opérateur o est applicable à un état e ?


def operateur_applicable(o, e):
    precond = precond_operateur(o)
    return (precond(e))

# sélection des opérateurs de os qui sont applicables à e


def operateurs_applicables(os, e):
    res = []
    for o in os:
        if operateur_applicable(o, e):
            res.append(o)
    print("")
    print("Liste des operateurs applicables à l'état suivant: ")
    # fill_board(e)
    print("Operateurs applicables: ")
    for x in res:
        print("-", x[0])
    return res


# application d'un opérateur o à un état e
def applique_operateur(o, e):
    action = action_operateur(o)
    return (action(e))


# recherche en profondeur brutale : boucle à l'infini le plus souvent
def recherche_en_profondeur(e, est_final, os):
    if est_final(e):
        return []
    else:
        operateurs = operateurs_applicables(os, e)
        for o in operateurs:
            # print(nom_operateur(o))
            ne = applique_operateur(o, e)
            chemin = recherche_en_profondeur(ne, est_final, os)
            if chemin != None:
                return [nom_operateur(o)] + chemin
        return None


# recherche en profondeur limitée
def recherche_en_profondeur_limitee(e, est_final, os, profondeur):
    if est_final(e):
        print("etat final")
        # fill_board(e)
        return []
    elif profondeur == 0:
        return None
    else:
        print("Debut d'un nouveau cycle")
        operateurs = operateurs_applicables(os, e)
        for o in operateurs:
            ne = applique_operateur(o, e)
            chemin = recherche_en_profondeur_limitee(
                ne, est_final, os, profondeur-1)
            if chemin != None:
                return [nom_operateur(o)] + chemin
        return None


# recherche avec mémoire
def recherche_en_profondeur_memoire(e, est_final, os, déjà):
    if est_final(e):
        return []
    elif e in déjà:
        print("e in deja")
        return None
    else:
        déjà.append(e)
        operateurs = operateurs_applicables(os, e)
        for o in operateurs:
            ne = applique_operateur(o, e)
            for l in ne:
                print(l)
            print()
            chemin = recherche_en_profondeur_memoire(ne, est_final, os, déjà)
            if chemin != None:
                # print([nom_operateur(o)] + chemin)
                return [nom_operateur(o)] + chemin
        return None


# recherche en profondeur limitée et avec mémoire
def recherche_en_profondeur_lim_mem(e, est_final, os, prof, déjà):
    if est_final(e):
        return []
    elif prof == 0:
        return None
    elif e in déjà:
        return None
    else:
        déjà.append(e)
        operateurs = operateurs_applicables(os, e)
        for o in operateurs:
            ne = applique_operateur(o, e)
            chemin = recherche_en_profondeur_lim_mem(
                ne, est_final, os, prof-1, déjà)
            print("Chemin = ", chemin)
            if chemin != None:
                return [nom_operateur(o)] + chemin
        return None


def recherche_en_largeur(e, est_final, os, fermés, succes):
    ouverts = [e]
    fermes = []
    while (e != [] and not succes):
        noeud = ouverts[0]
        if est_final(noeud):
            print("FINAL")
            succes = True
        else:
            ouverts.remove(noeud)
            fermes.append(noeud)
            operateurs = operateurs_applicables(os, noeud)
            for o in operateurs:
                sub_noeud = applique_operateur(o, e)
                if (sub_noeud not in ouverts) and (sub_noeud not in fermes):
                    ouverts.append(sub_noeud)

# recherche_en_largeur(e, est_final, os, [], False)
