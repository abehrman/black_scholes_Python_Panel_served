import numpy as np
import pandas as pd
import scipy.stats as stats


class BSMoption():
    
    def __init__(self, spot, exercise, sigma, time, rate, dividend_rate = None, dividend=None, continuous_compounding=True):
        
        self.spot = spot
        self.exercise = exercise
        self.sigma = sigma
        self.time = time
        self.dividend = dividend
        self.rate = rate
        
        if dividend_rate is not None:
            if dividend:
                raise ValueError("You can only input a dividend rate or a dividend amount.")
            self.dividend_rate = dividend_rate
            
        else:
            if dividend:
                self.dividend_rate = (dividend / spot)
            
            else: 
                self.dividend_rate = 0

        if continuous_compounding == True:
            self.rate = np.log(1+self.rate)
            self.dividend_rate = np.log(1+self.dividend_rate)

    def black_scholes_call(self, time=None, spot=None):
        
        if time is None:
            time = self.time
            
        if spot is None:
            spot = self.spot
        
        N_d1 = stats.norm(0,1).cdf(self._d1(spot, time)) # std. normal cum. density function @ d1
        N_d2 = stats.norm(0,1).cdf(self._d2(spot, time)) # std. normal cum. density function @ d2
        
        PV_k = self.exercise * np.exp(-self.rate * time) # present value of strike
        
        
        adj_spot = spot * np.exp(-self.dividend_rate * time) # adj. spot for dividends
        
        return (adj_spot * N_d1) - ((self.exercise * np.exp(-self.rate * time)) * N_d2)
    
    
    def black_scholes_put(self, time=None, spot=None, subtract_divs=False):
        
        if time is None:
            time = self.time
            
        if spot is None:
            spot = self.spot
        
        #call_px = self.black_scholes_call(time=time, spot=spot)

        #put-call parity = C + PV(x) = P + S

        # P = C + PV(x) - S

        adj_spot = spot * np.exp(-self.dividend_rate * time) # adj. spot for dividends
        
        
        N_d1 = stats.norm(0,1).cdf(-self._d1(spot, time)) # std. normal cum. density function @ d1
        N_d2 = stats.norm(0,1).cdf(-self._d2(spot, time)) # std. normal cum. density function @ d2
        
        put_px = (self.exercise * np.exp(-self.rate * time) * N_d2) - (np.exp(-self.dividend_rate * time) * spot * N_d1)

        return put_px
    
    def _d1(self, spot, time):
        
        distance = np.log(spot / self.exercise)

        growth = (self.rate - self.dividend_rate + (.5 * self.sigma ** 2)) * time

        numerator = distance + growth

        denominator = np.sqrt((self.sigma ** 2) * time)

        d1 = numerator / denominator

        return d1
    
    def _d2(self, spot, time):
        d2 = self._d1(spot, time) - (self.sigma * np.sqrt(time))
        return d2
    