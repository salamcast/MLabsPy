# decompyle3 version 3.3.2
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.5 (default, Sep  3 2020, 21:29:08) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Users\dude\Documents\MLabs_tools\MLabs_PlotLog.py
# Compiled at: 2021-02-07 12:21:11
# Size of source mod 2**32: 7776 bytes




"""
Created on Sun Feb  7 12:19:09 2021

@author: dude
"""
import numpy as np
from scipy import stats
import os
import matplotlib.pyplot as plt

global csv_clean, csv_format, csv_cols, tag, multi

global titles, units, ylabels

def cunits(c):
    ff = c.decode().strip('"').strip().strip("VAHzkWrh").strip()
    return float(ff)
def cts(t):
    return t.decode().strip('"')

csv_clean={ }
csv_format=('U8', 'f4', 'f4','f4', 'f4', 'f4','f4', 'f4', 'f4','f4', 'f4', 'f4', 'f4', 'f4','f4', 'f4', 'f4','f4', 'f4', 'f4', 'f4','f4', 'f4', 'f4', 'f4', 'f4', 'f4','f4', 'f4', 'f4','f4', 'f4', 'f4','f4', 'f4', 'f4', 'f4','f4', 'f4', 'f4','f4', 'f4', 'f4','f4', 'f4' )
csv_cols = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44)
for c in csv_cols:
    if c == 0:
        csv_clean[c]=cts
    else:
        csv_clean[c]=cunits
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


class MLabsPy:
    def __init__(self, file):
        log = np.loadtxt(
            file, 
            delimiter=';', 
            dtype={ 'names': tag, 'formats': csv_format },
            converters=csv_clean,
            skiprows=4,
            usecols=csv_cols 
        )
        for t in tag:
            setattr(self, t, log[:][t])

        self.v120 = np.concatenate((self.L1, self.L2, self.L3))
        self.v208 = np.concatenate((self.L12, self.L23, self.L31))
        self.amps = np.concatenate((self.A1, self.A2, self.A3, self.An))
        self.kW = np.concatenate((self.P1, self.P2, self.P3))        
        self.kAVr = np.concatenate((self.Q1, self.Q2, self.Q3))
        self.damps = np.concatenate((self.dA1, self.dA2, self.dA3, self.dAo))

    def csv_min(self, t):
        if t in tag or multi:
            return np.amin(getattr(self, t))

    def csv_max(self, t):
        if t in tag or multi:
            return np.amax(getattr(self, t))

    def csv_median(self, t):
        if t in tag or multi:
            return np.median(getattr(self, t))

    def csv_mean(self, t):
        if t in tag or multi:
            return np.mean(getattr(self, t))

    def csv_mode(self, t):
        if t in tag or multi:
            mode = stats.mode(getattr(self, t))
            return [ mode.mode[0], mode.count[0] ]
        

class Plot:

    def __init__(self, tag):
        self.tag = tag
        t = Labels(tag)
        self.title = t.title
        self.unit = t.unit
        self.ylabel = t.ylabel
        
        self.xlabel = t.xlabel

    width = 0.6
    pad = 0.6
    labelsize = 4
    rotation = 89

    def go(self, data={
            'x':[ 1, 2, 3, 4, 5], 
            'plot':[ {'dataset':[ 1.0, 5.6, 7.4, 6.0, 2.0 ], 
                      'tag':'float test', 
                      'color':'red'
                      }
                ]
        }, save=False):
        x = data['x']
        full = data['all']
        plot = data['plot1']
        self.y1 = np.amin(full)
        self.y2 = np.amax(full)
        plt.figure(figsize=[11, 8.5], dpi=300)
        self.plot_subtitle(full)
        self.do_plot(x, plot)
        plt.suptitle(self.title)
        if save is not False:
            try:
                os.mkdir(save)
            except:
                pass
            else:
                plt.savefig((save + '/' + self.tag + '.jpg'), dpi=300)
        plt.show()

    def plot_subtitle(self, D):
        self.subtitle = self.min_data()
        self.subtitle = self.subtitle + ', ' + self.max_data()
        self.subtitle = self.subtitle + ', ' + self.median_data(D)
        self.subtitle = self.subtitle + ', ' + self.mean_data(D)
        self.subtitle = self.subtitle + ', ' + self.mode_data(D)

    def min_data(self):
        return 'Min: ' + str(self.y1) + self.unit

    def max_data(self):
        return 'Max: ' + str(self.y2) + self.unit

    def median_data(self, D):
        return 'Median: ' + str(np.median(D)) + self.unit

    def mean_data(self, D):
        return 'Mean: ' + str(np.mean(D)) + self.unit

    def mode_data(self, D):
        m = stats.mode(D)
        return 'Mode: ' + str(m.mode[0]) + self.unit + ' X ' + str(m.count[0])

    def do_plot(self, x, plot):
        for p in plot:
            plt.plot(x, (p['dataset']), label=(p['tag']), color=(p['color']), linewidth='0.8')
        else:
            plt.tick_params(width=(self.width), pad=(self.pad), labelsize=(self.labelsize))
            xtick = 100
            while True:
                if xtick < len(x):
                    x = x[::2]

            plt.xticks(x, rotation=(self.rotation))
            plt.xlabel(self.xlabel)
            plt.yticks(np.linspace(self.y1, self.y2, 50))
            plt.ylabel(self.ylabel)
            plt.title(self.subtitle)
            plt.legend()


class Labels:
    def __init__(self, tag):
        self.tag = tag
        self.title = titles.get(tag, 'Default Plot Title')
        self.unit = units.get(tag, 'V')
        self.ylabel = ylabels.get(tag, 'Voltage')
        self.xlabel = "Time"
        self.color = colours.get(tag, 'pink')




titles = {
    'L1':'Ph-N voltages: V1', 
    'L2':'Ph-N voltages: V2',  
    'L3':'Ph-N voltages: V3',  
    'L12':'Ph-Ph voltages: U12', 
    'L23':'Ph-Ph voltages: U23',  
    'L31':'Ph-Ph voltages: U31',  
    'A1':'Phase currents: I1', 
    'A2':'Phase currents: I2',  
    'A3':'Phase currents: I3',  
    'An':'Phase currents: In', 
    'Vavr':'Average Ph-N voltage: Va', 
    'Uavr':'Average Ph-Ph voltage: Ua',  
    'Iavr':'Average current: Ia',  
    'Freq':'Frequency', 
    'P':'Total active power (kW)', 
    'Q':'Total reactive power (kVAr)',
    'S':'Total apparent power (kVA)',
    'PF':'Total power factor (pf)', 
    'dA1':'Demand Current (dI) dI1', 
    'dA2':'Demand Current (dI) dI2', 
    'dA3':'Demand Current (dI) dI3', 
    'dAo':'Demand Current (dI) dIo', 
    'dkW':'Demand Power (kW)', 
    'dkVAr':'Demand kVAr', 
    'THDL1':'Total Harmonic Distortion X (THD) THD L1', 
    'THDL2':'Total Harmonic Distortion Y (THD) THD L2', 
    'THDL3':'Total Harmonic Distortion Z (THD) THD L3', 
    'THDL12':'Total Harmonic Distortion X (THD) THD L12', 
    'THDL23':'Total Harmonic Distortion Y (THD) THD L23', 
    'THDL31':'Total Harmonic Distortion Z (THD) THD L31', 
    'THDA1':'Total Harmonic Distortion X (THD) THD I1', 
    'THDA2':'Total Harmonic Distortion Y (THD) THD I2', 
    'THDA3':'Total Harmonic Distortion Z (THD) THD I3', 
    'THDAn':'Total Harmonic Distortion N (THD) THD In',    
    'P1':'Total active power (kW)', 
    'P2':'Total active power (kW)',  
    'P3':'Total active power (kW)',   
    'Q1':'Total reactive power (kVAr)', 
    'Q2':'Total reactive power (kVAr)',  
    'Q3':'Total reactive power (kVAr)',   
    'kWhIm':'Import Power kWh', 
    'kWhEx':'Export Power kWh', 
    'kVArhI':'Inductive Power', 
    'kVArhC':'Capacitive Power',
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
    'A1':'A', 
    'A2':'A',
    'A3':'A',
    'An':'A',
    'Vavr':'V', 
    'Uavr':'V',
    'Iavr':'A',
    'Freq':'Hz',      
    'P':'kW', 
    'Q':'kVAr', 
    'S':'kVA', 
    'PF':'ind', 
    'dA1':'A', 
    'dA2':'A',  
    'dA3':'A',  
    'dAo':'A',  
    'dkW':'kW', 
    'dkVAr':'kVAr', 
    'THDAn':'%',  
    'THDL1':'%', 
    'THDL2':'%',  
    'THDL3':'%',  
    'THDL12':'%', 
    'THDL23':'%',  
    'THDL31':'%',  
    'THDA1':'%', 
    'THDA2':'%',  
    'THDA3':'%',   
    'P1':'kW',  
    'P2':'kW',  
    'P3':'kW',
    'Q1':'kVAr',  
    'Q2':'kVAr',  
    'Q3':'kVAr',
    'kWhIm':'kWh', 
    'kWhEx':'kWh', 
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

colours = {
    'L1':'Black', 
    'L2':'Blue',
    'L3':'Red',  
    'L12':'Black', 
    'L23':'Blue',
    'L31':'Red',
    'A1':'Black', 
    'A2':'Blue',
    'A3':'Red',
    'An':'Green',
    'Vavr':'Blue', 
    'Uavr':'Red',
    'Iavr':'Green',
    'Freq':'Orange',      
    'P':'Blue', 
    'Q':'Red', 
    'S':'Green', 
    'PF':'Brown', 
    'dA1':'Black', 
    'dA2':'Blue',  
    'dA3':'Red',  
    'dAo':'Green',  
    'dkW':'Purple', 
    'dkVAr':'orange', 
    'THDL1':'Black', 
    'THDL2':'Blue',  
    'THDL3':'Red',  
    'THDL12':'Black', 
    'THDL23':'Blue',  
    'THDL31':'Red',  
    'THDA1':'Black', 
    'THDA2':'Blue',  
    'THDA3':'Red',   
    'THDAn':'Green',
    'P1':'Black',  
    'P2':'Blue',  
    'P3':'Red',
    'Q1':'Black',  
    'Q2':'Blue',  
    'Q3':'Red',
    'kWhIm':'Blue', 
    'kWhEx':'Red', 
    'kVArhI':'Blue', 
    'kVArhC':'Red'
}
    
ylabels = {
    'L1':'Voltage', 
    'L2':'Voltage',  
    'L3':'Voltage',  
    'L12':'Voltage', 
    'L23':'Voltage',  
    'L31':'Voltage',  
    'A1':'Current (I)', 
    'A2':'Current (I)',  
    'A3':'Current (I)',  
    'An':'Current (I)',  
    'Vavr':'Voltage', 
    'Uavr':'Voltage',  
    'Iavr':'Current (I)',  
    'Freq':'Hz',
    'P':'kW', 
    'Q':'kVAr', 
    'S':'kVA', 
    'PF':'PF',   
    'dA1':'Demand Current (I)', 
    'dA2':'Demand Current (I)',  
    'dA3':'Demand Current (I)',  
    'dAo':'Demand Current (I)',  
    'dkW':'kW', 
    'dkVAr':'kVAr', 
    'THDAn':'THD %',  
    'THDL1':'THD %', 
    'THDL2':'THD %',  
    'THDL3':'THD %',  
    'THDL12':'THD %', 
    'THDL23':'THD %',  
    'THDL31':'THD %',  
    'THDA1':'THD %', 
    'THDA2':'THD %',  
    'THDA3':'THD %',  
    'P1':'kW',  
    'P2':'kW',  
    'P3':'kW',  
    'Q1':'kVAr',  
    'Q2':'kVAr',  
    'Q3':'kVAr',
    'kWhIm':'kWh', 
    'kWhEx':'kWh', 
    'kVArh':'kVArh', 
    'kVArhI':'kVArh', 
    'kVArhC':'kVArh',
    'v120':'Voltage',  
    'v208':'Voltage', 
    'amps':'Current (I)',
    'damps':'Demand Current (I)',
    'THDX':'THD %', 
    'THDY':'THD %',  
    'THDZ':'THD %',
    'kWh':'kWh',
    'kWatt':'kW',
    'kVAr':'kVAr', 
}



