
import requests
import json

#NUMBERS ARE OFF FOR LATEST CLOSE


def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

#INFO INPUTS

request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo"
response = requests.get(request_url)
#print(type(response)) #> <class 'requests.models.Response'>
#print(response.status_code) #>200
#print(response.text)

parsed_response = json.loads(response.text)

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

tsd = parsed_response["Time Series (Daily)"]

dates = list(tsd.keys()) #TODO ASSUME LATEST DAT IS FIRST
latest_day = dates[0]

latest_close = tsd[latest_day]["4. close"]




#get high price from each day
high_prices = []

low_prices = []
#recent_high = max(high_prices)
for date in dates:
    high_price = tsd[date]["2. high"]
    high_prices.append(float(high_price))

    low_price = tsd[date]["3. low"]
    low_prices.append(float(low_price))
recent_high = max(high_prices)
recent_low = min(low_prices)



print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print("LATEST DAY: " + last_refreshed) #########
print("LATEST CLOSE: " + to_usd(float(latest_close))) ##########
print("RECENT HIGH: " + to_usd(float(recent_high)))
print("RECENT LOW: " + to_usd(float(recent_low)))
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")