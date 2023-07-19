#%%
import pandas as pd
# files = ["Complete-List-of-Bank-ADRs-Traded-on-OTC-Markets-Dec-22-2020.xlsx",
#          "Complete-List-of-Bank-Stocks-listed-on-NASDAQ-Mar-13-23.xlsx",
# "Complete-List-of-Foreign-Banks-Stocks-listed-on-NYSE-Mar-26-23.xlsx",
# "Complete-List-of-US-Banks-Stocks-listed-on-NYSE-May-7-23.xlsx",]
all_banks = pd.read_csv("banks.csv", names=["name", "ticker"])

print(all_banks)
# all_banks = df
# df
#%%
all_banks["ticker"]
#%%
import yfinance as yf

msft = yf.Ticker("ZION", date=10)

# get all stock info
del msft.info["companyOfficers"]
msft.info
# %%
for property, value in vars(msft).items():
    print(property, ":", value)
# %%
import datetime
ress = msft._download_options(date=round((datetime.datetime.now() - datetime.timedelta(days=2)).timestamp()*1000))
# %%
ress
# %%
(datetime.datetime.now() - datetime.timedelta(days=2)).timestamp() 
# %%
dir(msft)
# %%
res=(msft.history(period="120mo"))
# %%
res=(msft.history_metadata)
# %%
res

# %%
(res["Low"][-1], res["Low"][1])
# %%
def argmax(iterable):
    return max(enumerate(iterable), key=lambda x: x[1])[0]
argmax(res["High"]), max(res["High"])
# %%


for tickername in all_banks["ticker"][85:]:
	if tickername in ["BIMB.KL", ]: continue
	try:
		ticker = yf.Ticker(tickername)
		res=(ticker.history(period="120mo"))
		mi, maxv = argmax(res["High"]), max(res["High"])
		print(tickername, res["Low"][1]/maxv)
		# if "industry" in ticker.info:
		# 	print(ticker.info["industry"])
		# 	print(ticker.info["marketCap"])
		# else:
		# 	print(ticker.info)
	except requests.exceptions.HTTPError as e:
		print(tickername)

# %%
