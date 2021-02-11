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

class MLabsPlot:

    def __init__(self, tag):
        self.tag = tag
        t = MLabsLabels(tag)
        self.title = t.title
        self.unit = t.unit
        self.ylabel = t.ylabel

    title = 'Default Plot Title'
    unit = 'V'
    ylabel = 'Voltage'
    xlabel = 'Time'
    width = 0.6
    pad = 0.6
    labelsize = 4
    rotation = 89

    def mkplot(self, data={'x':[
  1, 2, 3, 4, 5], 
 'all':[
  1.0, 5.6, 7.4, 6.0, 2.0, 1.0, 5.0, 4.0, 9.0, 7.0], 
 'plot1':[
  {'dataset':[
    1.0, 5.6, 7.4, 6.0, 2.0], 
   'tag':'float test', 
   'color':'red'}]}, save=False):
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


class MLabsLabels:

    def __init__(self, tag):
        self.tag = tag
        self.title = self.titles.get(tag, 'Default Plot Title')
        self.unit = self.units.get(tag, 'V')
        self.ylabel = self.ylabels.get(tag, 'Voltage')

    titles = {'L1':'Ph-N voltages: V1', 
     'L2':'Ph-N voltages: V2',  'L3':'Ph-N voltages: V3',  'L12':'Ph-Ph voltages: U12', 
     'L23':'Ph-Ph voltages: U23',  'L31':'Ph-Ph voltages: U31',  'A1':'Phase currents: I1', 
     'A2':'Phase currents: I2',  'A3':'Phase currents: I3',  'An':'Phase currents: In', 
     'Vavr':'Average Ph-N voltage: Va', 
     'Uavr':'Average Ph-Ph voltage: Ua',  'Iavr':'Average current: Ia',  'v120':'Ph-N voltages: V1-V2-V3', 
     'v208':'Ph-Ph voltages: U12-U23-U31', 
     'amps':'Phase currents: I1-I2-I3', 
     'P':'Total active power (kW)', 
     'P1':'Total active power (kW)', 
     'P2':'Total active power (kW)',  'P3':'Total active power (kW)',  'kWatt':'Total active power (kW) P1, P2, P3', 
     'Q':'Total reactive power (kVAr)', 
     'Q1':'Total reactive power (kVAr)', 
     'Q2':'Total reactive power (kVAr)',  'Q3':'Total reactive power (kVAr)',  'kVAr':'Total reactive power (kVAr) Q1, Q2, Q3', 
     'S':'Total apparent power (kVA)', 
     'Freq':'Frequency', 
     'PF':'Total power factor (pf)', 
     'damps':'Demand Current (dI) dI1, dI2, dI3', 
     'dA1':'Demand Current (dI) dI1', 
     'dA2':'Demand Current (dI) dI2', 
     'dA3':'Demand Current (dI) dI3', 
     'dAo':'Demand Current (dI) dIo', 
     'dkW':'Demand Power (kW)', 
     'dkVAr':'Demand kVAr', 
     'THDX':'Total Harmonic Distortion X (THD) THD L1, THD L12, THD I1', 
     'THDY':'Total Harmonic Distortion Y (THD) THD L2, THD L23, THD I2', 
     'THDZ':'Total Harmonic Distortion Z (THD) THD L3, THD L31, THD I3', 
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
     'kWh':'Power (kWh)', 
     'kWhIm':'Import Power kWh', 
     'kWhEx':'Export Power kWh', 
     'kVArh':'Power (kVArh)', 
     'kVArhI':'Inductive Power', 
     'kVArhC':'Capacitive Power'}
    units = {'L1':'V', 
     'L2':'V',  'L3':'V',  'L12':'V', 
     'L23':'V',  'L31':'V',  'A1':'A', 
     'A2':'A',  'A3':'A',  'An':'A',  'Vavr':'V', 
     'Uavr':'V',  'Iavr':'A',  'v120':'V', 
     'v208':'V', 
     'amps':'A', 
     'P':'kW', 
     'P1':'kW',  'P2':'kW',  'P3':'kW',  'kWatt':'kW', 
     'Q':'kVAr', 
     'Q1':'kVAr',  'Q2':'kVAr',  'Q3':'kVAr',  'kVAr':'kVAr', 
     'S':'kVA', 
     'Freq':'Hz', 
     'PF':'ind', 
     'damps':'A', 
     'dA1':'A', 
     'dA2':'A',  'dA3':'A',  'dAo':'A',  'dkW':'kW', 
     'dkVAr':'kVAr', 
     'THDX':'%', 
     'THDY':'%',  'THDZ':'%',  'THDAn':'%',  'THDL1':'%', 
     'THDL2':'%',  'THDL3':'%',  'THDL12':'%', 
     'THDL23':'%',  'THDL31':'%',  'THDA1':'%', 
     'THDA2':'%',  'THDA3':'%',  'kWh':'kWh', 
     'kVArh':'kVArh', 
     'kWhIm':'kWh', 
     'kWhEx':'kWh', 
     'kVArhI':'kVArh', 
     'kVArhC':'kVArh'}
    ylabels = {'L1':'Voltage', 
     'L2':'Voltage',  'L3':'Voltage',  'L12':'Voltage', 
     'L23':'Voltage',  'L31':'Voltage',  'A1':'Current (I)', 
     'A2':'Current (I)',  'A3':'Current (I)',  'An':'Current (I)',  'Vavr':'Voltage', 
     'Uavr':'Voltage',  'Iavr':'Current (I)',  'v120':'Voltage', 
     'v208':'Voltage', 
     'amps':'Current (I)', 
     'P':'kW', 
     'P1':'kW',  'P2':'kW',  'P3':'kW',  'kWatt':'kW', 
     'Q':'kVAr', 
     'Q1':'kVAr',  'Q2':'kVAr',  'Q3':'kVAr',  'kVAr':'kVAr', 
     'S':'kVA', 
     'Freq':'Hz', 
     'PF':'PF', 
     'damps':'Demand Current (I)', 
     'dA1':'Demand Current (I)', 
     'dA2':'Demand Current (I)',  'dA3':'Demand Current (I)',  'dAo':'Demand Current (I)',  'dkW':'kW', 
     'dkVAr':'kVAr', 
     'THDX':'THD %', 
     'THDY':'THD %',  'THDZ':'THD %',  'THDAn':'THD %',  'THDL1':'THD %', 
     'THDL2':'THD %',  'THDL3':'THD %',  'THDL12':'THD %', 
     'THDL23':'THD %',  'THDL31':'THD %',  'THDA1':'THD %', 
     'THDA2':'THD %',  'THDA3':'THD %',  'kWh':'kWh', 
     'kWhIm':'kWh', 
     'kWhEx':'kWh', 
     'kVArh':'kVArh', 
     'kVArhI':'kVArh', 
     'kVArhC':'kVArh'}
# okay decompiling G:\Recovery_20210210_183130\Users\dude\Documents\MLabs_tools\__pycache__\MLabs_PlotLog.cpython-38.pyc
