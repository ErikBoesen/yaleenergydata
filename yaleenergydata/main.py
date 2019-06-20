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
        self.reports = []
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
        print(raw['globalUse'])
        self.global_use = float(raw['globalUse'])
        self.global_square_foot_use = float(raw['globalSqftUse'])
        self.row_id = int(raw['rowid'])


class YaleEnergyData:
    API_TARGET = 'https://gw.its.yale.edu/soa-gateway/energy/data'

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get(self, params: dict = {}):
        """
        Make a GET request to the API.

        :param params: dictionary of custom params to add to request.
        """
        params['apikey'] = self.api_key
        print(params)
        request = requests.get(self.API_TARGET, params=params)
        if request.ok:
            return request.json()['ServiceResponse']
        else:
            # TODO: Can we be more helpful?
            raise Exception('API request failed.')

    def dateify(self, date) -> datetime.date:
        """
        Convert any supported input format into a datetime.date.
        """
        if type(date) == datetime.date:
            return date
        elif type(date) == datetime.datetime:
            return date.date()
        elif type(date) == tuple:
            year, month = date
        elif type(date) == str:
            year, month = date.split('-')[:2]
            year = int(year)
            month = int(month)
        return datetime.date(year=year, month=month, day=1)

    def stringify_date(self, date: datetime.date) -> str:
        """
        Convert a datetime object to a string in the approved format if necessary.
        """
        return date.strftime('%Y-%m-%d')

    def building(self, building_id: str, start_date, end_date=None) -> Building:
        """
        Generate a request to the API and fetch data within a given date range.

        :param building_id: ID of building to get data on. You may wish to use Yale's Building API to find an ID.
        :param start_date: date to start sampling from. Can be a string or datetime/date object, or year/month tuple.
        :param end_date: date to end sampling at. Formatting is the same as start_date. If not specified, today.
        """
        start_date = self.dateify(start_date)
        if end_date is None:
            end_date = start_date + datetime.timedelta(1 * 365 / 12)
        end_date = self.dateify(end_date)
        raw = self.get({
            'buildingID': building_id,
            'rangeStart': self.stringify_date(start_date),
            'rangeEnd': self.stringify_date(end_date),
        })
        from pprint import pprint
        if not raw:
            return None
        commodities = {}
        building = Building(raw[0])
        for entry in raw:
            if entry['commodityInfo'] not in commodities:
                commodities[entry['commodityInfo']] = Commodity(entry)
            commodities[entry['commodityInfo']].reports.append(Report(entry))
        for commodity in commodities:
            setattr(building, commodity, commodities[commodity])
        return building
