#!/bin/bash

# Chemin du fichier source (à ajuster selon votre dépôt)
SOURCE_FILE=".github/workflows/install.sh"

# Chemin de destination dans le répertoire stage-install
DESTINATION_DIR="${{ github.workspace }}/${{ inputs.custom-pi-gen-dir }}/stage-install"

# Copie du fichier
cp $SOURCE_FILE $DESTINATION_DIR