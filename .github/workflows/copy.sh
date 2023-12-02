#!/bin/bash

# Chemin du fichier source (à ajuster selon votre dépôt)
SOURCE_FILE=".github/workflows/install.sh"

# Chemin de destination dans le répertoire stage-install
# DESTINATION_DIR="$1/stage-install"

# # echo ${{github.workspace}}
# ls -la
# # Copie du fichier
# cp $SOURCE_FILE $DESTINATION_DIR

mkdir -p stage-install/
cp $SOURCE_FILE stage-install/prerun.sh
chmod +x stage-install/prerun.sh

# ls ./stage-install
