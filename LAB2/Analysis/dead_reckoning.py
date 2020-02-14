import pandas as pd 
import numpy as np 
import math
import matplotlib.pyplot as plt 
from mpl_toolkits import mplot3d
from scipy import signal, integrate
import datetime
import gc

imu = pd.read_csv(r'driving_imu.csv')
mag = pd.read_csv(r'driving_mag.csv')
imu['field.header.frame_id'] = 'imu'

a_x = imu['field.linear_acceleration.x']#[10000:35000]
a_y = imu['field.linear_acceleration.y']#[10000:35000]
mag_x = mag['field.magnetic_field.x']#[10000:35000]
mag_y = mag['field.magnetic_field.y']#[10000:35000]
w = imu['field.angular_velocity.z']#[10000:35000]
time = imu['field.header.stamp']

# -------------------------------------------------------------
sos = signal.butter(1, 0.1, 'hp', fs=500, output='sos')
a_x = signal.sosfilt(sos, a_x)
#a_y = signal.sosfilt(sos, a_y)

sos = signal.butter(1, 1, 'lp', fs=500, output='sos')
a_x = signal.sosfilt(sos, a_x)
a_y = signal.sosfilt(sos, a_y)
# ---------------------------------------------------------------

v_x = integrate.cumtrapz(a_x)


wX = w[:-1] * v_x

plt.subplot(1,2,1)
plt.plot(wX)

y_obs = -a_y

plt.subplot(1,2,2)
plt.plot(y_obs)
plt.show()

# -------------------------------------------------------------
del w 
del wX 
del y_obs 
del a_x 
del a_y 

gc.collect()

# -------------------------------------------------------------
heading = []
for i in range(len(mag_x)):
    heading.append(math.atan2(mag_y[i], mag_x[i]) * (180/np.pi))

#heading = np.unwrap(heading)
#plt.plot(heading)
#plt.show()

p_x = []
p_y = []

org_x = 0
org_y = 0

# ---------------------------------------------------------------

sos = signal.butter(3, 10, 'lp', fs=500, output='sos')
v_x = signal.sosfilt(sos, v_x)

# ---------------------------------------------------------------

for ii in range(len(v_x)):
    if ii == 0:
        continue
    vx = v_x[ii] * np.cos(heading[ii])
    vy = v_x[ii] * np.sin(heading[ii])
    timestep = (time[ii] - time[ii-1]) / 1000000000
    px = org_x + (vx*timestep)
    py = org_y + (vy*timestep)
    p_x.append(px)
    p_y.append(py)
    org_x = px
    org_y = py


plt.plot(p_x, p_y)
plt.show()

