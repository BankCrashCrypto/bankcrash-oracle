#%%
from yahoo_finance import Share

yahoo = Share('YHOO')

# %%
print(yahoo.get_open())
# %%

import yfinance as yf
jaaahoo = yf.Ticker("MSFT")
res = jaaahoo.info()
print(res)


# %%
import json
import requests
ticker="MSFT"
res=requests.get(f"https://eodhistoricaldata.com/api/fundamentals/{ticker}?api_token=64941a37784db9.21946561")
# print(json.loads(res.text).keys())
# print(json.loads(res.text).values())
# print(json.loads(res.text)["General"])
print(json.loads(res.text)["General"]["CurrencyCode"])
# %%
import pandas as pd
all_banks = pd.read_csv("banks.csv", names=["name", "ticker"])
print("CSV is loaded!")
# %%
import json
import requests
import yfinance as yf
for ticker in all_banks["ticker"]:
  
	stock = yf.Ticker(ticker)
	# res = (requests.get(f"https://eodhistoricaldata.com/api/fundamentals/{ticker}?api_token=64941a37784db9.21946561")).text
	# if res == "Symbol not found":
	# print(ticker)
	if ticker in ["BIMB.KL", "BSMX", "ITCB", "LMST", "SI"]:
		continue
	# print(res)
	# print(stock.info)
	inf = stock.info
	print("\"",ticker,"\": {", "\"shortName\": \"", inf['shortName'],"\", \"currency\": \"", inf['currency'],"\" },", sep="")

print("Don't forget to replace ZAc to ZAR! Johannesburg currency")
# [{ticker : json.loads((requests.get(f"https://eodhistoricaldata.com/api/fundamentals/{ticker}?api_token=64941a37784db9.21946561")
# ).text)["General"]["CurrencyCode"]} for ticker in all_banks["ticker"]]
# %%
print(all_banks["ticker"])
# %%
import yfinance as yf

def get_stock_currency(stock_symbol):
    stock = yf.Ticker(stock_symbol)
    return stock.info['currency']

print(get_stock_currency('AAPL'))
# %%

