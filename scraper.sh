#!/bin/bash

# URL of the USD/JPY page
URL="https://www.investing.com/currencies/usd-jpy"

# Download the HTML, extract the price, and save it to price.txt
curl -s $URL | grep -oP '"last":"\K[\d.]+(?=")' | head -n 1 > price.txt

# Display the extracted price
cat price.txt
