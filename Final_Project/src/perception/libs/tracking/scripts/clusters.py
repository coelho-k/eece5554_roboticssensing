#!/usr/bin/env python

import rospy
from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2 as pc2
from geometry_msgs.msg import Point

pub = rospy.Publisher('clusters_xyz', Point)

def calc_centres():
    pass

def callback(data):

    msg = Point()

    for p in pc2.read_points(data, field_names = ("x", "y", "z"), skip_nans=True):
        print (" x : %f  y: %f  z: %f" %(p[0],p[1],p[2]))
        msg.x = p[0]
        msg.y = p[1]
        msg.z = p[2]

        pub.publish(msg)


def main():

    rospy.init_node('cluster_node')
    rospy.Subscriber('/segmenter/points_clustered', PointCloud2, callback)

    rospy.spin()


if __name__ == '__main__':
    main()
