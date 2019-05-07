from random import shuffle

# construction d'un nouvel opérateur

# empty_board = [['x', 'x', 'x', 'x'], ['x', 'x', 'x', 'x'],
#                ['x', 'x', 'x', 'x'], ['x', 'x', 'x', 'x']]


# def show(matrice):
#     print("- - - - - -")
#     for bloc in matrice:
#         ligne = " "
#         for element in bloc:
#             ligne += str(element) + " "
#         print(f"|{ligne}|")
#     print("- - - - - -")


# def copie(matrice):
#     copied = []
#     for bloc in matrice:
#         coord_list = []
#         for coord in bloc:
#             coord_list.append(coord)
#         copied.append(coord_list)
#     return (copied)


# * Forme la grille a partir d'un etat


# def fill_board(etat):
#     instance = copie(empty_board)
#     for index, bloc in enumerate(etat):
#         f_line, f_col, s_line, s_col = bloc
#         instance[f_line][f_col] = index
#         instance[s_line][s_col] = index
#     show(instance)


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
    # print("Liste des operateurs applicables à l'état suivant: ")
    # fill_board(e)
    # print("Operateurs applicables: ")
    # for x in res:
    #     print("-", x[0])
    # res.reverse()
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
            chemin = recherche_en_profondeur_limitee(ne, est_final, os,
                                                     profondeur - 1)
            if chemin != None:
                return [action_operateur(o)] + chemin
        return None


# recherche avec mémoire


def recherche_en_profondeur_memoire(e, est_final, os, déjà):
    if est_final(e):
        return []
    elif e in déjà:
        return None
    else:
        déjà.append(e)
        print(f"Taille deja = {len(déjà)}")
        operateurs = operateurs_applicables(os, e)
        for o in operateurs:
            ne = applique_operateur(o, e)
            chemin = recherche_en_profondeur_memoire(ne, est_final, os, déjà)
            if chemin != None:
                return [action_operateur(o)] + chemin
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
            chemin = recherche_en_profondeur_lim_mem(ne, est_final, os,
                                                     prof - 1, déjà)
            # print("Chemin = ", chemin)
            if chemin != None:
                return [action_operateur(o)] + chemin
        return None


class Noeud:
    label = -1  #pour que label commence a 0 une fois initialisee
    arbre = [] #instances
    mouvements = []
    etats = []

    def __init__(self, etat, operateur):
        Noeud.label += 1
        self.label = Noeud.label
        self.etat = etat
        Noeud.etats.append(etat)
        Noeud.arbre.append(self)
        Noeud.mouvements.append(operateur)


# ouverts est la file
# fermes -> noeud parcourus
def recherche_en_largeur(etat_initial, est_final, os, fermes, succes):
    ouverts = [etat_initial]
    Noeud(etat_initial, None)
    count = -1
    while (ouverts != [] and not succes):
        count += 1
        noeud = ouverts[0]  # First In First Out
        # current_node = Noeud()
        if est_final(noeud):
            # print()
            final_label = Noeud.etats.index(noeud)
            noeud_final = Noeud.arbre[final_label]
            # noeud_final.parent = count
            # print(f"FINAL parent est n{noeud_final.parent}")
            # print(f"FINAL noeud n{count}")
            # print(f"Taille fermes = {len(fermes)}")
            parents = []
            label = noeud_final.label
            parents.append(label)
            while label !=0 :
                pere = Noeud.arbre[label].parent
                label = pere
                parents.append(pere)
            parents.reverse()
            # print("Padre", parents[1:])
            solution = []
            for label in parents[1:]:
                solution.append(Noeud.mouvements[label])
            # print("Solution", solution)
            return solution
            # succes = True
        else:
            del ouverts[0]
            # print(f"OUVERTS = {ouverts}")
            fermes.append(noeud)
            # print(f"Taille fermes = {len(fermes)}")
            operateurs = operateurs_applicables(os, noeud)
            successeurs = []
            # print()
            # print("Applicables")
            for operateur in operateurs:
                successeurs.append(applique_operateur(operateur, noeud))
                # print(f"- {nom_operateur(operateur)}")
            # Pour chaque successuer du noeud
            parent_id = count
            # print(f"Id du parent = {parent_id}")
            # print(f"Taille fermes = {len(fermes)}")
            for operateur, successeur in zip(operateurs, successeurs):
                # Si ce successeur ne fait pas partie de la file d'attente et s'il est nouveau
                if (successeur not in ouverts) and (successeur not in fermes):
                    # print(f"Operateur selectionne = {nom_operateur(operateur)}")
                        
                    # Rajouter ce noeud en fin de file d'attente
                    ouverts.append(successeur)
                    noeud_successeur = Noeud(successeur,action_operateur(operateur) )
                    # print(f"Noeud initialise= {noeud_successeur.label}")
                    noeud_successeur.parent = parent_id
                    # print(f"Le parent du noeud {noeud_successeur.label} est {parent_id}")
                    # successeur_id = Noeud.label
                    # print("Noeud successuer Initialisee")
                    # Noeud(successeur).parent = noeud
                    # Noeud(successeur).parent = Noeud(noeud)

                    # chemin = recherche_en_largeur(
                    #     successeur, est_final, os, fermes, False)
                    # print(nom_operateur(operateur))
                    # if chemin != None:
                    #     return [action_operateur(operateur)] + chemin
                    # return None
    

# def recherche_en_largeur(e, est_final, os, fermes, succes):
#     ouverts = [e]
#     while (ouverts != [] and not succes):
#         noeud = ouverts[0]
#         if est_final(noeud):
#             # print(f"Nombre de noeuds parcourus = {len(ouverts)}")
#             print("FINAL")
#             return []
#         else:
#             ouverts.remove(noeud)
#             fermes.append(noeud)
#             print(f"Taille fermes = {len(fermes)}")
#             operateurs = operateurs_applicables(os, noeud)
#             print("Applicables")
#             for op in operateurs:
#                 print(nom_operateur(op))
#             for o in operateurs:
#                 print(f"Operateur selectionne = {nom_operateur(op)}")
#                 successeur = applique_operateur(o, noeud)
#                 if (successeur not in ouverts) and (successeur not in fermes):
#                     ouverts.append(successeur)
#                     chemin = recherche_en_largeur(
#                         successeur, est_final, os, fermes, False)
#                     print(nom_operateur(o))
#                     if chemin != None:
#                         return [action_operateur(o)] + chemin
#                     return None

# recherche_en_largeur(e, est_final, os, [], False)
