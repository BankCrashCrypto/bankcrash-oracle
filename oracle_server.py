from flask import Flask, jsonify
from oracle import download_all_data
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

global db
global db_heatmap
global db_bank_crashes
global db_bank_list
global db_today_crashes


@app.route('/bank_mdds')
def get_data():
  global db
  responee = jsonify(db)
  responee.headers['Content-Type'] = 'application/json'
  return responee


if __name__ == '__main__':

  db = download_all_data()
  app.run(port=5000, debug=True)
  
  
