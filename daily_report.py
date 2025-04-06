import numpy as np
import time
import os
from datetime import datetime

# Function to read prices from the files (already scraped data)
def read_prices(filename):
    with open(filename, 'r') as file:
        prices = file.readlines()
    return [float(price.strip()) for price in prices]

# Function to calculate volatility, high, low, and average for a currency pair
def calculate_metrics(prices):
    volatility = np.std(prices)
    high = max(prices)
    low = min(prices)
    average = np.mean(prices)
    return volatility, high, low, average

# List of the currency pairs and their respective price files
currency_pairs = ['USD/JPY', 'EUR/USD', 'GBP/USD', 'USD/CHF', 'EUR/JPY']
prices_dict = {
    'USD/JPY': 'price.txt',  # USD/JPY price file
    'EUR/USD': 'price_eur_usd.txt',  # EUR/USD price file
    'GBP/USD': 'price_gbp_usd.txt',  # GBP/USD price file
    'USD/CHF': 'price_usd_chf.txt',  # USD/CHF price file
    'EUR/JPY': 'price_eur_jpy.txt',  # EUR/JPY price file
}

# Function to generate the daily report
def generate_daily_report():
    report = f"Daily Report - {datetime.now().strftime('%Y-%m-%d')}\n\n"
    
    for pair in currency_pairs:
        prices = read_prices(prices_dict[pair])
        volatility, high, low, average = calculate_metrics(prices)
        report += f"{pair}:\n"
        report += f"  Volatility: {volatility:.4f}\n"
        report += f"  High: {high:.4f}\n"
        report += f"  Low: {low:.4f}\n"
        report += f"  Average: {average:.4f}\n\n"

    # Save the report to a .txt file
    report_filename = f"daily_report_{datetime.now().strftime('%Y-%m-%d')}.txt"
    with open(report_filename, 'w') as file:
        file.write(report)

    print("Daily report generated successfully.")

# Run the report generation
generate_daily_report()
