import requests
from datetime import datetime


class ConnectionError(Exception):
    """Raised when an error occurs in connecting to the API."""
    pass


class YaleEnergyData:
    API_TARGET = 'https://gw.its.yale.edu/soa-gateway/energy/data'

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get(self, params: dict = {}):
        """
        Make a GET request to the API.

        :param endpoint: path to resource desired.
        :param params: dictionary of custom params to add to request.
        """
        params['apikey'] = self.api_key
        request = requests.get(self.API_TARGET, params=params)
        if request.ok:
            return request.json()
        else:
            # TODO: Can we be more helpful?
            raise ConnectionError('API request failed.')

    def fetch(self, building_id: str, start_date, end_date):
        """
        Build a request to the API and fetch data within a given date range.

        :param building_id: ID of building to get data on. You may wish to use Yale's Building API to find an ID.
        :param start_date: date to start sampling from. Can be a string or datetime object.
        :param end_date: date to end sampling at. Formatting is the same as start_date.
        """
        self.get(
