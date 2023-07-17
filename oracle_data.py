#%%
from datetime import datetime, time
import pandas as pd
import yfinance as yf
import requests
from p_tqdm import p_map
import math
import json
from quarters import QUARTER_DATES
from config_accounts import EOD_APY_KEY
from oracle_blockchain import sync_blockchain_information

LARGE_BANK_SIZE  = 500
MEDIUM_BANK_SIZE = 50
SMALL_BANK_SIZE  = 50

LARGE_BANK  = "LARGE_BANK"
MEDIUM_BANK = "MEDIUM_BANK"
SMALL_BANK  = "SMALL_BANK"

CRASH_MDD_VALUE = 98 # 98%

def today_ts():
    midnight = datetime.combine(datetime.now().date(), time.min)
    timestamp_midnight = int(midnight.timestamp())
    return timestamp_midnight

def bank_size_category(bank):
    if bank["MC"] > LARGE_BANK_SIZE:
      return LARGE_BANK
    elif bank["MC"] > MEDIUM_BANK_SIZE:
      return MEDIUM_BANK
    else:
      return SMALL_BANK

def bank_format(bank):
    return { 
        "shortname": bank['shortname'],
        "ticker": bank["ticker"],
        "type": bank_size_category(bank),
        "MC": bank["MC"],
        "price": bank["price"],
        "MDD": bank["MDD"],
        "CRASH_date": bank["CRASH_date"],
        "crashed": bank["MDD"] > CRASH_MDD_VALUE,
      }
  
def today_crashes(banks):
    today_crashes = {
      SMALL_BANK: 0,
      MEDIUM_BANK: 0,
      LARGE_BANK: 0,
    }
    for bank in banks:
      if bank["MDD"] <= CRASH_MDD_VALUE:
        continue
      today_crashes[bank_size_category(bank)] += 1
      
    return today_crashes


class DB_Banks:
    def __init__(self):
        self.all = {}
        self.bank_mdds = {}
        self.bank_list = {}
        self.bank_stats = {}  # ONLY calculate crashes from 2022.02.22... to be nice? :D TODO filter?
        self.bank_crashes_stats = {}
        self.bank_crashes_history = []
        self.bank_crashes_today = {}
        return

    def download(self):
        all_banks = pd.read_csv("banks.csv", names=["name", "ticker"])
        print("CSV is loaded!")
        # print(all_banks)
        # unfiltered_data = map(request_data, all_banks["ticker"][295:])
        unfiltered_data = map(request_data, all_banks["ticker"])
        # unfiltered_data = p_map(request_data, all_banks["ticker"])
        self.all = list(filter(lambda d: d, unfiltered_data))
        return
      
    def prepare_structures(self):
        mdds = sorted(self.all, key=lambda x: x["size"], reverse=True)
        blist = self.get_bank_lists()
        stats, crashes_stats = self.get_bank_stats()
        crashes_history = self.crashfilterformat()
        crashes_today = list(filter(lambda crash: crash["CRASH_date"]>today_ts(), self.bank_crashes_history))
        # we assign in one step to keep as atomic as possible... Stricter atomicity isn't important actually...
        self.bank_mdds, self.bank_list, self.bank_stats, self.bank_crashes_stats, self.bank_crashes_history, self.bank_crashes_today = mdds, blist, stats, crashes_stats, crashes_history, crashes_today 
        sync_blockchain_information(self.bank_crashes_stats[SMALL_BANK],self.bank_crashes_stats[MEDIUM_BANK],self.bank_crashes_stats[LARGE_BANK])
        return
      
    def refresh(self):
        self.download()
        self.prepare_structures()
        return 
      
    def get_bank_lists(self):
        return list(map(bank_format, self.all))
      
    def get_bank_stats(self):
        stats = {
          SMALL_BANK: 0,
          MEDIUM_BANK: 0,
          LARGE_BANK: 0,
        }
        crashes = {
          SMALL_BANK: 0,
          MEDIUM_BANK: 0,
          LARGE_BANK: 0,
        }
        for bank in self.all:
          bank_type = bank_size_category(bank)
          stats[bank_type] += 1
          if bank["MDD"] > CRASH_MDD_VALUE:
            crashes[bank_type] += 1
        return stats, crashes
    def crashfilterformat(self):
      return [{
          "ticker": bank["ticker"],
          "shortname": bank["shortname"],
          "type": bank_size_category(bank),
          "MDD": bank["MDD"],
          "CRASH_date": bank["CRASH_date"],
          "crashed": True,
          } for bank in self.all if bank["CRASH_date"] != None]
      
YAHOO_TO_EOD_EXCHANGE = {
  "SZ":"SHE",
  "SS":"SHG",
  "L":"LSE",
  "KL":"KLSE",
  "AX":"AU",
  # "PR":"XPRA",
  "NS":"NSE",
  # "F":"XFRA",
  "BD":"BUD",
  # "BK":"XBKK",
  "WA":"WAR",
  "DE":"XETRA",
  # "AX":"XASX",
  # "JK":"XIDX",
}
YAHOO_TO_EOD_TICKER = {
  "AXISBANK.BO": "AXISBANK.NSE"
}
FIX_DATA = {
  "FIBI.TA":   [{"shares": 100_000_000,    "dateFormatted": dat,} for dat in QUARTER_DATES],
  "600919.SS": [{"shares": 15_520_000_000, "dateFormatted": dat,} for dat in QUARTER_DATES],
  "601211.SS": [{"shares": 7_510_000_000,  "dateFormatted": dat,} for dat in QUARTER_DATES],
  "601939.SS": [{"shares": 9_590_000_000,  "dateFormatted": dat,} for dat in QUARTER_DATES],
  "601658.SS": [{"shares": 79_300_000_000, "dateFormatted": dat,} for dat in QUARTER_DATES],
  "BSLI3.SA":  [{"shares": 280_150_000,    "dateFormatted": dat,} for dat in QUARTER_DATES],
  "D05.SI":    [{"shares": 280_150_000,    "dateFormatted": dat,} for dat in QUARTER_DATES],
  "MB.MI":     [{"shares": 840_690_000,    "dateFormatted": dat,} for dat in QUARTER_DATES],
  "ISP.MI":    [{"shares": 18_260_000_000, "dateFormatted": dat,} for dat in QUARTER_DATES],
  "BMED.MI":   [{"shares": 738_850_000,    "dateFormatted": dat,} for dat in QUARTER_DATES],
  "UCG.MI":    [{"shares": 1_820_000_000,  "dateFormatted": dat,} for dat in QUARTER_DATES],
  "BAMI.MI":   [{"shares": 1_510_000_000,  "dateFormatted": dat,} for dat in QUARTER_DATES],
  "SBK.JO":    [{"shares": 1_650_000_000,  "dateFormatted": dat,} for dat in QUARTER_DATES],
  "NED.JO":    [{"shares": 485_250_000,    "dateFormatted": dat,} for dat in QUARTER_DATES],
  "FSR.JO":    [{"shares": 5_610_000_000,  "dateFormatted": dat,} for dat in QUARTER_DATES],
  "CPI.JO":    [{"shares": 115_790_000,    "dateFormatted": dat,} for dat in QUARTER_DATES],
  "DSY.JO":    [{"shares": 658_400_000,    "dateFormatted": dat,} for dat in QUARTER_DATES],
  "7182.T":    [{"shares": 3_620_000_000,  "dateFormatted": dat,} for dat in QUARTER_DATES],
  "8308.T":    [{"shares": 2_360_000_000,  "dateFormatted": dat,} for dat in QUARTER_DATES],
  "8421.T":    [{"shares": 708_220,        "dateFormatted": dat,} for dat in QUARTER_DATES],
  "8601.T":    [{"shares": 1_450_000_000,  "dateFormatted": dat,} for dat in QUARTER_DATES],
  "RAW.F":     [{"shares": 328_410_000,    "dateFormatted": dat,} for dat in QUARTER_DATES],
  "EBO.F":     [{"shares": 406_930_000,    "dateFormatted": dat,} for dat in QUARTER_DATES],
  "CIN.F":     [{"shares": 2_980_000_000,  "dateFormatted": dat,} for dat in QUARTER_DATES],
  "ZYE1.F":    [{"shares": 19_470_000,     "dateFormatted": dat,} for dat in QUARTER_DATES],
  "0B2.F":     [{"shares": 82_150_000,     "dateFormatted": dat,} for dat in QUARTER_DATES],
  # "BMRI.JK":   [{"shares": 93_330_000_000, "dateFormatted": dat,} for dat in QUARTER_DATES],
  # "BNLI.JK":   [{"shares": 26_880_000,    "dateFormatted": dat,} for dat in QUARTER_DATES],
  # "ISCTR.IS":  [{"shares": 0,    "dateFormatted": dat,} for dat in QUARTER_DATES],
  # "KLNMA.IS":  [{"shares": 0,    "dateFormatted": dat,} for dat in QUARTER_DATES],
  # "QNBFB.IS":  [{"shares": 0,    "dateFormatted": dat,} for dat in QUARTER_DATES],
  "MONET.PR":  [{"shares": 511_000_000,    "dateFormatted": dat,} for dat in QUARTER_DATES],
  "KOMB.PR":   [{"shares": 511_000_000,    "dateFormatted": dat,} for dat in QUARTER_DATES],
  "OTP.BD":    [{"shares": 278_890_000,    "dateFormatted": dat,} for dat in QUARTER_DATES],
  "SPL.WA":    [{"shares": 102_190_000,    "dateFormatted": dat,} for dat in QUARTER_DATES],
  "TTB.BK":    [{"shares": 96_870_000_000, "dateFormatted": dat,} for dat in QUARTER_DATES],
  "DANS.VI":   [{"shares": 858_320_000,    "dateFormatted": dat,} for dat in QUARTER_DATES],
  "U11.SI":    [{"shares": 1_680_000_000,  "dateFormatted": dat,} for dat in QUARTER_DATES],
}
def to_EOD_TICKER(ticker):
  if ticker in YAHOO_TO_EOD_TICKER.keys():
    return YAHOO_TO_EOD_TICKER[ticker]
  if len(ticker.split("."))==2:
    stock, exchange = ticker.split(".")
    if exchange in YAHOO_TO_EOD_EXCHANGE.keys():
      exchange = YAHOO_TO_EOD_EXCHANGE[exchange]
    return stock + "." + exchange
  return ticker

def log_round(number):
    if number != 0:
      magnitude = math.floor(math.log10(abs(number))) + 1
    else:
      return 0
    if magnitude > 3:
      return round(number, 0)
    return round(number, -magnitude + 3)

def argmax(iterable):
  return max(enumerate(iterable), key=lambda x: x[1])[0]

def recalculate_from_shares(ticker, res):
  if ticker in FIX_DATA.keys():
    # print("Fixed share for:", ticker)
    shares=FIX_DATA[ticker]
  else:
    eod_ticker = to_EOD_TICKER(ticker)
    # print(eod_ticker)
    url = f"https://eodhistoricaldata.com/api/fundamentals/{eod_ticker}?api_token={EOD_APY_KEY}&filter=outstandingShares::quarterly"
    data = requests.get(url)
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

  # print(market_cap)
  # print(market_cap[0]["value"],market_cap[-1]["value"])
  if math.isnan(market_cap[0]["value"]):
    print("NAN", shares)
  return market_cap  # PLEASE be warned we only check 10 years backward correctly... we don't calculate the data valid before as price will be constant due to we only have 10 years backward...

def request_data(tickername):
  print((tickername))
  # if tickername != "SBNY":
    # return {}
  if tickername in ["SI", "LMST", "BSMX", "ITCB", "BIMB.KL"]:  # somthing is wrong with these tickers on Yahoo API site...
    return {}
  try:
    ticker = yf.Ticker(tickername)
    res = ticker.history(period="120mo", proxy="91.203.25.28:4153")
    if res["High"].size==0:
      return {}
    url = f"https://eodhistoricaldata.com/api/historical-market-cap/{tickername}?from=2000-01-01&to=2030-12-31&api_token={EOD_APY_KEY}"
    MC_res = requests.get(url)
  except requests.exceptions.HTTPError as e:
    print(e)
    return {}
  if res["High"].size == 0:
    print("WTFFF???", res)
  max_i, maxv = argmax(res["High"]), max(res["High"])
  minv = min(res["Close"][max_i:])
  if MC_res.text[0:14]=="Error occurred":
    print(MC_res.text)
    print("WE throw a valid bank away!!! THIS IS NOT GOOD... WHAT is going on with the server?")
    return {}
  if MC_res.text=="Ticker Not Found.":
    market_caps = recalculate_from_shares(tickername, res)
    if len(market_caps)==0:
      print("TICKER NOT FOUND & couldn't recalculate")
      return {}
  else:
    # print(MC_res.text)
    market_caps = ([{"value": dat["value"], "date": datetime.timestamp(datetime.strptime(dat["date"],"%Y-%m-%d")), } for dat in json.loads(MC_res.text).values()])
    if len(market_caps) == 0:
      market_caps = recalculate_from_shares(tickername, res)
      if len(market_caps)==0:
        print("TICKER FOUND BUT zero value & couldn't recalculate")
        return {}
  # if len(market_caps) < 10:
  #   print(len(market_caps), market_caps)
  max_marketcap = max(market_caps, key=lambda x:x['value'])
  marketcap_million = max_marketcap["value"] / 1_000_000 # ticker.info["marketCap"] * (maxv/res["Close"][-1]) / 1_000_000 / 1_000
  mdd = (1-minv / maxv) * 100
  # print(list(row for row in res.iloc[max_i:].iterrows() if 1-row[1]["Close"] / maxv < CRASH_MDD_VALUE/100))
  first_crash_date = next((i for i, row in res.iloc[max_i:].iterrows() if (1-row["Close"] / maxv > CRASH_MDD_VALUE/100)), -1)
  if first_crash_date != -1 :
    print(first_crash_date, max_marketcap)
  crash_date_ts = None if first_crash_date == -1 else int(first_crash_date.timestamp())
  if minv < 0 or maxv < 0:
    marketcap_million = abs(marketcap_million)
    mdd = 0
  if mdd <= 0 or marketcap_million < 0 or minv < 0 or maxv < 0:
    print(tickername, marketcap_million, mdd)
  # print(tickername, estimated_marketcap, mdd)
  # ticker_info = ticker.info()
  ticker_info = {"shortName": "troll"}
  return {
      "shortname": ticker_info['shortName'],
      "ticker": tickername,
      "size": round(math.log10(marketcap_million), 3),
      "MC": round(marketcap_million, 0),
      "price": log_round(minv),
      "MDD": log_round(mdd),
      "CRASH_date": crash_date_ts,
  }

#%%
if __name__ == '__main__':
  request_data("MUFG")

# %%

# %%
if __name__ == '__main__':
  ticker = yf.Ticker("BBCA.JK")
  ticker = yf.Ticker("DANS.VI")

# %%
if __name__ == '__main__':
  print(ticker.info)
# %%
if __name__ == '__main__':
  res = ticker.history(period="120mo")

# %%
if __name__ == '__main__':
  _, maxv = argmax(res["High"]), max(res["High"])
  print(maxv)

# %%
if __name__ == '__main__':
  tickername = "DANS.VI"
  tickername = "BBCA.JK"
  tickername = "JPM"
  ticker = yf.Ticker(tickername)
  res = ticker.history(period="120mo")
  _, maxv = argmax(res["High"]), max(res["High"])
  estimated_marketcap_million = ticker.info["marketCap"] * (maxv/res["Close"][-1]) / 1_000_000 / 1_000
  mdd = (1-res["Close"][-1] / maxv )* 100
  print(tickername, estimated_marketcap_million, mdd, res["Close"][-1], maxv)
# %%
