#!/bin/bash

# URL of the USD/CHF page
URL="https://www.investing.com/currencies/usd-chf"

# Download the HTML, extract the price, and save it to price_usd_chf.txt
curl -s $URL | grep -oP '"instrument-price-last">(\K[\d,.]+)' | head -n 1 > price_gbp_usd.txt

# Display the extracted price
cat price_gbp_usd.txt
