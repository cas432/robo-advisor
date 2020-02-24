import json
import csv
import os
import datetime
import time
from dotenv import load_dotenv
import requests

load_dotenv()

#USD function

symbols = []
high_prices = []
low_prices = []

x=0

def to_usd(my_price):
    return "${0:,.2f}".format(my_price)


api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
#Get stock symbol





while True: 
    symbol = input("Please input your stock ticker symbol of choice: ")

        
    if symbol == "DONE":
        if len(symbols) == 0:
            print("\n    Please enter at least one stock symbol")
        else:
            break

    elif float(len(symbol)) <= 5 and symbol.isalpha():
        request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
        response = requests.get(request_url)

        if "Error Message" in response.text:
            print("\n    OOPS!: Sorry! This is not a existing stock symbol.\n")
            
        else:
            symbols.append(symbol)
     

    else:
        print("\n    Please enter a valid symbol or type 'DONE' to finish adding stocks. \n")


for s in symbols:
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={s}&apikey={api_key}"
    response = requests.get(request_url)
    parsed_response = json.loads(response.text)


    tsd = parsed_response["Time Series (Daily)"]
    dates = list(tsd.keys()) 
    dates.sort(reverse=True)
    
    latest_day = dates[0]
    last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]  
     
    latest_close = tsd[latest_day]["4. close"]

      #recent_high = max(high_prices)

    for date in dates:
        high_price = tsd[date]["2. high"]
        high_prices.append(float(high_price))
        low_price = tsd[date]["3. low"]
        low_prices.append(float(low_price))
    recent_high = max(high_prices)
    recent_low = min(low_prices)




    #csv_file_path = "data/prices.csv" # a relative filepath

    csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices_" + s + ".csv")

    csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

    with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
        writer = csv.DictWriter(csv_file, fieldnames=csv_headers, lineterminator = '\n')
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



    from datetime import date
    today = datetime.date.today().strftime("%Y/%m/%d")

    

    hour = time.strftime("%I:%M %p")
    request_date = str(today) + " " + str(hour)


    margin = 0.30
    threshold = (margin + 1) * recent_low

    prev_year = dates[1]
    prev_price = tsd[prev_year]["4. close"]

    prev_prev_year = dates[2]
    prev_prev_price = tsd[prev_prev_year]["4. close"]

    if float(latest_close) < threshold: 
        buy_low = True
    else:
        buy_low = False

    if float(latest_close) > float(prev_price) and float(prev_price) > float(prev_prev_price):
        rising_prices = True
    else:
        rising_prices = False

    if buy_low == True and rising_prices == True:
        recommendation = "HIGH OPPORTUNITY"
        reason = "The current price is within a 30% margin of the recent lowest price AND the past three stocks are trending upward"
    
    elif buy_low == True and rising_prices == False:
        recommendation = "MEDIUM OPPORTUNITY"
        reason = "The current price is within a 30% margin of the recent lowest price BUT the past three stocks are not trending upward"

    elif buy_low == False and rising_prices == True:
        recommendation = "MEDIUM OPPORTUNITY"
        reason = "The past three stocks are trending upward BUT the current price is not within a 30% margin of the recent lowest price"

    elif buy_low == False and rising_prices == False:
        recommendation = "LOW OPPORTUNITY"   
        reason = "The current price is not within a 30% margin of the recent lowest price AND the past three stocks are not trending upward"
    
    x = x + 1    

   
    print("\n" + str(x) + ". SELECTED SYMBOL: " + s)
    print("-------------------------")
    print("REQUESTING STOCK MARKET DATA...")
    print("REQUEST AT: " + request_date)
    print("-------------------------")
    print("LATEST DAY: " + last_refreshed) 
    print("LATEST CLOSE: " + to_usd(float(latest_close))) 
    print("RECENT HIGH: " + to_usd(float(recent_high)))
    print("RECENT LOW: " + to_usd(float(recent_low)))
    print("-------------------------")
    print("RECOMMENDATION: " + recommendation)
    print("RECOMMENDATION REASON: " + reason)
    print("-------------------------")
    print("WRITING DATA TO CSV: " + csv_file_path)
    print("-------------------------\n")

print("-------------------------")   
print("HAPPY INVESTING!")
print("-------------------------")
