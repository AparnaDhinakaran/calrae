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
import dateutil.parser
from dateutil.rrule import rrule, DAILY
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
from numpy import arange
import matplotlib.dates as mdates
from decimal import Decimal

from pprint import pprint

import day_reliability_data as connec_data


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


user_freq_data = [[58.46523186569027, 51.77172636400796, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 49.99999999999998, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 49.999999999999986, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.000000000000036, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 49.99999999999992, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.00000000000019, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 49.99999999999998, 50.00000000000002, 49.99999999999996, 49.999999999999986, 49.999999999999986, 50.000000000001016, 50.0, 50.00000000000002, 50.00000000000006, 49.99999999999998, 50.0, 50.000000000000014, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.00000000000012, 50.0, 50.0, 50.0, 50.08523402175825, 50.88006227579531, 50.81327969724032, 51.003577746882904, 41.2528543720248, 50.0, 50.77463113915857, 50.7163701966688, 50.24924404321588, 51.53914222193856, 50.09926020265346, 50.90163892953766, 51.4113088295562, 51.625817823631074, 51.53733012719155, 50.65516798626685, 51.132934924475585, 51.72897458313954, 50.73243316720257, 52.59530313459883, 51.74653868892329, 52.458024677719806, 52.27336392606454, 51.312215355513175, 50.82327625434725, 51.33977058467228, 51.967434875525505, 51.35728900062546, 51.804272788990495, 51.02542246969841, 52.56304594516208, 53.033949811971155, 51.66773916987605, 51.06635874762758, 50.0, 50.0, 50.0, 51.07035657201041, 50.75393253988411, 51.638825950509684, 50.99550104679978, 51.87258263342473, 50.0, 51.32508117064301, 51.45625245765553, 53.44520683407292, 53.13095261671551, 52.29698179249721, 52.00025724276644, 52.78845661069035, 52.465941989472384, 51.41933413948429, 52.747101200060285, 51.68259843319984, 52.57825455529372, 52.178015404857106, 52.1311091573757, 'nan', 51.065471000708605, 50.56929555308772, 51.11780736675636, 51.44215003842321, 'nan', 'nan', 51.648672825762986, 51.21505794074063, 51.50828396449264, 52.315424036245346, 51.55431449080931, 51.169799804797634, 51.00502416141324, 50.558388089807856, 51.02025786245447, 52.2285126936326, 50.55526073952457, 51.43979212436434, 50.4681234575835, 78.89981084179708, 79.29345843706331, 50.0, 'nan', 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 49.345098209462066, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0], [2.5359544401883567, 1.5619852201506625, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.6953022033862593, 1.7287417909646912, 1.8550702598808744, 2.042607451786844, 2.4752025584920885, 0.0, 1.8288424077664969, 1.9514671488390691, 1.155149774775704, 2.3442817030619394, 0.7421461578339482, 2.0335637526446697, 2.337803336799764, 2.4359890316419346, 2.2518187250368493, 1.6830628551917879, 2.0751071889574666, 2.250637148223187, 1.7972907684920811, 2.4780060108407733, 2.5816338240870706, 2.799058931055085, 2.7420379359035896, 2.335919091342878, 1.9201714448861225, 2.3478542827782203, 2.600551491106779, 2.301777761472226, 2.4262614319835296, 2.092700400224989, 2.405277362275021, 2.5132293335416382, 2.2858636522098723, 2.1178832522698654, 0.0, 0.0, 0.0, 2.0994176994852296, 1.7314863948534447, 2.303038966805646, 1.9634806033938024, 2.3395878083805814, 0.0, 2.2208760860031638, 2.2934909309649085, 2.419155470889399, 2.3419936753283572, 2.406820353244887, 2.4322275975677705, 2.436216086977781, 2.118279125745264, 2.0741891382867226, 2.0468656110504777, 2.0069397929066373, 1.9986268613628893, 2.1807348749156703, 1.9150779463122312, 2.1997015958116157, 1.7663681601342731, 1.5996772919551203, 1.8073933338551682, 2.143529897848078, 2.2595258508243057, 2.074156074378467, 2.0385947759177863, 2.0210272669592326, 2.0692567813507092, 2.2363009406229115, 2.0436659765897556, 1.8787411033929404, 1.7773970568688906, 1.113935980787961, 1.7067259670090797, 2.4627372889662884, 2.3946536760376516, 2.125695961082481, 1.3740706313328057, 1.5711858867863215, 0.5474239756073104, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.0737741880052485, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], ['2015-07-09T00:00:00', '2015-07-10T00:00:00', '2015-07-11T00:00:00', '2015-07-12T00:00:00', '2015-07-13T00:00:00', '2015-07-14T00:00:00', '2015-07-15T00:00:00', '2015-07-16T00:00:00', '2015-07-17T00:00:00', '2015-07-18T00:00:00', '2015-07-19T00:00:00', '2015-07-20T00:00:00', '2015-07-21T00:00:00', '2015-07-22T00:00:00', '2015-07-23T00:00:00', '2015-07-24T00:00:00', '2015-07-25T00:00:00', '2015-07-26T00:00:00', '2015-07-27T00:00:00', '2015-07-28T00:00:00', '2015-07-29T00:00:00', '2015-07-30T00:00:00', '2015-07-31T00:00:00', '2015-08-01T00:00:00', '2015-08-02T00:00:00', '2015-08-03T00:00:00', '2015-08-04T00:00:00', '2015-08-05T00:00:00', '2015-08-06T00:00:00', '2015-08-07T00:00:00', '2015-08-08T00:00:00', '2015-08-09T00:00:00', '2015-08-10T00:00:00', '2015-08-11T00:00:00', '2015-08-12T00:00:00', '2015-08-13T00:00:00', '2015-08-14T00:00:00', '2015-08-15T00:00:00', '2015-08-16T00:00:00', '2015-08-17T00:00:00', '2015-08-18T00:00:00', '2015-08-19T00:00:00', '2015-08-20T00:00:00', '2015-08-21T00:00:00', '2015-08-22T00:00:00', '2015-08-23T00:00:00', '2015-08-24T00:00:00', '2015-08-25T00:00:00', '2015-08-26T00:00:00', '2015-08-27T00:00:00', '2015-08-28T00:00:00', '2015-08-29T00:00:00', '2015-08-30T00:00:00', '2015-08-31T00:00:00', '2015-09-01T00:00:00', '2015-09-02T00:00:00', '2015-09-03T00:00:00', '2015-09-04T00:00:00', '2015-09-05T00:00:00', '2015-09-06T00:00:00', '2015-09-07T00:00:00', '2015-09-08T00:00:00', '2015-09-09T00:00:00', '2015-09-10T00:00:00', '2015-09-11T00:00:00', '2015-09-12T00:00:00', '2015-09-13T00:00:00', '2015-09-14T00:00:00', '2015-09-15T00:00:00', '2015-09-16T00:00:00', '2015-09-17T00:00:00', '2015-09-18T00:00:00', '2015-09-19T00:00:00', '2015-09-20T00:00:00', '2015-09-21T00:00:00', '2015-09-22T00:00:00', '2015-09-23T00:00:00', '2015-09-24T00:00:00', '2015-09-25T00:00:00', '2015-09-26T00:00:00', '2015-09-27T00:00:00', '2015-09-28T00:00:00', '2015-09-29T00:00:00', '2015-09-30T00:00:00', '2015-10-01T00:00:00', '2015-10-02T00:00:00', '2015-10-03T00:00:00', '2015-10-04T00:00:00', '2015-10-05T00:00:00', '2015-10-06T00:00:00', '2015-10-07T00:00:00', '2015-10-08T00:00:00', '2015-10-09T00:00:00', '2015-10-10T00:00:00', '2015-10-11T00:00:00', '2015-10-12T00:00:00', '2015-10-13T00:00:00', '2015-10-14T00:00:00', '2015-10-15T00:00:00', '2015-10-16T00:00:00', '2015-10-17T00:00:00', '2015-10-18T00:00:00', '2015-10-19T00:00:00', '2015-10-20T00:00:00', '2015-10-21T00:00:00', '2015-10-22T00:00:00', '2015-10-23T00:00:00', '2015-10-24T00:00:00', '2015-10-25T00:00:00', '2015-10-26T00:00:00', '2015-10-27T00:00:00', '2015-10-28T00:00:00', '2015-10-29T00:00:00', '2015-10-30T00:00:00', '2015-10-31T00:00:00', '2015-11-01T00:00:00', '2015-11-02T00:00:00', '2015-11-03T00:00:00', '2015-11-04T00:00:00', '2015-11-05T00:00:00', '2015-11-06T00:00:00', '2015-11-07T00:00:00', '2015-11-08T00:00:00', '2015-11-10T00:00:00', '2015-11-11T00:00:00', '2015-11-12T00:00:00', '2015-11-13T00:00:00', '2015-11-14T00:00:00', '2015-11-15T00:00:00', '2015-11-16T00:00:00', '2015-11-17T00:00:00', '2015-11-18T00:00:00', '2015-11-19T00:00:00', '2015-11-20T00:00:00', '2015-11-21T00:00:00', '2015-11-22T00:00:00', '2015-11-23T00:00:00', '2015-11-24T00:00:00', '2015-11-25T00:00:00', '2015-11-26T00:00:00', '2015-11-27T00:00:00', '2015-11-28T00:00:00', '2015-11-29T00:00:00', '2015-11-30T00:00:00', '2015-12-01T00:00:00', '2015-12-02T00:00:00', '2015-12-03T00:00:00', '2015-12-04T00:00:00', '2015-12-05T00:00:00', '2015-12-06T00:00:00', '2015-12-07T00:00:00', '2015-12-08T00:00:00', '2015-12-09T00:00:00', '2015-12-10T00:00:00', '2015-12-11T00:00:00', '2015-12-12T00:00:00', '2015-12-13T00:00:00', '2015-12-14T00:00:00', '2015-12-15T00:00:00', '2015-12-16T00:00:00', '2015-12-17T00:00:00', '2015-12-18T00:00:00', '2015-12-19T00:00:00', '2015-12-20T00:00:00', '2015-12-21T00:00:00', '2015-12-22T00:00:00', '2015-12-23T00:00:00', '2015-12-24T00:00:00', '2015-12-25T00:00:00', '2015-12-26T00:00:00', '2015-12-27T00:00:00', '2015-12-28T00:00:00', '2015-12-29T00:00:00', '2015-12-30T00:00:00', '2015-12-31T00:00:00', '2016-01-01T00:00:00', '2016-01-02T00:00:00', '2016-01-03T00:00:00', '2016-01-04T00:00:00', '2016-01-05T00:00:00', '2016-01-06T00:00:00', '2016-01-07T00:00:00', '2016-01-08T00:00:00', '2016-01-09T00:00:00', '2016-01-10T00:00:00', '2016-01-11T00:00:00', '2016-01-12T00:00:00', '2016-01-13T00:00:00', '2016-01-14T00:00:00', '2016-01-15T00:00:00', '2016-01-16T00:00:00', '2016-01-17T00:00:00', '2016-01-18T00:00:00', '2016-01-19T00:00:00', '2016-01-20T00:00:00', '2016-01-21T00:00:00', '2016-01-22T00:00:00', '2016-01-23T00:00:00', '2016-01-24T00:00:00', '2016-01-25T00:00:00', '2016-01-26T00:00:00', '2016-01-27T00:00:00', '2016-01-28T00:00:00', '2016-01-29T00:00:00', '2016-01-30T00:00:00', '2016-01-31T00:00:00', '2016-02-01T00:00:00', '2016-02-02T00:00:00', '2016-02-03T00:00:00', '2016-02-04T00:00:00', '2016-02-05T00:00:00', '2016-02-06T00:00:00', '2016-02-07T00:00:00', '2016-02-08T00:00:00', '2016-02-09T00:00:00', '2016-02-10T00:00:00', '2016-02-11T00:00:00', '2016-02-12T00:00:00', '2016-02-13T00:00:00', '2016-02-14T00:00:00', '2016-02-15T00:00:00', '2016-02-16T00:00:00', '2016-02-17T00:00:00', '2016-02-18T00:00:00', '2016-02-19T00:00:00', '2016-02-20T00:00:00', '2016-02-21T00:00:00', '2016-02-22T00:00:00', '2016-02-23T00:00:00', '2016-02-24T00:00:00', '2016-02-25T00:00:00', '2016-02-26T00:00:00', '2016-02-27T00:00:00', '2016-02-28T00:00:00', '2016-02-29T00:00:00', '2016-03-01T00:00:00', '2016-03-02T00:00:00', '2016-03-03T00:00:00', '2016-03-04T00:00:00', '2016-03-05T00:00:00', '2016-03-06T00:00:00', '2016-03-07T00:00:00', '2016-03-08T00:00:00', '2016-03-09T00:00:00', '2016-03-10T00:00:00', '2016-03-11T00:00:00', '2016-03-12T00:00:00', '2016-03-13T00:00:00', '2016-03-14T00:00:00', '2016-03-15T00:00:00', '2016-03-16T00:00:00', '2016-03-17T00:00:00', '2016-03-18T00:00:00', '2016-03-19T00:00:00', '2016-03-20T00:00:00', '2016-03-21T00:00:00', '2016-03-22T00:00:00', '2016-03-23T00:00:00', '2016-03-24T00:00:00', '2016-03-25T00:00:00', '2016-03-26T00:00:00', '2016-03-27T00:00:00', '2016-03-28T00:00:00', '2016-03-29T00:00:00', '2016-03-30T00:00:00', '2016-03-31T00:00:00', '2016-04-01T00:00:00', '2016-04-02T00:00:00', '2016-04-03T00:00:00', '2016-04-04T00:00:00', '2016-04-05T00:00:00', '2016-04-06T00:00:00', '2016-04-07T00:00:00', '2016-04-08T00:00:00', '2016-04-09T00:00:00', '2016-04-10T00:00:00', '2016-04-11T00:00:00', '2016-04-12T00:00:00', '2016-04-13T00:00:00', '2016-04-14T00:00:00', '2016-04-15T00:00:00', '2016-04-16T00:00:00', '2016-04-17T00:00:00', '2016-04-18T00:00:00', '2016-04-19T00:00:00', '2016-04-20T00:00:00', '2016-04-21T00:00:00']]



# Open a json file
with open('user_voltage_data.json') as f:
    user_voltage_data = json.load(f)

def parse_voltage_time():
  for user in user_to_sensor_id.keys():
    user_voltage_time1 = []
    for i in range(0, len(user_voltage_data[user][2])):
      time1 = dateutil.parser.parse(user_voltage_data[user][2][i])
      user_voltage_time1.append(time1)

    user_voltage_data[user][2] = user_voltage_time1

parse_voltage_time()

def parse_freq_time():
  user_freq_time2 = []
  for i in range(0, len(user_freq_data[2])):
    time2 = dateutil.parser.parse(user_freq_data[2][i])
    user_freq_time2.append(time2)

  user_freq_data[2] = user_freq_time2

parse_freq_time()

# # print user_voltage_data['KIT1-0003'][2]
# # def unixtime_to_readable():

# #   for user in user_to_sensor_id.keys():
# #     user_voltage_time1 = []
# #     for i in range(0, len(user_voltage_data[user][i])):
# #       datetime.datetime.fromtimestamp(user_voltage_data[user][i])





# def plot_individual_voltage():
#     fig, ax = plt.subplots()
#     ax.plot_date(user_voltage_data['KIT1-0003'][2], user_voltage_data['KIT1-0003'][0], fmt='b-') # x = array of dates, y = array of numbers

#     fig.autofmt_xdate()

#     # For tickmarks and ticklabels every week
#     ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
#     ax.xaxis.set_major_locator(mdates.DayLocator(interval=15))

#     # For tickmarks and ticklabels every other week
#     #ax.xaxis.set_major_locator(WeekdayLocator(byweekday=MO, interval=2))

#     plt.grid(True)
#     plt.show()

# # plot_individual_voltage()

# # plt.plot(user_voltage_data['KIT1-0003'][2], user_voltage_data['KIT1-0003'][0])
# # plt.show()

# # def plot_connec_timeseries(rows,cols):

# #   users = list(data.connec.keys())
# #   user_counter = 0


# #   def plot(ax, user, user_id):
# #     datetimes = connec_data.connec[user][1]
# #     value = connec_data.connec[user][0]
# #     dates = matplotlib.dates.date2num(datetimes)
# #     ax.plot(dates, value)
# #     ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
# #     ax.xaxis.set_major_locator(mdates.DayLocator(interval=15))
# #     plt.xticks(rotation=30)
# #     ax.set_xlabel('DateTime', fontsize=8)
# #     ax.set_ylabel('connec', fontsize=8)
# #     ax.set_title('User ID ' + str(user_id), fontsize=8)
# #     ax.set_ylim([-1,1])

# #   fig, axes = plt.subplots(nrows=rows, ncols=cols)
# #   plt.title('connec Timeseries')
# #   for row in axes:
# #       for ax in row:
# #           user = users[user_counter]
# #           user_id = int(user[-2:])
# #           while user_id > rows*cols:
# #             user_counter +=1
# #             user = users[user_counter]
# #             user_id = int(user[-2:])
# #           plot(ax, user, user_id)
# #           user_counter +=1
# #           print user
# #           # print user[-3:]
# #   plt.tight_layout()
# #   plt.gcf().autofmt_xdate()
# #   plt.show()

# # print connec_data.connec['KIT1-0003'][1]

# # plot_connec_timeseries(2,2)
# def plot_individual_connec():
#     fig, ax = plt.subplots()
#     ax.plot_date(connec_data.connec['KIT1-0003'][1], connec_data.connec['KIT1-0003'][0], fmt='b-') # x = array of dates, y = array of numbers

#     fig.autofmt_xdate()

#     # For tickmarks and ticklabels every week
#     ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
#     ax.xaxis.set_major_locator(mdates.DayLocator(interval=15))

#     # For tickmarks and ticklabels every other week
#     #ax.xaxis.set_major_locator(WeekdayLocator(byweekday=MO, interval=2))

#     plt.grid(True)
#     plt.show()

# # plot_individual_connec()


def plot_combined():

  plt.figure('KIT1-0003')
  plt.subplot(311)
  plt.plot(user_voltage_data['KIT1-0003'][2], user_voltage_data['KIT1-0003'][0],'b-')
  plt.ylabel('Voltage')
  plt.subplot(312)
  plt.plot(connec_data.connec['KIT1-0003'][1], connec_data.connec['KIT1-0003'][0],'r-')
  plt.ylabel('Connection')
  plt.ylim(-2, 2)
  plt.subplot(313)
  plt.plot(user_freq_data[2],user_freq_data[0], 'b-')
  plt.ylabel('system frequency')
  plt.show()

plot_combined()



