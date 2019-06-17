import requests


class ConnectionError(Exception):
    """Raised when an error occurs in connecting to the API."""
    pass


class YaleEnergyData:
    API_ROOT = 'https://gw.its.yale.edu/soa-gateway/energy/'

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get(self, endpoint: str, params: dict = {}):
        """
        Make a GET request to the API.

        :param endpoint: path to resource desired.
        :param params: dictionary of custom params to add to request.
        """
        request = requests.get(self.API_ROOT + endpoint)
        if request.ok:
            return request.json()
        else:
            # TODO: Can we be more helpful?
            raise ConnectionError('API request failed.')
