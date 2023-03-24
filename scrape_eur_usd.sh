#!/bin/bash

URL="https://www.x-rates.com/calculator/?from=EUR&to=USD&amount=1"
OUTPUT_DIR="/home/parallels/A4"
OUTPUT_FILE="$OUTPUT_DIR/data.csv"

# Créez le dossier de sortie si nécessaire
mkdir -p "$OUTPUT_DIR"

# Créez un nouveau fichier data.csv avec les en-têtes de colonne appropriées si nécessaire
if [ ! -f "$OUTPUT_FILE" ] || ! grep -q "timestamp,rate" "$OUTPUT_FILE"; then
    echo "timestamp,rate" > $OUTPUT_FILE
fi

# Récupérer le taux de change EUR/USD
rate=$(curl -s "$URL" | grep -oP '(?<=<span class="ccOutputRslt">)[^<]+(?=<span class="ccOutputTrail">)')
decimal=$(curl -s "$URL" | grep -oP '(?<=<span class="ccOutputTrail">)[^<]+(?=<\/span>)')

# Concaténer le taux et les décimales
complete_rate="${rate}${decimal}"

# Afficher le taux de change récupéré
echo "Taux de change EUR/USD : $complete_rate"
# Enregistrer le taux de change et la date dans data.csv
timestamp=$(date +"%Y-%m-%d %H:%M:%S")
echo "$timestamp,$complete_rate" >> $OUTPUT_FILE
