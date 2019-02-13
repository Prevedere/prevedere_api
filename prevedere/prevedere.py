import requests


class Api:
    API_KEY = ""

    def __init__(self, api_key: str = API_KEY):
        self.api_key = api_key

    def fetch(self, path: str, payload: dict = None) -> dict:
        if payload is None:
            payload = {}
        payload['ApiKey'] = self.api_key
        url = f'https://api.prevedere.com{path}'
        try:
            r = requests.get(url, params=payload)
            r.raise_for_status()
        except requests.exceptions.RequestException as err:
            print(err)
        else:
            return r.json()

    def indicator(self, provider: str, provider_id: str) -> dict:
        path = f'/indicator/{provider}/{provider_id}'
        return self.fetch(path)

    def indicator_series(self,
                         provider: str,
                         provider_id: str,
                         freq: str = 'Monthly',
                         calculation: str = None,
                         offset: int = 0) -> dict:
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
        ("None","PeriodOverPeriod","YearOverYear","ThreePeriodMoving",
        "FivePeriodMoving","ThreePeriodYearOverYear")
        :type calculation: string

        :param offset: Number of periods to offset
        :type offset: int
        """

        path = f'/indicator/series/{provider}/{provider_id}'
        payload = {'Frequency': freq, 'Offset': offset, "Calculation": calculation}
        return self.fetch(path, payload)

    def correlation(self,
                    endog_provider: str,
                    endog_provider_id: str,
                    exog_provider: str,
                    exog_provider_id: str,
                    frequncy: str = "Monthly",
                    calculation: str = "ThreePeriodYearOverYear") -> dict:
        path = (f'/correlation/{endog_provider}/{endog_provider_id}/'
                f'{exog_provider}/{exog_provider_id}/'
                f'{frequncy}/{calculation}')
        return self.fetch(path)

    def search(self, query: str) -> dict:
        path = '/search'
        payload = {'Query': query}
        return self.fetch(path, payload)

    def raw_model(self, model_id: str) -> dict:
        path = f'/rawmodel/{model_id}'
        return self.fetch(path)

    def forecast(self, model_id: str) -> dict:
        path = f'/forecast/{model_id}'
        return self.fetch(path)

    def providers(self) -> dict:
        path = '/provider'
        return self.fetch(path)

    def workbench(self, workbench_id: str) -> dict:
        path = f'/workbench/{workbench_id}'
        return self.fetch(path)


def main():
    pass


if __name__ == '__main__':
    main()
