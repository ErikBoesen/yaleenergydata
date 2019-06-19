import yaleenergydata
import os

api = yaleenergydata.YaleEnergyData(os.environ['YALE_API_TOKEN'])

print(api.get('data', params={
    'buildingID': '3600',
    'rangeStart': '2015-07-01',
    'rangeEnd': '2015-08-01',
}))
