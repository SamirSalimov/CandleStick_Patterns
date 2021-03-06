#!/usr/bin/python3

#import pandas as pd
from pandas import Series, read_csv, DatetimeIndex
from scipy import stats
from numpy import arange, where, diff, array, all, concatenate

import pandas as pd
import pandas_datareader.data as web
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.dates as mdates

class Tools_cl(object):

    def __init__(self,file,ma_period=1,lr_period=2):
        self.file = file
        self.ma_period = ma_period
        self.lr_period = lr_period
        self.hammer_trend_slope = 0.087
        self.issuer_list = read_csv(self.file)
        #        self.moving_average()
        #        self.ma_linear_regretion()
        #        self.umbrella_candle()
        #        self.hammer()
        #        self.hanging_man()
        self.trend()
        self.issuer_list.to_csv('issuer_list.csv')

    def moving_average(self):
        self.issuer_list['MA'] = Series.rolling(self.issuer_list['Close'], window=self.ma_period, min_periods=self.ma_period).mean()

    def ma_linear_regretion(self):
        y = arange(float(self.lr_period))
        for index in range((self.ma_period - 1), len(self.issuer_list) - self.lr_period + 1,
                           1):  # from end of issuer_list
            for index2 in range(self.lr_period): #prepare array len(lr_period)
                y[index2] = self.issuer_list['MA'][index+index2]
            slope, intercept, r_value, p_value, std_err = stats.linregress(arange(self.lr_period), y)
            self.issuer_list.set_value([index + self.lr_period - 1], 'LR', slope)

    def umbrella_candle (self):
        u_shadow_size_parameter = 0.2
        body_size_parameter = 0.1
        for index in range(len(self.issuer_list)):
            Open = self.issuer_list['Open'][index]
            High = self.issuer_list['High'][index]
            Low = self.issuer_list['Low'][index]
            Close = self.issuer_list['Close'][index]
            if (Close > Open): #white candle
                Candle = High - Low
                Body = Close - Open
                U_Shadow = High - Close
                L_Shadow = Open - Low
                if ((Body > 0) & (L_Shadow >= float(2) * Body) & (U_Shadow <= u_shadow_size_parameter * Candle) & (Body >= body_size_parameter * Candle)): # parameters of umbrella candle
                    self.issuer_list.set_value([index], 'Umbrella', 'True')
                else:
                    self.issuer_list.set_value([index], 'Umbrella', 'False')
            else: # same for black candle
                Candle = High - Low
                Body = Open - Close
                U_Shadow = High - Open
                L_Shadow = Close - Low
                if ((Body > 0) & (L_Shadow >= float(2) * Body) & (U_Shadow <= u_shadow_size_parameter * Candle) & (Body >= body_size_parameter * Candle)):
                    self.issuer_list.set_value([index], 'Umbrella', 'True')
                else:
                    self.issuer_list.set_value([index], 'Umbrella', 'False')

    def average_slope(self):
        pass

    def local_min(self):
        pass

    def local_max(self):
        pass

    def hammer(self):
        self.issuer_list['Hammer'] = 'False'
        umbrella_index = self.issuer_list.loc[(self.issuer_list.Umbrella == 'True')].index.tolist()
        for index in umbrella_index:
            if (index >= self.ma_period + self.lr_period - 2):
                if((self.issuer_list.Low[index-1] >= self.issuer_list.Low[index]) & (self.issuer_list.Low[index+1] >= self.issuer_list.Low[index])):
                    if (self.issuer_list.LR[index] < 0):
                        self.issuer_list.set_value([index+1], 'Hammer', 'HA')
                        self.issuer_list.set_value([index], 'Hammer', 'H')
                        self.issuer_list.set_value([index-1], 'Hammer', 'HB')

    def hanging_man(self):
        self.issuer_list['Hanging Man'] = 'False'
        umbrella_index = self.issuer_list.loc[(self.issuer_list.Umbrella == 'True')].index.tolist()
        for index in umbrella_index:
            if (index >= self.ma_period + self.lr_period - 2):
                if ((self.issuer_list.High[index - 1] <= self.issuer_list.High[index]) & (
                    self.issuer_list.High[index + 1] <= self.issuer_list.High[index])):
                    if (self.issuer_list.LR[index] > 0):
                        self.issuer_list.set_value([index + 1], 'Hanging Man', 'HMA')
                        self.issuer_list.set_value([index], 'Hanging Man', 'HM')
                        self.issuer_list.set_value([index - 1], 'Hanging Man', 'HMB')





def main():

    a = Tools_cl('intc.csv',10,5)

if __name__ == "__main__": main()
