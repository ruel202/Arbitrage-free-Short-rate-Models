import numpy as np
import pandas as pd
import QuantLib as ql
import matplotlib.pyplot as plt


'''No-Arbitrage models '''
class Arbitrage_Free():
    def __init__(self,sigma, a, r, T,i, today_date, num_path #trial
                 ): #(volatility rate, reversion rate(speed of change), initial short rate, one time period, number of time periods)
        self.sigma=sigma
        self.a=a #forward_rate
        self.r=r
        self.T=T
        self.i=i# number of dt period
        self.num_path=num_path #int
        self.daycount= ql.Thirty360(ql.Thirty360.BondBasis)
        self.today_date= ql.Settings.instance().evaluationDate
        self.flat_curve= ql.FlatForward(self.today_date, ql.QuoteHandle(ql.SimpleQuote(self.a)),self.daycount) 
        self.spot_curve_handle= ql.YieldTermStructureHandle(self.flat_curve)
        self.hw_process= ql.HullWhiteProcess(self.spot_curve_handle,a,sigma)
        self.dW = ql.GaussianRandomSequenceGenerator(ql.UniformRandomSequenceGenerator(T, ql.UniformRandomGenerator())) # create a gaussian process
        self.seq = ql.GaussianPathGenerator(self.hw_process, self.i, T,self.dW, False)
    def node(self):
        array= np.zeros((self.num_path,self.T+1))
        for a in range (self.num_path) :
            sample_path= self.seq.next()
            path= sample_path.value()
            time = [path.time(j) for j in range(len(path))]
            value = [path[i] for i in range(len(path))]
            array[a,:]= np.array(value)
        return np.array(time), array
