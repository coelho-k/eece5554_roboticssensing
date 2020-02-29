import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from scipy import stats

field_static = pd.read_csv(r'fieldMoving.csv')
easting = field_static['field.utm_easting']#[:-100]
northing = field_static['field.utm_northing']#[:-100]
altitude = field_static['field.altitude']

easting = easting - np.min(easting)
northing = northing  - np.min(northing)

#easting = [ii for ii in easting if ii < 0.09]
#northing = [ii for ii in northing if ii > 0.05]

easting_var = np.var(easting)
northing_var = np.var(northing)

#offset = np.sqrt((easting[0] - easting[len(easting) - 1])**2 + (northing[0] - northing[len(northing) - 1])**2)
#print('Offset = ', offset)

print(easting_var)
print(northing_var)

plt.plot(easting, northing)
#plt.xlim(-0.02,0.02)
#plt.ylim(-0.06,0.06)
plt.show()

plt.plot(altitude)
plt.show()

#slope, intercept, r_value, p_value, std_err = stats.linregress(easting[6:18],northing[6:18])
#slope, intercept, r_value, p_value, std_err = stats.linregress(easting[19:26],northing[19:26])
#slope, intercept, r_value, p_value, std_err = stats.linregress(easting[27:40],northing[27:40])
#slope, intercept, r_value, p_value, std_err = stats.linregress(easting[41:52],northing[41:52])

plt.subplot(1,2,1)
plt.title('Easting')
plt.hist(easting)
plt.subplot(1,2,2)
plt.title('Northing')
plt.hist(northing)
plt.show()