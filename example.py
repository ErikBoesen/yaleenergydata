import yaleenergydata
import os
import datetime

# "energy" name can be whatever is most convenient for your program
energy = yaleenergydata.YaleEnergyData(os.environ['YALE_API_TOKEN'])

# You can use datetime objects or YYYY-MM-DD or YYYY-MM strings or tuples
building = energy.building(3600, '2015-07-01')
building = energy.building(3600, (2015, 7), (2019, 4))
