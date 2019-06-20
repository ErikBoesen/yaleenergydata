import requests
import datetime


class _base:
    def __init__(self, raw):
        self.raw = raw


class Building(_base):
    def __init__(self, raw):
        super().__init__(raw)
        self.campus = raw['campus']
        self.utility_area = raw['utilityArea']
        self.id = raw['facid']
        self.name = raw['buildingName']
        self.square_footage = raw['SQR_FEET']


class Commodity(_base):
    def __init__(self, raw):
        super().__init__(raw)
        self.name = raw['commodityInfo']
        self.native_use_unit = raw['nativeUseUnit']
        self.common_use_unit = raw['commonUseUnit']
        self.global_use_unit = raw['globalUseUnit']
        self.global_square_foot_use_unit = raw['globalSqftUseUnit']


class Report(_base):
    def parse_date(self, raw: str):
        year, month = raw.strip('-01 00:00:00.0').split('-')
        return int(year), int(month)

    def __init__(self, raw):
        super().__init__(raw)
        self.year, self.month = self.parse_date(raw['usageMonth'])
        self.native_use = float(raw['nativeUse'])
        self.common_use = float(raw['commonUse'])
        self.global_use = float(raw['globalUse'])
        self.global_square_foot_use = float(raw['globalSqftUse'])


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

    def building(self, building_id: str, start_date, end_date=None) -> Building:
        """
        Generate a request to the API and fetch data within a given date range.

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
        if not raw:
            return None
        commodities = {}
        building = Building(raw[0])
        """
        for entry in raw:
            report = Report(entry)
            if commodities.get() is None:
                days[date] = {}
            days[date][meal_code].items.append(item)
        meals = []
        for day in days:
            for meal in days[day]:
                meals.append(days[day][meal])
        """
        return building
