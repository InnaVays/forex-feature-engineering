
import pandas as pd
import numpy as np
import functions

class Pair_tester:
    def __init__(self, path, pair, granularity, pip, year = 2021):
        self.df = pd.read_pickle( f"{path}{pair}_{granularity}.pkl" )
        self.pip = pip
        self.year = year
        self.initialize_dataframe()
        self.indicators_name = []
        self.stop_loss = None
        self.take_profit = None
        self.exit_condition_long = None
        self.exit_condition_short = None
        self.enter_condition_long = None
        self.enter_condition_short = None
        self.best_strategies = None
        self.strategies_list = None

    def initialize_dataframe(self):
        num_col = [x for x in self.df.columns if x not in['volume','time'] ]
        self.df[num_col] = self.df[num_col].apply(pd.to_numeric)
        self.df.index = pd.to_datetime(self.df.time)
        self.df = self.df[self.df.index.year == self.year]
        self.df.rename(columns = {'volume':'Volume','mid_o':'Open','mid_c':'Close','mid_l':'Low','mid_h':'High','time':'Date'},inplace=True)
        self.df['Spr'] = (self.df.ask_c - self.df.bid_c)
        self.df = self.df.drop(['bid_o', 'bid_h', 'bid_l', 'bid_c', 'ask_o', 'ask_h', 'ask_l', 'ask_c'],axis=1)
        
        self.df['Day'] = self.df.index.date
        index_list =sorted(set(self.df['Day']))
        df_1D = pd.DataFrame( index = index_list, columns = [ 'Open']  )
        df_1D.Open = [ self.df['Open'][ self.df.Day == idx ][0] for idx in index_list ]

        self.df['Date_start'] = np.nan 
        for date in df_1D.index:
            self.df.Date_start[(date.year == self.df.index.year) & (date.month == self.df.index.month) \
                        & (date.day == self.df.index.day)] = df_1D.Open[ df_1D.index == date ][0]

        self.df['Date_start'].ffill( inplace = True)
        self.df['Short_trend'] = np.where( self.df.Date_start < self.df.Close, 1, 0 )
        self.df['Short_trend'] = np.where( self.df.Date_start > self.df.Close, -1, self.df.Short_trend )

    def add_indicator(self, name, enter_long_vector, enter_short_vector):
        self.indicators_name.append( name )
        #self.df[name+'_value'] = value_vector
        self.df[name+'_enter_long'] = enter_long_vector
        self.df[name+'_enter_short'] = enter_short_vector

    def set_enter_condition(self, long_vector, short_vector):
        self.enter_condition_long = long_vector
        self.enter_condition_short = short_vector

    def set_stop_loss_vector( self, vector):
        self.stop_loss = vector

    def set_take_profit_vector( self, vector):
        self.take_profit = vector

    def set_exit_condition( self, long_vector,  short_vector):
        self.exit_condition_long = long_vector
        self.exit_condition_short = short_vector

    def run_simulator(self):
        Strategy = functions.trade_simulator(self.df.Close, self.df.High, self.df.Low, self.df.Spr, 
                                                enter_long=self.enter_condition_long, 
                                                enter_short=self.enter_condition_short, 
                                                take_profit=self.take_profit, 
                                                stop_loss=self.stop_loss, 
                                                )
        self.df['Position'] = Strategy[1]
        self.df['Win_loss'] = Strategy[0]

    def get_labels(self, win_rate):
        # LABELS for 2 CLASSES
        Labels  = np.zeros( len(self.df.Close) )
        Labels[:] = np.nan
        Go = True
        #win_rate = pips*self.pip
        i = 0
        for i in range(0,len(Labels)):
            exit_price_plus = self.df.Close[i] + win_rate[i]
            exit_price_minus = self.df.Close[i] - win_rate[i]
            Go = True
            j = 1
            while Go:
                if i+j > len(Labels)-1:
                    break
                if (exit_price_plus <= self.df.High[i+j]):
                    Labels[i] = 1
                    Go = False
                    continue
                elif (exit_price_minus >= self.df.Low[i+j]):
                    Labels[i] = -1
                    Go = False
                    continue
                else:
                    j += 1
        self.df['Labels_2'] = Labels

    def apply_bunch_of_indicators(self):
        functions.apply_bunch_of_indicators( self )

    def run_indicators_search(self, threshold):
        names_num = len(self.indicators_name)

        strategies_df = pd.DataFrame( columns = ['Indicator_1','Indicator_2','Indicator_3',
                                            'short_luck_ratio', 'long_luck_ratio','short_opps','long_opps'] )

        for i in range(0, names_num-2):
            for j in range(i+1, names_num-1):
                for k in range(j+1, names_num):
                    enter_condition_long = self.df[self.indicators_name[i]+'_enter_long'] \
                                            & self.df[self.indicators_name[j]+'_enter_long'] \
                                            & self.df[self.indicators_name[k]+'_enter_long'] 
                    
                    enter_condition_short = self.df[self.indicators_name[i]+'_enter_short'] \
                                                & self.df[self.indicators_name[j]+'_enter_short'] \
                                                & self.df[self.indicators_name[k]+'_enter_short'] 
                        
                    short_opps = sum(enter_condition_short)
                    long_opps = sum(enter_condition_long)
                        
                    if long_opps == 0:
                        long_luck_ratio = 0
                    else:
                        long_luck_ratio = sum(self.df.Labels_2[ enter_condition_long ] == 1)/ long_opps
                        
                    if short_opps == 0:
                        short_luck_ratio = 0
                    else:
                        short_luck_ratio = sum(self.df.Labels_2[ enter_condition_short ] == -1)/ short_opps
                    strategies_df = strategies_df.append({'Indicator_1': self.indicators_name[i],
                                                            'Indicator_2': self.indicators_name[j],
                                                            'Indicator_3': self.indicators_name[k],
                                                            'short_luck_ratio': short_luck_ratio,
                                                            'long_luck_ratio': long_luck_ratio,
                                                            'short_opps': short_opps,
                                                            'long_opps': long_opps }, ignore_index=True)

        best_strategies = strategies_df[ (strategies_df['short_luck_ratio'] > threshold) &
                                        (strategies_df['long_luck_ratio'] > threshold) &
                                        (strategies_df['short_opps'] > 1) &
                                        (strategies_df['long_opps'] > 1) ].sort_values('short_opps', ascending=False)
        print('Number of potential strategies: ',len(best_strategies))
        self.best_strategies = best_strategies

    def get_best_strategies_from_df(self, best_strategies_df):
        strategies_num = len(best_strategies_df)
        strategies_list = []
        for i in range(0, strategies_num):
            
            enter_condition_long =    self.df[best_strategies_df.iloc[i,0]+'_enter_long'] \
                                    & self.df[best_strategies_df.iloc[i,1]+'_enter_long'] \
                                    & self.df[best_strategies_df.iloc[i,2]+'_enter_long'] 
                    
            enter_condition_short =   self.df[best_strategies_df.iloc[i,0]+'_enter_short'] \
                                    & self.df[best_strategies_df.iloc[i,1]+'_enter_short'] \
                                    & self.df[best_strategies_df.iloc[i,2]+'_enter_short'] 
            
            self.df['Strategy_'+str(i)] = np.where( enter_condition_long, 1,  0)
            self.df['Strategy_'+str(i)] = np.where( enter_condition_short, -1,  self.df['Strategy_'+str(i)])
            strategies_list.append('Strategy_'+str(i))
        self.strategies_list = strategies_list
    
    def strategy_plot(self):
        functions.strategy_outcome(self.df, 'Win_loss', 'Position')