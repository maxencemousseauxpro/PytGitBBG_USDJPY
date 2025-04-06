import requests
from datetime import datetime

# URL to scrape USD/JPY price from Investing.com
URL = "https://www.investing.com/currencies/usd-jpy"

# Function to scrape the price
def scrape_usd_jpy():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        
        # Find the price using the specific HTML structure (this needs to be dynamic based on actual structure)
        start = response.text.find('"last":') + len('"last":')
        end = response.text.find(',', start)
        price = response.text[start:end].strip()
        return price
    except Exception as e:
        print(f"Error scraping data: {e}")
        return None

# Function to save report daily
def save_daily_report():
    price = scrape_usd_jpy()
    
    if price:
        report_date = datetime.now().strftime('%Y-%m-%d')
        report_content = f"USD/JPY Daily Report - {report_date}\n\n"
        report_content += f"Current Price: {price} USD/JPY\n"
        
        # Save the report to a file
        with open(f"daily_report_{report_date}.txt", "w") as f:
            f.write(report_content)
        print(f"Report saved for {report_date}")
    else:
        print("Failed to retrieve the price. Report not saved.")

# Run the function to generate the report
if __name__ == "__main__":
    save_daily_report()
