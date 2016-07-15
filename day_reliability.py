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
from datetime import date
from dateutil.rrule import rrule, DAILY
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
from numpy import arange
import matplotlib.dates as mdates
from decimal import Decimal
import day_reliability_data as data


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

# connec TimeSeries for each user
def connec_timeseries():

  user_connec_data = {}

  for user in user_to_sensor_id.keys():

    user_connec_data[user] = []
    user_connec_value = []
    # user_connec_std = []
    user_connec_time = []
    internal_id = user_to_sensor_id[user]

    d1 = datetime.datetime(2015, 7, 9, 0, 0)
    d2 = datetime.datetime(2016, 6, 30, 0, 0)

    timeseries_cursor = db.day.find( { "utctime":{ "$gte": d1,
      "$lte": d2}, "sensor": internal_id,
      "tag": "output" })

    for record in timeseries_cursor:
      time  = record['utctime']
      mean = record['mean']
      # std = record['std']
      user_connec_value.append(mean)
      # user_connec_std.append(std)
      user_connec_time.append(time)

    user_connec_data[user] = [user_connec_value, user_connec_time]

  return user_connec_data

# print data.connec

# print user_connec_data

# Plotting Data
def plot_connec_timeseries(rows,cols):

  users = list(data.connec.keys())
  user_counter = 0


  def plot(ax, user, user_id):
    datetimes = data.connec[user][1]
    value = data.connec[user][0]
    dates = matplotlib.dates.date2num(datetimes)
    ax.plot(dates, value)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=15))
    plt.xticks(rotation=30)
    ax.set_xlabel('DateTime', fontsize=8)
    ax.set_ylabel('connec', fontsize=8)
    ax.set_title('User ID ' + str(user_id), fontsize=8)
    ax.set_ylim([-1,1]) 

  fig, axes = plt.subplots(nrows=rows, ncols=cols)
  plt.title('connec Timeseries')
  for row in axes:
      for ax in row:
          user = users[user_counter]
          user_id = int(user[-2:])
          while user_id > rows*cols:
            user_counter +=1
            user = users[user_counter]
            user_id = int(user[-2:])
          plot(ax, user, user_id)
          user_counter +=1
          print user
          # print user[-3:]
  plt.tight_layout()
  plt.gcf().autofmt_xdate()
  plt.show()

print data.connec['KIT1-0003'][1]

# plot_connec_timeseries(2,2)
def plot_individual():
    fig, ax = plt.subplots()
    ax.plot_date(data.connec['KIT1-0003'][1], data.connec['KIT1-0003'][0], fmt='b-') # x = array of dates, y = array of numbers        

    fig.autofmt_xdate()

    # For tickmarks and ticklabels every week
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=15))

    # For tickmarks and ticklabels every other week
    #ax.xaxis.set_major_locator(WeekdayLocator(byweekday=MO, interval=2))

    plt.grid(True)
    plt.show()

plot_individual()

# plt.plot(data.connec['KIT1-0001'][1], data.connec['KIT1-0001'][0])
# # plt.axis([0, 6, 0, 20])
# plt.gcf().autofmt_xdate()
# plt.show()
