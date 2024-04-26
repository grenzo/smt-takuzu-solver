# Résolveur de Takuzu

## Utilisation

Ce script Python est conçu pour résoudre des grilles Takuzu. Assurez-vous d'avoir Z3 installé sur votre ordinateur avant de l'utiliser. Vous aurez également besoin de la bibliothèque Tkinter pour afficher les étapes de la résolution.

Pour installer Z3, vous pouvez suivre les instructions sur le site officiel : [Z3 GitHub](https://github.com/Z3Prover/z3).

Pour installer Tkinter, vous pouvez exécuter la commande suivante :

```
sudo apt-get install python3-tk
```

Pour résoudre une grille Takuzu, exécutez la commande suivante dans votre terminal :

```
python3 takuzu2.py nom_grille.txt [-a]
```

Remplacez `nom_grille.txt` par le chemin vers votre fichier de grille Takuzu à résoudre.

Si vous souhaitez afficher les étapes de la résolution, ajoutez l'option `-a`.

Le résultat de la résolution sera écrit dans un fichier nommé `nom_grille_sol.txt`. Ce fichier contiendra la solution de la grille.

## Exemple

Supposons que vous ayez une grille Takuzu nommée `grille.txt` que vous souhaitez résoudre. Voici comment vous pouvez utiliser ce script pour afficher les étapes de la résolution :

```
python3 takuzu.py grille.txt -a
```

Une fois que le script a terminé son exécution, vous trouverez la solution dans un fichier appelé `grille_sol.txt`.

Vous pouvez également utiliser le script sans l'option `-a` pour simplement obtenir la solution sans afficher les étapes.
