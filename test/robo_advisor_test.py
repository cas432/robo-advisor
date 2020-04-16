from app.robo_advisor import to_usd, parse_response, calc_recent_high, calc_recent_low, calc_close_price, get_url, sms_math_lower, sms_math_upper,threshold_calc
import json
import pytest
import os

def test_to_usd():

    result = to_usd(1223.6)
    assert result == "$1,223.60"



def test_calc_recent_high():
    temp_list = []
    tsd = {'2020-04-15': {'1. open': '80.7900', '2. high': '80.9800', '3. low': '79.4000', '4. close': '79.7900', '5. volume': '2972689'}, '2020-04-14': {'1. open': '81.6000', '2. high': '82.1700', '3. low': '80.3400', '4. close': '82.0200', '5. volume': '3390797'}, '2020-04-13': {'1. open': '80.6000', '2. high': '81.1600', '3. low': '78.4200', '4. close': '79.5300', '5. volume': '2739490'}, '2020-04-09': {'1. open': '78.6300', '2. high': '82.6400', '3. low': '78.6300', '4. close': '81.5900', '5. volume': '5478970'}, '2020-04-08': {'1. open': '74.0800', '2. high': '78.9000', '3. low': '73.5800', '4. close': '78.2200', '5. volume': '3891794'}, '2020-04-07': {'1. open': '75.6300', '2. high': '76.2400', '3. low': '73.1501', '4. close': '73.4400', '5. volume': '4258840'}} 
    high = calc_recent_high(tsd,"2020-04-15",temp_list)
    assert high == 80.98



def test_calc_recent_low():
    temp_list = []
    tsd = {'2020-04-15': {'1. open': '80.7900', '2. high': '80.9800', '3. low': '79.4000', '4. close': '79.7900', '5. volume': '2972689'}, '2020-04-14': {'1. open': '81.6000', '2. high': '82.1700', '3. low': '80.3400', '4. close': '82.0200', '5. volume': '3390797'}, '2020-04-13': {'1. open': '80.6000', '2. high': '81.1600', '3. low': '78.4200', '4. close': '79.5300', '5. volume': '2739490'}, '2020-04-09': {'1. open': '78.6300', '2. high': '82.6400', '3. low': '78.6300', '4. close': '81.5900', '5. volume': '5478970'}, '2020-04-08': {'1. open': '74.0800', '2. high': '78.9000', '3. low': '73.5800', '4. close': '78.2200', '5. volume': '3891794'}, '2020-04-07': {'1. open': '75.6300', '2. high': '76.2400', '3. low': '73.1501', '4. close': '73.4400', '5. volume': '4258840'}}
    low = calc_recent_low(tsd,"2020-04-15",temp_list)
    assert low == 79.4


def test_parse_response():

    s = "FB"
    parsed_response = parse_response(s)
    assert isinstance(parsed_response, dict)
    assert "Meta Data" in parsed_response.keys()
    assert "Time Series (Daily)" in parsed_response.keys()
    assert parsed_response["Meta Data"]["2. Symbol"] == s






def test_sms_math_lower():
    result = sms_math_lower(0.05,100)
    assert result == 95

def test_sms_math_upper():
    result = sms_math_upper(0.05,100)
    assert result == 105


def test_threshold_calc():
    result = threshold_calc(0.10,1000)
    assert result == 1100



