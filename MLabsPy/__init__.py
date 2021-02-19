"""
Created on Sun Feb 7 12:19:09 2021

@author: Abu Khadeejah Karl

MLabsPy 

Parse and Plot your PM-XXX Series Power Meter daily CSV log



"""
import numpy as np
from scipy import stats
import os
import matplotlib.pyplot as plt




class MLabsPy:
    def __init__(self, file):
        csv_clean={ }
        for c in Labels.csv_cols:
            if c == 0:
                csv_clean[c]=Labels.cts
            else:
                csv_clean[c]=Labels.cunits
        self.log = np.loadtxt(
            file, 
            delimiter=';', 
            dtype={ 'names': Labels.tag, 'formats': Labels.csv_format },
            converters=csv_clean,
            skiprows=4,
            usecols=Labels.csv_cols 
        )
        
        for t in Labels.tag:
            setattr(self, t, self.log[:][t])
        # multi
        for m in Labels.multi:
            p = []
            # col
            for item in Labels.multi[m]:
                p = np.concatenate((p, getattr(self, item)))
            setattr(self, m, p)
            
            
    def csv_min(self, t):
        if t in Labels.tag or Labels.multi:
            return np.amin(getattr(self, t, Labels.defaultY))

    def csv_max(self, t):
        if t in Labels.tag or Labels.multi:
            return np.amax(getattr(self, t, Labels.defaultY))

    def csv_median(self, t):
        if t in Labels.tag or Labels.multi:
            return np.median(getattr(self, t, Labels.defaultY))

    def csv_mean(self, t):
        if t in Labels.tag or Labels.multi:
            return np.mean(getattr(self, t, Labels.defaultY))

    def csv_mode(self, t):
        if t in Labels.tag or Labels.multi:
            mode = stats.mode(getattr(self, t, Labels.defaultY))
            return [ mode.mode[0], mode.count[0] ]

    def getStats(self, t):
        return {
            'min': self.csv_min(t),
            'max': self.csv_max(t),
            'median': self.csv_median(t),
            'mean': self.csv_mean(t),
            'mode': self.csv_mode(t)
        }
        
    def getRow(self, t):
        return { 
                'dataset': getattr(self,t, Labels.defaultY), 
                'tag': Labels.ylabels.get(t, 'Unknown: ' + t), 
                'color': Labels.colors.get(t, 'Pink') 
        }

    def getData(self, t):
        if t in Labels.tag:
            return [ self.getRow(t) ] 
        elif t in Labels.multi:
            d = []
            for l in Labels.multi[t]:
                d.append(self.getRow(l))
            return d

    def plotData(self, t='120v'):
        return { 'x':self.ts, 'plot': self.getData(t), 'stats': self.getStats(t) }
    
    def getCSVdata(self, t):
        if t in Labels.multi:
            CSV=[]
            CSV.append( "ts," + ",".join( Labels.multi[t]) )
            # loop the data
            x=0
            while x < len(self.ts):
                line=[]
                line.append(self.log[x]['ts'])
                for l in Labels.multi[t]:
                    line.append(str(self.log[x][l]))
                CSV.append( ",".join(line) ) 
                x+=1
            return CSV

'''
Plot()

uses matplotlib to plot data from the MLabsPy.plotData(tag)
and can save them to a save directory

'''
class Plot:
    def __init__(self, tag, save='PlotTests'):
        self.tag = tag
        if save is not False:
            try:
                os.mkdir(save)
            except:
                pass
            self.file = save + '/' + tag + '.jpg'
        else:
            self.file = False
    
    line = 0.7
    # ticks    
    width = 2
    pad = 2
    labelsize = 10
    # xticks
    xskip = 2
    xtick = 35
    rotation = -89
    # yticks
    ytick = 16
    # image
    figsize = [ 11, 8.5 ]
    dpi = 300
    

    def go(self, data=False):
        if data is False:
            data = Labels.defaultPlotData
        x = data['x']
        y1, y2 = data['stats']['min'], data['stats']['max']

        self.unit = Labels.units.get(self.tag, '???')
        # start setting up plot
        self.do_plot(x, data['plot'])
        # trim down time for display
        plt.xlabel(Labels.xlabel)
        plt.ylabel(Labels.ylabels.get(self.tag, 'Y AXIS'))
        plt.suptitle(Labels.titles.get(self.tag, 'Default Plot Title'))
        plt.title(self.plot_subtitle(data['stats']))

        while self.xtick < len(x):
            x = x[::self.xskip]
        plt.tick_params(width=(self.width), pad=(self.pad), labelsize=(self.labelsize))
        plt.xticks(x, rotation=(self.rotation))

        plt.yticks(np.linspace(y1, y2, self.ytick))
        plt.legend()
        plt.figure(figsize=self.figsize, dpi=self.dpi)
        if self.file is not False:
            plt.savefig((self.file), dpi=self.dpi)
        plt.show()



    def plot_subtitle(self, D = False ):
        if D is False:
            D = Labels.defaultPlotData['stats']
        return self.min_data(D['min']) + ', ' + self.max_data(D['max']) + ', ' + self.median_data(D['median']) + ', ' + self.mean_data(D['mean']) + ', ' + self.mode_data(D['mode'])

    def min_data(self, D = 0.0):
        return 'Min: ' + str(round(D, 2)) + " " + self.unit

    def max_data(self, D = 0.0):
        return 'Max: ' + str(round(D, 2)) + " " + self.unit

    def median_data(self, D = 0.0):
        return 'Median: ' + str(round(D, 2)) + " " + self.unit

    def mean_data(self, D = 0.0):
        return 'Mean: ' + str(round(D, 2)) + " " + self.unit

    def mode_data(self, D = [ 0, 1 ]):
        return 'Mode: ' + str(round(D[0], 2)) + " " + self.unit + ' X ' + str(D[1])

    def do_plot(self, x, plot):
        for p in plot:
            plt.plot(x, (p['dataset']), label=(p['tag']), color=(p['color']), linewidth=self.line)
        
'''
Loads the values in the lables.py based on tag
'''
class Labels:
    def __init__(self, tag='defalts'):
        self.tag = tag

    def cunits(c):
        ff = c.decode().strip('"').strip().strip("VAHzkWrh").strip()
        return float(ff)
    def cts(t):
        return t.decode().strip('"')

    xlabel = "Time"

    defaultX = [ 1, 2, 3, 4, 5]

    defaultY = [ -66.6, -6.0, 66.6, 6.0, 2.0 ]

    defaultPlotRow = [{'dataset': defaultY, 'tag':'default data', 'color':'pink' }]

    defaultPlotData = {
            'x': defaultX, 
            'plot': defaultPlotRow,
            'stats': { 'min':66.6, 'max': 66.6, 'median': 0.0, 'mean': 0.0, 'mode': [ 0, 1 ] }
        }

    csv_format=('U8', 'f4', 'f4','f4', 'f4', 'f4','f4', 'f4', 'f4','f4', 'f4', 'f4', 'f4', 'f4','f4', 'f4', 'f4','f4', 'f4', 'f4', 'f4','f4', 'f4', 'f4', 'f4', 'f4', 'f4','f4', 'f4', 'f4','f4', 'f4', 'f4','f4', 'f4', 'f4', 'f4','f4', 'f4', 'f4','f4', 'f4', 'f4','f4', 'f4' )
    csv_cols = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44)

    tag = ( 
       'ts',
       'L1', 'L2', 'L3', 
       'L12', 'L23', 'L31',
       'I1', 'I2', 'I3', 'In',
       'Freq', 
       'Vavr', 'Uavr', 'Iavr', 
       'P', 'Q', 'S', 
       'PF', 
       'dI1', 'dI2', 'dI3', 'dIo', 
       'dkW', 
       'dkVAr',
       'THDL1', 'THDL2', 'THDL3', 'THDL12', 'THDL23', 'THDL31',
       'THDI1', 'THDI2', 'THDI3', 'THDIn',
       "P1", "P2", "P3",
       "Q1", "Q2", "Q3",
       "kWh_Im", "kWh_Ex",
       "kVArhC", "kVArhI"
       )

    # this is the grouping for plot and CSV output
    multi ={
    'v120':['L1', 'L2', 'L3'],
    'v208':['L12', 'L23', 'L31'], 
    'amps':['I1', 'I2', 'I3', 'In'],
    'damps':['dI1', 'dI2', 'dI3', 'dIo'],
    'THDX':['THDL1', 'THDL12', 'THDI1' ], 
    'THDY':['THDL2', 'THDL23', 'THDI2' ],  
    'THDZ':['THDL3', 'THDL31', 'THDI3' ],
    'kWatt':[ "P1", "P2", "P3" ],
    'kVAr':[ "Q1", "Q2", "Q3" ],
    'kWh':[ "kWh_Im", "kWh_Ex" ],
    'kVArh': [ "kVArhC", "kVArhI" ]
    }

    titles = {
    'L1':'Ph-N voltages: V1', 
    'L2':'Ph-N voltages: V2',  
    'L3':'Ph-N voltages: V3',  
    'L12':'Ph-Ph voltages: U12', 
    'L23':'Ph-Ph voltages: U23',  
    'L31':'Ph-Ph voltages: U31',  
    'I1':'Phase currents: I1', 
    'I2':'Phase currents: I2',  
    'I3':'Phase currents: I3',  
    'In':'Phase currents: In', 
    'Vavr':'Average Ph-N voltage: Va', 
    'Uavr':'Average Ph-Ph voltage: Ua',  
    'Iavr':'Average current: Ia',  
    'Freq':'Frequency', 
    'P':'Total active power: P', 
    'Q':'Total reactive power: Q',
    'S':'Total apparent power: S',
    'PF':'Total Power Factor: PF', 
    'dI1':'Demand Current (dI) dI1', 
    'dI2':'Demand Current (dI) dI2', 
    'dI3':'Demand Current (dI) dI3', 
    'dIo':'Demand Current (dI) dIo', 
    'dkW':'Demand Active Power: dkW', 
    'dkVAr':'Demand Reactive Power: dkVAr', 
    'THDL1':'Total Harmonic Distortion X (THD) L1', 
    'THDL2':'Total Harmonic Distortion Y (THD) L2', 
    'THDL3':'Total Harmonic Distortion Z (THD) L3', 
    'THDL12':'Total Harmonic Distortion X (THD) L12', 
    'THDL23':'Total Harmonic Distortion Y (THD) L23', 
    'THDL31':'Total Harmonic Distortion Z (THD) L31', 
    'THDI1':'Total Harmonic Distortion X (THD) I1', 
    'THDI2':'Total Harmonic Distortion Y (THD) I2', 
    'THDI3':'Total Harmonic Distortion Z (THD) I3', 
    'THDIn':'Total Harmonic Distortion N (THD) In',    
    'P1':'Active Power: P1', 
    'P2':'Active Power: P2',  
    'P3':'Active Power: P3',   
    'Q1':'Reactive Power: Q1', 
    'Q2':'Reactive Power: Q2',  
    'Q3':'Reactive Power: Q3',   
    'kWh_Im':'Import Power (kWh)', 
    'kWh_Ex':'Export Power (kWh)', 
    'kVArhI':'Inductive Power (kVArh)', 
    'kVArhC':'Capacitive Power (kVArh)',
    'v120':'Ph-N voltages: V1-V2-V3', 
    'v208':'Ph-Ph voltages: U12-U23-U31', 
    'amps':'Phase currents: I1-I2-I3',
    'kWatt':'Total active power (kW) P1-P2-P3',
    'kVAr':'Total reactive power (kVAr) Q1-Q2-Q3',
    'damps':'Demand Current (dI) dI1-dI2-dI3',
    'THDX':'Total Harmonic Distortion X (THD) L1-L12-I1', 
    'THDY':'Total Harmonic Distortion Y (THD) L2-L23-I2', 
    'THDZ':'Total Harmonic Distortion Z (THD) L3-L31-I3', 
    'kWh':'Power (kWh)', 
    'kVArh':'Power (kVArh)'
    }

    units = {
    'L1':'V', 
    'L2':'V',
    'L3':'V',  
    'L12':'V', 
    'L23':'V',
    'L31':'V',
    'I1':'A', 
    'I2':'A',
    'I3':'A',
    'In':'A',
    'Vavr':'V', 
    'Uavr':'V',
    'Iavr':'A',
    'Freq':'Hz',      
    'P':'kW', 
    'Q':'kVAr', 
    'S':'kVA', 
    'PF':'ind', 
    'dI1':'A', 
    'dI2':'A',  
    'dI3':'A',  
    'dIo':'A',  
    'dkW':'kW', 
    'dkVAr':'kVAr', 
    'THDIn':'%',  
    'THDL1':'%', 
    'THDL2':'%',  
    'THDL3':'%',  
    'THDL12':'%', 
    'THDL23':'%',  
    'THDL31':'%',  
    'THDI1':'%', 
    'THDI2':'%',  
    'THDI3':'%',   
    'P1':'kW',  
    'P2':'kW',  
    'P3':'kW',
    'Q1':'kVAr',  
    'Q2':'kVAr',  
    'Q3':'kVAr',
    'kWh_Im':'kWh', 
    'kWh_Ex':'kWh', 
    'kVArhI':'kVArh', 
    'kVArhC':'kVArh',
    'v120':'V', 
    'v208':'V', 
    'amps':'A',    
    'damps':'A', 
    'THDX':'%', 
    'THDY':'%',  
    'THDZ':'%',
    'kWatt':'kW',  
    'kVAr':'kVAr',
    'kWh':'kWh',
    'kVArh':'kVArh'
    }

    colors = {
    'L1':'Black', 
    'L2':'Blue',
    'L3':'Red',  
    'L12':'Black', 
    'L23':'Blue',
    'L31':'Red',
    'I1':'Black', 
    'I2':'Blue',
    'I3':'Red',
    'In':'Green',
    'Vavr':'Blue', 
    'Uavr':'Red',
    'Iavr':'Green',
    'Freq':'Orange',      
    'P':'Blue', 
    'Q':'Red', 
    'S':'Green', 
    'PF':'Brown', 
    'dI1':'Black', 
    'dI2':'Blue',  
    'dI3':'Red',  
    'dIo':'Green',  
    'dkW':'Purple', 
    'dkVAr':'orange', 
    'THDL1':'Black', 
    'THDL2':'Black',  
    'THDL3':'Black',  
    'THDL12':'Blue', 
    'THDL23':'Blue',  
    'THDL31':'Blue',  
    'THDI1':'Red', 
    'THDI2':'Red',  
    'THDI3':'Red',   
    'THDIn':'Green',
    'P1':'Black',  
    'P2':'Blue',  
    'P3':'Red',
    'Q1':'Black',  
    'Q2':'Blue',  
    'Q3':'Red',
    'kWh_Im':'Blue', 
    'kWh_Ex':'Red', 
    'kVArhI':'Blue', 
    'kVArhC':'Red'
    }
    
    ylabels = {
    'L1':'Voltage (V1)', 
    'L2':'Voltage (V2)',  
    'L3':'Voltage (V3)',  
    'L12':'Voltage (U12)', 
    'L23':'Voltage (U23)',  
    'L31':'Voltage (U31)',  
    'I1':'Current (I1)', 
    'I2':'Current (I2)',  
    'I3':'Current (I3)',  
    'In':'Current (In)',  
    'Vavr':'Voltage (V-avr)', 
    'Uavr':'Voltage (U-avr)',  
    'Iavr':'Current (I-avr)',  
    'Freq':'Freq. (Hz)',
    'P':'Total Active Power (kW)', 
    'Q':'Total Reactive Power (kVAr)',
    'S':'Total Apparent Power (kVA)',
    'PF':'Total Power Factor (PF)', 
    'dI1':'Demand Current (dI1)', 
    'dI2':'Demand Current (dI2)',  
    'dI3':'Demand Current (dI3)',  
    'dIo':'Demand Current (dIo)',  
    'dkW':'Demand Power (kW)', 
    'dkVAr':'Demand Power (kVAr)', 
    'THDL1':'X (THD) L1', 
    'THDL2':'Y (THD) L2', 
    'THDL3':'Z (THD) L3', 
    'THDL12':'X (THD) L12', 
    'THDL23':'Y (THD) L23', 
    'THDL31':'Z (THD) L31', 
    'THDI1':'X (THD) I1', 
    'THDI2':'Y (THD) I2', 
    'THDI3':'Z (THD) I3', 
    'THDIn':'N (THD) In', 
    'P1':'Active power (kW)', 
    'P2':'Active power (kW)',  
    'P3':'Active power (kW)',   
    'Q1':'Reactive power (kVAr)', 
    'Q2':'Reactive power (kVAr)',  
    'Q3':'Reactive power (kVAr)',
    'kWh_Im':'Import Power (kWh)', 
    'kWh_Ex':'Export Power (kWh)', 
    'kVArhI':'Inductive Power', 
    'kVArhC':'Capacitive Power',
    'v120':'Voltage (V)',  
    'v208':'Voltage (U)', 
    'amps':'Current (I)',
    'damps':'Demand Current (dI)',
    'THDX':'X (THD) %', 
    'THDY':'Y (THD) %',  
    'THDZ':'Z (THD) %',
    'kWh':'Power (kWh)',
    'kVArh':'Power (kVArh)', 
    'kWatt':'Total Active Power (kW)',
    'kVAr':'Total Reactive Power (kVAr)'
    }