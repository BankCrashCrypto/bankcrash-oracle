#%%

import requests
import json
from joblib import Memory
from config_accounts import OEXR_APP_ID

memory = Memory("cache_EXR.all_request")


@memory.cache
def get_historical_exchange_rate(base_currency, target_currency, date):
	url = f"https://openexchangerates.org/api/historical/{date}.json?app_id={OEXR_APP_ID}"

	response = requests.get(url)

	if response.status_code == 200:
		data = json.loads(response.text)
		rate = data['rates'][target_currency] / data['rates'][base_currency]
		return rate
	else:
		print(response.text)
		return None



