import requests
from dotenv import load_dotenv

import csv
import json
import os
import datetime

#TODO datetime module


now = datetime.datetime.now()
#print("CHECK OUT AT", now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"))



#TODO: create dollar conversion function

def to_usd(my_price):
  return "${0:,.2f}".format(my_price)

#TODO loads environment variables set in a ".env" file, including the value of the ALPHAVANTAGE_API_KEY variable
load_dotenv()

# see: https://www.alphavantage.co/support/#api-key
api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
#print("API KEY: " + api_key)

symbol = input("Please specify a stock symbol: ")

# see: https://www.alphavantage.co/documentation/#daily (or a different endpoint, as desired)
# TODO: assemble the request url to get daily data for the given stock symbol...

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey=(api_key"

# TODO: use the "requests" package to issue a "GET" request to the specified url, and store the JSON response in a variable...

response = requests.get(request_url)
#print(type(response))       # <class 'requests.models.Response'>
#print(response.status_code) #200
#print(response.text)        #str




# TODO: further parse the JSON response...

parsed_response = json.loads(response.text)
last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]


# TODO: traverse the nested response data structure to find the latest closing price and other values of interest...


tsd = parsed_response["Time Series (Daily)"] #short for time series daily

dates = list(tsd.keys()) #create list from tsd date keys, and sort to ensure latest day is first.
latest_day =  dates[0] #make dynamic

latest_price_usd = tsd[latest_day]["4. close"]

#TODO get high price for each day

high_prices = []
low_prices =[]

for date in dates:
  high_price = tsd[date]["2. high"]
  low_price = tsd[date]["3. low"]
  high_prices.append(float(high_price))
  low_prices.append(float(low_price))

recent_high = max(high_prices)
recent_low = min(low_prices)


# INFO OUTPUTS
#

# TODO: write response data to a CSV file

#csv_file_path = "data/prices.csv"  # a relative filepath

csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

with open(csv_file_path, "w") as csv_file:  # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader()  # uses fieldnames set above
    for date in dates:#loop through each day
       daily_prices =tsd[date]
       writer.writerow({
          "timestamp": date,
          "open": daily_prices["1. open"],
          "high": daily_prices["2. high"],
           "low": daily_prices["3. low"],
           "close": daily_prices["4. close"],
           "volume": daily_prices["5. volume"]
          })


    #writer.writerow({"city": "New York", "name": "Mets"})
    #writer.writerow({"city": "Boston", "name": "Red Sox"})
    #writer.writerow({"city": "New Haven", "name": "Ravens"})





# TODO: further revise the example outputs below to reflect real information
print("-----------------")
print(f"STOCK SYMBOL: {symbol}")
print("RUN AT: ", now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"))
print("-----------------")
print(f"LATEST DAY OF AVAILABLE DATA: {last_refreshed}")
print(f"LATEST DAILY CLOSING PRICE: {to_usd(float(latest_price_usd))}")
print(f"RECENT HIGH:{to_usd(float(recent_high))} ")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-----------------")
print("RECOMMENDATION: Buy!")
print("RECOMMENDATION REASON: Because the latest closing price is within threshold XYZ etc., etc. and this fits within your risk tolerance etc., etc.")
print("-----------------")
print(f"WRITING DATA TO CSV {csv_file_path}")
print("-----------------")
print(" HAPPY INVESTING!")
print("-----------------")
