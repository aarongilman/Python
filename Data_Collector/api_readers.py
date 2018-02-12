# Import python packages
import requests
import sqlite3
import json
import config   # Local file config.py with API keys

def api_reader(s_id, source, update=True):
    """Collect data from web APIs"""
    if str(source).lower() == 'bls':
        bls_key = config.bls_key   # BLS API key from registration
        api = 'https://api.bls.gov/publicAPI/v2/timeseries/data/'
        url = '{}?registrationkey={}'.format(api, bls_key)

        if update == False:
    	   start_year = "2008"
        else:
    	   start_year = "2015"

        # Info for sending with post request
        headers = {'Content-type': 'application/json'}
        data = json.dumps({"seriesid": [s_id],  # BLS series ID
                 "startyear": start_year, "endyear": "2017"})

        # Request json data from BLS API
        p = requests.post(url, data=data, headers=headers).json()
        print(p['status'])  # Print whether API request was successful

        # Location within API results of time series and footnotes
        r = p['Results']['series'][0]['data']

        # json date and value to list of tuples
        dates = ['{}-{}-01'.format(i['year'], i['period'][1:]) for i in r]
        data = zip(dates, [float(i['value']) for i in r])

        # Connect to SQL database and check for series
        conn = sqlite3.connect('macro_data.db')

        # Create and fill the table
        conn.execute("create table if not exists {}(Date, Value)".format(s_id))
        conn.executemany("insert into {}(Date, Value) values (?, ?)".format(s_id), data)

        # Save and close
        conn.commit()
        conn.close()
    else: 
        print('Error: source not available')