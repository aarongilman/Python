# Import libraries
import pandas as pd
import pandas_datareader.data as web
import datetime
import os
import glob
import shutil

import stocks

# Executive Dash begins here
import execdash

import requests # Python 2.7, requests version 2.12.4

url = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/'
key = 'CompactData/IFS/M.DE.PCPI_PC_CP_A_PT' # adjust as needed
data = requests.get('{}{}'.format(url,key)).json()
# Navigate to observations in JSON data
obs = data['CompactData']['DataSet']['Series']['Obs']

# Create pandas dataframe from the observations
df = pd.DataFrame(obs)[['@OBS_VALUE','@TIME_PERIOD']]
df.columns = ['value', 'date']
df.loc[:,'value'] = df['value'].astype(float).round(1)
df = df.set_index(pd.to_datetime(df['date']))['value']

lvalue = df[-1]
ldate = str(df.index[-1].strftime('%b %Y'))
onemo = round(lvalue - df[-2], 2)
onemoar = '<i class="fa fa-caret-up" aria-hidden="true"></i>'
if onemo < -0.01:
    onemoar = '<i class="fa fa-caret-down" aria-hidden="true"></i>'
latest = ' Latest: {}: {}% <br>  One month change: {} {}'.format(ldate, lvalue, onemoar, onemo)

from datetime import datetime as dt
import time
xlabel = time.mktime(dt(1995, 2, 1, 2, 0, 0).timetuple())*1000

from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, Span, Label, HoverTool, Range1d
from bokeh.embed import components

source = ColumnDataSource({'x': df.index, 'y': df.values, 'Date': df.index.strftime('%b %Y')})
tooltips = """
            <div>
                <span style="font-size: 12px;">@Date:</span>
                <span style="font-size: 12px; font-weight: bold;">@y{1.1}</span>
            </div>
"""
# horizontal line at zero
hline = Span(location=0, dimension='width', line_color='gray', line_width=1)
p = figure(width=700,height=300,x_axis_type='datetime',
           tools=['pan,wheel_zoom,box_zoom,reset'], logo=None,
           toolbar_location="below", toolbar_sticky=False)
p.add_layout(hline)
p.sizing_mode = 'scale_width'
p.line('x', 'y', source = source, line_width=3, color='Orange', alpha=1.0, level='overlay')
p.xgrid.grid_line_color = None
p.outline_line_color = 'white'
p.axis.axis_line_color = 'white'
citation = Label(x=xlabel, y=5.5, render_mode='css', x_units='data', text_font_size='9pt',
                 text_color='#686868', text=latest, background_fill_color='white', background_fill_alpha=1.0)
p.add_layout(citation)
p.add_tools(HoverTool(tooltips=tooltips, line_policy='nearest', show_arrow=False))
p.toolbar.active_drag = None
script, div = components(p)

with open('C:/Working/bdecon.github.io/plots/de_cpi.html', 'w') as text_file:
    text_file.write(                  # txt file created
        '{} {}'.format(script, div)
    )

url = 'https://www.quandl.com/api/v3/datasets/CURRFX/USDMXN.csv?api_key=x7q1kgMKv96cXx83GtSN&start_date=2016-01-01'
df = pd.read_csv(url, parse_dates=['Date'], index_col='Date')

lvalue = round(df.iloc[0]['Rate'],3)
ldate = str(df.index[0].strftime('%b %d, %Y'))
onemo = round((lvalue - df.iloc[21]['Rate']) / df.iloc[21]['Rate'] * 100, 2)
onemoar = '<i class="fa fa-caret-up" aria-hidden="true"></i>'
if onemo < -0.01:
    onemoar = '<i class="fa fa-caret-down" aria-hidden="true"></i>'
latest = ' Latest: {}: {} <br>  One month change: {} {}%'.format(ldate, lvalue, onemoar, onemo)

source = ColumnDataSource({'x': df.index, 'y': df['Rate'], 'Date': df.index.format()})
tooltips = """
            <div>
                <span style="font-size: 12px;">@Date:</span>
                <span style="font-size: 12px; font-weight: bold;">@y</span>
            </div>
"""
p = figure(width=700,height=300,x_axis_type='datetime',tools=['pan, wheel_zoom,box_zoom,reset'],
           logo=None, toolbar_location="below", toolbar_sticky=False)
#p.title.text = 'Mexican Pesos (MXN) per U.S. Dollar (USD)'
p.title.text_font_size='14pt'
p.yaxis.axis_label = 'MXN/USD'
citation = Label(x=60, y=21.1, render_mode='css', x_units='screen', text_font_size='9pt',
                 text_color='#686868', text=latest, background_fill_color='white', background_fill_alpha=1.0)
p.add_layout(citation)
p.sizing_mode = 'scale_width'
p.line('x', 'y', source = source, line_width=3, color='Blue')
p.xgrid.grid_line_color = None
p.outline_line_color = 'white'
p.axis.axis_line_color = 'white'
p.add_tools(HoverTool(tooltips=tooltips, show_arrow=False, point_policy='snap_to_data'))
p.toolbar.active_drag = None
script, div = components(p)

with open('C:/Working/bdecon.github.io/plots/usdmxn.html', 'w') as text_file:
    text_file.write(                  # txt file created
        '{} {}'.format(script, div)
    )

# Volatility index (VIX) from CBOE
vixurl = 'http://www.cboe.com/publish/scheduledtask/mktdata/datahouse/vixcurrent.csv'
vixcol = ['Date', 'Open', 'High', 'Low', 'VIXCLS']
df = pd.read_csv(vixurl, skiprows=3023, names=vixcol, parse_dates=['Date']).set_index('Date')['VIXCLS']

lvalue = df[-1]
ldate = str(df.index[-1].strftime('%b %d, %Y'))
onemo = round((lvalue - df[-21]) / df[-21] * 100, 2)
onemoar = '<i class="fa fa-caret-up" aria-hidden="true"></i>'
if onemo < -0.01:
    onemoar = '<i class="fa fa-caret-down" aria-hidden="true"></i>'
latest = ' Latest: {}: {} <br>  One month change: {} {}%'.format(ldate, lvalue, onemoar, onemo)

xlabel = time.mktime(dt(2016, 7, 3, 2, 0, 0).timetuple())*1000

source = ColumnDataSource({'x': df.index, 'y': df.values, 'Date': df.index.strftime('%b %d, %Y')})
tooltips = """
            <div>
                <span style="font-size: 12px;">@Date:</span>
                <span style="font-size: 12px; font-weight: bold;">@y{1.1}</span>
            </div>
"""
# horizontal line at zero
hline = Span(location=0, dimension='width', line_color='gray', line_width=1)
p = figure(width=700,height=300,x_axis_type='datetime',
           tools=['pan,wheel_zoom,box_zoom,reset'], logo=None,
           toolbar_location="below", toolbar_sticky=False)
p.add_layout(hline)
p.sizing_mode = 'scale_width'
p.line('x', 'y', source = source, line_width=3, color='Green', alpha=1.0, level='overlay')
p.xgrid.grid_line_color = None
p.outline_line_color = 'white'
p.axis.axis_line_color = 'white'
citation = Label(x=xlabel, y=26.8, render_mode='css', x_units='data', text_font_size='9pt',
                 text_color='#686868', text=latest, background_fill_color='white', background_fill_alpha=1.0)
p.add_layout(citation)
p.add_tools(HoverTool(tooltips=tooltips, line_policy='nearest', show_arrow=False))
p.toolbar.active_drag = None
script, div = components(p)

with open('C:/Working/bdecon.github.io/plots/vix.html', 'w') as text_file:
    text_file.write(                  # txt file created
        '{} {}'.format(script, div)
    )

# Updated inputs to pandas datareader:
source = 'fred'
start = datetime.datetime(2010,1,1)
series = ['GDPC1']

# Retrieve data as pandas dataframe named df
df = web.DataReader(series[0], source, start, )

# Calculate growth rate
df['Y'] = ((1 + (df[series[0]] - df[series[0]].shift(1))/df[series[0]].shift(1))**4 - 1) * 100
df['Y'] = df['Y'].round(1)
# String Date column
df['quarter'] = df.index.quarter
df['year'] = df.index.strftime('%Y')
df['strdate'] = df.year.map(str) + " Q" + df.quarter.map(str)

# Declare variables for chart label
Y = (df[series[0]][-1] / 1000).round(decimals=1)
q = df.quarter[-1]
y = df.year[-1]
ch = df['Y'][-1].round(decimals=1)

df = df.dropna()

latest = '{} Q{}: Real GDP: {}T; Growth: {}%'.format(y, q, Y, ch)
xlabel = time.mktime(dt(2010, 7, 3, 2, 0, 0).timetuple())*1000
source = ColumnDataSource({'x': df.index, 'y': df['Y'], 'Date': df.strdate})

def get_width():
    mindate = min(source.data['x'])
    maxdate = max(source.data['x'])
    return 0.8 * (maxdate-mindate).total_seconds()*1000 / len(source.data['x'])

tooltips = """
            <div>
                <span style="font-size: 12px;">@Date:</span>
                <span style="font-size: 12px; font-weight: bold;">@y{1.1}</span>
            </div>
"""
# horizontal line at zero
hline = Span(location=0, dimension='width', line_color='gray', line_width=1)
p = figure(width=700,height=300,x_axis_type='datetime',
           tools=['pan,wheel_zoom,box_zoom,reset'], logo=None,
           toolbar_location="below", toolbar_sticky=False, y_range=Range1d(-3, 6.5))
p.add_layout(hline)
p.sizing_mode = 'scale_width'
p.vbar('x', width=get_width(), bottom=0, top='y', source = source, color='Red', alpha=1.0, level='overlay')
p.xgrid.grid_line_color = None
p.outline_line_color = 'white'
p.axis.axis_line_color = 'white'
citation = Label(x=xlabel, y=5, render_mode='css', x_units='data', text_font_size='9pt',
                 text_color='#686868', text=latest, background_fill_color='white', background_fill_alpha=1.0)
p.add_layout(citation)
p.add_tools(HoverTool(tooltips=tooltips, show_arrow=False))
p.toolbar.active_drag = None

script, div = components(p)
with open('C:/Working/bdecon.github.io/plots/gdp.html', 'w') as text_file:
    text_file.write(                  # txt file created
        '{} {}'.format(script, div)
    )

# Run latex files
os.chdir('C:/Working/Python/Macro_Dash/')
os.system('pdflatex ExecDash.tex')

# Run stata do file for chartbook
os.chdir('C:/Working/USA/dofiles/')
os.system('"C:\Program Files (x86)\Stata14\Stata-64" /e do 01_dashboard_USA.do')

# Clear tikz external folder
os.chdir('C:/Working/USA/datafiles/tikz/')
filelist = glob.glob("*")
for f in filelist:
    os.remove(f)

# Run LaTeX file
os.chdir('C:/Working/USA/datafiles/')
os.system('pdflatex -synctex=1 -interaction=nonstopmode -shell-escape MacroDash.tex')

# Copy pdf files to website
os.chdir('C:/Working/USA/datafiles/')
shutil.copy('MacroDash.pdf', 'C:/Working/bdecon.github.io/')
os.chdir('C:/Working/Python/Macro_Dash/')
shutil.copy('ExecDash.pdf', 'C:/Working/bdecon.github.io/Dash/')

# Push to website
os.chdir('C:/Working/bdecon.github.io/')
os.system('git commit -am "Updated dash"')
os.system('git push origin master')
