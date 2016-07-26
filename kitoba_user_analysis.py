from pymongo import MongoClient
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import datetime
import json, ast
from geopy.distance import vincenty
from datetime import date
from dateutil.rrule import rrule, DAILY
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
from numpy import arange
import matplotlib.dates as mdates
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from scipy.cluster.vq import kmeans2
from scipy.cluster.vq import kmeans
from scipy.cluster.vq import kmeans,vq, whiten
import matplotlib.patches as mpatches
from sklearn.manifold import TSNE
from matplotlib import colors
from sklearn.decomposition import PCA


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

# user_to_sensor_id, user_location = user_info()
user_to_sensor_id = {'KIT1-0018': 'ubqkit1-21-3', 'KIT1-0019': 'ubqkit1-21-5', 'KIT1-0014': 'ubqkit1-11-3', 'KIT1-0015': 'ubqkit1-11-1', 'KIT1-0016': 'ubqkit1-20-4', 'KIT1-0017': 'ubqkit1-10-1', 'KIT1-0010': 'ubqkit1-20-2', 'KIT1-0011': 'ubqkit1-12-2', 'KIT1-0012': 'ubqkit1-10-2', 'KIT1-0013': 'ubqkit1-20-5', 'KIT1-0034': 'ubqkit1-24-2', 'KIT1-0032': 'ubqkit1-23-6', 'KIT1-0033': 'ubqkit1-24-1', 'KIT1-0030': 'ubqkit1-23-4', 'KIT1-0031': 'ubqkit1-23-5', 'KIT1-0009': 'ubqkit1-11-2', 'KIT1-0008': 'ubqkit1-20-3', 'KIT1-0003': 'ubqkit1-21-4', 'KIT1-0002': 'ubqkit1-21-2', 'KIT1-0001': 'ubqkit1-21-1', 'KIT1-0007': 'ubqkit1-10-3', 'KIT1-0006': 'ubqkit1-12-1', 'KIT1-0005': 'ubqkit1-20-1', 'KIT1-0004': 'ubqkit1-12-3', 'KIT1-0025': 'ubqkit1-22-4', 'KIT1-0024': 'ubqkit1-22-3', 'KIT1-0027': 'ubqkit1-23-1', 'KIT1-0026': 'ubqkit1-22-5', 'KIT1-0021': 'ubqkit1-13-2', 'KIT1-0020': 'ubqkit1-13-1', 'KIT1-0023': 'ubqkit1-22-2', 'KIT1-0022': 'ubqkit1-22-1', 'KIT1-0029': 'ubqkit1-23-3', 'KIT1-0028': 'ubqkit1-23-2'}
user_location = {'KIT1-0018': (-0.26262, 32.43005), 'KIT1-0019': (-0.2627, 32.43018), 'KIT1-0014': (-0.26263, 32.43001), 'KIT1-0015': (-0.2626, 32.42948), 'KIT1-0016': (-0.26254, 32.42985), 'KIT1-0017': (-0.26253, 32.4298), 'KIT1-0010': (-0.26251, 32.4297), 'KIT1-0011': (-0.26258, 32.42978), 'KIT1-0012': (-0.2625, 32.42967), 'KIT1-0013': (-0.26253, 32.42978), 'KIT1-0034': (-0.2622, 32.4291), 'KIT1-0032': (-0.26213, 32.43005), 'KIT1-0033': (-0.26228, 32.4299), 'KIT1-0030': (-0.26207, 32.43008), 'KIT1-0031': (-0.26216, 32.43), 'KIT1-0009': (-0.2626, 32.42988), 'KIT1-0008': (-0.26255, 32.43969), 'KIT1-0003': (-0.26253, 32.4299), 'KIT1-0002': (-0.26262, 32.42999), 'KIT1-0001': (-0.26261, 32.4296), 'KIT1-0007': (-0.2625, 32.42962), 'KIT1-0006': (-0.26256, 32.42972), 'KIT1-0005': (-0.26255, 32.4298), 'KIT1-0004': (-0.26259, 32.42984), 'KIT1-0025': (-0.26247, 32.43019), 'KIT1-0024': (-0.26238, 32.43025), 'KIT1-0027': (-0.2622, 32.43001), 'KIT1-0026': (-0.26255, 32.43018), 'KIT1-0021': (-0.26238, 32.43001), 'KIT1-0020': (-0.26243, 32.43001), 'KIT1-0023': (-0.26209, 32.4303), 'KIT1-0022': (-0.26225, 32.43022), 'KIT1-0029': (-0.26224, 32.4299), 'KIT1-0028': (-0.2621, 32.43001)}

# Voltage TimeSeries for each user
def voltage_timeseries(d1 = datetime.datetime(2015, 8, 1, 0, 0), d2 = datetime.datetime(2015, 10, 31, 0, 0)):

  user_data = {}
  for user in user_to_sensor_id.keys():
    user_data[user] = [[], [], [], [], [], [], [], [], []]
    internal_id = user_to_sensor_id[user]

    voltage_cursor = db.day.find( { "utctime":{ "$gte": d1,
      "$lte": d2}, "sensor": internal_id,
      "tag": "v_rms" })

    current_cursor = db.day.find( { "utctime":{ "$gte": d1,
      "$lte": d2}, "sensor": internal_id,
      "tag": "i_rms" })

    pf_cursor = db.day.find( { "utctime":{ "$gte": d1,
      "$lte": d2}, "sensor": internal_id,
      "tag": "pf" })

    cursors = {'voltage': (voltage_cursor, 0, 1, 2), 'current': (current_cursor, 3, 4, 5), 'power': (pf_cursor, 6, 7, 8)}

    for cursor_key in cursors.keys():
      cursor_value = cursors[cursor_key]
      cursor = cursor_value[0]
      time_idx = cursor_value[1]
      mean_idx = cursor_value[2]
      std_idx = cursor_value[3]
      for record in cursor:
        time  = record['utctime']
        mean = record['mean']
        std = record['std']
        time_list = user_data[user][time_idx]
        mean_list = user_data[user][mean_idx]
        std_list = user_data[user][std_idx]
        mean_list.append(mean)
        time_list.append(time)
        std_list.append(std)

  return user_data

user_data = voltage_timeseries()
print("USER DATA\n", user_data)

# Plotting Data
def plot_voltage_timeseries(rows,cols):

  users = list(user_data.keys())

  def plot(ax, user_id, datetimes, mean, title):
    dates = matplotlib.dates.date2num(datetimes)
    ax.plot(dates, mean)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=15))
    plt.xticks(rotation=30)
    ax.set_xlabel('DateTime', fontsize=8)
    ax.set_ylabel(title, fontsize=8)
    ax.set_title('User ID ' + str(user_id), fontsize=8)

  plot_types = {'voltage': ('Voltage Timeseries', 'Voltage', 0, 1, 2),
  'current': ('Current Timeseries', 'Current', 3, 4, 5), 'power': ("Power Timeseries", 'Power', 6, 7, 8)}

  for plot_key in plot_types.keys():
    print(plot_key)
    fig, axes = plt.subplots(nrows=rows, ncols=cols)
    plot_params = plot_types[plot_key]
    plt.title(plot_params[0])
    user_counter = 0
    for row in axes:
        for ax in row:
            user = users[user_counter]
            user_id = int(user[-2:])
            while user_id > rows*cols:
              user_counter+=1
              user = users[user_counter]
              user_id = int(user[-2:])
            datetimes = user_data[user][plot_params[2]]
            mean = user_data[user][plot_params[3]]
            plot(ax, user_id, datetimes, mean, plot_params[1])
            user_counter +=1
    plt.tight_layout()
    plt.gcf().autofmt_xdate()
    plt.show()

plot_voltage_timeseries(4,4)

def distance_voltage():
  shedLat = -0.262729177
  shedLon = 32.42977985
  shed_location = (shedLat, shedLon)
  distance = []
  badusers = []
  avg_voltage = []
  users = list(user_data.keys())
  for user in users:
      user_loc = user_location[user]
      user_distance = vincenty(shed_location, user_loc).meters
      voltages = user_data[user][1]
      if user_distance < 500 and len(voltages) > 1 :
        mean = np.mean(voltages)
        avg_voltage.append(mean)
        distance.append(user_distance)
      else:
        badusers.append(user)
  print("Bad Users", badusers)

    # make the scatter plot
  plt.scatter(distance, avg_voltage, marker='o')

  # determine best fit line
  par = np.polyfit(distance, avg_voltage, 1, full=True)

  slope=par[0][0]
  intercept=par[0][1]
  xl = [min(distance), max(distance)]
  yl = [slope*xx + intercept for xx in xl]

  # coefficient of determination, plot text
  variance = np.var(avg_voltage)
  residuals = np.var([(slope*xx + intercept - yy)  for xx,yy in zip(distance,avg_voltage)])
  Rsqr = np.round(1-residuals/variance, decimals=2)
  plt.text(.9*max(distance)+.1*min(distance),.9*max(avg_voltage)+.1*min(avg_voltage),'$R^2 = %0.2f$'% Rsqr, fontsize=15)

  plt.xlabel("Distance")
  plt.ylabel("Voltage")

  # error bounds
  yerr = [abs(slope*xx + intercept - yy)  for xx,yy in zip(distance,avg_voltage)]
  par = np.polyfit(distance, yerr, 2, full=True)

  yerrUpper = [(xx*slope+intercept)+(par[0][0]*xx**2 + par[0][1]*xx + par[0][2]) for xx,yy in zip(distance,avg_voltage)]
  yerrLower = [(xx*slope+intercept)-(par[0][0]*xx**2 + par[0][1]*xx + par[0][2]) for xx,yy in zip(distance,avg_voltage)]

  plt.plot(xl, yl, 'b')
  plt.plot(distance, yerrLower, '--r')
  plt.plot(distance, yerrUpper, '--g')
  plt.title("Distance Voltage Relationship")

  blue_patch = mpatches.Patch(color='Blue', label='Line of Best Fit')
  red_patch = mpatches.Patch(color='Red', label='Distance and Voltage Error (Lower)')
  green_patch = mpatches.Patch(color='Green', label='Distance and Voltage Error (Upper)')
  plt.legend(handles=[red_patch, blue_patch, green_patch])
  plt.show()

distance_voltage()


def cluster_setup():
  shedLat = -0.262729177
  shedLon = 32.42977985
  X = [] # 16 users * 22 features
  user_cluster = {}
  users_cursor = customers.find()
  for user in user_data.keys():
      avg_voltage = np.mean(user_data[user][1])
      avg_current = np.mean(user_data[user][4])
      avg_power = np.mean(user_data[user][7])
      user_cluster[user] = [user, avg_voltage, avg_current, avg_power]
  for user in user_location.keys():
      user_loc = user_location[user]
      user_distance = vincenty(shed_location, user_loc).meters
      user_cluster[user].append(user_distance)
  business_types = set()
  business_count = 0
  business_type_mapping = {}
  device_types = set()
  user_device_mapping = {}
  for record in users_cursor:
    user = record['internal_id'].encode('ascii')
    business = record['business_type'].encode('ascii')]
    if business not in business_types:
      business_types.add(business)
      business_type_mapping[business] = business_count
      business_count += 1
    user_cluster[record['internal_id']].append(business_type_mapping[business])
    user_cluster[record['internal_id'].append(record['Total Revenue (Month)'])
    user_cluster[record['internal_id'].append(record['Pays Now (Day)'])
    device_group = record['business_type'].encode('ascii')].split(',')
    for elem in device_group:
      quantity, device = device_group.split(" ")
      if device not in device_types:
        device_types.add(device)
      if user not in user_device_mapping.keys()
        user_device_mapping[user] = {}
      user_device_mapping[user][device] = quantity
  device_type_list = list(device_types)
  for device_type in device_type_list:
    for user in user_device_mapping.keys():
      user_cluster[user].append(user_device_mapping[user][device_type])
  for user in user_cluster.keys():
    X.append(user_cluster[user])
  return np.array(X)

  #X = [user_num, average_daily_voltage, average_daily_current, average_daily_power, distance, business_type, revenue, pays_now, num_lights, num_V, num_computer, num_fans, num_speakers, num_signs, num_bar, num_game machine]
  return X

X = cluster_setup()
print("X", X)

def cluster_users(X):

TRIMMED_X = X[:, 1 : len(X[0]) - 1]

"""
Reduction Mode: 0 - TSNE, 1 - PCA
"""

REDUCTION_MODE = 1

if REDUCTION_MODE == 0 :
  model = TSNE(n_components=2, random_state=0)
  np.set_printoptions(suppress=True)
  reduced_X = model.fit_transform(TRIMMED_X)
else:
  pca = PCA(n_components=2)
  reduced_X = pca.fit_transform(X)

x = []
y = []
for i in range(len(reduced_X)):
  x.append(reduced_X[i][0])
  y.append(reduced_X[i][1])

user_id = []
weighted_coeffients = []
for i in range(len(X)):
  user = X[i]
  user_id.append(user[0])
  coefficients = []
  for j in range(1,len(invertor)-1):
    coefficients.append(abs(invertor[j])/summation)
  weighted_coeffients.append(coefficients)


KMeansCoefficients = np.array(coefficients)
print(KMeansCoefficients.shape)

centroids, distance = kmeans(KMeansCoefficients, 2)
print ("Centroids for KMeansCoefficients", centroids)
labels, distance = vq(KMeansCoefficients,centroids)
colors = ['red','green','blue','purple']
color_list = []
for i in range(len(labels)):
  if labels[i]== 0:
    color_list.append('r')
  elif labels[i] == 1:
    color_list.append('g')
  elif labels[i] == 2:
    color_list.append('b')
  elif labels[i] == 3:
    color_list.append('purple')

fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(x, y,  c=color_list, label=user_id)

annotate_labels = ['{0}'.format(i) for i in user_id]
for annotate_label, x_point, y_point in zip(annotate_labels, x, y):
    ax.annotate(
        annotate_label,
        xy = (x_point, y_point), xytext = (-1, 1),
        textcoords = 'offset points', ha = 'right', va = 'bottom',
        bbox = dict(boxstyle = 'round,pad=0.8', fc = 'yellow', alpha = 0.05),
        )

patch1 = mpatches.Patch(color='red', label='Group 1')
patch2 = mpatches.Patch(color='green', label='Group 2')
patch3 = mpatches.Patch(color='blue', label='Group 3')
patch4 = mpatches.Patch(color='purple', label='Group 4')
ax.legend(handles=[patch1, patch2, patch3, patch4])

ax.set_title('Kitoba User Analysis')

plt.show()

