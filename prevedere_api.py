
import requests
import json
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize

class PrevedereAPI:
    API_KEY = ""

    def __init__(self,api_key=API_KEY):
        self.api_key = api_key

    def fetch(self, path, payload):
        url = f'https://api.prevedere.com{path}'
        r = requests.get(url,params=payload)
        df = pd.DataFrame(r.json())
        return df
    
    def get_indicator(self,provider,provider_id,freq='Monthly',offset=None):
        """
        Create a pandas dataframe with data from the API.
        
        :param url:
        :type url: string
        :param freq: Frequency of indicator to retrieve
        :type freq: string
        """
        path = f'/indicator/series/{provider}/{provider_id}'
        payload = {'ApiKey': self.api_key,'Frequency': freq, 'Offset': offset}
        df = self.fetch(path,payload)

        if "Date" in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
            df.set_index("Date", inplace=True)
        return df
    
    def get_providers(self):
        path = '/providers'
        payload = {'ApiKey': self.api_key}
        return self.fetch(path,payload)

    def get_analysis_jobs(self):
        path = '/analysisjobs'
        payload = {'ApiKey': self.api_key}
        return self.fetch(path,payload)
    
    def search_indicators(self, query):
        path = '/search'
        payload = {'ApiKey': self.api_key,'Query': query}
        results = self.fetch(path,payload)
        return json_normalize(data = results['Results'])
    
    def three_period_year_over_year(self,df, col="Value"):
        if not isinstance(df,pd.DataFrame):
            raise TypeError('Input data must be a dataframe')
        return df.rolling(3).sum()/(df.rolling(3).sum().shift(12))-1

def main():
    prev = PrevedereAPI()
    print(prev.search_indicators('+coal +other +fuels'))
if __name__ == '__main__':
    main()
