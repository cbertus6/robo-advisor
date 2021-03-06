
import csv
import json
import os
import requests

from dotenv import load_dotenv

load_dotenv()

def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

#
# INFO INPUTS
#

api_key = os.environ.get("ALPHAVANTAGE_API_KEY")

symbol = input("Please enter the stock symbol of the company you would like to lookup: ")

request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + str(symbol) + "&apikey=" + str(api_key)

response = requests.get(request_url)
# print(type(response))
# print(response.status_code)
# print(response.text)

if 'Error' in response.text:
    print("Please make sure the stock symbol inputted is valid.")
    exit()

parsed_response = json.loads(response.text)

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

# provides current time and date
import datetime
now = datetime.datetime.now()

# created a list of dates
tsd = parsed_response["Time Series (Daily)"]
dates = list(tsd.keys()) #TODO: consider sorting to ensure dates are in order

latest_day = dates[0]

latest_close = tsd[latest_day]["4. close"]

# finding maximum of all the high prices and minimum of all the low prices
high_prices = []
low_prices = []

for date in dates:
    high_price = tsd[date]["2. high"]
    high_prices.append(float(high_price))
    low_price = tsd[date]["3. low"]
    low_prices.append(float(low_price))

recent_high = max(high_prices)
recent_low = min(low_prices)


# breakpoint()

#
# INFO OUTPUTS
#

# Writing information in CSV file
csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

with open(csv_file_path, "w", newline="") as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader() # uses fieldnames set above
    for date in dates:
        daily_prices = tsd[date]
        writer.writerow({
            "timestamp": date,
            "open": daily_prices["1. open"],
            "high": daily_prices["2. high"],
            "low": daily_prices["3. low"],
            "close": daily_prices["4. close"],
            "volume": daily_prices["5. volume"]
         })

print("-------------------------")
print("SELECTED SYMBOL: " + symbol)
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: " + now.strftime('%Y-%m-%d %I:%M %p'))
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
if float(latest_close) > (float(recent_high) * 0.9):
   print("RECOMMENDATION: SELL NOW! THE CURRENT PRICE IS TOO HIGH!")
elif float(latest_close) < (float(recent_low) * 1.1):
    print("RECOMMENDATION: BUY NOW! THE CURRENT PRICE IS TOO LOW")
else:
    print("RECOMMENDATION: HOLD STEADY, DON'T MAKE A DECISION YET")
print("-------------------------")
print(f"WRITING DATA TO CSV: {csv_file_path}...")
print("-------------------------")
print("BUY LOW, SELL HIGH!")
print("-------------------------")

# csv_file_path = "data/prices.csv" # a relative filepath

import matplotlib.pyplot as plt

#X = []
#Y = []

closing_prices = []

for date in dates:
    closing_price = tsd[date]["4. close"]
    closing_prices.append(float(closing_price))
   
plt.plot(dates, closing_prices)

# Labeling the X-axis 
plt.xlabel('Dates') 

# Labeling the Y-axis 
plt.ylabel('Prices') 

# Give a title to the graph
plt.title(symbol + ' Price Data') 

plt.show()