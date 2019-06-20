import yaleenergydata
import os

# "energy" name can be whatever is most convenient for your program
energy = yaleenergydata.YaleEnergyData(os.environ['YALE_API_TOKEN'])

# You can use datetime objects or YYYY-MM-DD or YYYY-MM strings
building = energy.building(3600, '2015-07-01')
building = energy.building(3600, datetime.date(year=2018), datetime.date(2019))
