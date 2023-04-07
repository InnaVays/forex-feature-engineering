import header

import requests
import pandas as pd
from dateutil.parser import *

class OandaAPI():
    def __init__( self):
        self.session = requests.Session()
            
    def get_instruments_df( self ):
        url = f"{header.OANDA_URL}/accounts/{header.ACCOUNT_ID}/instruments"
        response = self.session.get(url, params=None, headers = header.SECURE_HEADER)
        code = response.status_code
        data = response.json()
        if code == 200:
            df = pd.DataFrame.from_dict( data['instruments'] )
            return df[['name','type','displayName','pipLocation','marginRate']]
        else:
            return None
    
    def save_instruments_pickle( self ):
        df = self.get_instruments_df()
        if df is not None:
            df.to_pickle( "instruments.pkl" )
        
    def fetch_candles( self , pair_name, count=None, granularity = 'H1', date_from = None, date_to = None, as_df = False ):
        url = f"{header.OANDA_URL}/instruments/{pair_name}/candles"    
        params = dict( count = count, granularity = granularity, price = 'BMA')
        
        if date_from is not None and date_to is not None:
            params['from'] = int(date_from.timestamp())
            params['to'] = int(date_to.timestamp())
        elif count is not None:
            params['count'] = count
        else:
            params['count'] = 4000

        response = self.session.get(url, params=params, headers = header.SECURE_HEADER)   
        if response.status_code != 200:
            return response.status_code, None
        if as_df:
            json_data = response.json()['candles']
            return response.status_code, OandaAPI.cadles_to_df(json_data)
        else:
            return response.status_code, response.json()
    
    @classmethod
    def cadles_to_df(cls, json_data):
        new_data = []
        for candle in json_data:
            if candle['complete'] == False:
                continue
            new_dict = {}
            new_dict['time'] = candle['time']
            new_dict['volume'] = candle['volume']
            for price in ['bid','mid','ask']:
                for ohlc in ['o','h','l','c']:
                    new_dict[f'{price}_{ohlc}'] = float(candle[price][ohlc])
            new_data.append(new_dict) 
        df = pd.DataFrame.from_dict(new_data)
        df['time'] = [parse(x) for x in df.time]
        return df

class OANDAInstrument():
    def __init__( self, specifics):  
        self.name = specifics['name']
        self.ins_type = specifics['type']
        self.display_name = specifics['displayName']
        self.pip_location = pow(10,specifics['pipLocation'])
        self.margin_rate = specifics['marginRate']
        
    def __repr__(self):
        return str( vars(self) ) 
        
    @classmethod
    def get_instrument_dict_from_file(cls):
        df = pd.read_pickle( "instruments.pkl" )
        df_dict = df.to_dict(orient = 'records')
        instruments_list = [ OANDAInstrument(x) for x in df_dict ]
        instrument_keys = [x.name for x in instruments_list]
        dictionary = { k:v  for (k,v) in zip(instrument_keys, instruments_list) }
        return dictionary
                
    def get_pairs_from_list(self, currencies_list):
        OANDA_pairs = self.get_instrument_dict_from_file().keys()
        pairs_list = []
        for p1 in currencies_list:
            for p2 in currencies_list:
                pair = f'{p1}_{p2}'
                if pair in OANDA_pairs :
                    pairs_list.append(pair)
        return pairs_list

if __name__ == "__main__":
    pass