clear all
set more off
use "C:\Working\econ_data\micro\data\cepr_org_2016.dta", clear

gen ptvol = 0
replace ptvol = 1 if uhoursi < 35 & ptecon == 0
keep if age > 19 & age < 41
keep if empl == 1


gen rndwgt=round(orgwgt/12,1)
keep if orgwgt ~= .

table state [fw=rndwgt], c(mean ptvol)

gen medexp = 0
replace medexp = 1 if inlist(state, 82,47, 72, 11, 46, 45, 35, 59, 87, 54, 74, 58, 43, 62, 64, 56, 63, 73, 57, 83)
* 34, 35, 91, 
table medexp [fw=rndwgt], c(mean ptvol)

