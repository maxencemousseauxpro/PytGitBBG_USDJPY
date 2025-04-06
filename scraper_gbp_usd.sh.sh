#!/bin/bash

# URL of the GBP/USD page
URL="https://www.investing.com/currencies/gbp-usd"

# Download the HTML, extract the price, and save it to price_gbp_usd.txt
curl -s $URL | grep -oP '"instrument-price-last">(\K[\d,.]+)' | head -n 1 > price_gbp_usd.txt

# Display the extracted price
cat price_gbp_usd.txt
