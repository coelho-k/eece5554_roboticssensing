import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

sitting = pd.read_csv('data_sitting.csv')
print(sitting.head())

plt.scatter(sitting['field.utm_easting'] - np.min(sitting['field.utm_easting']), sitting['field.utm_northing'] - np.min(sitting['field.utm_northing']), marker='x')
plt.scatter(np.mean(sitting['field.utm_easting'])- np.min(sitting['field.utm_easting']), np.mean(sitting['field.utm_northing'])- np.min(sitting['field.utm_northing']))
plt.title('Sitting')
plt.xlabel('utm_easting')
plt.ylabel('utm_northing')
plt.show()

print(np.mean(sitting['field.utm_easting'])- np.min(sitting['field.utm_easting']), np.mean(sitting['field.utm_northing'])- np.min(sitting['field.utm_northing']))
print(np.std(sitting['field.utm_easting'] - np.min(sitting['field.utm_easting'])))
print(np.std(sitting['field.utm_northing'] - np.min(sitting['field.utm_northing'])))



plt.subplot(1,2,1)
plt.title('Sitting')
plt.hist(sitting['field.utm_easting'])
plt.xlabel('utm_easting')
plt.subplot(1,2,2)
plt.title('Sitting')
plt.hist(sitting['field.utm_northing'])
plt.xlabel('utm_northing')
plt.show()

x = np.corrcoef(sitting['field.utm_easting'], sitting['field.utm_northing'])
print(x)