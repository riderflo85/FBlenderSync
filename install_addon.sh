#!/bin/bash

BLENDER_ADDONS_PATH=$1
ZIP_FILE=../fblender_sync.zip


if ! test -d "$BLENDER_ADDONS_PATH"; then
    echo "Le chemin ${BLENDER_ADDONS_PATH} n'existe pas !"
    exit 1
else
    ./makearchive.sh

    if ! test -f "$ZIP_FILE"; then
        echo "Erreur : Le fichier ZIP '$ZIP_FILE' n'existe pas."
        exit 1
    fi

    unzip "$ZIP_FILE" -d "$BLENDER_ADDONS_PATH"
    # Vérifie si la décompression s'est bien passée
    if [ $? -eq 0 ]; then
        echo "Le fichier '$ZIP_FILE' a été décompressé avec succès dans '$BLENDER_ADDONS_PATH'."
    else
        echo "Erreur : La décompression du fichier '$ZIP_FILE' a échoué."
        exit 1
    fi
fi
