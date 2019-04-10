from random import shuffle

# construction d'un nouvel opérateur


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
    for l in (e):
        print(l)
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
        for l in (e):
            print(l)
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
    #   ouverts = { état initial } ; fermés = vide ; succes = faux
    #   Tant que (ouverts non vide) et (non succes) faire
    ouverts = [e]
    fermes = []
    # ouverts.append(e)
    while (e != [] and not succes):
        noeud = ouverts[-1]
        # Si est_final(n) Alors succès=vrai
        if est_final(noeud):
            return []
        else:
            # Sinon ouverts = ouverts privé de n
            ouverts.remove(noeud)
            #fermés = fermés + n
            fermes.append(noeud)
            #           Pour chaque successeurs s de n faire
            operateurs = operateurs_applicables(os, e)
            for o in operateurs:

                ne = applique_operateur(o, e)
            #   Si (s n’est ni dans ouverts ni dans fermés) Alors
                if (ne not in ouverts) and (ne not in fermes):
                    #       ouverts = ouverts + s
                    ouverts.append(ne)
            #       père(s) = n
                pere = n
            #               Fin si
            #           Fin pour
            #       Fin si
            #   Fin TQ
            # Fin


# recherche_en_largeur(e, est_final, os, [], False)
