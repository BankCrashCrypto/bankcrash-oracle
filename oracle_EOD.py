
import requests
import json
import math
from datetime import datetime
from config_accounts import EOD_APY_KEY
from ETL import to_EOD_TICKER
from HARDCODED_VALUES import FIX_DATA
from joblib import Memory

memory = Memory("cache.all_request")

@memory.cache
def get_eod_fundamentals(ticker):
  eod_ticker = to_EOD_TICKER(ticker)
  url = f"https://eodhistoricaldata.com/api/fundamentals/{eod_ticker}?api_token={EOD_APY_KEY}&filter=outstandingShares::quarterly"
  return requests.get(url)


def get_market_cap_from_EOD(tickername):
  eod_ticker = to_EOD_TICKER(tickername)
  url = f"https://eodhistoricaldata.com/api/historical-market-cap/{eod_ticker}?from=2000-01-01&to=2030-12-31&api_token={EOD_APY_KEY}"
  return requests.get(url)


def recalculate_shares_from_EOD(ticker, res):
  if ticker in FIX_DATA.keys():
    # print("Fixed share for:", ticker)
    shares=FIX_DATA[ticker]
  else:
    # print(eod_ticker)
    data = get_eod_fundamentals(ticker)
    if data.text == "" or data.text=="Symbol not found":
      # print("Symbol not found: message", data.text)
      return []
    if type(json.loads(data.text)) is str:
      print("ERROR MESSAGE:", data, data.text)
      return []
    shares = list(json.loads(data.text).values())
  market_cap = []
  ti = 0 
  for share in shares[::-1]:
    element = datetime.strptime(share["dateFormatted"],"%Y-%m-%d")
    timestamp = datetime.timestamp(element)-3600
    if timestamp > datetime.now().timestamp():
      break
    while timestamp>res.index[ti].timestamp():
        ti+=1
        # trueti = ti if res.index[ti].timestamp()-timestamp==0 else ti-1
        price = res["Close"][ti]
        market_cap.append({
          "value": price*share["shares"], 
          "date":  res.index[ti].timestamp()
          })

  if math.isnan(market_cap[0]["value"]):
    print("NAN", shares)
    
  return market_cap  # PLEASE be warned we only check 10 years backward correctly... we don't calculate the data valid before as price will be constant due to we only have 10 years backward...


