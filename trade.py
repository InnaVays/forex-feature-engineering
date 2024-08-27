import numpy as np

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


def strategy_return(data_sl, win_loss, position, print_stat=True, show_plot = True):
    data_sl['win_loss'] = data_sl[ win_loss ]
    data_sl['position'] = data_sl[ position ]

    data_sl_win_loss = data_sl[['win_loss','position']][data_sl.win_loss != 0].copy()

    data_sl_win_loss[['strategy_return']] = 0
    data_sl_win_loss.strategy_return = data_sl_win_loss.position.shift(1)*(data_sl_win_loss.win_loss - 
                                                        data_sl_win_loss.win_loss.shift(1))/data_sl_win_loss.win_loss.shift(1)
    data_sl_win_loss.strategy_return = (1+data_sl_win_loss.strategy_return).cumprod()
    data_sl_win_loss['strategy_return_%'] = data_sl_win_loss.strategy_return*100-100

    if show_plot:
        data_sl_win_loss[['strategy_return_%']].plot(figsize=(15,3),grid=True)
    
    if print_stat:
        print('FINAL RETURN :  %.2f ' % (data_sl_win_loss.strategy_return[-1]*100) )
        print('MAX RETURN:  %.2f ' % (data_sl_win_loss.strategy_return.max()*100) )
        print('MIN RETURN:  %.2f ' % (data_sl_win_loss.strategy_return.min()*100) )

    return data_sl_win_loss


def strategy_stats(data_sl_win_loss, print_stat=True):

    data_sl_win_loss['returns'] = data_sl_win_loss.position.shift()*(data_sl_win_loss.win_loss - \
                                                                    data_sl_win_loss.win_loss.shift(1))
    wins = data_sl_win_loss.returns[data_sl_win_loss.returns>0].count()
    losses = data_sl_win_loss.returns[data_sl_win_loss.returns<0].count()

    mean_win = data_sl_win_loss.returns[data_sl_win_loss.returns>0].mean()
    mean_loss = data_sl_win_loss.returns[data_sl_win_loss.returns<0].mean()
    if print_stat:
        print('Wins: ', wins,'; Losses: ', losses, '; Win rate: ','%.3g'%(wins/(wins+losses)))
        print('Average profit in pips: ','%.3g'%(mean_win/0.0001),'; Average loss in pips: ','%.3g'%(-mean_loss/0.0001))

    return wins, losses, mean_win, mean_loss
