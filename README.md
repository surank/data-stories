# London Crimes Kaggle Data Set Analysis
The Jupyter notebook within this repository will hopefully serve as an educational guide to help you get some understanding of analysing a data set.
The Project will cover the folowing:

Loading the Data into Hive. (I will assume you have installed hive and hadoop and have at least some basic knowledge of how these work)

Pull data from  hive into python and query the results using Pandas

Visualise the results using plotly

***Getting the Data***

The Data for this project can be obtained from the following location: [London Crimes 2008-2016](https://www.kaggle.com/jboysen/london-crime)
you will need an account but fret not you can just use your google or facebook credentials. 

***Prepping the Data for Hive***

The first thing we need to do is get the headers from the file:

*suran@Kenobi:~/Documents$ head -1 london_crime_by_lsoa.csv*
*lsoa_code,borough,major_category,minor_category,value,year,month*

Take note of the headers as you will need them later. 

Now we finally strip the headers from the csv file as we do not need it when loading the data into the hive table.

*suran@Kenobi:~/Documents$ sed '1d' london_crime_data.csv >london_crime_clean.csv*
*suran@Kenobi:~/Documents$ head -1 london_crime_clean.csv* 
*E01001116,Croydon,Burglary,Burglary in Other Buildings,0,2016*

With our clean csv file in place we are ready to create the hive table and load the data

***Loading Data into Hive***

Firstly, let’s create an external table so we can load the csv file, after that we create an internal table and load the data from the external table.

hive> create database london_crimes;

OK

Time taken: 5.054 seconds

hive> use london_crimes;

OK

Time taken: 0.046 seconds

hive> create table if not exists crimes (
    > lsoa_code string,
    > borough string,
    > major_category string,
    > minor_category string,
    > value int,
    > year int)
    > row format delimited
    > fields terminated by ','
    > stored as textfile;

OK

Time taken: 0.633 seconds

let’s load the csv data:

hive> load data local inpath '/home/suran/Documents/london_crime_clean.csv' overwrite into table crimes;

Loading data to table london_crimes.crimes

OK


Time taken: 14.429 seconds
hive> select * from crimes limit 10;

OK

E01001116 Croydon Burglary Burglary in Other Buildings 0 2016

E01001646 Greenwich Violence Against the Person Other violence 0 2016

E01000677 Bromley Violence Against the Person Other violence 0 2015
....

Time taken: 1.935 seconds, Fetched: 10 row(s)

looking good finally we can create the hive managed orc table:

hive> create table londoncrimes stored as orc as Select * from crimes;

Bada Boom Bada Bing! Your data is now ready to be analysed. 

*** Installing plotly, Pandas and Pyhive.

From a command line  execute the following:

*pip install pandas*
*pip install pyhive*
*pip install plotly*

***Installing Jupyer Notebook***

[How To Install Jupyter Notebook ](http://jupyter.readthedocs.io/en/latest/install.html)


Now go forth! and learn. 

Ps - You will need to use nbviewer if you want to view the plots as github does not render the iframes. 

[London Crimes NoteBook] (https://nbviewer.jupyter.org/github/surank/data-stories/blob/lodon-crimes/Crime.ipynb)


