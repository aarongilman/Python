Data_Collector
======

Updated: January 21, 2018 <br>
Author:  Brian Dew <br>
Descr:   Collect economic data of interest and store in SQL database.
Files:   data_collector.ipynb (to work on, until final)<br>

*Goal for usage:*<br>
In[1]:<br>
import data_collector as dc<br>
jobs_data = dc.collect('jobs_report')<br>
print(jobs_data.epop[-1])<br>

Out[1]:<br>
Date          epop<br>
2017-12-01	  79.1	

========

### Brian To Do:
* create new, clean data_collector.ipynb file
* add section to print package versions and sys version
* define collect to take several reports as inputs
* for each report, build a list of series
* for each report build dict of request details