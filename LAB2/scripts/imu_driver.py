#!/usr/bin/env python

import rospy, math, serial, time, string, re, logging
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Imu
from sensor_msgs.msg import MagneticField
import message_filters

logger = logging.getLogger('rosout')

def get_frame_id():
        """Get the TF frame_id.
        Queries rosparam for the ~frame_id param. If a tf_prefix param is set,
        the frame_id is prefixed with the prefix.
        Returns:
            str: The fully-qualified TF frame ID.
        """
        frame_id = rospy.get_param('~frame_id', 'imu')
        # Add the TF prefix
        prefix = ""
        prefix_param = rospy.search_param('tf_prefix')
        if prefix_param:
            prefix = rospy.get_param(prefix_param)
            return "%s/%s" % (prefix, frame_id)
        else:
            return frame_id

def euler_to_quaternion(yaw, pitch, roll):

        yaw = yaw * (np.pi / 180)
        pitch = yaw * (np.pi / 180)
        roll = roll * (np.pi / 180)

        qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
        qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
        qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
        qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)

        return [qx, qy, qz, qw]

def add_sentence(imu_string, frame_id, timestamp=None):
        """Public method to provide a new IMU sentence to the driver.
        Args:
            imu_string (str): IMU sentence in string form.
            frame_id (str): TF frame ID of the GPS receiver.
            timestamp(rospy.Time, optional): Time the sentence was received.
                If timestamp is not specified, the current time is used.

        Returns:
            msg: The imu and mag message
        """


        if timestamp:
            current_time = timestamp
        elif '$VNYMR' in imu_string:

            #print(imu_string)
            imu_string = imu_string[:-3]
            imu_string = imu_string.split(',')[1:]
            #print(imu_string)

            for ii in range(0, len(imu_string)): 
                imu_string[ii] = float(imu_string[ii]) 

            #print(imu_string)
            # Time
            current_time = rospy.get_rostime()

            # Creating Message Objects
            imu_data = Imu()
            mag_data = MagneticField()

            # Fill Headers for both messages
            # Add the x, y, z fields
            imu_data.header.stamp = current_time
            imu_data.header.frame_id = frame_id
            mag_data.header.stamp = current_time
            mag_data.header.frame_id = frame_id

            # Convert YPR to Quaternion
            quat = euler_to_quaternion(imu_string[0], imu_string[1], imu_string[2])
            print(quat)

            # Fill in the data fields
            imu_data.angular_velocity.x = imu_string[9]
            imu_data.angular_velocity.y = imu_string[10]
            imu_data.angular_velocity.z = imu_string[11]
            imu_data.linear_acceleration.x = imu_string[6]
            imu_data.linear_acceleration.y = imu_string[7]
            imu_data.linear_acceleration.z = imu_string[8]
            imu_data.orientation.x = quat[0]
            imu_data.orientation.y = quat[1]
            imu_data.orientation.z = quat[2]
            imu_data.orientation.w = quat[3]

            mag_data.magnetic_field.x = imu_string[3]
            mag_data.magnetic_field.y = imu_string[4]
            mag_data.magnetic_field.z = imu_string[5]

            #print (imu_data, mag_data)
            
            return imu_data, mag_data

            
def main():
    """Create and run the imu ROS node.
    Creates a ROS IMU Driver and feeds it IMU sentence strings from a serial device.
    ROS parameters:
        ~port (str): Path of the serial device to open.
        ~baud (int): Baud rate to configure the serial device.
    """
    rospy.init_node('imu_driver')
    pub_imu = rospy.Publisher('imu_data', Imu)
    pub_mag = rospy.Publisher('mag_data', MagneticField)
    #rate = rospy.Rate(20)

    serial_port = rospy.get_param('~port', '/dev/ttyUSB0')
    serial_baud = rospy.get_param('~baud', 115200)
    frame_id = get_frame_id()

    try:
        GPS = serial.Serial(port=serial_port, baudrate=serial_baud, timeout=2)
        try:
            while not rospy.is_shutdown():
                data = GPS.readline().strip()
                #print(data)
                try:
                    i_data, m_data = add_sentence(data, frame_id)
                    print(i_data, m_data)
                    if i_data and m_data == None:
                        rospy.logwarn('Message not parsed correctly') 
                    else:
                        #print(i_data)
                        pub_imu.publish(i_data)
                        pub_mag.publish(m_data)

                except ValueError:
                    rospy.logwarn(
                        'Publishing went wrong'
                        )

        except (rospy.ROSInterruptException, serial.serialutil.SerialException):
            GPS.close()  # Close GPS serial port
    except serial.SerialException as ex:
        rospy.logfatal(
            "Could not open serial port: I/O error({0}): {1}".format(ex.errno, ex.strerror))

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass