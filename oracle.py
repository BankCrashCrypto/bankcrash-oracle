#%%

import requests
import socket
import time
import asyncio
from oracle_server import app, data
from waitress import serve


async def async_run_data_server(data):
  while True:
    time.sleep(1000)
    data.refresh()
  
def main(multithreaded):
  print("data is loading...")
  data.refresh(multithreaded)
  print("data is initialized!")

  loop = asyncio.get_event_loop()
  loop.create_task(async_run_data_server(data))

  hostname = socket.gethostname()
  ip_address = socket.gethostbyname(hostname)# %%
  true_ip_address = requests.get('http://ifconfig.me').text
  port = 8079
  print(f"Running server on http://{ip_address}:{port}  ({true_ip_address}) {hostname}")
  serve(app, host=hostname, port=port, url_scheme='https')

# main()
# %%
