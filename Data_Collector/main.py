# Economic Data Collector
# Name: main.py
# Auth: Brian Dew
# Date: Dec 31, 2017
# Desc: Check/update/retrieve economic data and store in SQL database.

# Import python packages
import sqlite3
from api_readers import api_reader as dr
from datetime import datetime
today = datetime.now().date()

# Main variables
s_list = ['CES0000000001', 'CES3000000001', 'CES0500000003',
			'LNS12300060', 'LNS12300061', 'LNS12300062']
dur = 65
source = 'BLS'

# Connect to SQL database and check for series
conn = sqlite3.connect('macro_data.db')
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
res = c.fetchall()

for s_id in s_list:
	if s_id in [i[0] for i in res]:   # Check in series in database
		print('{}: Series Available!'.format(s_id))
		s = c.execute("select * from {}".format(s_id)).fetchall()
		if len(s) > 0:  # Check if database series is blank
			lt_dt = datetime.strptime(s[0][0], '%Y-%m-%d').date()
			if (today - lt_dt).days >= dur:  # Update if needed
				print('Needs updating, though...')
				print('last available: {}'.format(s[0][0]))
				#try:
					#dr(s_id, source)
				#except:
					#print('Series collection failed')
				# return series here, eventually
			else:
				print('And up-to-date!') 
				print('last available: {}'.format(s[0][0]))
				# return series here eventually     
		#else: 
			#print('{}: New table - old name'.format(s_id))
			#dr(s_id, source, update=False)      # Get new data
			# return series here eventually 
	else: 
		print('{}: New table'.format(s_id))
		#try:
			#dr(s_id, source, update=False)          # Get new data
		#except: 
			#print('Series collection failed')
		# return series here eventually 

conn.close()