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
        log = np.loadtxt(
            file, 
            delimiter=';', 
            dtype={ 'names': Labels.tag, 'formats': Labels.csv_format },
            converters=csv_clean,
            skiprows=4,
            usecols=Labels.csv_cols 
        )
        for t in Labels.tag:
            setattr(self, t, log[:][t])

        self.v120 = np.concatenate((self.L1, self.L2, self.L3))
        self.v208 = np.concatenate((self.L12, self.L23, self.L31))
        self.amps = np.concatenate((self.I1, self.I2, self.I3, self.In))
        self.kW = np.concatenate((self.P1, self.P2, self.P3))        
        self.kAVr = np.concatenate((self.Q1, self.Q2, self.Q3))
        self.damps = np.concatenate((self.dI1, self.dI2, self.dI3, self.dIo))

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
        if t in Labels.tag:
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
'''
Plot()

uses matplotlib to plot data from the MLabsPy.plotData(tag)
and can save them to a save directory

'''
class Plot:
    def __init__(self, tag, save='PlotTests'):
        self.tag = tag
        try:
            os.mkdir(save)
            self.file = save + '/' + tag + '.jpg'
        except:
            self.file = False

        
    width = 0.6
    pad = 0.6
    labelsize = 4
    rotation = 89
    figsize = [ 11, 8.5 ]
    dpi = 300

    def go(self, data=False):
        if data is False:
            data = Labels.defaultPlotData

        x = data['x']
#        t = Labels(self.tag)
        y1, y2 = data['stats']['min'], data['stats']['max']
        self.unit = Labels.units.get(self.tag, '???')

        # start setting up plot
        self.do_plot(x, data['plot'])
        # trim down time for display
        plt.xlabel(Labels.xlabel)
        plt.ylabel(Labels.ylabels.get(self.tag, 'Y AXIS'))
        plt.suptitle(Labels.titles.get(self.tag, 'Default Plot Title'))
        plt.title(self.plot_subtitle(data['stats']))

        xtick = 100
        while xtick < len(x):
            x = x[::2]
        plt.tick_params(width=(self.width), pad=(self.pad), labelsize=(self.labelsize))
        plt.xticks(x, rotation=(self.rotation))
        plt.yticks(np.linspace(y1, y2, 60))
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
        return 'Min: ' + str(D) + self.unit

    def max_data(self, D = 0.0):
        return 'Max: ' + str(D) + self.unit

    def median_data(self, D = 0.0):
        return 'Median: ' + str(D) + self.unit

    def mean_data(self, D = 0.0):
        return 'Mean: ' + str(D) + self.unit

    def mode_data(self, D = [ 0, 1 ]):
        return 'Mode: ' + str(D[0]) + self.unit + ' X ' + str(D[1])

    def do_plot(self, x, plot):
        for p in plot:
            plt.plot(x, (p['dataset']), label=(p['tag']), color=(p['color']), linewidth='0.8')
        
'''
Loads the values in the lables.py based on tag
'''
class Labels:
    def __init__(self, tag='defalts'):
        self.tag = tag
#        self.title = Labels.titles.get(tag, 'Default Plot Title')
#        self.unit = Labels.units.get(tag, '???')
#        self.ylabel = Labels.ylabels.get(tag, 'Tag not found')       
#        self.color = Labels.colors.get(tag, 'pink')

    def cunits(c):
        ff = c.decode().strip('"').strip().strip("VAHzkWrh").strip()
        return float(ff)
    def cts(t):
        return t.decode().strip('"')

    xlabel = "Time"

    defaultX = [ 1, 2, 3, 4, 5]

    defaultY = [ 1.0, 5.6, 7.4, 6.0, 2.0 ]

    defaultPlotRow = [{'dataset': defaultY, 'tag':'default data', 'color':'pink' }]

    defaultPlotData = {
            'x': defaultX, 
            'plot': defaultPlotRow,
            'stats': { 'min':1.0, 'max': 7.4, 'median': 0.0, 'mean': 0.0, 'mode': [ 0, 1 ] }
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
       "kVArh-C", "kVArh-I"
       )

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
    'kVArh': [ "kVArh-C", "kVArh-I" ]
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
    'P':'Total active power (kW)', 
    'Q':'Total reactive power (kVAr)',
    'S':'Total apparent power (kVA)',
    'PF':'Total power factor (pf)', 
    'dI1':'Demand Current (dI) dI1', 
    'dI2':'Demand Current (dI) dI2', 
    'dI3':'Demand Current (dI) dI3', 
    'dIo':'Demand Current (dI) dIo', 
    'dkW':'Demand Power (kW)', 
    'dkVAr':'Demand kVAr', 
    'THDL1':'Total Harmonic Distortion X (THD) THD L1', 
    'THDL2':'Total Harmonic Distortion Y (THD) THD L2', 
    'THDL3':'Total Harmonic Distortion Z (THD) THD L3', 
    'THDL12':'Total Harmonic Distortion X (THD) THD L12', 
    'THDL23':'Total Harmonic Distortion Y (THD) THD L23', 
    'THDL31':'Total Harmonic Distortion Z (THD) THD L31', 
    'THDI1':'Total Harmonic Distortion X (THD) THD I1', 
    'THDI2':'Total Harmonic Distortion Y (THD) THD I2', 
    'THDI3':'Total Harmonic Distortion Z (THD) THD I3', 
    'THDIn':'Total Harmonic Distortion N (THD) THD In',    
    'P1':'Total active power (kW)', 
    'P2':'Total active power (kW)',  
    'P3':'Total active power (kW)',   
    'Q1':'Total reactive power (kVAr)', 
    'Q2':'Total reactive power (kVAr)',  
    'Q3':'Total reactive power (kVAr)',   
    'kWh_Im':'Import Power kWh', 
    'kWh_Ex':'Export Power kWh', 
    'kVArh-I':'Inductive Power', 
    'kVArh-C':'Capacitive Power',
    'v120':'Ph-N voltages: V1-V2-V3', 
    'v208':'Ph-Ph voltages: U12-U23-U31', 
    'amps':'Phase currents: I1-I2-I3',
    'kWatt':'Total active power (kW) P1, P2, P3',
    'kVAr':'Total reactive power (kVAr) Q1, Q2, Q3',
    'damps':'Demand Current (dI) dI1, dI2, dI3',
    'THDX':'Total Harmonic Distortion X (THD) THD L1, THD L12, THD I1', 
    'THDY':'Total Harmonic Distortion Y (THD) THD L2, THD L23, THD I2', 
    'THDZ':'Total Harmonic Distortion Z (THD) THD L3, THD L31, THD I3', 
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
    'kVArh-I':'kVArh', 
    'kVArh-C':'kVArh',
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
    'kVArh-I':'Blue', 
    'kVArh-C':'Red'
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
    'Freq':'Hz',
    'P':'kW', 
    'Q':'kVAr', 
    'S':'kVA', 
    'PF':'PF',   
    'dI1':'Demand Current (dI1)', 
    'dI2':'Demand Current (dI2)',  
    'dI3':'Demand Current (dI3)',  
    'dIo':'Demand Current (dIo)',  
    'dkW':'kW', 
    'dkVAr':'kVAr', 
    'THDIn':'THD %',  
    'THDL1':'THD %', 
    'THDL2':'THD %',  
    'THDL3':'THD %',  
    'THDL12':'THD %', 
    'THDL23':'THD %',  
    'THDL31':'THD %',  
    'THDI1':'THD %', 
    'THDI2':'THD %',  
    'THDI3':'THD %',  
    'P1':'kW',  
    'P2':'kW',  
    'P3':'kW',  
    'Q1':'kVAr',  
    'Q2':'kVAr',  
    'Q3':'kVAr',
    'kWh_Im':'kWh', 
    'kWh_Ex':'kWh', 
    'kVArh':'kVArh', 
    'kVArh-I':'kVArh', 
    'kVArh-C':'kVArh',
    'v120':'Voltage (V)',  
    'v208':'Voltage (U)', 
    'amps':'Current (I)',
    'damps':'Demand Current (dI)',
    'THDX':'THD %', 
    'THDY':'THD %',  
    'THDZ':'THD %',
    'kWh':'kWh',
    'kWatt':'kW',
    'kVAr':'kVAr', 
    }