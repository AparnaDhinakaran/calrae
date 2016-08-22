from pymongo import MongoClient
import numpy as np
import matplotlib
# # Force matplotlib to not use any Xwindows backend.
# matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import datetime
from bson import json_util
import json, ast
from geopy.distance import vincenty
from datetime import tzinfo, timedelta, datetime
from pytz import timezone
import pytz
from dateutil.rrule import rrule, DAILY
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
from numpy import arange
import matplotlib.dates as mdates
from decimal import Decimal
import dateutil.parser
import copy



client = MongoClient()
db = client['stellar-monitor']
customers = db.customer1


# Relationship between user number and sensor  # {kitoba1: 12-1, kitobo3: 12-3}
def user_info():
  user_to_sensor = {}
  user_location = {}
  users_cursor = customers.find()
  for record in users_cursor:
    user_location[record['internal_id'].encode('ascii')] = (record['Latitude'], record['Longitude'])
    user_to_sensor[record['internal_id'].encode('ascii')] = record['monitoring_device_id'].encode('ascii')
  ast.literal_eval(json.dumps(user_to_sensor))
  return user_to_sensor, user_location

#user_to_sensor_id, user_location = user_info()
user_to_sensor_id = {'KIT1-0018': 'ubqkit1-21-3', 'KIT1-0019': 'ubqkit1-21-5', 'KIT1-0014': 'ubqkit1-11-3', 'KIT1-0015': 'ubqkit1-11-1', 'KIT1-0016': 'ubqkit1-20-4', 'KIT1-0017': 'ubqkit1-10-1', 'KIT1-0010': 'ubqkit1-20-2', 'KIT1-0011': 'ubqkit1-12-2', 'KIT1-0012': 'ubqkit1-10-2', 'KIT1-0013': 'ubqkit1-20-5', 'KIT1-0034': 'ubqkit1-24-2', 'KIT1-0032': 'ubqkit1-23-6', 'KIT1-0033': 'ubqkit1-24-1', 'KIT1-0030': 'ubqkit1-23-4', 'KIT1-0031': 'ubqkit1-23-5', 'KIT1-0009': 'ubqkit1-11-2', 'KIT1-0008': 'ubqkit1-20-3', 'KIT1-0003': 'ubqkit1-21-4', 'KIT1-0002': 'ubqkit1-21-2', 'KIT1-0001': 'ubqkit1-21-1', 'KIT1-0007': 'ubqkit1-10-3', 'KIT1-0006': 'ubqkit1-12-1', 'KIT1-0005': 'ubqkit1-20-1', 'KIT1-0004': 'ubqkit1-12-3', 'KIT1-0025': 'ubqkit1-22-4', 'KIT1-0024': 'ubqkit1-22-3', 'KIT1-0027': 'ubqkit1-23-1', 'KIT1-0026': 'ubqkit1-22-5', 'KIT1-0021': 'ubqkit1-13-2', 'KIT1-0020': 'ubqkit1-13-1', 'KIT1-0023': 'ubqkit1-22-2', 'KIT1-0022': 'ubqkit1-22-1', 'KIT1-0029': 'ubqkit1-23-3', 'KIT1-0028': 'ubqkit1-23-2'}
user_location = {'KIT1-0018': (-0.26262, 32.43005), 'KIT1-0019': (-0.2627, 32.43018), 'KIT1-0014': (-0.26263, 32.43001), 'KIT1-0015': (-0.2626, 32.42948), 'KIT1-0016': (-0.26254, 32.42985), 'KIT1-0017': (-0.26253, 32.4298), 'KIT1-0010': (-0.26251, 32.4297), 'KIT1-0011': (-0.26258, 32.42978), 'KIT1-0012': (-0.2625, 32.42967), 'KIT1-0013': (-0.26253, 32.42978), 'KIT1-0034': (-0.2622, 32.4291), 'KIT1-0032': (-0.26213, 32.430046), 'KIT1-0033': (-0.26228, 32.4299), 'KIT1-0030': (-0.26207, 32.43008), 'KIT1-0031': (-0.26216, 32.43), 'KIT1-0009': (-0.2626, 32.42988), 'KIT1-0008': (-0.26255, 32.42969), 'KIT1-0003': (-0.26253, 32.4299), 'KIT1-0002': (-0.26262, 32.42999), 'KIT1-0001': (-0.26261, 32.4296), 'KIT1-0007': (-0.2625, 32.42962), 'KIT1-0006': (-0.26256, 32.42972), 'KIT1-0005': (-0.26255, 32.4298), 'KIT1-0004': (-0.26259, 32.42984), 'KIT1-0025': (-0.26247, 32.43019), 'KIT1-0024': (-0.26238, 32.43025), 'KIT1-0027': (-0.2622, 32.43001), 'KIT1-0026': (-0.26255, 32.43018), 'KIT1-0021': (-0.26238, 32.43001), 'KIT1-0020': (-0.26243, 32.43001), 'KIT1-0023': (-0.26209, 32.4303), 'KIT1-0022': (-0.26225, 32.43022), 'KIT1-0029': (-0.26224, 32.4299), 'KIT1-0028': (-0.2621, 32.43001)}
user_location_by_port1_20 = {'KIT1-0016': (-0.26254, 32.42985),'KIT1-0010': (-0.26251, 32.4297),'KIT1-0013': (-0.26253, 32.42978),'KIT1-0008': (-0.26255, 32.42969),'KIT1-0005': (-0.26255, 32.4298)}
# print(user_location)
#print(user_to_sensor_id)

good_users = {'KIT1-0016': 'ubqkit1-20-4', 'KIT1-0017': 'ubqkit1-10-1', 'KIT1-0010': 'ubqkit1-20-2', 'KIT1-0011': 'ubqkit1-12-2', 'KIT1-0014': 'ubqkit1-11-3', 'KIT1-0009': 'ubqkit1-11-2', 'KIT1-0008': 'ubqkit1-20-3', 'KIT1-0012': 'ubqkit1-10-2', 'KIT1-0015': 'ubqkit1-11-1', 'KIT1-0003': 'ubqkit1-21-4', 'KIT1-0002': 'ubqkit1-21-2', 'KIT1-0001': 'ubqkit1-21-1', 'KIT1-0013': 'ubqkit1-20-5', 'KIT1-0007': 'ubqkit1-10-3', 'KIT1-0006': 'ubqkit1-12-1', 'KIT1-0005': 'ubqkit1-20-1', 'KIT1-0004': 'ubqkit1-12-3'}
# for i in range (01, 18):
#   good_users['KIT1-00' + '%02d' %(i,)] = user_to_sensor_id['KIT1-00' + '%02d' %(i,)]


# Voltage TimeSeries for each user
def power_timeseries():
  user_power_data = {}
  d1 = datetime(2015, 10, 25, 0, 0, 0)
  d2 = datetime(2015, 10, 31, 0, 0, 0)
  timeseries_cursor = db.sensorgeneric.find( { "utctime":{ "$gte": d1,
    "$lte": d2}, "tag": "active_pwr" })
  
  for user in good_users.keys():
    timeseries_cursor2 = copy.deepcopy(timeseries_cursor)
    user_power_data[user] = []
    user_power_value = []
    # user_power_std = []
    user_power_time = []
    internal_id = good_users[user]    
    print "internal_id: "+internal_id
    
    # timeseries_cursor = db.sensorgeneric.find( { "utctime":{ "$gte": d1,
    # "$lte": d2}, "tag": "active_pwr", "sensor": internal_id  })

    for record in timeseries_cursor2:
      print "record_sensor: "+record['sensor']
      print record['sensor'] == internal_id
      if record['sensor'] == internal_id:
        time  = record['utctime']
        value = record['value']
        # std = record['std']
        user_power_value.append(value)
        # user_voltage_std.append(std)
        user_power_time.append(time)

    user_power_data[user] = [user_power_value, user_power_time]

  return user_power_data

# min_power_data = power_timeseries()

# print min_power_data['KIT1-0005']

# # Writing exported data into a json file
# with open('min_power_data_2015_10_31.json', 'w') as f :
#     json.dump(min_power_data, f, default=json_util.default)

# Importing the json file
with open('min_power_data_2015_10_31.json') as f:
  min_power_data = json.load(f)

# print min_power_data

specific_user = 'KIT1-0016'
def parse_time():
  min_power_time2 = []
  for i in range(0, len(min_power_data[specific_user][1])):
    utc = pytz.utc
    utc_dt = datetime.utcfromtimestamp(min_power_data[specific_user][1][i]['$date']/1000).replace(tzinfo=utc)
    kam_time = timezone('Africa/Kampala')
    time2 = kam_time.normalize(utc_dt.astimezone(kam_time))
    min_power_time2.append(time2)
  min_power_data[specific_user][1] = min_power_time2

  return min_power_data

parse_time()

# print min_power_data['KIT1-0005'][1]

plt.plot(min_power_data[specific_user][1], min_power_data[specific_user][0])
# plt.ylim(-10, 2000)
plt.title(specific_user)  
plt.show()


