# DerekBot

## Attention 

Ce bot discord a été créé dans le but d'un cour de python, c'est donc mon tout premier bot, des bugs sont a prévoir.

## Description du bot

DerekBot comme son homologue Derek Bum aime le chaos, et quoi de mieux pour faire regner le chaos qu'un bot stupide avec des fonctions
stupides ?

Si vous etes prêts sortez vos

> Kitchen guns.

et allons voir ce bot de plus près

![Kitchen Gun](https://c.tenor.com/ocEiJ47ed9wAAAAC/kitchen-gun.gif)

## Prérequis a installer

Comme tout bot codé en python, il dépend de quelques librairies.
Les 4 ci-dessous sont les seules neccessaires pour faire tourné cette chose.

- Discord : pip install -U discord.
- DotEnv : pip install -U python-dotenv.
- Requests : pip install -U requests.
- JSon : pip install -U json.

## Fonctions

Ci-dessous vous trouverez une liste des commandes du bot triées par familles.
Toutes les commandes sont éxécutées avec le préfix (&).

les <> sont les parametres obligatoires.
les [] sont optionnels.

***

### Basiques

> hello \[user].

Affiche un message de bonjour a l'utilisateur mentionné.
Par defaut personne n'est mentionné, l'auteur de la commande sera la cible.

> spotify \[user].

Affiche le status spotify de l'utilisateur si il/elle est actif/ve sur spotify.
Par defaut personne n'est mentionné, l'auteur de la commande sera la cible.

> help \[commande].

Affiche les détails d'une commande.

***

### Utiles

> jeu \<difficulté>.

Jouez au mastermind avec DerekBot, deviner le nombre a 4 chiffre de XavBot et vous avez gagné. difficultés : 1 = Facile | 2 = Normal |
3 = Difficile | 4 = Impossible.
X = Mauvais chiffre | ~ = Bon chiffre pas au bon endroit | O = Bon chiffre au bon endroit.

> meteo \<adresse>.

Derek vous donne la météo pour les 4 prochaines heures a l'adresse entrée

### Emotes

> addMoji \<emote1> \<emote2> ... \<emoteN>.

Permet d'ajouter une emote a la liste des emotes utilisables par DerekBot. /!\ les differentes emotes doivent êtres séparées par un espace.

> mojiesList.

Demande a DerekBot d'afficher la liste des emotes qu'il a en mémoire.

> daleatoire.

Demande a DerekBot d'afficher une emote aléatoire parmis celles qu'il a en mémoire.

***

### Quotes

> derekNorris.

DerekBot vous racontera une blague sur chuck norris.

> derekSagesse.

DerekBot vous aidera dans votre vie avec une citation inspirante de Kayne West.

> derekBall [Message]

Posez une question a Derekbot et il vous répondra avec toute sa sagesse.

***

### CHAOS

> ping [user]

Mentionne un nombre aléatoire de fois l'utilisateur.
Par defaut personne n'est mentionné, l'auteur de la commande sera la cible (mais pourquoi vous feriez ça ?).

> russe

Fais un tir de roullette russe.
