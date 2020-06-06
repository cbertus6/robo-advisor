
import requests
import json

def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

#
# INFO INPUTS
#

request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo"

response = requests.get(request_url)
# print(type(response))
# print(response.status_code)
# print(response.text)

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

# finding maximum of all the high prices
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

print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: " + now.strftime('%Y-%m-%d %I:%M %p'))
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")