import pandas as pd 
import numpy as np 
import math
import matplotlib.pyplot as plt 
import matplotlib.mlab as mlab
from mpl_toolkits import mplot3d
from scipy import signal, integrate, stats
import datetime

imu = pd.read_csv(r'driving_imu.csv')
mag = pd.read_csv(r'driving_mag.csv')

a_x = imu['field.linear_acceleration.x']
a_y = imu['field.linear_acceleration.y']
a_z = imu['field.linear_acceleration.z']
w_x = imu['field.angular_velocity.x']
w_y = imu['field.angular_velocity.y']
w_z = imu['field.angular_velocity.z']
m_y = mag['field.magnetic_field.y']
m_x = mag['field.magnetic_field.x']
m_z = mag['field.magnetic_field.z']


plt.subplot(2,3,1)
plt.title('Linear Acceleration - X')
plt.plot(a_x)

plt.subplot(2,3,2)
plt.title('Linear Acceleration - Y')
plt.plot(a_y)

plt.subplot(2,3,3)
plt.title('Linear Acceleration - Z')
plt.plot(a_z)

plt.subplot(2,3,4)
plt.title('Linear Acceleration - X')
xmin, xmax = min(a_x), max(a_x)  
lnspc = np.linspace(xmin, xmax, len(a_x))
m, s = stats.norm.fit(a_x) # get mean and standard deviation  
pdf_g = stats.norm.pdf(lnspc, m, s) # now get theoretical values in our interval  
plt.plot(lnspc, pdf_g, label="Norm") # plot it
plt.hist(a_x, normed=True)


plt.subplot(2,3,5)
plt.title('Linear Acceleration - Y')
xmin, xmax = min(a_y), max(a_y)  
lnspc = np.linspace(xmin, xmax, len(a_y))
m, s = stats.norm.fit(a_y) # get mean and standard deviation  
pdf_g = stats.norm.pdf(lnspc, m, s) # now get theoretical values in our interval  
plt.plot(lnspc, pdf_g, label="Norm") # plot it
plt.hist(a_y, normed=True)

plt.subplot(2,3,6)
plt.title('Linear Acceleration - Z')
xmin, xmax = min(a_z), max(a_z)  
lnspc = np.linspace(xmin, xmax, len(a_z))
m, s = stats.norm.fit(a_z) # get mean and standard deviation  
pdf_g = stats.norm.pdf(lnspc, m, s) # now get theoretical values in our interval  
plt.plot(lnspc, pdf_g, label="Norm") # plot it
plt.hist(a_z, normed=True)

plt.tight_layout()
plt.show()

plt.subplot(2,3,1)
plt.title('Angular Velocity - X')
plt.plot(w_x)

plt.subplot(2,3,2)
plt.title('Angular Velocity - Y')
plt.plot(w_y)

plt.subplot(2,3,3)
plt.title('Angular Velocity - Z')
plt.plot(w_z)

plt.subplot(2,3,4)
plt.title('Angular Velocity - X')
xmin, xmax = min(w_x), max(w_x)  
lnspc = np.linspace(xmin, xmax, len(w_x))
m, s = stats.norm.fit(w_x) # get mean and standard deviation  
pdf_g = stats.norm.pdf(lnspc, m, s) # now get theoretical values in our interval  
plt.plot(lnspc, pdf_g, label="Norm") # plot it
plt.hist(w_x, normed=True)


plt.subplot(2,3,5)
plt.title('Angular Velocity - Y')
xmin, xmax = min(w_y), max(w_y)  
lnspc = np.linspace(xmin, xmax, len(w_y))
m, s = stats.norm.fit(w_y) # get mean and standard deviation  
pdf_g = stats.norm.pdf(lnspc, m, s) # now get theoretical values in our interval  
plt.plot(lnspc, pdf_g, label="Norm") # plot it
plt.hist(w_y, normed=True)

plt.subplot(2,3,6)
plt.title('Angular Velocity - Z')
xmin, xmax = min(w_z), max(w_z)  
lnspc = np.linspace(xmin, xmax, len(w_z))
m, s = stats.norm.fit(w_z) # get mean and standard deviation  
pdf_g = stats.norm.pdf(lnspc, m, s) # now get theoretical values in our interval  
plt.plot(lnspc, pdf_g, label="Beta") # plot it
plt.hist(w_z, normed=True)

plt.tight_layout()
plt.show()

plt.subplot(2,3,1)
plt.title('Magnetic Field - X')
plt.plot(m_x)

plt.subplot(2,3,2)
plt.title('Magnetic Field - Y')
plt.plot(m_y)

plt.subplot(2,3,3)
plt.title('Magnetic Field - Z')
plt.plot(m_z)

plt.subplot(2,3,4)
plt.title('Magnetic Field - X')
plt.hist(m_x, normed=True)


plt.subplot(2,3,5)
plt.title('Magnetic Field - Y')
plt.hist(m_y, normed=True)

plt.subplot(2,3,6)
plt.title('Magnetic Field - Z')
plt.hist(m_z, normed=True)

plt.tight_layout()
plt.show()
