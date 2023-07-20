#%%
from datetime import datetime
from p_tqdm import p_map
import pandas as pd
import yfinance as yf
import requests
import math
import json
from oracle_currency import get_historical_exchange_rate
from oracle_EOD import recalculate_shares_from_EOD, get_market_cap_from_EOD
from oracle_blockchain import sync_blockchain_information
from utils import argmax, log_round, today_ts
from HARDCODED_VALUES import QUARTER_DATES, BANK_INFO, PENNIES
from ETL import correct_data

from CONSTANTS import LARGE_BANK_SIZE, MEDIUM_BANK_SIZE, SMALL_BANK_SIZE, LARGE_BANK, MEDIUM_BANK, SMALL_BANK, CRASH_MDD_VALUE




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

    def download(self, multithreaded):
        all_banks = pd.read_csv("banks.csv", names=["name", "ticker"])
        print("CSV is loaded!")
        # print(all_banks)
        if multithreaded:
          unfiltered_data = p_map(request_data, all_banks["ticker"])
        else:
          # unfiltered_data = map(request_data, all_banks["ticker"][295:])
          unfiltered_data = map(request_data, all_banks["ticker"])
        
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
      
    def refresh(self, multithreaded):
        self.download(multithreaded)
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
          if bank["CRASH_date"] != None:
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
        "crashed": bank["CRASH_date"] != None,
      }
  

  
def request_data(tickername):
  # if tickername != "SBNY":
  # if tickername != "CVLY":
  #   return {}
  print((tickername))
  # if tickername in ["BIMB.KL", "BSMX", "ITCB", "LMST", "SI"]: # delisted banks from yahoo
  #   continue
  try:
    ticker = yf.Ticker(tickername)
    res = ticker.history(period="120mo")  # , proxy="91.203.25.28:4153"  BUSE divident event out of range???
    if res["High"].size==0:
      return {}
  except Exception as e:
    if (str(e)[0:49]== "The following 'Dividends' events are out-of-range"):
      res = ticker.history(period="121mo") 
    else:
      return {}
  except requests.exceptions.HTTPError as e:
    print(e)
    return {}
  MC_list = get_market_cap_from_EOD(tickername)
  correct_data(tickername, res)
  max_i, maxv = argmax(res["High"]), max(res["High"])
  minv = min(res["Close"][max_i:])
  
  if len(MC_list) == 0:
    market_caps = recalculate_shares_from_EOD(tickername, res)
    if len(market_caps)==0:
      print("TICKER FOUND BUT zero value & couldn't recalculate")
      return {}
  else:
    market_caps = ([{"value": dat["value"], "date": datetime.timestamp(datetime.strptime(dat["date"],"%Y-%m-%d")), } for dat in MC_list])
      
  max_marketcap = max(market_caps, key=lambda x:x['value'])
  marketcap_million = max_marketcap["value"] / 1_000_000 # ticker.info["marketCap"] * (maxv/res["Close"][-1]) / 1_000_000 / 1_000
  mdd = (1-minv / maxv) * 100
  # for (i, qq) in (res.iloc[2268:2273].iterrows()):
  #   print(i, qq)
  # print(minv, maxv)
  
  # print(list(row for row in res.iloc[max_i:].iterrows() if 1-row[1]["Close"] / maxv < CRASH_MDD_VALUE/100))
  first_crash_date = next((i for i, row in res.iloc[max_i:].iterrows() if (1-row["Close"] / maxv > CRASH_MDD_VALUE/100)), -1)
  if first_crash_date != -1 :
    print(first_crash_date, max_marketcap)
  crash_date_ts = None if first_crash_date == -1 else int(first_crash_date.timestamp())

    # marketcap_million, mdd = abs(marketcap_million), 0
  ticker_info = BANK_INFO[tickername]
  currenci = ticker_info["currency"]
  exchrate = get_historical_exchange_rate(currenci, 'USD', datetime.fromtimestamp(max_marketcap["date"]).strftime('%Y-%m-%d'))
  if currenci in PENNIES.keys():
    exchrate *= 0.01
  marketcap_million_usd = marketcap_million * exchrate
  
  if mdd <= 0 or marketcap_million_usd < 0 or minv < 0 or maxv < 0:
    print(tickername, marketcap_million_usd, mdd)
  assert not (minv < 0 or maxv < 0)
    
  return {
      "shortname": ticker_info['shortName'],
      "ticker": tickername,
      "size": round(math.log10(marketcap_million_usd), 3),
      "MC": round(marketcap_million_usd, 0),
      "price": log_round(minv),
      "MDD": log_round(mdd),
      "CRASH_date": crash_date_ts,
  }

#%%
