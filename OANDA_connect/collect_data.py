import datetime as dt
import pandas as pd
from dateutil.parser import *

from oanda_api import OANDAInstrument
from oanda_api import OandaAPI

insruments_to_get = {
   # 'D' : 24*60,
   # 'H4': 60*4,
    'H1': 60,
   # 'M15': 15
   # 'M1': 1
}

def get_utc(date_str):
    d = parse(date_str)
    return d.replace(tzinfo = dt.timezone.utc) 

def create_file(pair, granularity, api, candle_count):
    time_step = insruments_to_get[granularity]*candle_count
    
    end_date = get_utc("2022-12-31 23:59:59")
    date_from = get_utc("2018-01-01 00:00:00")
    
    candles_dataframes = []
    date_to = date_from
    n = 0
    while date_to < end_date:
        date_to = date_from + dt.timedelta(minutes = time_step)
        if date_to > end_date:
            date_to = end_date
            
        code, new_candle_df = api.fetch_candles(pair, 
                                            granularity=granularity, 
                                            date_from=date_from, 
                                            date_to= date_to,
                                            as_df = True )
        if (code == 200) and (len(new_candle_df) > 0):
            n += 1
            candles_dataframes = candles_dataframes.append( new_candle_df , ignore_index=True)
        elif code != 200:
            print('ERROR ', pair, granularity, date_from, date_to)
            break
        date_from = date_to
    
    final_df = pd.concat(candles_dataframes, axis=0)
    final_df.drop_duplicates(subset='time', inplace = True)
    final_df.sort_values(by='time', inplace = True)
    final_df.to_pickle( "hist_data/"+str(pair)+"_"+str(granularity)+".pkl" )
    print( "Collected: ", pair, granularity, final_df.iloc[0].time, final_df.iloc[-1].time)

def run_collection():
    pair_list = ['AUD','CAD','USD','GBP','EUR']
    api = OandaAPI()
    api.save_instruments_pickle()
    for g in insruments_to_get.keys():
        for i in OANDAInstrument.get_pairs_from_list(pair_list):
            create_file(i, g, api)
            
if __name__ == "__main__":
    run_collection()
            
