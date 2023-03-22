#!/bin/bash

url="https://www.worldometers.info/"
content=$(curl -s "$url")

population=$(echo "$content" | grep -oP 'Current World Population : <strong>\K[^<]*')

timestamp=$(date +"%Y-%m-%d %H:%M:%S")

echo "$timestamp,$population" >> data.csv
#!/bin/bash

url="https://www.worldometers.info/"
content=$(curl -s "$url")

population=$(echo "$content" | grep -oP 'Current World Population : <strong>\K[^<]*')

echo "Population mondiale actuelle : $population"
