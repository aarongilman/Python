//CPS 2015

use year state hhwgt age popstat perhh inch_all rinch_all rhrearn rhrwage using cepr_march_2015, clear

 

//CPS 2014

append using cepr_march_2014, keep(year state hhwgt age popstat perhh inch_all rinch_all rhrearn rhrwage)

 

//CPS 2013

append using cepr_march_2013, keep(year state hhwgt age popstat perhh inch_all rinch_all rhrearn rhrwage)

 

//CPS 2012

append using cepr_march_2012, keep(year state hhwgt age popstat perhh inch_all rinch_all rhrearn rhrwage)

 

keep if state == 14

 

svyset [hhwgt], vce(linearized)

 

table year [pweight= hhwgt], c(median inch_all count inch_all)
