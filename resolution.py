
# construction d'un nouvel opérateur
def nouvel_operateur (nom,precond,effet):
    return (nom,precond,effet)

# accès aux éléments d'un opérateur
def nom_operateur (o):
    return o[0]
def precond_operateur (o):
    return o[1]
def action_operateur (o):
    return o[2]

# est-ce qu'un opérateur o est applicable à un état e ?
def operateur_applicable (o,e):
    precond = precond_operateur(o)
    return (precond(e))

# sélection des opérateurs de os qui sont applicables à e
def operateurs_applicables (os,e):
    res = []
    for o in os:
        if operateur_applicable(o,e):
            res.append(o)
    return res


# application d'un opérateur o à un état e
def applique_operateur (o,e):
    action = action_operateur(o)
    return (action(e))


# recherche en profondeur brutale : boucle à l'infini le plus souvent
def recherche_en_profondeur (e,est_final,os):
    if est_final(e):
        return []
    else:
        operateurs = operateurs_applicables(os,e)
        for o in operateurs:
            #print(nom_operateur(o))
            ne = applique_operateur(o,e)
            chemin = recherche_en_profondeur(ne,est_final,os)
            if chemin != None:
                return [ nom_operateur(o) ] + chemin
        return None


# recherche en profondeur limitée
def recherche_en_profondeur_limitee (e,est_final,os,profondeur):
    if est_final(e):
        return []
    elif profondeur == 0:
        return None
    else:
        operateurs = operateurs_applicables(os,e)
        for o in operateurs:
            ne = applique_operateur(o,e)
            chemin = recherche_en_profondeur_limitee(ne,est_final,os,profondeur-1)
            if chemin != None:
                return [ nom_operateur(o) ] + chemin
        return None


# recherche avec mémoire
def recherche_en_profondeur_memoire (e,est_final,os,déjà):
    if est_final(e):
        return []
    elif e in déjà:
        return None
    else:
        déjà.append(e)
        operateurs = operateurs_applicables(os,e)
        for o in operateurs:
            ne = applique_operateur(o,e)
            chemin = recherche_en_profondeur_memoire(ne,est_final,os,déjà)
            if chemin != None:
                return [ nom_operateur(o) ] + chemin
        return None


# recherche en profondeur limitée et avec mémoire
def recherche_en_profondeur_lim_mem (e,est_final,os,prof,déjà):
    if est_final(e):
        return []
    elif prof==0:
        return None
    elif e in déjà:
        return None
    else:
        déjà.append(e)
        operateurs = operateurs_applicables(os,e)
        for o in operateurs:
            ne = applique_operateur(o,e)
            chemin = recherche_en_profondeur_lim_mem(ne,est_final,os,prof-1,déjà)
            if chemin != None:
                return [ nom_operateur(o) ] + chemin
        return None


