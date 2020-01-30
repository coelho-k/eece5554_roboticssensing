#!/usr/bin/env python

# Certain methods and formatting taken and modified from the nmea_navsat ROS driver 
# https://github.com/ros-drivers/nmea_navsat_driver

import rospy, math, serial, time, string, re, logging
from std_msgs.msg import String
from gps.msg import gps_data
import utm_converter

logger = logging.getLogger('rosout')

def safe_float(field):
    """Convert  field to a float.
    Args:
        field: The field (usually a str) to convert to float.
    Returns:
        The float value represented by field or NaN if float conversion throws a ValueError.
    """
    try:
        return float(field)
    except ValueError:
        return float('NaN')


def safe_int(field):
    """Convert  field to an int.
    Args:
        field: The field (usually a str) to convert to int.
    Returns:
        The int value represented by field or 0 if int conversion throws a ValueError.
    """
    try:
        return int(field)
    except ValueError:
        return 0

def convert_latitude(field):
    """Convert a latitude string to floating point decimal degrees.
    Args:
        field (str): Latitude string, expected to be formatted as DDMM.MMM, where
            DD is the latitude degrees, and MM.MMM are the minutes latitude.
    Returns:
        Floating point latitude in decimal degrees.
    """
    return safe_float(field[0:2]) + safe_float(field[2:]) / 60.0


def convert_longitude(field):
    """Convert a longitude string to floating point decimal degrees.
    Args:
        field (str): Longitude string, expected to be formatted as DDDMM.MMM, where
            DDD is the longitude degrees, and MM.MMM are the minutes longitude.
    Returns:
        Floating point latitude in decimal degrees.
    """
    return safe_float(field[0:3]) + safe_float(field[3:]) / 60.0

def convert_time(nmea_utc):

    pass

parse_maps = {
    "GGA": [
        ("fix_type", int, 6),
        ("latitude", convert_latitude, 2),
        ("latitude_direction", str, 3),
        ("longitude", convert_longitude, 4),
        ("longitude_direction", str, 5),
        ("altitude", safe_float, 9),
        ("mean_sea_level", safe_float, 11),
        ("hdop", safe_float, 8),
        ("num_satellites", safe_int, 7),
        ("utc_time", convert_time, 1),
    ]
}

def parse_nmea_sentence(nmea_sentence):
    """Parse a NMEA sentence string into a dictionary.
    Args:
        nmea_sentence (str): A single NMEA sentence of one of the types in parse_maps.
    Returns:
        A dict mapping string field names to values for each field in the NMEA sentence or
        False if the sentence could not be parsed.
    """
    # Check for a valid nmea sentence
    if not re.match(
            r'(^\$GP|^\$GN|^\$GL|^\$IN).*\*[0-9A-Fa-f]{2}$', nmea_sentence):
        logger.debug(
            "Regex didn't match, sentence not valid NMEA? Sentence was: %s" %
            repr(nmea_sentence))
        return False
    fields = [field.strip(',') for field in nmea_sentence.split(',')]

    # Ignore the $ and talker ID portions (e.g. GP)
    sentence_type = fields[0][3:]

    """if sentence_type not in parse_maps:
        logger.debug("Sentence type %s not in parse map, ignoring."
                     % repr(sentence_type))
        return False

    parse_map = parse_maps[sentence_type]

    parsed_sentence = {}
    for entry in parse_map:
        parsed_sentence[entry[0]] = entry[1](fields[entry[2]])"""

    if sentence_type in parse_maps:
        parse_map = parse_maps[sentence_type]
        parsed_sentence = {}
        for entry in parse_map:
            parsed_sentence[entry[0]] = entry[1](fields[entry[2]])
        return {sentence_type: parsed_sentence}
    else:
        pass


    #return {sentence_type: parsed_sentence}

def get_frame_id():
        """Get the TF frame_id.
        Queries rosparam for the ~frame_id param. If a tf_prefix param is set,
        the frame_id is prefixed with the prefix.
        Returns:
            str: The fully-qualified TF frame ID.
        """
        frame_id = rospy.get_param('~frame_id', 'gps')
        # Add the TF prefix
        prefix = ""
        prefix_param = rospy.search_param('tf_prefix')
        if prefix_param:
            prefix = rospy.get_param(prefix_param)
            return "%s/%s" % (prefix, frame_id)
        else:
            return frame_id


def add_sentence(nmea_string, frame_id, timestamp=None):
        """Public method to provide a new NMEA sentence to the driver.
        Args:
            nmea_string (str): NMEA sentence in string form.
            frame_id (str): TF frame ID of the GPS receiver.
            timestamp(rospy.Time, optional): Time the sentence was received.
                If timestamp is not specified, the current time is used.
        Returns:
            bool: True if the NMEA string is successfully processed, False if there is an error.
        """
        #if not check_nmea_checksum(nmea_string):
        #    rospy.logwarn("Received a sentence with an invalid checksum. " +
        #                  "Sentence was: %s" % repr(nmea_string))
        #    return False

        parsed_sentence = parse_nmea_sentence(nmea_string)
        #print(parsed_sentence)
        if not parsed_sentence:
            rospy.logdebug(
                "Failed to parse NMEA sentence. Sentence was: %s" %
                nmea_string)
            return False

        if timestamp:
            current_time = timestamp
        else:
            current_time = rospy.get_rostime()
            current_fix = gps_data()

            data = parsed_sentence['GGA']

            fix_type = data['fix_type']

            current_fix.header.stamp = current_time
            current_fix.header.frame_id = frame_id
            latitude = data['latitude']
            if data['latitude_direction'] == 'S':
                latitude = -latitude
            current_fix.latitude = latitude

            longitude = data['longitude']
            if data['longitude_direction'] == 'W':
                longitude = -longitude
            current_fix.longitude = longitude


            # Altitude is above ellipsoid, so adjust for mean-sea-level
            altitude = data['altitude'] + data['mean_sea_level']
            current_fix.altitude = altitude

            current_fix.utm_easting, current_fix.utm_northing, current_fix.zone, current_fix.letter = utm_converter.from_latlon(current_fix.latitude, current_fix.longitude)
            print(current_fix)
            return current_fix
        #else:
        #    return False


def main():
    """Create and run the nmea_serial_driver ROS node.
    Creates a ROS NMEA Driver and feeds it NMEA sentence strings from a serial device.
    ROS parameters:
        ~port (str): Path of the serial device to open.
        ~baud (int): Baud rate to configure the serial device.
    """
    rospy.init_node('nmea_serial_driver')
    pub = rospy.Publisher('gps_data', gps_data)
    rate = rospy.Rate(20)

    serial_port = rospy.get_param('~port', '/dev/ttyACM0')
    serial_baud = rospy.get_param('~baud', 4800)
    frame_id = get_frame_id()

    try:
        GPS = serial.Serial(port=serial_port, baudrate=serial_baud, timeout=2)

        try:
            while not rospy.is_shutdown():
                data = GPS.readline().strip()
                try:
                    cf = add_sentence(data, frame_id)
                    if cf == False:
                        pass
                    else:
                        print(cf)
                        pub.publish(cf)
                        rate.sleep()
                except ValueError as e:
                    rospy.logwarn(
                        "Value error, likely due to missing fields in the NMEA message. "
                        "Error was: %s. Please report this issue at "
                        "github.com/ros-drivers/nmea_navsat_driver, including a bag file with the NMEA "
                        "sentences that caused it." %
                        e)

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