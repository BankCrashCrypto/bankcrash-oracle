#%%
import pandas as pd
import yfinance as yf
import requests
from p_tqdm import p_map

import math


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
    _, maxv = argmax(res["High"]), max(res["High"])
    estimated_marketcap_million = ticker.info["marketCap"] * (maxv/res["Close"][-1]) / 1_000_000 / 1_000
    mdd = (1-res["Close"][-1] / maxv) * 100
    if res["Close"][-1] < 0 or maxv < 0:
      estimated_marketcap_million = abs(estimated_marketcap_million)
      mdd = 0
    if mdd <= 0 or estimated_marketcap_million < 0 or res["Close"][-1] < 0 or maxv < 0:
      print(tickername, estimated_marketcap_million, mdd)
    # print(tickername, estimated_marketcap, mdd)
    return {
        "shortname": ticker.info['shortName'],
        "name": tickername,
        "MDD": log_round(mdd),
        "size": round(math.log10(estimated_marketcap_million), 3),
        "price": log_round(res["Close"][-1])
    }
  except requests.exceptions.HTTPError as e:
    print(e)
  return {}


def download_all_data():
  all_banks = pd.read_csv("banks.csv", names=["name", "ticker"])
  print(all_banks)
  all_data = p_map(request_data, all_banks["ticker"][0:])
  all_data = filter(lambda d: d, all_data)
  database = sorted(all_data, key=lambda x: x["size"], reverse=True)
  return database


if __name__ == '__main__':
  download_all_data()


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
