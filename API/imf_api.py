import requests # Python 2.7, requests version 2.12.4

url = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/'
key = 'CompactData/IFS/M.GB.PMP_IX' # adjust codes here
data = requests.get('{}{}'.format(url,key)).json()
data['CompactData']['DataSet']['Series']['Obs'][-1]
