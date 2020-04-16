import json
import csv
import os
import datetime
import time
import requests
import pytest
import plotly
import plotly.graph_objs as go

from datetime import date
from dotenv import load_dotenv
from twilio.rest import Client


load_dotenv()

api_key = os.environ.get("ALPHAVANTAGE_API_KEY","OOPS, please specify env var called 'ALPHAVANTAGE_API_KEY'")
symbols = []
x=0
i=0

def to_usd(my_price):
    '''Convert numeric value into currency formatting'''
    return f"${my_price:,.2f}"

def print_message(message):
    '''Formatting for header/footer'''
    print("-------------------------")
    print(message)
    print("-------------------------")


def get_graph(dates, prices_list_no_usd,s):
    '''Plot graph'''
    plotly.offline.plot({
    "data": [go.Scatter(x=dates, y=prices_list_no_usd)],
    "layout": go.Layout(yaxis=dict(tickprefix="$", tickangle=45), title="Historical Stock Prices: " + s)
    }, auto_open=True) 

def get_date():
    '''Get date infomration'''
    today = datetime.date.today().strftime("%Y/%m/%d")
    hour = time.strftime("%I:%M %p")
    request_date = str(today) + " " + str(hour)
    return request_date

def sms_math_upper(sms_margin,price_today):
    '''calculate upper bound'''
    upperbound = (1 + sms_margin) * float(price_today)
    return upperbound
    

def sms_math_lower(sms_margin, price_yesterday):   
    '''calculate lower bound'''        
    lowerbound = (1 - sms_margin) * float(price_yesterday)
    return lowerbound

def get_url(s):
    '''get URL'''
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={s}&apikey={api_key}"
    response = requests.get(request_url)
    return response

def parse_response(s):
    '''get text info from URL source'''
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={s}&apikey={api_key}"
    response = requests.get(request_url)
    parsed_response = json.loads(response.text)
    return parsed_response

def calc_recent_high(tsd,date,high_prices):
    '''calculate recent high price'''
    high_price = tsd[date]["2. high"]
    high_prices.append(float(high_price))
    recent_high = max(high_prices)
    return recent_high
    
def calc_recent_low(tsd,date,low_prices):
    '''calculate recent low price'''
    low_price = tsd[date]["3. low"]
    low_prices.append(float(low_price))
    recent_low = min(low_prices)
    return recent_low

def calc_close_price(tsd,date):
    '''calculate closing price'''
    close_price = tsd[date]["4. close"]
    return close_price

def threshold_calc(margin,recent_low):
    '''calculate threshold for rec'''
    threshold = (margin + 1) * recent_low
    return threshold

def write_csv(csv_file_path,csv_headers,dates,tsd):
    '''write out file'''
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


if __name__ == "__main__":

    print_message("Welcome to our automated stock advisory service!")

    print("\nPlease enter any stock(s) that you want to know more about (Max of 5 at a time).")
    print("When finished, type 'DONE'.\n")


    

    #1.  INPUT VALIDATION
    while True: 
        symbol = input("Please input a stock symbol: ")

            
        if symbol == "DONE":
            if len(symbols) == 0:
                print("\n    Please enter at least one stock symbol.\n")
            else:
                break

        elif float(len(symbol)) <= 5 and symbol.isalpha():

            symbols.append(symbol)
            if len(symbols) > 5:
                stock5 = symbols[4]
                print("\n***Sorry! We can only process 5 stocks at a time due to API constraints. Any entry after Stock '" + stock5 + "' will not be analyzed.***")
                stock6 = symbols[5]
                del symbols[5:]
                break

        else:
            print("\n    Sorry your input is not valid. Please enter a symbol consisting of 1-5 letters[ (Ex. MSFT)]. \n")


        

    #2. READING STOCK INFORMATION
    for s in symbols:
        
        dates = []
        prices_list = []
        prices_list_no_usd = []

        #Get URL
        response = get_url(s)
           
        #Parse scraped text
        parsed_response = parse_response(s)
        
        x = x + 1 #keep counter for numbers

        if "Error Message" in response.text:
            print("\n" + str(x) + ". OOPS!: I couldn't seem to find any trading data for the '" + s + "' symbol. Sorry!\n")
                
        else:

            tsd = parsed_response["Time Series (Daily)"]
            dates = list(tsd.keys()) 
            dates.sort(reverse=True)


            latest_day = dates[0]
            last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]  
            latest_close = tsd[latest_day]["4. close"]

            high_prices = []
            low_prices = []

            for date in dates:
                recent_high = calc_recent_high(tsd,date,high_prices)
                recent_low = calc_recent_low(tsd,date,low_prices)
                close_price = calc_close_price(tsd,date)
                
                prices_list.append(to_usd(float(close_price)))
                prices_list_no_usd.append(float(close_price))
         
        
            csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices_" + s + ".csv")
      

            csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

            write_csv(csv_file_path,csv_headers,dates,tsd)

        #3. GET DATES
            request_date = get_date()


        #4. RECOMMENDATIONS
            margin = 0.30
            
            threshold = threshold_calc(margin,recent_low)

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
                reason = "The latest closing price is within 30% of the recent lowest price AND the past three stock prices are trending upward. This is a great time to invest!"
            
            elif buy_low == True and rising_prices == False:
                recommendation = "MEDIUM OPPORTUNITY"
                reason = "The latest closing price is within 30% of the recent lowest price BUT the past three stock prices have not been trending upward. This is an ok time to invest."

            elif buy_low == False and rising_prices == True:
                recommendation = "MEDIUM OPPORTUNITY"
                reason = "The past three stock prices are trending upward BUT the latest closing price is not within 30% of the recent lowest price. This is an ok time to invest."

            elif buy_low == False and rising_prices == False:
                recommendation = "LOW OPPORTUNITY"   
                reason = "The latest closing price is not within 30% of the recent lowest price AND the past three stock prices have not been trending upward. This is an bad time to invest!"
            
            
            #5. OUTPUT
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

            print_message("WRITING DATA TO CSV: " + csv_file_path)


            #6. GRAPHS
            get_graph(dates, prices_list_no_usd,s)
            
                
            #7. SMS OUTPUT 
            sms_margin =  0.05
            price_today = prices_list_no_usd[0]
            price_yesterday = prices_list_no_usd[1]

            lowerbound = sms_math_lower(sms_margin,price_yesterday)
            upperbound = sms_math_upper(sms_margin,price_today)
            
            format_price_today = prices_list[0]
            format_price_yesterday = prices_list[1]

            TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "OOPS, please specify env var called 'TWILIO_ACCOUNT_SID'")
            TWILIO_AUTH_TOKEN  = os.environ.get("TWILIO_AUTH_TOKEN", "OOPS, please specify env var called 'TWILIO_AUTH_TOKEN'")
            SENDER_SMS  = os.environ.get("SENDER_SMS", "OOPS, please specify env var called 'SENDER_SMS'")
            RECIPIENT_SMS  = os.environ.get("RECIPIENT_SMS", "OOPS, please specify env var called 'RECIPIENT_SMS'")

            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

            if price_today > upperbound: 
                content = "PRICE MOVEMENT ALERT: Hello! We have detected that the stock '" + s + "' has increased by more than 5% within the past day! It is currently at " + format_price_today + " compared to " + "its price of" + format_price_yesterday + " yesterday."        
                message = client.messages.create(to=RECIPIENT_SMS, from_=SENDER_SMS, body=content)
            elif price_today < lowerbound:
                content = "PRICE MOVEMENT ALERT: Hello! We have detected that the stock '" + s + "' has decreased by more than 5% within the past day! It is currently at " + format_price_today+ " compared to its price of " + format_price_yesterday + " yesterday."        
                message = client.messages.create(to=RECIPIENT_SMS, from_=SENDER_SMS, body=content)
            else:
                pass
        
      
    print_message("HAPPY INVESTING!")


