#%%
from datetime import datetime, time
import pandas as pd
import yfinance as yf
import requests
from p_tqdm import p_map
import math

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
        self.bank_stats = {}
        self.bank_crashes_stats = {}
        self.bank_crashes_history = []
        self.bank_crashes_today = {}
        return

    def download(self):
        all_banks = pd.read_csv("banks.csv", names=["name", "ticker"])
        print(all_banks)
        # unfiltered_data = p_map(request_data, all_banks["ticker"][300:340])
        unfiltered_data = p_map(request_data, all_banks["ticker"])
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


def request_data(tickername):
  if tickername in ["BIMB.KL", "DANS.VI", "MTPOF"]:
    return {}
  try:
    ticker = yf.Ticker(tickername)
    res = ticker.history(period="60mo")
  except requests.exceptions.HTTPError as e:
    print(e)
    return {}
  max_i, maxv = argmax(res["High"]), max(res["High"])
  minv = min(res["Close"][max_i:])
  estimated_marketcap_million = ticker.info["marketCap"] * (maxv/res["Close"][-1]) / 1_000_000 / 1_000
  mdd = (1-minv / maxv) * 100
  # print(list(row for row in res.iloc[max_i:].iterrows() if 1-row[1]["Close"] / maxv < CRASH_MDD_VALUE/100))
  first_mdd_date = next((i for i, row in res.iloc[max_i:].iterrows() if (1-row["Close"] / maxv > CRASH_MDD_VALUE/100)), -1)
  if first_mdd_date != -1 :
    print(first_mdd_date)
  crash_date_ts = None if first_mdd_date == -1 else int(first_mdd_date.timestamp())
  if minv < 0 or maxv < 0:
    estimated_marketcap_million = abs(estimated_marketcap_million)
    mdd = 0
  if mdd <= 0 or estimated_marketcap_million < 0 or minv < 0 or maxv < 0:
    print(tickername, estimated_marketcap_million, mdd)
  # print(tickername, estimated_marketcap, mdd)
  return {
      "shortname": ticker.info['shortName'],
      "ticker": tickername,
      "size": round(math.log10(estimated_marketcap_million), 3),
      "MC": round(estimated_marketcap_million, 0),
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
