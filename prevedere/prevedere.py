import requests
import pandas as pd
from pandas.io.json import json_normalize


class Api:
    API_KEY = ""

    def __init__(self, api_key: str = API_KEY):
        self.api_key = api_key

    def fetch(self, path: str, payload: dict = {}) -> dict:
        url = f'https://api.prevedere.com{path}'
        payload['ApiKey'] = self.api_key
        r = requests.get(url, params=payload)
        return r.json()
    
    def indicator_series(self,
                         provider: str,
                         provider_id: str,
                         freq: str = 'Monthly',
                         calculation: str = None,
                         offset: int = 0,
                         verbose: bool = False) -> pd.DataFrame:
        """
        Create a pandas dataframe with data from the API.

        :param provider: Code for a data provider, can be hexidecimal or abbreviated name.
        :type provider: str

        :param provider_id: Specific ProviderID for the indicator.
        :type provider_id: str

        :param freq: Frequency of indicator to retrieve
        ("Annual","SemiAnnual","Quarterly","Monthly","BiWeekly","Weekly","Daily")
        :type freq: str

        :param calculation: Calculation to transform the indicator
        ("None","PeriodOverPeriod","YearOverYear","ThreePeriodMoving","FivePeriodMoving","ThreePeriodYearOverYear")
        :type calculation: string

        :param offset: Number of periods to offset
        :type offset: int

        :param verbose:
        :type verbose: bool
        """
        path = f'/indicator/series/{provider}/{provider_id}'
        payload = {'Frequency': freq, 'Offset': offset, "Calculation": calculation}
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

    def indicator(self, provider: str, provider_id: str) -> pd.DataFrame:
        path = f'/indicator/{provider}/{provider_id}'
        return json_normalize(self.fetch(path)).T
    
    def providers(self) -> dict:
        path = '/providers'
        return self.fetch(path)

    def analysis_jobs(self) -> dict:
        path = '/analysisjobs'
        return self.fetch(path)
    
    def search(self, query: str) -> pd.DataFrame:
        path = '/search'
        payload = {'Query': query}
        results = self.fetch(path, payload)
        return json_normalize(data=results['Results'])

    def model(self, model_id: str) -> dict:
        path = f'/rawmodel/{model_id}'
        return self.fetch(path)


def main():
    pass


if __name__ == '__main__':
    main()

