import numpy as np
import pandas as pd
import pandas_ta as ta


# INDICATORS

def apply_bunch_of_indicators( pair ):
    # SMMA short cross
    SMMA_f = ta.smma(pair.df.Close, 3)
    SMMA_s = ta.smma(pair.df.Close, 5)
    enter_long =  ( SMMA_f > SMMA_s ) & ( SMMA_f.shift() < SMMA_s.shift() ) 
    enter_short = ( SMMA_f < SMMA_s ) & ( SMMA_f.shift() > SMMA_s.shift() ) 
    pair.add_indicator( 'SMMA_1_cross', enter_long, enter_short )

    # SMA cross
    SMA = ta.smma(pair.df.Close, 10)
    enter_long =  ( SMA < pair.df.Close ) 
    enter_short = ( SMA > pair.df.Close ) 
    pair.add_indicator( 'SMA_1_cross', enter_long, enter_short )

    # SMA cross
    SMA = ta.smma(pair.df.Close, 20)
    enter_long =  ( SMA < pair.df.Close ) 
    enter_short = ( SMA > pair.df.Close ) 
    pair.add_indicator( 'SMA_2_cross', enter_long, enter_short )

    # SMMA long cross
    SMMA_f = ta.smma(pair.df.Close, 10)
    SMMA_s = ta.smma(pair.df.Close, 20)
    enter_long =  ( SMMA_f > SMMA_s ) & ( SMMA_f.shift() < SMMA_s.shift() ) 
    enter_short = ( SMMA_f < SMMA_s ) & ( SMMA_f.shift() > SMMA_s.shift() ) 
    pair.add_indicator( 'SMMA_2_cross', enter_long, enter_short )

    # BB
    BB = ta.ema(pair.df.Close,20)
    BB_up = BB + 0.8*pair.df.Close.rolling(20).std()
    BB_down = BB - 0.8*pair.df.Close.rolling(20).std()
    enter_long =  ( BB_up.shift() > pair.df.Close.shift() ) & ( BB_up < pair.df.Close )
    enter_short = ( BB_down.shift() < pair.df.Close.shift() ) & ( BB_down > pair.df.Close )
    pair.add_indicator( 'BB_1', enter_long, enter_short )

    # BB
    BB = ta.ema(pair.df.Close,50)
    BB_up = BB + 1*pair.df.Close.rolling(50).std()
    BB_down = BB - 1*pair.df.Close.rolling(50).std()
    enter_long =  ( BB_up.shift() > pair.df.Close.shift() ) & ( BB_up < pair.df.Close )
    enter_short = ( BB_down.shift() < pair.df.Close.shift() ) & ( BB_down > pair.df.Close )
    pair.add_indicator( 'BB_2', enter_long, enter_short )

    # RSI 14:
    RSI_14 = ta.rsi(pair.df.Close, length=14)
    enter_long = (RSI_14 > 50)
    enter_short = (RSI_14 < 50)
    pair.add_indicator( 'RSI_14', enter_long, enter_short )

    # RSI 3:
    RSI_3 = ta.rsi(pair.df.Close, length=3)
    enter_long = (RSI_3 > 70) & (RSI_3.shift() < RSI_3)
    enter_short = (RSI_3 < 30) & (RSI_3.shift() > RSI_3)
    pair.add_indicator( 'RSI_3', enter_long, enter_short )

    # MACD:
    MACD = ta.ema(pair.df.Close, 12) - ta.ema(pair.df.Close,26)
    MACDh = MACD-ta.ema(MACD, 9)
    enter_long = (MACDh > 0) & (MACDh.shift() < 0)
    enter_short = (MACDh < 0) & (MACDh.shift() > 0)
    pair.add_indicator( 'MACD', enter_long, enter_short )

    # Awesome Oscillator: ao
    AO = ta.ao(high=pair.df.High,low=pair.df.Low)
    enter_long = AO > AO.shift() 
    enter_short = AO < AO.shift()
    pair.add_indicator( 'AO', enter_long, enter_short )

    #Stochastic Oscillator: stoch
    Stochstics = ta.stoch(close = pair.df.Close, high=pair.df.High,low=pair.df.Low, k=12, d = 3, smooth = 4 )
    STOCHk = Stochstics.iloc[:,0]
    STOCHh = Stochstics.iloc[:,2]
    enter_long = (STOCHk < 50) & (STOCHh > 0)
    enter_short = (STOCHk > 50) & (STOCHh < 0)
    pair.add_indicator( 'STOCH', enter_long, enter_short )

    # CCI
    CCI = ta.cci(close=pair.df.Close,low=pair.df.Low,high=pair.df.High, length=20)
    enter_long = (CCI > 100) & (CCI.shift() < CCI)
    enter_short = (CCI < -100) & (CCI.shift() > CCI)
    pair.add_indicator( 'CCI', enter_long, enter_short )

    # Money Flow Index: mfi
    MFI = ta.mfi(close = pair.df.Close, high = pair.df.High, low=pair.df.Low, volume=pair.df.Volume )
    enter_long = (MFI > 50)
    enter_short = (MFI < 50)
    pair.add_indicator( 'MFI', enter_long, enter_short )

    #Stochastic RSI: stochrsi
    Stochrsi = ta.stochrsi(close = pair.df.Close)
    STOCHRSIk = Stochrsi.iloc[:,0]
    STOCHRSId = Stochrsi.iloc[:,1]
    enter_long = (STOCHRSIk < 30) & (STOCHRSIk > STOCHRSId)
    enter_short = (STOCHRSIk > 70) & (STOCHRSIk < STOCHRSId)
    pair.add_indicator( 'STOCHRSI', enter_long, enter_short )

    # Volume weighted average price
    VWAP = ta.vwap(close = pair.df.Close , high = pair.df.High, low=pair.df.Low, volume=pair.df.Volume)
    enter_long = (VWAP.shift() > pair.df.Close.shift()) & (VWAP < pair.df.Close)
    enter_short = (VWAP.shift() < pair.df.Close.shift()) & (VWAP > pair.df.Close)
    pair.add_indicator( 'MFI', enter_long, enter_short )

    #Keltner Channel: kc
    KC = ta.kc(close = pair.df.Close, high = pair.df.High, low=pair.df.Low )
    enter_long = (KC.iloc[:,0] > pair.df.Close)
    enter_short = (KC.iloc[:,2] < pair.df.Close)
    pair.add_indicator( 'KC', enter_long, enter_short )

    #Chaikin Money Flow: cmf
    CMF = ta.cmf(close = pair.df.Close, high = pair.df.High, low=pair.df.Low, volume=pair.df.Volume )
    enter_long = (CMF > 0) & (CMF.shift() < 0 )
    enter_short = (CMF < 0) & (CMF.shift() > 0 )
    pair.add_indicator( 'CMF', enter_long, enter_short )
    
    #Rate of Change: roc
    ROC = ta.roc(close = pair.df.Close , high = pair.df.High, low=pair.df.Low)
    enter_long = (ROC > 0) & (ROC.shift() < 0 )
    enter_short = (ROC < 0) & (ROC.shift() > 0 )
    pair.add_indicator( 'ROC', enter_long, enter_short )    

    # Average Directional Movement Index: adx
    ADX = ta.adx(close = pair.df.Close, high = pair.df.High, low=pair.df.Low ).iloc[:,0]
    enter_long = (ADX > 25) 
    enter_short = (ADX > 25) 
    pair.add_indicator( 'ADX', enter_long, enter_short ) 

    #Momentum: mom
    MOM = ta.mom(close = pair.df.Close , high = pair.df.High, low=pair.df.Low)
    enter_long = (MOM > 0) 
    enter_short = (MOM < 0) 
    pair.add_indicator( 'MOM', enter_long, enter_short ) 

    #Williams %R: willr
    WILLR = ta.willr(close =  pair.df.Close, high =  pair.df.High, low= pair.df.Low )
    enter_long = (WILLR > -20) 
    enter_short = (WILLR < -80) 
    pair.add_indicator( 'WILLR', enter_long, enter_short ) 
    
    #Parabolic Stop and Reverse: psar
    PSAR = ta.psar(close = pair.df.Close, high = pair.df.High, low=pair.df.Low )
    enter_long = ~PSAR.iloc[:,0].isna()
    enter_short = ~PSAR.iloc[:,1].isna()
    pair.add_indicator( 'PSAR', enter_long, enter_short ) 

    #Supertrend: supertrend
    Supertrend = ta.supertrend(close = pair.df.Close, high=pair.df.High,low=pair.df.Low)
    enter_long = Supertrend.iloc[:,1] == 1
    enter_short = Supertrend.iloc[:,1] == -1
    pair.add_indicator( 'supertrend', enter_long, enter_short ) 

    #Increasing: increasing
    Increasing = ta.increasing(close = pair.df.Close, high=pair.df.High,low=pair.df.Low)
    enter_long = Increasing == 1
    enter_short = Increasing == 0
    pair.add_indicator( 'increasing', enter_long, enter_short ) 

    # Support/Resistance
    resist_cond = (pair.df.High > pair.df.High.shift()) & (pair.df.High.shift() > pair.df.High.shift(2)) 
    support_cond = (pair.df.Low < pair.df.Low.shift()) & (pair.df.Low.shift() < pair.df.Low.shift(2))
    
    pair.df['Resist'] = np.where( resist_cond , pair.df.High, np.nan )
    pair.df['Resist'].ffill( inplace = True )

    pair.df['Support'] = np.where( support_cond, pair.df.Low, np.nan )
    pair.df['Support'].ffill( inplace = True )

    enter_long = (pair.df.Close < pair.df.Support) & (pair.df.Close.shift() > pair.df.Support.shift()) \
                & (pair.df.Resist > pair.df.Support)
    enter_short = (pair.df.Close > pair.df.Resist) & (pair.df.Close.shift() < pair.df.Resist.shift()) \
                & (pair.df.Resist > pair.df.Support)
    pair.add_indicator( 'support_resist', enter_long, enter_short ) 

    # Quantiles
    EMA = ta.ema(pair.df.Close, 30)
    test_short = pair.df.Close - EMA
    test_quant_up =  test_short.rolling(40).quantile(1 - 0.05)
    test_quant_down = test_short.rolling(40).quantile(0.05)
    enter_long = (test_short < test_quant_down ) & (test_short.shift() > test_quant_down.shift() )
    enter_short = (test_short > test_quant_up ) & (test_short.shift() < test_quant_up.shift() )
    pair.add_indicator( 'Quantiles', enter_long, enter_short ) 
                            
def trade_simulator(Close, High, Low, Spr, enter_long, enter_short, take_profit, stop_loss ):
    Position = np.zeros(len(Close))
    Win_loss = np.zeros(len(Close))
    Ent_exit = np.zeros(len(Close))
    for i in range(1, len(Win_loss) ):  
        # strategy_return INDICATORS : LONG ENTER:
        if (enter_long[i]==1) & (Position[i-1] == 0) & (take_profit[i] == take_profit[i]) & (stop_loss[i] == stop_loss[i]):
            Position[i] = 1
            Win_loss[i] = Close[i] + Spr[i]/2
            Ent_exit[i] = 0
            stop_price = Close[i] - stop_loss[i]
            exit_price = Close[i] + take_profit[i]
            #print('go Long')
            continue    
            # EXIT THE CURRENT Position: EXIT LONG
        if Position[i-1] == 1:
            if (stop_price > Low[i]): 
                Position[i] = 0
                Win_loss[i] = stop_price - Spr[i]/2
                Ent_exit[i] = 1
                continue
            elif (exit_price < High[i]): 
                Position[i] = 0
                Win_loss[i] = exit_price - Spr[i]/2
                Ent_exit[i] = 2
                continue
            else:
                Position[i] = 1
                continue
        # strategy_return INDICATORS : SHORT ENTER:
        if (enter_short[i]==1) & (Position[i-1] == 0) & (take_profit[i] == take_profit[i]) & (stop_loss[i] == stop_loss[i]):
            Position[i] = -1
            Win_loss[i] = Close[i] - Spr[i]/2
            stop_price = Close[i] + stop_loss[i]
            exit_price = Close[i] - take_profit[i]
            Ent_exit[i] = 0
            continue
        # EXIT THE CURRENT Position: EXIT SHORT
        if Position[i-1] == -1:
            if (stop_price < High[i]): 
                Position[i] = 0
                Win_loss[i] = stop_price + Spr[i]/2
                Ent_exit[i] = 1
                continue
            elif (exit_price > Low[i]): 
                Position[i] = 0
                Win_loss[i] = exit_price + Spr[i]/2
                Ent_exit[i] = 2
                continue
            else:
                Position[i] = -1
    return [Win_loss, Position, Ent_exit]


def strategy_outcome(data_sl, win_loss, position):
    data_sl['win_loss'] = data_sl[ win_loss ]
    data_sl['position'] = data_sl[ position ]

    data_sl_win_loss = data_sl[['win_loss','position']][data_sl.win_loss != 0].copy()

    data_sl_win_loss[['strategy_return']] = 0
    data_sl_win_loss.strategy_return = data_sl_win_loss.position.shift(1)*(data_sl_win_loss.win_loss - 
                                                        data_sl_win_loss.win_loss.shift(1))/data_sl_win_loss.win_loss.shift(1)
    data_sl_win_loss.strategy_return = (1+data_sl_win_loss.strategy_return).cumprod()
    data_sl_win_loss['strategy_return_%'] = data_sl_win_loss.strategy_return*100-100

    data_sl_win_loss[['strategy_return_%']].plot(figsize=(15,3),grid=True)

    print('FINAL RETURN :  %.2f ' % (data_sl_win_loss.strategy_return[-1]*100) )
    print('MAX RETURN:  %.2f ' % (data_sl_win_loss.strategy_return.max()*100) )
    print('MIN RETURN:  %.2f ' % (data_sl_win_loss.strategy_return.min()*100) )

    data_sl_win_loss['returns'] = data_sl_win_loss.position.shift()*(data_sl_win_loss.win_loss - \
                                                                    data_sl_win_loss.win_loss.shift(1))

    wins = data_sl_win_loss.returns[data_sl_win_loss.returns>0].count()
    losses = data_sl_win_loss.returns[data_sl_win_loss.returns<0].count()

    mean_win = data_sl_win_loss.returns[data_sl_win_loss.returns>0].mean()
    mean_loss = data_sl_win_loss.returns[data_sl_win_loss.returns<0].mean()

    print('Wins: ', wins,'; Losses: ', losses, '; Win rate: ','%.3g'%(wins/(wins+losses)))
    print('Average profit in pips: ','%.3g'%(mean_win/0.0001),'; Average loss in pips: ','%.3g'%(-mean_loss/0.0001))

