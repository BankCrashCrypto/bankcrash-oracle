#%%
import requests
import pandas as pd

def get_alpha_vantage_data(symbol, api_key):
    base_url = "https://www.alphavantage.co/query"
    function = "OVERVIEW"

    data = { "function": function,
             "symbol": symbol,
             "apikey": api_key }

    response = requests.get(base_url, params=data)

    return response.json()["MarketCapitalization"]

api_key = "NLUY5HGVQMYRWI85"
symbol = "AAPL"
market_cap = get_alpha_vantage_data(symbol, api_key)

print(f"The market cap of {symbol} is {market_cap}")
# %%
import requests
EOD_APY_KEY = "64941a37784db9.21946561"
url = "https://eodhistoricaldata.com/api/eod/AAPL.US?from=2000-01-01&to=2022-12-31&api_token=64941a37784db9.21946561"
url = "https://eodhistoricaldata.com/api/eod/JPM?from=2000-01-01&to=2022-12-31&api_token=64941a37784db9.21946561"
url = f"https://eodhistoricaldata.com/api/historical-market-cap/JPM?from=2000-01-01&to=2022-12-31&api_token={EOD_APY_KEY}"
# url = f"https://eodhistoricaldata.com/api/historical-market-cap/NDA-FI.HE?from=2000-01-01&to=2024-12-31&api_token={EOD_APY_KEY}"
# url = f"https://eodhistoricaldata.com/api/fundamentals/NDA-FI.HE?api_token={EOD_APY_KEY}&filter=outstandingShares::quarterly"
# url = "https://eodhistoricaldata.com/api/historical-market-cap/AAPL.US?from=2000-01-01&to=2022-12-31&api_token=64941a37784db9.21946561"
data = requests.get(url)
# Parse data here
print(data.text)
# %%
# %%
import yfinance as yf
msft = yf.Ticker("MSFT")
# res=msft.get_info(proxy="https://194.182.163.117:3128")
# res=msft.info()
res=msft.get_info(proxy="91.203.25.28:4153")
# res=msft.history(period="120mo", proxy="91.203.25.28:4153")
# res=msft.get_info(proxy="http://41.65.103.27:1976")
# res=msft.get_info(proxy="27.72.244.228:8080")
print(res)
# %%
list(json.loads(data.text).values())
# %%
"CPI.JO"
"ETE.AT"
"EUROB.AT"
# %%
"U11.SI", "O39.SI", "DANS.VI", "MTPOF", "SHBI",  "BSMX", "ITCB", "BIMB.KL"
# %%
import json
import requests
EOD_APY_KEY = "64941a37784db9.21946561"
ticker="002142.SHE"
url = f"https://eodhistoricaldata.com/api/fundamentals/{ticker}?api_token={EOD_APY_KEY}&filter=outstandingShares::quarterly"
data = requests.get(url)
print(data.text)
shares = list(json.loads(data.text).values())
print(shares)
# %%
print((requests.get(f"https://eodhistoricaldata.com/api/exchanges-list/?api_token={EOD_APY_KEY}")).text)
# %%


#%%
TTB.BK

VMUK.L
STAN.L

WBC.AX
SUN.AX
NAB.AX
MQG.AX


5819.KL
1295.KL
1023.KL



# MONET.PR
# KOMB.PR

UNIONBANK.NS
SOUTHBANK.NS
SBIN.NS
RBLBANK.NS
PSB.NS
PNB.NS

RAW.F
EBO.F


BSLI3.SA  MISSING


OTP.BD


U11.SI
O39.SI    # SINGAPORE kellene legyen

8308.T   # TOKYO Stock exchange
8421.T
8601.T

# TTB.BK

SBK.JO    # Johannesburg
NED.JO
FSR.JO


SPL.WA
PKO.WA
PEO.WA
MBK.WA

MB.MI  # MILAN?
ISP.MI
BMED.MI
UCG.MI

# Euronext Paris
# PA / XPAR
# flag
# Euronext Brussels
# BR / XBRU
# flag
# Euronext Lisbon
# LS / XLIS
# flag
# Euronext Amsterdam
# AS / XAMS


PBB.DE

AXISBANK.BO   # BSE indiai exchnage... AXISBANK.NSE


FIBI.TA  # NA, lehet hogy FIX 100m shares?


#%%
SI
LMST
SHBI
U11.SI
BSMX
ITCB
#%%
"600919.SS"
"600919.SHG"
"601211.SS"
"601211.SHG"
"601658.SS"
"601658.SHG"
"601939.SS"
"601939.SHG"
#%%

# %%

# %%
import yfinance as yf
ticker="NDA-FI.HE"
ticker = yf.Ticker(ticker)
res = ticker.history(period="240mo")
# %%
print(res)
# %%
print((res.index[0].timestamp()))
print((res.index[1].timestamp()))
print((res.index[1200].timestamp()))
# %%
price_tss = [res.index[i].timestamp() for i in range(0,len(res))]
# %%
import math
print((1664488800.0-1531256400.0)/24/60/60*5/7)
print(int(math.ceil((1664488800.0-1531256400.0)/24/60/60*5/7)))
print((res.index[0+int(math.ceil((1664488800.0-1531256400.0)/24/60/60*5/7))].timestamp()))

# %%
(1681851600.0-1531256400.0)/24/60/60
# %%
import datetime
print((shares[0]["dateFormatted"]))
print(type(shares[0]["dateFormatted"]))
 
# %%
market_cap = []
ti = 0 
for share in shares[::-1]:
    element = datetime.datetime.strptime(share["dateFormatted"],"%Y-%m-%d")
    timestamp = datetime.datetime.timestamp(element)-3600
    while timestamp>res.index[ti].timestamp():
        ti+=1
    print(timestamp,res.index[ti-1].timestamp()-timestamp,res.index[ti].timestamp()-timestamp, share["dateFormatted"])
    trueti = ti if res.index[ti].timestamp()-timestamp==0 else ti-1
    print(trueti, ti)
    price = res["Close"][trueti]
    print(price)
    market_cap.append((price*share["shares"], res.index[ti].timestamp()))

# %%
market_cap
# %%
# %%
[d for d in shares]
# %%
# %%
def generate_dates(start_year, end_year):
    result = []
    months = [("12", "31"), ("09", "30"), ("06", "30"), ("03", "31")]

    for year in range(start_year, end_year - 1, -1):
        for month, day in months:
            result.append(f"{year}-{month}-{day}")

    return result

dates = generate_dates(2022, 2003)
for date in dates:
    print(date)
# %%
# %%
import json
max(list(json.loads(data.text).values()), key=lambda x:x['value'])
# %%
https://eodhistoricaldata.com/api/historical-market-cap/AAPL.US?api_token=64941a37784db9.21946561
# %%
import yfinance as yf
ticker = yf.Ticker("0016.HK")
print(( ticker.history(period="60mo")))
print((ticker.info))
# %%
import requests

try:
    response = requests.get('https://finance.yahoo.com', timeout=5)
    # If the response was successful, no Exception will be raised
    print(response.raise_for_status())
    print('Yahoo Finance is up and running.')
except Exception as err:
    print(f'Error occurred: {err}. Yahoo Finance might be down.')
# %%

# %%
(data.text)
# %%
import pandas as pd
from io import StringIO
pd.read_csv(StringIO(data.text))
# %%
{'address1': 
    '383 Madison Avenue', 'city': 'New York', 'state': 'NY', 'zip': '10179',
    'country': 'United States', 'phone': '212 270 6000', 'website': 'https://www.jpmorganchase.com', 
    'industry': 'Banks—Diversified', 'sector': 'Financial Services', 
    'longBusinessSummary': 'JPMorgan Chase & Co. operates as a financial services company worldwide. It operates through four segments: Consumer & Community Banking (CCB), Corporate & Investment Bank (CIB), Commercial Banking (CB), and Asset & Wealth Management (AWM). The CCB segment offers deposit, investment and lending products, cash management, and payments and services to consumers and small businesses; mortgage origination and servicing activities; residential mortgages and home equity loans; and credit cards, auto loans, leases, and travel services. The CIB segment provides investment banking products and services, including corporate strategy and structure advisory, and equity and debt markets capital-raising services, as well as loan origination and syndication; payments and cross-border financing; and cash and derivative instruments, risk management solutions, prime brokerage, and research. This segment also offers securities services, including custody, fund accounting and administration, and securities lending products for asset managers, insurance companies, and public and private investment funds. The CB segment provides financial solutions, including lending, payments, investment banking, and asset management to small and midsized companies, local governments, nonprofit clients, and large corporations; and commercial real estate banking services to investors, developers, and owners of multifamily, office, retail, industrial, and affordable housing properties. The AWM segment offers multi-asset investment management solutions in equities, fixed income, alternatives, and money market funds to institutional clients and retail investors; and retirement products and services, brokerage, custody, estate planning, lending, deposits, and investment management products. The company also provides ATM, online and mobile, and telephone banking services. JPMorgan Chase & Co. was founded in 1799 and is headquartered in New York, New York.', 
    'fullTimeEmployees': 296877, 
    'companyOfficers': [{'maxAge': 1, 'name': 'Mr. James  Dimon', 'age': 66, 'title': 'Chairman & CEO', 'yearBorn': 1956, 'fiscalYear': 2022, 'totalPay': 6818729, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Mr. Daniel Eduardo Pinto', 'age': 59, 'title': 'Pres & COO', 'yearBorn': 1963, 'fiscalYear': 2022, 'totalPay': 7162401, 'exercisedValue': 7226498, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Mr. Jeremy  Barnum', 'age': 49, 'title': 'Exec. VP & CFO', 'yearBorn': 1973, 'fiscalYear': 2022, 'totalPay': 5255000, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Ms. Mary Callahan Erdoes', 'age': 55, 'title': 'Chief Exec. Officer of Asset & Wealth Management', 'yearBorn': 1967, 'fiscalYear': 2022, 'totalPay': 10655000, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Ms. Marianne  Lake', 'age': 52, 'title': 'Co-Chief Exec. Officer of Consumer & Community Banking', 'yearBorn': 1970, 'fiscalYear': 2022, 'totalPay': 7520688, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Ms. Jennifer A. Piepszak', 'age': 51, 'title': 'Co-Chief Exec. Officer of Consumer & Community Banking', 'yearBorn': 1971, 'fiscalYear': 2022, 'totalPay': 7455000, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Ms. Elena A. Korablina', 'age': 48, 'title': 'MD, Firmwide Controller & Principal Accounting Officer', 'yearBorn': 1974, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Ms. Lori Ann Beer', 'age': 54, 'title': 'Global Chief Information Officer', 'yearBorn': 1968, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Mr. Mikael  Grubb', 'title': 'Head of Investor Relations', 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Ms. Stacey  Friedman', 'age': 53, 'title': 'Exec. VP & Gen. Counsel', 
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         'yearBorn': 1969, 'exercisedValue': 0, 'unexercisedValue': 0}], 
    'auditRisk': 10, 'boardRisk': 3, 
    'compensationRisk': 8, 'shareHolderRightsRisk': 3, 'overallRisk': 6, 'governanceEpochDate': 1685577600, 
    'compensationAsOfEpochDate': 1672444800, 'maxAge': 86400, 'priceHint': 2, 'previousClose': 142.32, 
    'open': 142.31, 'dayLow': 138.95, 'dayHigh': 142.6, 'regularMarketPreviousClose': 142.32, 
    'regularMarketOpen': 142.31, 'regularMarketDayLow': 138.95, 'regularMarketDayHigh': 142.6, 
    'dividendRate': 4.0, 'dividendYield': 0.0279, 'exDividendDate': 1688515200, 'payoutRatio': 0.295, 
    'fiveYearAvgDividendYield': 2.8, 'beta': 1.086267, 'trailingPE': 10.285925, 'forwardPE': 9.977127, 
    'volume': 9680828, 'regularMarketVolume': 9680828, 'averageVolume': 11497387, 
    'averageVolume10days': 9056960, 'averageDailyVolume10Day': 9056960, 'bid': 138.1, 'ask': 139.37, 
    'bidSize': 3200, 'askSize': 900, 'marketCap': 407893245952, 'fiftyTwoWeekLow': 101.28, 'fiftyTwoWeekHigh': 144.34, 'priceToSalesTrailing12Months': 3.1588778, 'fiftyDayAverage': 138.2526,
    'twoHundredDayAverage': 131.5685, 'trailingAnnualDividendRate': 4.0, 'trailingAnnualDividendYield': 0.028105676, 'currency': 'USD', 'enterpriseValue': -322498953216, 'profitMargins': 0.32539, 
    'floatShares': 2896660039, 'sharesOutstanding': 2922289920, 'sharesShort': 17187232, 'sharesShortPriorMonth': 18681417, 'sharesShortPreviousMonthDate': 1682640000, 'dateShortInterest': 1685491200, 
    'sharesPercentSharesOut': 0.0058999998, 'heldPercentInsiders': 0.00897, 'heldPercentInstitutions': 0.71988, 'shortRatio': 1.61, 'shortPercentOfFloat': 0.0058999998, 'bookValue': 94.336, 
    'priceToBook': 1.4796048, 'lastFiscalYearEnd': 1672444800, 'nextFiscalYearEnd': 1703980800, 'mostRecentQuarter': 1680220800, 'earningsQuarterlyGrowth': 0.524, 'netIncomeToCommon': 40240001024,
    'trailingEps': 13.57, 'forwardEps': 13.99, 'pegRatio': -2.26, 'lastSplitFactor': '3:2', 'lastSplitDate': 960768000, 'enterpriseToRevenue': -2.498, 'exchange': 'NYQ', 'quoteType': 'EQUITY', 
    'symbol': 'JPM', 'underlyingSymbol': 'JPM', 'shortName': 'JP Morgan Chase & Co.', 'longName': 'JPMorgan Chase & Co.', 'firstTradeDateEpochUtc': 322151400, 'timeZoneFullName': 'America/New_York', 
    'timeZoneShortName': 'EDT', 'uuid': 'bc753df4-b894-3e19-9c58-995ef66d8e67', 'gmtOffSetMilliseconds': -14400000, 'currentPrice': 139.58, 'targetHighPrice': 193.0, 'targetLowPrice': 140.0, 
    'targetMeanPrice': 160.65, 'targetMedianPrice': 159.0, 'recommendationMean': 2.1, 'recommendationKey': 'buy', 'numberOfAnalystOpinions': 24, 'totalCash': 1420403015680, 'totalCashPerShare': 486.058, 'totalDebt': 651852972032, 'totalRevenue': 129125998592, 'revenuePerShare': 43.57, 
    'returnOnAssets': 0.01091, 'returnOnEquity': 0.14267, 'grossProfits': 122306000000, 'operatingCashflow': 37795000320, 'earningsGrowth': 0.559, 'revenueGrowth': 0.233, 'grossMargins': 0.0, 'ebitdaMargins': 0.0, 'operatingMargins': 0.40575, 'financialCurrency': 'USD', 
    'trailingPegRatio': 2.9345}