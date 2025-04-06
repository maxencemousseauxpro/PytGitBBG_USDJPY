#!/bin/bash

# URL of the EUR/USD page
URL="https://www.investing.com/currencies/eur-usd"

# Download the HTML, extract the price, and save it to price_eur_usd.txt
curl -s $URL | grep -oP '"instrument-price-last">(\K[\d,.]+)' | head -n 1 > price_eur_usd.txt

# Display the extracted price
cat price_eur_usd.txt
