#!/bin/bash

URL="https://www.x-rates.com/calculator/?from=EUR&to=USD"
OUTPUT_FILE="data.csv"

# Récupérer le taux de change EUR/USD
rate=$(curl -s $URL | grep -oP '(?<=<span class="ccOutputTrail">)[^<]+(?=<\/span>)')

# Afficher le taux de change récupéré
echo "Taux de change EUR/USD : $rate"

# Enregistrer le taux de change et la date dans data.csv
timestamp=$(date +"%Y-%m-%d %H:%M:%S")
echo "$timestamp,$rate" >> $OUTPUT_FILE
