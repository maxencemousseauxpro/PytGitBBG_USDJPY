#!/bin/bash

# URL of the EUR/JPY page
URL="https://www.investing.com/currencies/eur-jpy"

# Download the HTML, extract the price, and save it to price_gbp_usd.txt
curl -s $URL | grep -oP '"instrument-price-last">(\K[\d,.]+)' | head -n 1 > price_gbp_usd.txt

# Display the extracted price
cat price_gbp_usd.txt
