import numpy as np
import pandas as pd
import os

from pathlib import Path

#url = 'https://sandbox.iexapis.com/stable/stock/twtr/chart/1y/20190109?chartByDay=true&token=Tsk_d19a63cb677f46e3a663e48d3bcf38ed'

#url = 'https://sandbox.iexapis.com/stable/stock/twtr/chart/5y?chartCloseOnly=true&chartByDay=true&token=Tsk_d19a63cb677f46e3a663e48d3bcf38ed'

#response = requests.request(url=url, method='get')

#pd.read_json(response.content)

def get_stock_prices(filepath):
    df = pd.read_csv(filepath)

    
    


def calc_vol(stock_prices: pd.DataFrame, frame: str="w") -> np.float64:
    """calculate vol

    options are 
        d = daily
        w = weekly
        a = annual
    """

    frame = frame.lower()

    if frame == 'd':
        return stock_prices.std() * np.sqrt(252)
    
    elif frame == 'w':
        return stock_prices.std() * np.sqrt(52)
    
    elif frame == 'a':
        return stock_prices.std()

    else:
        raise ValueError("Unknown frame type, must use one of 'd', 'w', or 'a'")

