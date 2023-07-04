#%%
import requests
import socket
import time
import asyncio
from oracle_data import DB_Banks
from oracle_server import get_bank_list, get_bank_mdds, get_bank_stats,get_bank_crashes_today, get_bank_crashes_history, get_bank_crashes_stats, app, data
from waitress import serve


async def async_run_data_server(data):
  while True:
    time.sleep(1000)
    data.refresh()
  

data.refresh()
print("data is initialized!")

loop = asyncio.get_event_loop()
loop.create_task(async_run_data_server(data))

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)# %%
true_ip_address = requests.get('http://ifconfig.me').text
port = 8080
print(f"Running server on http://{ip_address}:{port}  ({true_ip_address}) {hostname}")
serve(app, host=hostname, port=port)

#%%
