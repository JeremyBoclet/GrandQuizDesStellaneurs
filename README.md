# GrandQuizDesStellaneurs
1 - Installation d'un interpreteur Python
    (https://www.python.org/downloads/)

2 - Ajouter python et pip au PATH du pc

3 - Installer Pycharms (IDE pour dev)

4 - Installer les dépendances / packages (pip install ou directement dans pycharms)
    - pandas, pip, pyexcel, pygame, Django .....


Pour ajouter / modifier le quiz

- Les boutons sont des images stockées dans le dossier .\Assets
- Les joueurs sont des images stockées dans le dossier .\Assets\Player (Ils doivent être référencé dans le fichier excel Players.ods)
- Les questions images sont stockées dans le dossier .\Assets\Annexe (il y a également un sous dossier "Zoom" qui représente l'image une fois cliqué. Si elle n'existe pas alors l'image sera juste étirée)
- La source des questions audio sont stockées dans le dossier .\Assets\Sounds et sont au format .mp3

Toutes les questions sont stockées dans le fichier ods questions.ods
    - Un onglet par thème + 1 onglet finale avec la category_name correspondant au joueur possédant le thème (pour le comptage de point)
    - ExternalName est le nom + extention de l'image ou du son
    - TypeQuestion correspond au type de la question (audio = audio, image = img, texte = txt)

Dans le code les questions sont stockées dans des listes alimentées dans le script : Screen_Round.py
    Chaque thème doit avoir sa correspondance dans le fichier excel ainsi qu'une image de bouton associée dans .\Assets
    L'objet "Button" à pour paramètre le nom du thème, la position X, Y, ainsi que sa taille en longeur puis en largueur
    