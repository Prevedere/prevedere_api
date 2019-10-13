import configparser
import csv
import io
import json
import logging
from pathlib import Path, PurePath
import re
from uuid import UUID

import requests


class Api:
    """
    TODO:
    - Add information about what an API key is, how to get one, and how to use Swagger 
    - Reference PEP standards for class docstrings
    """    
    def __init__(self, api_key: str = None, base: str = None, log: bool =None):
        """
        API can be initialized directly by passing string, if not it looks for prevedere_api.ini in current working directory.
        Copy the prevedere_api.ini.example file and remove `.example` from the end.
        Change the api key to your key.
        """
        if log:
            if type(log) == int:
                level = log
            else:
                level=logging.INFO
            self.log = log
            logging.basicConfig(format='%(levelname)s-%(message)s', level=level)
        else:
            self.log = False

        if api_key is None:
            try:
                assert PurePath(__file__).name == 'api.py'
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
                    if 'base' in config['keys']:
                        base = config['keys']['base']
                    assert api_key != "1234567890abcdef1234567890abcdef"
                except KeyError as e:
                    logging.exception(f'API key not found in {filepath}: ' + repr(e))
                except AssertionError as e:
                    raise ApiKeyError('Config file found, but API key has not been set. Please change the API key in '+ str(filepath)) from e
                    logging.exception()
            else:
                raise FileNotFoundError('prevedere_api.ini config file not found in directory: ' + str(filepath.parent))
                logging.exception()
        
        if base:
            self.base = base
            logging.debug(f'Using "{self.base}" instead of "api."')
        else:
            self.base = 'api'
        
        try:
            self.api_key = str(UUID(api_key))
            self.context = self.fetch('/context')
        except (TypeError, ValueError, requests.exceptions.HTTPError) as e:
            raise ApiKeyError(f"'{api_key}' is not a valid API Key. " +\
            "Please check the config file or string that was passed to the constructor and try again.") from e
            logging.exception()
    
    @property
    def url(self):
        return f'https://{self.base}.prevedere.com'

    def fetch(self, path: str, payload: dict = None, method: str = 'GET', data: str = None) -> dict:
        if payload is None:
            payload = {}
        payload['ApiKey'] = self.api_key

        try:
            if method=='GET':
                r = requests.get(f'{self.url}{path}', params=payload)
            elif method=='POST':
                r = requests.post(f'{self.url}{path}', params=payload, data=data)
            r.raise_for_status()

            if self.log:
                try:
                    endpoint = re.search('^\/\w*\/?', path)[0]
                except:
                    endpoint = 'endpoint'
                else:
                    logging.info(f'{method} request to {endpoint} took {r.elapsed.total_seconds():.2f} seconds (status code: {r.status_code})')
            return r.json()

        except requests.exceptions.HTTPError as e:
            logging.exception(r.text)
        except requests.exceptions.ConnectionError as e:
            logging.exception('Connection Error')
        except requests.exceptions.Timeout as e:
            logging.exception('Timeout Error')
        except requests.exceptions.RequestException as e:
            logging.exception('Requests Error')              
        except json.decoder.JSONDecodeError as e:
            logging.exception("Could not read response as JSON")

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

    # POST
    def get_integrations(self):
        return self.fetch('/clientdimensions')
    
    def get_client_dimensions(self, client_dimension_group_id):
        integrations = self.get_integrations()
        for i in integrations:
            if i['Id'] == client_dimension_group_id:
                return i
        raise Exception(f'ClientDimensionGroupId not found: {client_dimension_group_id}')
    
    def get_fields(self, client_dimension_group_id):
        dimensions = self.get_client_dimensions(client_dimension_group_id)
        fields = list(dimensions['Mapping'].values()) + ['Measure', 'Date', 'Value']
        return set(fields)

    @staticmethod
    def make_csv(data: list, fields: set) -> str:
        """
        Turns data into a CSV string to be uploaded.
        Data must contain the **specific dimensions** for the integration job,
        as well as the fields, "Measure", "Date", and "Value".
        Date is in format 'YYYY-MM-DD'
        :param data: A list of records with {'key':'value'} entries.
            e.g. [
                {
                    'Region':'East', 
                    'Product':'Product 1', 
                    'Date': '2019-09-01', 
                    'Measure':'Sales', 
                    'Value':100
                    },
                {
                    'Region':'East', 
                    'Product':'Product 1', 
                    'Date': '2019-10-01', 
                    'Measure':'Sales', 
                    'Value':200
                    },
            ]
        :type fields: A list or set of keys in each record.
            e.g. set(['Region', 'Product', 'Date', 'Measure', 'Value'])
        
        returns: CSV string

        example: Api.make_csv(data=[], fields=[])
        """
        s = io.StringIO(newline='')
        writer = csv.DictWriter(s, fieldnames=fields)
        writer.writeheader()
        for d in data:
            writer.writerow(d)
        return s.getvalue()

    @staticmethod
    def get_csv_fields(csv_data):
        reader = csv.DictReader(io.StringIO(csv_data))
        return set(reader.fieldnames)

    @staticmethod
    def check_post_response(response):
        if response['Success'] == True:
            logging.info('POST suceeded.')
        else:
            raise requests.exceptions.RequestException(f"""
        POST Failed: 
        {response['Message']}
        """
        )

    def validate_data(
        self,
        data: str,
        client_dimension_group_id: str,
    ):
        # Make sure fields match up
        app_fields = self.get_fields(client_dimension_group_id)
        csv_fields = self.get_csv_fields(data)
        assert app_fields == csv_fields, f"""
        Fields do not match.
        App Fields: {app_fields}
        CSV Fields: {csv_fields}
        """

        response = self.fetch(
            method='POST',
            path=f'/validateclientdata/{client_dimension_group_id}',
            data={'InlineData': data}
        )

        self.check_post_response(response)

    def upload_data(
        self,
        data: str,
        client_dimension_group_id: str,
        should_delete_existing_records: bool = True,
        should_replace_if_record_exists: bool = True
    ):
        payload={
            # If false, becomes additive to existing records
            'ShouldReplaceRecordIfExists': should_replace_if_record_exists,
            }

        response = self.fetch(
            method='POST',
            path=f'/importclientdata/{client_dimension_group_id}/{should_delete_existing_records}',
            data={'InlineData':data},
            payload=payload
            )
        
        self.check_post_response(response)


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
