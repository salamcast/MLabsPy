# MLabsPy

I origonally started this project while working for an in-house AV company, mostly as a 
Power Distribution Technicain and Rigger, in my speare time.  It was only a basic script 
that ploted 3 graphs, made some HTML files with plotly and had to be run from the console. 

MLabsPy is a python parser for the Motion Labs Power Meter log format.  

The data by itself is usless without context, this is the starting block to help bring this 
data into a position to be ploted or inserted into a Database to give it some more context.  
With Big Data and all the tools avalable, an events company with enough forward thinking 
could use this data along with sales notes, client check in notes, in room support calls, 
rentals, wifi codes, recordings, invoices, salesforce records, worker notes reguarding a 
specific event and organize it by timestamp to get better insite into how your services 
are being used and patterens of use. 



## PM-XXX Series Power Meter Logger

Details for the local Data logging format and how to import into excel is discussed in the 
manual (pg 23, 8. Local Data Logging):

https://www.motionlabs.com/wp-content/uploads/PM-XXX-UM.pdf

Excel is slow with large datasets (45 x 7000), unless you have a good workstation.  This python program 
(numpy) is much faster in my opinion. Jupyter Notebooks has been very helpful in developing 
this program and Spyder.  The plots I made with excel in the past didn't look very large nor 
detailed.  matplotlib does a good job marking larger plot images, plotly made some nice 
HTML/Js graphs with the ablity to zoom in and look at the data in ways you can't with excel 
or numbers

# Prerequisets 

* numpy
* scipy
* matplotlib (plot test)
* jupyter-notebooks (optional)

# How-To Use

Bellow is all the information about the columns in the log file and the tag names to
access the data after it has been parsed.  Many of the tags have been shortened from
the origonal one.  I have also added tags for plots that have multiple lines plotted.



### plotData returns a data structure like: 

```
{
    'x': [1,2,3,4,5],
    'stats': {
        'min': 0.,
        'max': 10.,
        'median': 0.,
        'mean': 0.,
        'mode': [ 0, 1 ]
    },
    'plot': [ {  
        'dataset': [ 1.,5.6,7.4,6.,2. ],
        'tag': "float test",
        'color': 'red'
    }],
}
```
### Using the MLabsPy.Plot class to plot the data

```
import MLabsPy as m

file = './test/test.csv'
ML = m.MLabsPy(file)

# Ploting
p = ML.plotData('v208')
plot = m.Plot(x)
plot.go(p)

```

### Using the MLabsPy.MLabsPy class to get CSV data

getCSVdata() returns an array if CSV data, for file writting or pandas.
this data has been cleaned, so it can be easily imported in excel after 
making the CSV file.  the first value is a time stamp,the rest are floats.

```
import MLabsPy as m

file = './test/test.csv'
ML = m.MLabsPy(file)

CSV = ML.getCSVdata('v208')

```

### More information in Jupyter Notebooks

I have created a jupyter notebook for this class to help you see the ploting
in action.  all the access tags are listed there along with some more information
about the data being logged.