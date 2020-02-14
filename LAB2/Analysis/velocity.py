import pandas as pd 
import numpy as np 
import math
import matplotlib.pyplot as plt 
from mpl_toolkits import mplot3d
from scipy import signal, integrate
import datetime
import transforms3d

#-----------------------------------------
# Estimate forward velocity --> means only in x-direction ??
#------------------------------------------------------------------------

imu = pd.read_csv(r'driving_imu.csv')
imu['field.header.frame_id'] = 'imu'
gps = pd.read_csv(r'driving_gps.csv')
mag = pd.read_csv(r'driving_mag.csv')

fig = plt.figure()

a_x = imu['field.linear_acceleration.x']
a_y = imu['field.linear_acceleration.y']
a_z = imu['field.linear_acceleration.z']
utm_easting = gps['field.utm_easting']
utm_northing = gps['field.utm_northing']
utm_easting = utm_easting - np.min(utm_easting)
utm_northing = utm_northing - np.min(utm_northing)
time = gps['field.header.stamp'] / 1e9
time_imu = imu['field.header.stamp'] / 1e9 
mag_x = mag['field.magnetic_field.x']
mag_y = mag['field.magnetic_field.y']
o_x = imu['field.orientation.x']
o_y = imu['field.orientation.y']
o_z = imu['field.orientation.z']
o_w = imu['field.orientation.w']
temp = imu['field.angular_velocity.z']


# ------------------------------------------------------------------------------
alpha = (0.1325 + (-0.0375)) / 2
beta = (0.275 + 0.125) / 2

mag_x = mag_x - alpha
mag_y = mag_y - beta

x1 = 0.083
y1 = 0.041
x2 = -0.031
y2 = 0.072

# Magnitudes
r = np.sqrt(x1**2 + y1**2)
q = np.sqrt(x2**2 + y2**2)

# Angle
theta = math.asin(y1/r)

# Rotation Matrix
R = [[math.cos(theta), math.sin(theta)], [-math.sin(theta), math.cos(theta)]]

# Do the rotation
mag_x, mag_y = np.matmul(R, [mag_x, mag_y])

#plt.plot(x, y)
#plt.grid()
#plt.show()

# Scaling for the minor axis
scaler = q / r
print(scaler)

# Rescaling the minor axis
mag_x = mag_x / scaler

R = [[math.cos(-theta), math.sin(-theta)], [-math.sin(-theta), math.cos(-theta)]]

mag_x, mag_y = np.matmul(R, [mag_x, mag_y])


# -------------------------------------------------------------------------------

# Plot the raw signal
#plt.subplot(1,3,1)
#plt.plot(time_imu, a_x)

# Remove Offset
a_x = a_x - np.mean(a_x[75])
#a_x[4000:11000] = a_x[4000:11000] +  np.mean(a_x[4000:11000])
#a_x[0:5000] = 0
#a_x[7500:10500] = np.abs(a_x[7500:10500])

#a_x = [-2.5 if ii < -2.5 else ii for ii in a_x]
#a_x[5000:] = a_x[5000:] -  np.mean(a_x[5000:6750])
#a_x[14850:] = a_x[14850:] -  np.mean(a_x[14850:17955])
#a_x[19815:] = a_x[19815:] -  np.mean(a_x[19815:21100])
#a_x[25050:] = a_x[25050:] -  np.mean(a_x[25050:25750])
#a_x[27400:] = a_x[27400:] -  np.mean(a_x[27400:28480])
#a_x[30000:] = a_x[30000:] -  np.mean(a_x[30000:31200])
#a_x[33060:] = a_x[33060:] -  np.mean(a_x[33060:33330])

plt.subplot(1,2,1)
plt.plot(a_x)

chunk = 5000

for ii in range(7500, 10500):
    c_mean = np.mean(a_x[ii:ii + 10])
    a_x[ii] = c_mean


for ii in range(0, len(a_x), chunk):

    c_mean = np.mean(a_x[ii:ii+chunk])

    var = np.var(a_x[ii:ii+chunk])

    #if var < 0.05:
    #    a_x[ii:ii+chunk] = c_mean

    #else:
    a_x[ii:ii + chunk] = a_x[ii:ii+chunk] - c_mean

#a_x[21250:21600] = 0

plt.subplot(1,2,2)
plt.plot( a_x)
plt.show()

#time = [datetime.datetime.fromtimestamp(item) for item in time] 
#time_imu = [datetime.datetime.fromtimestamp(item) for item in time_imu] 


# Cumulative addition for integration
v_x = integrate.cumtrapz(a_x, dx = 0.025)
v_x = [0 if i < 0 else i for i in v_x]
#.subplot(1,2,1)
plt.plot(time_imu[:-1], v_x, label = 'IMU Velocity')
#plt.show()


# -------------- GPS COMPARISONS --------------------
# Calculating successive difference for utm values to get some sort of distance estimate
d_easting = np.gradient(utm_easting)
d_northing = np.gradient(utm_northing)
length = np.sqrt(d_easting**2 + d_northing**2)  
#plt.subplot(1,2,2)
plt.plot(time, length , label = 'GPS')

plt.title('Velocity Comparison')
plt.xlabel('Time')
plt.ylabel('Velocity (m/s)')
plt.legend()
plt.show()

print(utm_easting[0])
print(utm_northing[0])

plt.plot(v_x)
plt.show()

fig = plt.figure()
a_x = imu['field.linear_acceleration.x']
plt.plot(time, length, label = 'GPS')
plt.legend()
plt.show()

# --------------------------------------- 3 ------------------------------------------------------


heading = []
for i in range(len(mag_y)):
    heading.append(math.atan2(mag_y[i], mag_x[i]))

heading_gyro = integrate.cumtrapz(-temp, dx = 0.025) 

heading_gyro = (heading_gyro + np.pi) % (2 * np.pi) - np.pi

#sos = signal.butter(1, 0.05, 'lp', fs=10, output='sos')
#heading = signal.sosfilt(sos, heading)

#sos = signal.butter(1, 0.0005, 'hp', fs=10, output='sos')
#heading_gyro = signal.sosfilt(sos, heading_gyro)

#heading = 0.20*heading_gyro + 0.80*heading

heading = heading_gyro

heading[24250:] = heading[24250:] + 0.3

plt.plot(heading)
plt.title('Heading')
plt.ylabel('Yaw Angle')
plt.xlabel('Points')
plt.show()


p_x = []
p_y = []

org_x = 0
org_y = 0

for ii in range(len(v_x)):
    if ii == 0:
        continue
    vx = v_x[ii] * np.cos(heading[ii])
    vy = v_x[ii] * np.sin(heading[ii])
    timestep = (time_imu[ii] - time_imu[ii-1]) 
    px = org_x + (vx*timestep)
    py = org_y + (vy*timestep)
    p_x.append(px)
    p_y.append(py)
    org_x = px
    org_y = py

p_x = [x*1.25  for x in p_x]
p_y = [y  for y in p_y]

theta =  20 * (np.pi / 180)

R = [[math.cos(theta), math.sin(theta)], [-math.sin(theta), math.cos(theta)]]

p_x, p_y = np.matmul(R, [p_x, p_y])

p_x = [x + 50 for x in p_x]
p_y = [y + 8 for y in p_y]

print(p_x[0])
print(p_y[0])

plt.plot(p_x, p_y)
plt.plot(utm_easting, utm_northing)
plt.title('Trajectory')
plt.xlabel('Position (Easting)')
plt.ylabel('Position (Northing)')
plt.show()


wX = (temp[:-1] * v_x) 
y_obs = a_y

plt.plot(wX, label = 'wX')
plt.plot(y_obs, label = 'y_obs')
plt.xlabel('Points')
plt.ylabel('Velocity')
plt.legend()
plt.show()


x_c = (a_y - wX) / np.gradient(temp)
x_c = np.nanmean(x_c) 
print(x_c)

car_acc = a_x + ((temp**2) * 0.2657)


for ii in range(7500, 10500):
    c_mean = np.mean(car_acc[ii:ii + 10])
    car_acc[ii] = c_mean


for ii in range(0, len(car_acc), chunk):

    c_mean = np.mean(car_acc[ii:ii+chunk])

    var = np.var(car_acc[ii:ii+chunk])

    #if var < 0.05:
    #    car_acc[ii:ii+chunk] = c_mean

    #else:
    car_acc[ii:ii + chunk] = car_acc[ii:ii+chunk] - c_mean

car_vel = integrate.cumtrapz(car_acc, dx = 0.025)
car_vel = [0 if i < 0 else i for i in car_vel]

plt.plot(car_vel, label = 'x_c')
plt.plot(v_x, label = 'No x_c')
plt.legend()
plt.show()