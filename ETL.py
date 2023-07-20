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


def to_EOD_TICKER(ticker):
  if ticker in YAHOO_TO_EOD_TICKER.keys():
    return YAHOO_TO_EOD_TICKER[ticker]
  if len(ticker.split("."))==2:
    stock, exchange = ticker.split(".")
    if exchange in YAHOO_TO_EOD_EXCHANGE.keys():
      exchange = YAHOO_TO_EOD_EXCHANGE[exchange]
    return stock + "." + exchange
  return ticker


def correct_data(tickername, res):
  if tickername == "CPI.JO":
    res.drop(res.iloc[2270].name, inplace=True)
    res.drop(res.iloc[2268].name, inplace=True)
  else:
    return
  
  
  
  
  