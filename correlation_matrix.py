import pandas as pd
import numpy as np

pd.read_json('user_voltage_data.json')

# frame = pd.DataFrame(np.ndarray(user_voltage_data['KIT1-0003'][0], connec_data.connec['KIT1-0003'][0]), columns = ['a', 'b'])

# print len(user_voltage_data['KIT1-0003'][0]) 
# print len(connec_data.connec['KIT1-0003'][0])

a = np.array(user_voltage_data['KIT1-0003'][0])
a[184] = a[183]

# for i in range (0, len(a)):
#   if math.isnan(a[i]) == True:
#     a[i] == a[183]
#     print i
# print a[184]

# print(a[0])
b = np.array(connec_data.connec['KIT1-0003'][0])
# print(b[0])
b[184] = b[183]
# for i in range (0, len(b)):
#   int(b[i])

c = np.column_stack((a,b))
# print(np.shape(c))

frame = pd.DataFrame(c, columns = ['a', 'b'])
print frame.cov()
# frame['a'].corr(frame['b'])