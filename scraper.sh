#!/bin/bash

# URL de la page USD/JPY
URL="https://www.investing.com/currencies/usd-jpy"

# Télécharger le HTML, extraire le prix et le sauvegarder dans price.txt
curl -s $URL | grep -oP '"last":\K[\d.]+ ' | head -n 1 > price.txt

# Afficher le prix extrait
cat price.txt
