import requests
import json
import configparser
from uuid import UUID
from pathlib import Path, PurePath
import logging

class Api:
    
    def __init__(self, api_key: str = None):
        """
        API can be initialized directly by passing string, if not it looks for prevedere_api.ini in current working directory.
        Copy the prevedere_api.ini.example file and remove `.example` from the end.
        Change the api key to your key.
        """
        if api_key is None:
            try:
                assert PurePath(__file__).name == 'prevedere.py'
                cwd = PurePath(__file__).parent
            except AssertionError as e:
                logging.exception('Prevedere.Api not initialized from prevedere.py')
                cwd = Path.cwd()
                logging.exception('Looking for config in' + str(cwd))

            filepath = Path(cwd.joinpath('prevedere_api.ini'))
            if filepath.is_file():
                config = configparser.ConfigParser()
                config.read(filepath)
                try:
                    api_key = config['keys']['api key']
                    assert api_key != "1234567890abcdef1234567890abcdef"
                except KeyError as e:
                    logging.exception(f'API key not found in {filepath}: ' + repr(e))
                except AssertionError as e:
                    raise ApiKeyError('Config file found, but API key has not been set. Please change the API key in '+ str(filepath)) from e
                    logging.exception()
            else:
                raise FileNotFoundError('prevedere_api.ini config file not found in directory: ' + str(filepath.parent))
                logging.exception()
        
        try:
            self.api_key = str(UUID(api_key))
            company = self.fetch('/company')
            if len(company) == 1:
                self.company = company[0]
                logging.info('Successfully validated as ' + self.company['Name'])
        except (TypeError, ValueError, requests.exceptions.HTTPError) as e:
            raise ApiKeyError(f"'{api_key}' is not a valid API Key. " +\
            "Please check the config file or string that was passed to the constructor and try again.") from e
            logging.exception()

    def fetch(self, path: str, payload: dict = None) -> dict:
        if payload is None:
            payload = {}
        payload['ApiKey'] = self.api_key
        url = f'https://api.prevedere.com{path}'
        try:
            r = requests.get(url, params=payload)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logging.warn('HTTP Error: ' + repr(r.json()))
            raise
        except requests.exceptions.ConnectionError as e:
            logging.exception('Connection Error')
        except requests.exceptions.Timeout as e:
            logging.exception('Timeout Error')
        except requests.exceptions.RequestException as e:
            logging.exception('Requests Error')

        try:
            return r.json()
        except json.decoder.JSONDecodeError as e:
            logging.exception("JSON Error")

    def indicator(self, provider: str, provider_id: str) -> dict:
        path = f'/indicator/{provider}/{provider_id}'
        return self.fetch(path)

    def indicator_series(self,
                         provider: str,
                         provider_id: str,
                         freq: str = 'Monthly',
                         calculation: str = None,
                         start_date: str = None,
                         end_date: str = None,
                         offset: int = 0) -> dict:
        """
        Returns a dict object with data from the API.

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

        :param start_date: Start date for indicator in form "YYYY-MM-DD"
        :type calculation: string

        :param end_date: End date for indicator in form "YYYY-MM-DD"
        :type calculation: string

        :param offset: Number of periods to offset
        :type offset: int
        """

        path = f'/indicator/series/{provider}/{provider_id}'
        payload = {'Frequency': freq,
                   'Offset': offset,
                   "Calculation": calculation,
                   "StartDate": start_date,
                   "EndDate": end_date}
        return self.fetch(path, payload)

    def correlation(self,
                    endog_provider: str,
                    endog_provider_id: str,
                    exog_provider: str,
                    exog_provider_id: str,
                    frequency: str = "Monthly",
                    calculation: str = "ThreePeriodYearOverYear") -> dict:
        path = (f'/correlation/{endog_provider}/{endog_provider_id}/'
                f'{exog_provider}/{exog_provider_id}/'
                f'{frequency}/{calculation}')
        return self.fetch(path)

    def search(self, query: str) -> dict:
        path = '/search'
        payload = {'Query': query}
        return self.fetch(path, payload)

    def raw_model(self,
                  model_id: str,
                  exclude_indicators: bool = True,
                  as_of_date: str = None) -> dict:
        """
        :param model_id: UUID for the forecast model
        :type model_id: str

        :param exclude_indicators: Whether to return only indicators used in model, or all associated indicators
        :type exclude_indicators: bool

        :param as_of_date: Get the model only using data up to the specified date (YYYY-MM-DD). Used for backtesting.
        :type as_of_date: str
        """

        payload = {"ExcludeIndicators": exclude_indicators,
                   "AsOfDate": as_of_date}
        path = f'/rawmodel/{model_id}'
        return self.fetch(path, payload)

    def forecast(self, model_id: str, as_of_date: str = None) -> dict:
        """
        :param model_id: UUID for the forecast model
        :type model_id: str

        :param as_of_date: Get the model only using data up to the specified date (YYYY-MM-DD). Used for backtesting.
        :type as_of_date: str
        """

        path = f'/forecast/{model_id}'
        payload = {"AsOfDate": as_of_date}
        return self.fetch(path, payload)

    def providers(self) -> dict:
        path = '/provider'
        return self.fetch(path)

    def workbench(self, workbench_id: str) -> dict:
        path = f'/workbench/{workbench_id}'
        return self.fetch(path)

class ApiKeyError(ValueError):
    '''Raise when API is improperly formatted or invalid'''
    def __init__(self, message=None):
        if message is None:
            message = "An error occured with the provided API Key."
        self.message = message 

def main():
    pass

if __name__ == '__main__':
    main()
