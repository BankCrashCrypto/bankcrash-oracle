#%%
import time
import asyncio

async def async_run_data_server(data):
    while True:
        time.sleep(1000)
        data.refresh()
  
def run_data_server(data):
    data.refresh()
    asyncio.run(async_run_data_server(data)) 


if __name__ == '__main__':
    from oracle_data import DB_Banks
    data = DB_Banks()
    run_data_server(data)


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
