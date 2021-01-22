import black_scholes_merton as bsm
from pytest import approx

def test_price_ex1():
    # https://medium.com/magnimetrics/black-scholes-model-first-steps-bdcbe1691da7

    spot = 60
    exercise = 58
    rate = .035
    time = .5
    div_rate = .0125
    sigma = .2

    myOption = bsm.BSMoption(
        spot, exercise, sigma, time, rate, div_rate, continuous_compounding=False)
    

    d1 = myOption._d1(spot, time)
    d2 = myOption._d2(spot, time)

    assert d1 == approx(.39,.01)
    assert round(d2, 4) ==  approx(.2486,.05)

    assert round(myOption.black_scholes_call(),2) == 4.77

    assert round(myOption.black_scholes_put(), 2) == 2.14
        
    return None

def test_price_ex2():
    # https://www.erieri.com/blackscholes

    spot = 25
    exercise = 15
    rate = .05
    time = 3.5
    div_rate = .0
    sigma = .2

    myOption = bsm.BSMoption(
        spot, exercise, sigma, time, rate, div_rate, continuous_compounding=False)
    

    d1 = myOption._d1(spot, time)
    d2 = myOption._d2(spot, time)

    assert round(myOption.black_scholes_call(),4) == approx(12.4942)

    assert round(myOption.black_scholes_put(), 3) == approx(0.086)
        
    return None

def test_price_ex3():
    
    """
    vars = [10.56, 10.56, .2450843192, 10, .0039, .48/10.56]
    baseCall = 1.17903666
    basePut = 0.775891492651252

    draw_both_tables(vars, baseCall, basePut)"""

    spot = 10.56
    exercise = 10.56
    rate = .0039
    time = 10
    div_rate = .48/10.56
    sigma = .2450843192

    myOption = bsm.BSMoption(
        spot, exercise, sigma, time, rate, div_rate)
    

    d1 = myOption._d1(spot, time)
    d2 = myOption._d2(spot, time)

    assert round(myOption.black_scholes_call(),4) == approx(1.1790,.1)
    
    #assert round(myOption.black_scholes_put(subtract_divs=True), 4) == approx(.7760,.1)
        
    return None

def test_price_ex4():
    
    """
    # spot, exercise, sigma, time, rate, dividend_rate = None
    vars = [9.68, 9.68, .2439949672, 6.5, 0.05, .48/9.68]
    baseCall = 3.60688165

    draw_both_tables(vars, baseCall)"""

    spot = 9.68
    exercise = 9.68
    rate = .05
    time = 6.5
    div_rate = 0
    sigma = .2439949672

    myOption = bsm.BSMoption(
        spot, exercise, sigma, time, rate, div_rate)
    

    d1 = myOption._d1(spot, time)
    d2 = myOption._d2(spot, time)

    assert round(myOption.black_scholes_call(),4) == approx(3.60688165,.1)
    
    
        
    return None
    
