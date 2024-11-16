# Puissance 4 (Ingescape Circle - Whiteboard)

Projet réalisé par **Bastien LALANNE** et **Marc GUEDON** dans le câdre de la 3ème année d'école d'ingénieur en Systèmes Robotiques et Intéractifs à l'UPSSITECH.
Il s'agit du jeu Puissance 4 développé grâce à la plateforme Ingescape Circle et avec le Whiteboard.

## Installation

Copiez les dossiers ```Puissance4_View``` et ```Puissance4_Controller``` dans le dossier ```sandbox``` de votre installation Ingescape. \
**ATTENTION** : Assurez-vous que le dossier ```Puissance4_View/data``` reste dans ce dossier !

## Instructions

### Démarrer le jeu

Vous pouvez démarrer Ingescape Circle v4, et ouvrir ```puissance4.igssystem```. Il faudra également démarrer le Whiteboard. \
Assurez-vous que le port soit le même dans Circle, dans le Whiteboard, ainsi que dans le fichier main de ```Puissance4_View```, et de ```Puissance4_Controller```. \
Pour démarrer le jeu, il faut d'abord exécuter le fichier ```main.py``` de ```Puissance4_View```, puis celui de ```Puissance4_Controller```. \
Le jeu va alors automatiquement démarrer.

### Jouer au jeu

Pour jouer à notre Puissance 4, toutes les commandes sont décrites directement sur le whiteboard mais aussi dans le chat du whiteboard. \
Ainsi, dans la partie choix de la couleur, il faut appuyer sur les flèches gauche/droite (←/→) pour changer la couleur puis sur "Entrer" pour valider le choix. \
Dans la partie jeu, il faut appuyer sur les flèches gauche/droite (←/→) pour changer de colonne puis sur "Entrer" ou sur la flèche bas (↓) pour valider la colonne.

## Bugs

Le jeu peut finir par être bloqué si l'utilisateur spam la touche flèche bas. Nous avons déjà limité la présence de ce bug, mais il est malheureusement toujours présent.