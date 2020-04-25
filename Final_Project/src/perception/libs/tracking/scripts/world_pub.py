#!/usr/bin/env python  
import roslib
import rospy
import tf
from sensor_msgs.msg import NavSatFix
import sys
import re
import datetime
import calendar
import math
import logging
import gps_converter


isFirst = True
startEN = [-1, -1]
eastNorth = [-1, -1]

def gps_callback(data):
    global isFirst, eastNorth, startEN
    if (data is not None):
        if (isFirst):
            startGPS = data
            isFirst = False
            startEN = convertToUTM(data)
            rospy.loginfo("Start [Easting, Northing]: " + str(startEN))
        #end if
    eastNorth = convertToUTM(data)
# end def

# to convert the NavSatFix data to utm coordinates
def convertToUTM(gps_data):
    values = [-1, -1]
    convert_result = gps_converter.from_latlon(gps_data.latitude, gps_data.longitude)
    values[0] = convert_result[0] # easting
    values[1] = convert_result[1] # northing 
    return values


# World Frame Publisher
if __name__ == '__main__':
    rospy.init_node('world_pub')
    rospy.loginfo('Starting World Frame Publisher ...')
    rospy.wait_for_message("/vehicle/gps/fix", NavSatFix)
    rospy.Subscriber("/vehicle/gps/fix", NavSatFix, gps_callback)

    br = tf.TransformBroadcaster()
    rate = rospy.Rate(10000.0)
    eastDiff = 0
    northDiff = 0
    while not rospy.is_shutdown():
        eastDiff = eastNorth[0] - startEN[0]
        northDiff = eastNorth[1] - startEN[1]
        rospy.loginfo("East Diff: " + str(eastDiff) + "\nNorth Diff: " + str(northDiff))
        br.sendTransform((eastDiff, northDiff, 0.0),
                         (0.0, 0.0, 0.0, 1.0),
                         rospy.Time.now(),
                         "base_footprint",
                         "world")
        rate.sleep()