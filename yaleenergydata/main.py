import requests
import date


class Building:
    def __init__(self, raw):



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
            raise Exception('API request failed.')

    def stringify_date(self, date) -> str:
        """
        Convert a datetime object to a string in the approved format if necessary.
        """
        if type(date) in (datetime.datetime, datetime.date):
            date = date.strftime('%Y-%m-%d')
        return date

    def fetch(self, building_id: str, start_date, end_date=None):
        """
        Build a request to the API and fetch data within a given date range.

        :param building_id: ID of building to get data on. You may wish to use Yale's Building API to find an ID.
        :param start_date: date to start sampling from. Can be a string or datetime/date object.
        :param end_date: date to end sampling at. Formatting is the same as start_date. If not specified, today.
        """
        start_date = stringify_date(start_date)
        end_date = stringify_date(end_date || datetime.date.today())
        raw = self.get({
            'buildingID': building_id,
            'rangeStart': start_date,
            'rangeEnd': end_date,
        })
        days = {}
        for raw_item in raw:
            date = raw_item['MENUDATE']
            meal_code = raw_item['MEALCODE']
            item = Item(raw_item, self)
            if days.get(date) is None:
                days[date] = {}
            if days[date].get(meal_code) is None:
                days[date][meal_code] = Meal(raw_item, self)
            days[date][meal_code].items.append(item)
        meals = []
        for day in days:
            for meal in days[day]:
                meals.append(days[day][meal])
        return meals
