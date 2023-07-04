#%%
from flask import Flask, jsonify
from flask_cors import CORS
from oracle_data import DB_Banks


app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

data = DB_Banks()


@app.route('/bank_list')
def get_bank_list():
  print(data.bank_list)
  responee = jsonify(data.bank_list)
  responee.headers['Content-Type'] = 'application/json'
  return responee

@app.route('/bank_mdds')
def get_bank_mdds():
  print(data.bank_mdds)
  responee = jsonify(data.bank_mdds)
  responee.headers['Content-Type'] = 'application/json'
  return responee

@app.route('/bank_stats')
def get_bank_stats():
  print(data.bank_stats)
  responee = jsonify(data.bank_stats)
  responee.headers['Content-Type'] = 'application/json'
  return responee


@app.route('/bank_crashes_stats')
def get_bank_crashes_stats():
  print(data.bank_crashes_stats)
  responee = jsonify(data.bank_crashes_stats)
  responee.headers['Content-Type'] = 'application/json'
  return responee

@app.route('/bank_crashes_history')
def get_bank_crashes_history():
  print(data.bank_crashes_history)
  responee = jsonify(data.bank_crashes_history)
  responee.headers['Content-Type'] = 'application/json'
  return responee

@app.route('/bank_crashes_today')
def get_bank_crashes_today():
  print(data.bank_crashes_today)
  responee = jsonify(data.bank_crashes_today)
  responee.headers['Content-Type'] = 'application/json'
  return responee

def create_app():
   return app
 
#%%
if __name__ == '__main__':
  from waitress import serve
  data.refresh()
  # run_data_server(data)
  # with app.app_context():
  #   (get_bank_list())
  #   (get_bank_mdds())
  #   (get_bank_stats())
  #   (get_bank_crashes_stats())
  #   (get_bank_crashes_history())
  #   (get_bank_crashes_today())
  # app.run(port=5000)#, debug=True)
  serve(app, host="0.0.0.0", port=8080)
  
  

# %%
