import requests
import pandas as pd
from pandas.io.json import json_normalize


class api:
    API_KEY = ""

    def __init__(self, api_key=API_KEY):
        self.api_key = api_key

    def fetch(self, path, payload):
        url = f'https://api.prevedere.com{path}'
        r = requests.get(url,params=payload)
        df = pd.DataFrame(r.json())
        return df
    
    def get_indicator(self, provider, provider_id, freq='Monthly', calculation=None, offset=0):
        """
        Create a pandas dataframe with data from the API.
        
        :param url:
        :type url: string
        :param freq: Frequency of indicator to retrieve
        :type freq: string
        :param offset: Number of periods to offset
        :type offset: int
        :param calculation: Calculation to transform the indicator
        :type calculation: string
        """
        path = f'/indicator/series/{provider}/{provider_id}'
        payload = {'ApiKey': self.api_key,'Frequency': freq, 'Offset': offset, "Calculation": calculation}
        df = self.fetch(path, payload)

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



def main():
    pass


if __name__ == '__main__':
    main()
