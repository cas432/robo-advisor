
import json
import csv
import os

from dotenv import load_dotenv
import requests

load_dotenv()

#USD function
def to_usd(my_price):
    return "${0:,.2f}".format(my_price)


api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
#Get stock symbol
symbols = []



while True: 
    symbol = input("Please input your stock ticker symbol of choice:")
         
    
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

    dates = list(tsd.keys()) #TODO ASSUME LATEST DAY IS FIRST. sort chronologically?
    
    print(dates[0])
    print(dates[1])
    print(dates[2])
    dates.sort()
    print(dates[0])
    print(dates[1])
    print(dates[3])





    latest_day = dates[0]
    last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]  
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

    print("-------------------------")
    print("SELECTED SYMBOL: " + s)
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
    print("WRITING DATA TO CSV: " + csv_file_path)
    print("-------------------------")
    print("HAPPY INVESTING!")
    print("-------------------------")



#detect/handle response errors
#if "Error Message" in response.text:
     #   print("OOOPS")
      #  exit()
