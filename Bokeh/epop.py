import pandas as pd
import numpy as np


def epop(df):
    """Calculate the employment to population ratio"""
    emp = df['PREMPNOT'].values
    wgt = df['PWSSWGT'].values
    ep = np.average(np.where(emp == 1, 1, 0), weights=wgt)
    return ep


def epop_calc():
    dft = pd.DataFrame()
    query = 'PRTAGE >= 25 and PRTAGE <= 54'
    query1 = 'PESEX == 1'
    query2 = 'PESEX == 2'
    col_list = ['HRMONTH', 'PRTAGE', 'PREMPNOT', 'PWSSWGT', 'PESEX']
    path = 'C:/Working/econ_data/micro/data'
    for year in range(1994, 2019):
        file = f'{path}/cps_{year}.ft'
        df = pd.read_feather(file, nthreads=4)[col_list].query(query)
        year_vals = df.groupby('HRMONTH').apply(epop)
        for month, epop_val in year_vals.iteritems():
            date = pd.to_datetime(f'{year}-{month}-01')
            dft.at[date, 'Total'] = epop_val * 100
        df2 = df.query(query1)
        year_vals = df2.groupby('HRMONTH').apply(epop)
        for month, epop_val in year_vals.iteritems():
            date = pd.to_datetime(f'{year}-{month}-01')
            dft.at[date, 'Men'] = epop_val * 100
        df2 = df.query(query2)
        year_vals = df2.groupby('HRMONTH').apply(epop)
        for month, epop_val in year_vals.iteritems():
            date = pd.to_datetime(f'{year}-{month}-01')
            dft.at[date, 'Women'] = epop_val * 100
    return dft.rolling(12).mean().dropna()
