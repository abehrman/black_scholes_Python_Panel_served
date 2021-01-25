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

    def black_scholes_call(self, spot=None, exercise=None, time=None, sigma=None, rate=None, dividend_rate=None):
        
        if spot is None:
            spot = self.spot
        
        if exercise is None:
            exercise = self.exercise

        if time is None:
            time = self.time

        if sigma is None:
            sigma = self.sigma
        
        if rate is None:
            rate = self.rate

        if dividend_rate is None:
            dividend_rate = self.dividend_rate
            
        
        N_d1 = stats.norm(0,1).cdf(self._d1(spot, exercise, time, sigma, rate, dividend_rate)) # std. normal cum. density function @ d1
        N_d2 = stats.norm(0,1).cdf(self._d2(spot, exercise, time, sigma, rate, dividend_rate)) # std. normal cum. density function @ d2
        
        PV_k = exercise * np.exp(-rate * time) # present value of strike
        
        
        adj_spot = spot * np.exp(-dividend_rate * time) # adj. spot for dividends
        
        return (adj_spot * N_d1) - ((exercise * np.exp(-rate * time)) * N_d2)
    
    
    def black_scholes_put(self, spot=None, exercise=None, time=None, sigma=None, rate=None, dividend_rate=None):
        
        if spot is None:
            spot = self.spot
        
        if exercise is None:
            exercise = self.exercise

        if time is None:
            time = self.time

        if sigma is None:
            sigma = self.sigma
        
        if rate is None:
            rate = self.rate

        if dividend_rate is None:
            dividend_rate = self.dividend_rate
        
        #call_px = self.black_scholes_call(time=time, spot=spot)

        #put-call parity = C + PV(x) = P + S

        # P = C + PV(x) - S

        adj_spot = spot * np.exp(-dividend_rate * time) # adj. spot for dividends
        
        #put_px = call_px + self.exercise * np.exp(-self.rate * time) - spot

        # wasn't producing the correct answer

        #N_d1 = stats.norm(0,1).cdf(-self._d1(spot, time)) # std. normal cum. density function @ d1
        #N_d2 = stats.norm(0,1).cdf(-self._d2(spot, time)) # std. normal cum. density function @ d2
        
        N_d1 = stats.norm(0,1).cdf(-self._d1(spot, exercise, time, sigma, rate, dividend_rate)) # std. normal cum. density function @ d1
        N_d2 = stats.norm(0,1).cdf(-self._d2(spot, exercise, time, sigma, rate, dividend_rate)) # std. normal cum. density function @ d2
        
        put_px = (exercise * np.exp(-rate * time) * N_d2) - (np.exp(-dividend_rate * time) * spot * N_d1)

        return put_px
    
    def _d1(self, spot, exercise, time, sigma, rate, dividend_rate):
        
        distance = np.log(spot / exercise)

        growth = (rate - dividend_rate + (.5 * sigma ** 2)) * time

        numerator = distance + growth

        denominator = np.sqrt((sigma ** 2) * time)

        d1 = numerator / denominator

        return d1
    
    def _d2(self, spot, exercise, time, sigma, rate, dividend_rate):
        d2 = self._d1(spot, exercise, time, sigma, rate, dividend_rate) - (sigma * np.sqrt(time))
        return d2
    