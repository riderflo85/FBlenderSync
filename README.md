Voici un exemple de fichier README pour votre projet FBlenderSync :

# FBlenderSync

FBlenderSync est une application Python pour Blender qui permet aux utilisateurs de stocker et télécharger leurs fichiers Blender sur le cloud Dropbox. Cette application permet aux utilisateurs de Blender qui changent d'ordinateur de retrouver leurs fichiers facilement, de les télécharger pour les ouvrir automatiquement avec Blender et de les envoyer sur leur compte Dropbox.

## Prérequis

- Un compte Dropbox
- Python 3.x
- La bibliothèque Python Requests

## Installation

1. Clonez le dépôt GitHub FBlenderSync sur votre machine. \
OU [Téléchargez](https://github.com/riderflo85/FBlenderSync/archive/refs/heads/main.zip) le dépôt .zip 
```
git clone https://github.com/votre-nom/FBlenderSync.git
```

2. Installez la bibliothèque Python Requests à l'aide de pip.
```
pip install requests
```

## Utilisation

1. Ouvrez Blender et sélectionnez "Edit" > "Preferences" > "Add-ons" > "Install".
2. Sélectionnez le fichier "FBlenderSync.zip" dans le dossier "FBlenderSync" que vous avez cloné.
3. Activez l'add-on en cochant la case à côté de "FBlenderSync".
4. Allez sur le site [Dropbox App Console](https://www.dropbox.com/developers/apps) et créez une nouvelle application. Vous aurez besoin de générer un jeton d'accès pour autoriser votre application à accéder à votre compte Dropbox.
5. Dans Blender, allez dans "FBlenderSync" > "Settings" et entrez votre jeton d'accès Dropbox dans le champ prévu à cet effet. \
\
!!! A FINIR DE RÉDIGER !!!

6. Pour téléverser un fichier sur Dropbox, sélectionnez "FBlenderSync" > "Upload File" et sélectionnez le fichier à téléverser. Le fichier sera téléversé dans le dossier par défaut spécifié dans les paramètres.
7. Pour télécharger un fichier depuis Dropbox, sélectionnez "FBlenderSync" > "Download File" et sélectionnez le fichier à télécharger. Le fichier sera téléchargé dans le dossier par défaut spécifié dans les paramètres et ouvert automatiquement avec Blender.

## Utilisation de la bibliothèque Python Requests

Pour interagir avec l'API Dropbox, FBlenderSync utilise la bibliothèque Python Requests. Cette bibliothèque est une alternative légère et populaire au SDK Python de Dropbox et est couramment utilisée dans de nombreux projets Python. En utilisant Requests, nous évitons d'ajouter une dépendance supplémentaire à installer au niveau global sur la machine de l'utilisateur, ce qui peut rendre l'installation et la configuration de l'application plus complexes pour l'utilisateur final.

Si vous souhaitez utiliser une autre bibliothèque pour interagir avec l'API Dropbox, vous pouvez modifier le code en conséquence. Veuillez noter que cela peut nécessiter l'installation de dépendances supplémentaires.

## Licence

FBlenderSync est sous licence MIT. Veuillez consulter le fichier LICENSE pour plus d'informations.