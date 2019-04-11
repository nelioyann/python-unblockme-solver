from random import shuffle

# construction d'un nouvel opérateur

empty_board = [	['x', 'x', 'x', 'x'],
                ['x', 'x', 'x', 'x'],
                ['x', 'x', 'x', 'x'],
                ['x', 'x', 'x', 'x']
                ]


def show(matrice):
    print("- - - - - -")
    for bloc in matrice:
        ligne = " "
        for element in bloc:
            ligne += str(element) + " "
        print(f"|{ligne}|")
    print("- - - - - -")


def copie(matrice):
    copied = []
    for bloc in matrice:
        coord_list = []
        for coord in bloc:
            coord_list.append(coord)
        copied.append(coord_list)
    return(copied)

# * Forme la grille a partir d'un etat


def fill_board(etat):
    instance = copie(empty_board)
    for index, bloc in enumerate(etat):
        f_line, f_col, s_line, s_col = bloc
        instance[f_line][f_col] = index
        instance[s_line][s_col] = index
    show(instance)


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
    # print("")
    print("Liste des operateurs applicables à l'état suivant: ")
    fill_board(e)
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
        # print("Debut d'un nouveau cycle")
        operateurs = operateurs_applicables(os, e)
        for o in operateurs:
            ne = applique_operateur(o, e)
            chemin = recherche_en_profondeur_limitee(
                ne, est_final, os, profondeur-1)
            if chemin != None:
                return [action_operateur(o)] + chemin
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
            # print("Chemin = ", chemin)
            if chemin != None:
                return [action_operateur(o)] + chemin
        return None


def recherche_en_largeur(e, est_final, os, fermés, succes):
    ouverts = [e]
    fermes = []
    while (ouverts != [] and not succes):
        noeud = ouverts[0]
        if est_final(noeud):
            print("FINAL")
            succes = True
        else:
            print(ouverts)
            ouverts.remove(noeud)
            fermes.append(noeud)
            operateurs = operateurs_applicables(os, noeud)
            for o in operateurs:
                sub_noeud = applique_operateur(o, noeud)
                print("Sub Noeud", sub_noeud)
                fill_board(sub_noeud)
                if (sub_noeud not in ouverts) and (sub_noeud not in fermes):
                    ouverts.append(sub_noeud)
    print("Ouverts = ", ouverts)
    print("Fermes = ", fermes)
    for k in fermes:
        fill_board(k)
# recherche_en_largeur(e, est_final, os, [], False)
