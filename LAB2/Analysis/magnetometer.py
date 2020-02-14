import pandas as pd 
import numpy as np 
import math
import matplotlib.pyplot as plt 
from mpl_toolkits import mplot3d
from scipy import signal, integrate
import transforms3d

fig = plt.figure()
#ax = plt.axes(projection='3d')

mag = pd.read_csv(r'driving_mag.csv')
imu = pd.read_csv(r'driving_imu.csv')
mag['field.header.frame_id'] = 'mag'
#print(imu['field.header.frame_id'])

x = mag['field.magnetic_field.x'][8000:10000]
y = mag['field.magnetic_field.y'][8000:10000]
z = mag['field.magnetic_field.z'][8000:10000]
o_x = imu['field.orientation.x']
o_y = imu['field.orientation.y']
o_z = imu['field.orientation.z']
o_w = imu['field.orientation.w']

temp = imu['field.angular_velocity.z'][8000:10000]
#plt.plot(temp)
#plt.show()


plt.subplot(2,2,1)
plt.title('Original Data')
plt.xlabel('mag_x')
plt.ylabel('mag_y')
plt.plot(x, y)
plt.grid()
#plt.show()

# Using xmax, ymax, xmin, ymin to remove offsets
# Did not use any functions because of error in data
# Visual Inspection
beta = (0.275 + 0.125) / 2
alpha = (0.1325 + (-0.0375)) / 2

x = x - alpha
y = y - beta
plt.subplot(2,2,2)
plt.title('Hard Iron Offset Removed')
plt.plot(x, y)
plt.xlabel('mag_x')
plt.ylabel('mag_y')
plt.grid()
#plt.show()

# Finding the major and minor axes
# x1, y1 = major
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
x, y = np.matmul(R, [x, y])

#plt.plot(x, y)
#plt.grid()
#plt.show()

# Scaling for the minor axis
scaler = q / r
print(scaler)

# Rescaling the minor axis
x = x / scaler

plt.subplot(2,2,3)
plt.title('Rescaling Axes for \n Soft Iron Offset Removal')
plt.plot(x, y)
plt.xlabel('mag_x')
plt.ylabel('mag_y')
plt.grid()
#plt.show()

# Final Rotation 
R = [[math.cos(-theta), math.sin(-theta)], [-math.sin(-theta), math.cos(-theta)]]

x, y = np.matmul(R, [x, y])

# Accounting for hard and soft offsets
plt.subplot(2,2,4)
plt.title('Final after all correction')
plt.plot(x, y)
plt.xlabel('mag_x')
plt.ylabel('mag_y')
plt.grid()
plt.tight_layout()
plt.show()


"""yaw = []
for ii in range(8000,10000):
    #yaw.append(math.atan2(2.0*(o_y[ii]*o_z[ii] + o_w[ii]*o_x[ii]), o_w[ii]*o_w[ii] -o_x[ii]*o_x[ii] - o_y[ii]*o_y[ii] + o_z[ii]*o_z[ii])*(np.pi/180))
    yaw.append(transforms3d.euler.quat2euler([o_w[ii], o_x[ii], o_y[ii], o_z[ii]]))
    #plt.plot(yaw[0][ii])

df = pd.DataFrame(yaw, columns =['x', 'y', 'z'])
plt.plot(df['y'])
plt.show()"""

heading = []
for i in range(len(y)):
    heading.append(math.atan2(y[i], x[i]))

#heading = np.unwrap(heading)
plt.subplot(1,2,1)
plt.title('Yaw From Magnetometer')
plt.ylabel('Yaw Angle')
plt.xlabel('Points')
plt.plot(heading)
#plt.show()

heading_gyro = integrate.cumtrapz(-temp, dx = 0.025) 

heading_gyro = (heading_gyro + np.pi) % (2 * np.pi) - np.pi

plt.subplot(1,2,2)
plt.title('Yaw From Yaw Rate')
plt.ylabel('Yaw Angle')
plt.xlabel('Points')
plt.plot(heading_gyro)
plt.show()


sos = signal.butter(1, 0.05, 'lp', fs=10, output='sos')
heading = signal.sosfilt(sos, heading)

sos = signal.butter(1, 0.0005, 'hp', fs=10, output='sos')
heading_gyro = signal.sosfilt(sos, heading_gyro)

new = 0.20*heading_gyro + 0.80*heading[:-1]

plt.plot(heading, label = 'Magnetometer')
plt.plot(heading_gyro, label = 'Gyro')
plt.plot(new, label = 'Filter')
plt.xlabel('Points')
plt.ylabel('Yaw Angle')
plt.legend()
plt.show()


yaw = []

for ii in range(len(o_y)):
    yaw.append(transforms3d.euler.quat2euler([o_w[ii], o_x[ii], o_y[ii], o_z[ii]]))

df = pd.DataFrame(yaw, columns =['x', 'y', 'z'])
plt.plot(np.unwrap(-df['z']))
plt.show()

