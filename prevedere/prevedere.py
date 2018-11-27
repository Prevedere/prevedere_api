import requests
import pandas as pd
from pandas.io.json import json_normalize


class Api:
    API_KEY = ""

    def __init__(self, api_key=API_KEY):
        self.api_key = api_key

    def fetch(self, path, payload):
        url = f'https://api.prevedere.com{path}'
        r = requests.get(url, params=payload)
        return r.json()
    
    def indicator_series(self, provider, provider_id, freq='Monthly', calculation=None, offset=0, verbose=False):
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
        :param verbose:
        :type verbose: boolean
        """
        path = f'/indicator/series/{provider}/{provider_id}'
        payload = {'ApiKey': self.api_key,'Frequency': freq, 'Offset': offset, "Calculation": calculation}
        df = pd.DataFrame(self.fetch(path, payload))
        df.columns = df.columns.str.lower()

        if verbose:
            print(self.indicator(provider, provider_id).loc[
                      ['ProviderId',
                       'Provider.Name',
                       'Name',
                       'Source',
                       'Units',
                       'Frequency',
                       'StartTime',
                       'EndTime']
                  ])

        if "date" in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            df.set_index("date", inplace=True)

        return df

    def indicator(self, provider, provider_id):
        """
        :param provider:
        :param provider_id:
        """
        path = f'/indicator/{provider}/{provider_id}'
        payload = {'ApiKey': self.api_key}
        return json_normalize(self.fetch(path, payload)).T
    
    def providers(self):
        path = '/providers'
        payload = {'ApiKey': self.api_key}
        return self.fetch(path,payload)

    def analysis_jobs(self):
        path = '/analysisjobs'
        payload = {'ApiKey': self.api_key}
        return self.fetch(path,payload)
    
    def search(self, query):
        path = '/search'
        payload = {'ApiKey': self.api_key,'Query': query}
        results = self.fetch(path,payload)
        return json_normalize(data = results['Results'])

    def model(self, model_id):
        path = f'/rawmodel/{model_id}'
        payload = {'ApiKey': self.api_key}
        return self.fetch(path, payload)


def main():
    pass


if __name__ == '__main__':
    main()