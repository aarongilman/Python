# Import preliminaries
import requests
import pandas as pd
import json

# Local file with API key
import config


def api(series, date_range):
    """Collect list of series from BLS API for given dates"""
    # The url for BLS API v2
    url = 'https://api.bls.gov/publicAPI/v2/timeseries/data/'

    # API key in config.py which contains: bls_key = 'key'
    key = '?registrationkey={}'.format(config.bls_key)

    # Handle dates
    dates = [(str(date_range[0]), str(date_range[1]))]
    while int(dates[-1][1]) - int(dates[-1][0]) > 10:
        dates = [(str(date_range[0]), str(date_range[0] + 9))]
        d1 = int(dates[-1][0])
        while int(dates[-1][1]) < date_range[1]:
            d1 = d1 + 10
            d2 = min([date_range[1], d1 + 9])
            dates.append((str(d1), (d2)))

    df = pd.DataFrame()

    for start, end in dates:
        # Submit the list of series as data
        data = json.dumps({
            "seriesid": list(series.keys()),
            "startyear": start, "endyear": end})

        # Post request for the data
        p = requests.post(
            f'{url}{key}',
            headers={'Content-type': 'application/json'},
            data=data).json()

        for s in p['Results']['series']:
            col = series[s['seriesID']]
            for r in s['data']:
                date = pd.to_datetime(
                    (f"{r['year']}Q{r['period'][-1]}"
                     if r['period'][0] == 'Q'
                     else f"{r['periodName']} {r['year']}"))
                df.at[date, col] = float(r['value'])
    df = df.sort_index()
    # Output results
    print('Post Request Status: {}'.format(p['status']))

    return df
