import json
import csv
import os
import datetime
import time
import requests
import plotly
import plotly.graph_objs as go

from datetime import date
from dotenv import load_dotenv
from twilio.rest import Client


load_dotenv()

symbols = []
high_prices = []
low_prices = []
x=0
i=0

print("\nWelcome to our automated stock advisory service!\n")
print("Please enter any stock(s) that you want to know more about (Maximum of 5 at a time).")
print("When finished, type 'DONE'.\n")

def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

api_key = os.environ.get("ALPHAVANTAGE_API_KEY","OOPS, please specify env var called 'ALPHAVANTAGE_API_KEY'")

#1.  INPUT VALIDATION
while True: 
    symbol = input("Please input a stock symbol: ")

        
    if symbol == "DONE":
        if len(symbols) == 0:
            print("\n    Please enter at least one stock symbol")
        else:
            break

    elif float(len(symbol)) <= 5 and symbol.isalpha():

        symbols.append(symbol)
        if len(symbols) > 5:
            stock5 = symbols[4]
            print("\nSorry! We can only process 5 stocks at a time due to API constraints. Any entry after '" + stock5 + "' will not be analyzed.")
            stock6 = symbols[5]
            del symbols[5:]
            break

    else:
        print("\n    Sorry your input is not valid. Please enter a symbol consisting of 1-5 alphabetic letters. \n")


    

#2. READING STOCK INFORMATION
for s in symbols:
    
    dates = []
    prices_list = []
    prices_list_no_usd = []

    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={s}&apikey={api_key}"
    response = requests.get(request_url)
    parsed_response = json.loads(response.text)

    if "Error Message" in response.text:
        print("\n OOPS!: Sorry! I couldn't seem to find any trading data for the '" + s + "' symbol. Sorry!\n")
            
    

    

    tsd = parsed_response["Time Series (Daily)"]
    dates = list(tsd.keys()) 
    dates.sort(reverse=True)


    latest_day = dates[0]
    last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]  
    latest_close = tsd[latest_day]["4. close"]


    for date in dates:
        high_price = tsd[date]["2. high"]
        high_prices.append(float(high_price))
        low_price = tsd[date]["3. low"]
        low_prices.append(float(low_price))

        close_price = tsd[date]["4. close"]
        prices_list.append(to_usd(float(close_price)))
        prices_list_no_usd.append(float(close_price))

    recent_high = max(high_prices)
    recent_low = min(low_prices)

 
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

#3. GET DATES
    today = datetime.date.today().strftime("%Y/%m/%d")

    hour = time.strftime("%I:%M %p")
    request_date = str(today) + " " + str(hour)

#4. RECOMMENDATIONS
    margin = 0.30
    threshold = (margin + 1) * recent_low

    prev_year = dates[1]
    prev_price = tsd[prev_year]["4. close"]

    prev_prev_year = dates[2]
    prev_prev_price = tsd[prev_prev_year]["4. close"]

    if float(latest_close) <= threshold: 
        buy_low = True
    else:
        buy_low = False

    if float(latest_close) > float(prev_price) and float(prev_price) > float(prev_prev_price):
        rising_prices = True
    else:
        rising_prices = False

    if buy_low == True and rising_prices == True:
        recommendation = "HIGH OPPORTUNITY"
        reason = "The current price is within a 30% margin of the recent lowest price AND the past three stocks are trending upward. This is a great time to invest!"
    
    elif buy_low == True and rising_prices == False:
        recommendation = "MEDIUM OPPORTUNITY"
        reason = "The current price is within a 30% margin of the recent lowest price BUT the past three stocks are not trending upward.This is an ok time to invest"

    elif buy_low == False and rising_prices == True:
        recommendation = "MEDIUM OPPORTUNITY"
        reason = "The past three stocks are trending upward BUT the current price is not within a 30% margin of the recent lowest price.This is an ok time to invest"

    elif buy_low == False and rising_prices == False:
        recommendation = "LOW OPPORTUNITY"   
        reason = "The current price is not within a 30% margin of the recent lowest price AND the past three stocks are not trending upward. This is an bad time to invest"
    
    #5. OUTPUT
    x = x + 1 #keep counter for output

    print("\n" + str(x) + ". SELECTED SYMBOL: " + s)
    print("-------------------------")
    print("REQUESTING STOCK MARKET DATA...")
    print("REQUEST AT: " + request_date)
    print("-------------------------")
    print("LATEST DAY: " + latest_day) 
    print("LATEST CLOSE: " + to_usd(float(latest_close))) 
    print("RECENT HIGH: " + to_usd(float(recent_high)))
    print("RECENT LOW: " + to_usd(float(recent_low)))
    print("-------------------------")
    print("RECOMMENDATION: " + recommendation)
    print("RECOMMENDATION REASON: " + reason)
    print("-------------------------")
    print("WRITING DATA TO CSV: " + csv_file_path)
    print("-------------------------\n")

    # #6. GRAPHS
    # plotly.offline.plot({
    # "data": [go.Scatter(x=dates, y=prices_list)],
    # "layout": go.Layout(title="Historical Stock Prices: " + s)
    # }, auto_open=True)
    
    # #7. SMS OUTPUT 
    # sms_margin =  0.05
    # price_today = prices_list_no_usd[0]
    # price_yesterday = prices_list_no_usd[1]

     
    # upperbound = (1 + sms_margin) * float(price_today)
    # lowerbound = (1 - sms_margin) * float(price_yesterday)
    
    # format_price_today = prices_list[0]
    # format_price_yesterday = prices_list[1]

    # TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "OOPS, please specify env var called 'TWILIO_ACCOUNT_SID'")
    # TWILIO_AUTH_TOKEN  = os.environ.get("TWILIO_AUTH_TOKEN", "OOPS, please specify env var called 'TWILIO_AUTH_TOKEN'")
    # SENDER_SMS  = os.environ.get("SENDER_SMS", "OOPS, please specify env var called 'SENDER_SMS'")
    # RECIPIENT_SMS  = os.environ.get("RECIPIENT_SMS", "OOPS, please specify env var called 'RECIPIENT_SMS'")

    # client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    # if price_today > upperbound: 
    #     content = "PRICE MOVEMENT ALERT: Hello! We have detected that the stock '" + s + "' has increased by more than 5% within the past day! It is currently at " + format_price_today + " compared to " + "its price of" + format_price_yesterday + " yesterday."        
    #     message = client.messages.create(to=RECIPIENT_SMS, from_=SENDER_SMS, body=content)
    # elif price_today < lowerbound:
    #     content = "PRICE MOVEMENT ALERT: Hello! We have detected that the stock '" + s + "' has decreased by more than 5% within the past day! It is currently at " + format_price_today+ " compared to its price of " + format_price_yesterday + " yesterday."        
    #     message = client.messages.create(to=RECIPIENT_SMS, from_=SENDER_SMS, body=content)
    # else:
    #     break
    
  

print("-------------------------")   
print("HAPPY INVESTING!")
print("-------------------------")


