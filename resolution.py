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
            chemin = recherche_en_profondeur_limitee(ne, est_final, os, profondeur - 1)
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

# Recherche en largeur
# Cette classe conservera le parent de chaque noeud parcouru
# Une fois qu'on aura trouve le noeud solution on effectuera une remontee progressive des parents jusqu'au noeud racine (label = 0)
class Noeud:
    label = -1  #pour que label commence a 0 une fois initialisee
    arbre = [] # instances des noeuds
    mouvements = [] # mouvements/operateurs a l'origine de chaque instance (arbre et mouvemnts sont de meme taille)
    etats = [] # coordonnees des blocs pour chaque instances/noeuds parcourus

    def __init__(self, etat, operateur):
        Noeud.label += 1
        self.label = Noeud.label
        self.etat = etat
        Noeud.etats.append(etat)
        Noeud.arbre.append(self)
        Noeud.mouvements.append(operateur)


# ouverts est la file d'attente
# fermes -> noeud parcourus
def recherche_en_largeur(etat_initial, est_final, os, fermes, succes):
    ouverts = [etat_initial]
    Noeud(etat_initial, None)
    count = -1
    while (ouverts != [] and not succes):
        count += 1 # Nombre de loop effectues
        noeud = ouverts[0]  # First In First Out
        if est_final(noeud):
            # On a acces qu'aux coordonnees de l'etat final et non pas a son instance
            # On peut retrouver le label du noeud en le situant dans la listes des etats
            final_label = Noeud.etats.index(noeud)
            # On retrouve l'instance grace au label
            noeud_final = Noeud.arbre[final_label]
            parents = [] # Liste des labels de tous les parents
            label = noeud_final.label
            parents.append(label)
            # Tant que le label de la racine n'est pas atteint
            while label !=0 :
                # Recupere le parent du label actuel
                pere = Noeud.arbre[label].parent
                # Le parent devient le nouveau label actuel
                label = pere
                # On rajoute le parent a la liste
                parents.append(pere)
            # On inverse la liste pour qu'elle commence par la racine
            parents.reverse()
            # print("Padre", parents[1:])
            solution = [] # Liste des mouvements qui menent a la solution
            # L'etat initial parents[0] n'est a l'origine d'aucun operateur, on l'omets donc
            for label in parents[1:]:
                solution.append(Noeud.mouvements[label])
            return solution
        else:
            del ouverts[0]
            fermes.append(noeud)
            operateurs = operateurs_applicables(os, noeud)
            successeurs = []
            for operateur in operateurs:
                successeurs.append(applique_operateur(operateur, noeud))
            # Label du parent des prochains noeuds successeurs
            parent_id = count
            # Pour chaque successuer du noeud et chaque operateur qui lui est associe
            for operateur, successeur in zip(operateurs, successeurs):
                # Si ce successeur ne fait pas partie de la file d'attente et s'il est nouveau
                if (successeur not in ouverts) and (successeur not in fermes):
                    # Rajouter ce noeud en fin de file d'attente
                    ouverts.append(successeur)
                    noeud_successeur = Noeud(successeur, action_operateur(operateur) )
                    noeud_successeur.parent = parent_id
