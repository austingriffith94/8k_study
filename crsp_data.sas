/*Austin Griffith
/*12/2/2017
/*Event Study*/

OPTIONS ls = 70 nodate nocenter;
OPTIONS missing = '';

/*file paths need to be updated according to current computer*/
%let Ppath = P:\Event Study;
%let Cpath = Q:\Data-ReadOnly\COMP;
%let Dpath = Q:\Data-ReadOnly\CRSP;

libname comp "&Cpath";
libname crsp "&Dpath";

/*---------------------------merge sec and funda cik---------------------------*/
/*import sec csv*/
proc import out = sec datafile = "&Ppath\sec.csv"
dbms = csv
replace;
run;

/*drops csv index*/
data sec;
set sec;
format date mmddyy10.;
obs_year = year(date);
CIK = CIK + 0;
drop _ url;
run;

/*read in funda*/
data funda;
set comp.funda(keep = GVKEY CUSIP CIK CONM);
CUSIP = substr(CUSIP,1,8);
nCIK = CIK*1;
drop CIK;
run;

/*rename numeric cik*/
data funda;
set funda;
CIK = nCIK;
drop nCIK;
run;

/*sort variables for merge*/
%let sort_var = CIK;

/*sort funda by cik for merge*/
proc sort data = funda;
by &sort_var;
run;

/*sort by cik for merge*/
proc sort data = sec;
by &sort_var;
run;

/*merge funda and sec data for matches*/
data check;
merge funda (in = a) sec (in = b);
by &sort_var;
if a and b;
run;

/*---------------------------merge dsf and merged---------------------------*/
/*pulls dsf data*/
data dsf;
set crsp.dsf(keep = CUSIP RET VOL DATE SHROUT);
dsf_year = year(DATE);
format DATE mmddyy10.;
if dsf_year >= 1994 and dsf_year <= 2016;
run;

/*sort merged by cusip*/
/*removed repeated cusip*/
proc sort data = check nodupkey;
by CUSIP;
run;

/*sort dsf by cusip*/
proc sort data = dsf;
by CUSIP;
run;

/*merge the funda/sec and dsf by cusip*/
data merged;
merge check (in = a) dsf (in = b);
by CUSIP;
if a and b;
run;

/*clean merged of missing values*/
/*gets difference between observation sec year and dsf year*/
data out;
set merged;
diff_year = obs_year - dsf_year;
if nmiss(RET) then delete;
if nmiss(VOL) then delete;
run;

/*get year of observation and year before*/
data asdf;
set out;
if diff_year = 1 or diff_year = 0;
run;

/*---------------------------market data---------------------------*/
/*pull market data for desired years*/
data dsi;
set crsp.dsi;
year = year(date);
if year <= 2016;
if year >= 1994;
run;

/*---------------------------export merged and market data---------------------------*/
proc export data = asdf
dbms = csv
outfile = "&Ppath\dsf.csv"
replace;
run;

proc export data = dsi
dbms = csv
outfile = "&Ppath\dsi.csv"
replace;
run;

