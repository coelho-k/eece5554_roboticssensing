;; Auto-generated. Do not edit!


(when (boundp 'gps::gps_data)
  (if (not (find-package "GPS"))
    (make-package "GPS"))
  (shadow 'gps_data (find-package "GPS")))
(unless (find-package "GPS::GPS_DATA")
  (make-package "GPS::GPS_DATA"))

(in-package "ROS")
;;//! \htmlinclude gps_data.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass gps::gps_data
  :super ros::object
  :slots (_header _latitude _longitude _altitude _utm_easting _utm_northing _zone _letter ))

(defmethod gps::gps_data
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:latitude __latitude) 0.0)
    ((:longitude __longitude) 0.0)
    ((:altitude __altitude) 0.0)
    ((:utm_easting __utm_easting) 0)
    ((:utm_northing __utm_northing) 0)
    ((:zone __zone) 0)
    ((:letter __letter) "")
    )
   (send-super :init)
   (setq _header __header)
   (setq _latitude (float __latitude))
   (setq _longitude (float __longitude))
   (setq _altitude (float __altitude))
   (setq _utm_easting (round __utm_easting))
   (setq _utm_northing (round __utm_northing))
   (setq _zone (round __zone))
   (setq _letter (string __letter))
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:latitude
   (&optional __latitude)
   (if __latitude (setq _latitude __latitude)) _latitude)
  (:longitude
   (&optional __longitude)
   (if __longitude (setq _longitude __longitude)) _longitude)
  (:altitude
   (&optional __altitude)
   (if __altitude (setq _altitude __altitude)) _altitude)
  (:utm_easting
   (&optional __utm_easting)
   (if __utm_easting (setq _utm_easting __utm_easting)) _utm_easting)
  (:utm_northing
   (&optional __utm_northing)
   (if __utm_northing (setq _utm_northing __utm_northing)) _utm_northing)
  (:zone
   (&optional __zone)
   (if __zone (setq _zone __zone)) _zone)
  (:letter
   (&optional __letter)
   (if __letter (setq _letter __letter)) _letter)
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; float64 _latitude
    8
    ;; float64 _longitude
    8
    ;; float64 _altitude
    8
    ;; int64 _utm_easting
    8
    ;; int64 _utm_northing
    8
    ;; int64 _zone
    8
    ;; string _letter
    4 (length _letter)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; float64 _latitude
       (sys::poke _latitude (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _longitude
       (sys::poke _longitude (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _altitude
       (sys::poke _altitude (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; int64 _utm_easting
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke _utm_easting (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class _utm_easting) (= (length (_utm_easting . bv)) 2)) ;; bignum
              (write-long (ash (elt (_utm_easting . bv) 0) 0) s)
              (write-long (ash (elt (_utm_easting . bv) 1) -1) s))
             ((and (class _utm_easting) (= (length (_utm_easting . bv)) 1)) ;; big1
              (write-long (elt (_utm_easting . bv) 0) s)
              (write-long (if (>= _utm_easting 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long _utm_easting s)(write-long (if (>= _utm_easting 0) 0 #xffffffff) s)))
     ;; int64 _utm_northing
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke _utm_northing (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class _utm_northing) (= (length (_utm_northing . bv)) 2)) ;; bignum
              (write-long (ash (elt (_utm_northing . bv) 0) 0) s)
              (write-long (ash (elt (_utm_northing . bv) 1) -1) s))
             ((and (class _utm_northing) (= (length (_utm_northing . bv)) 1)) ;; big1
              (write-long (elt (_utm_northing . bv) 0) s)
              (write-long (if (>= _utm_northing 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long _utm_northing s)(write-long (if (>= _utm_northing 0) 0 #xffffffff) s)))
     ;; int64 _zone
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke _zone (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class _zone) (= (length (_zone . bv)) 2)) ;; bignum
              (write-long (ash (elt (_zone . bv) 0) 0) s)
              (write-long (ash (elt (_zone . bv) 1) -1) s))
             ((and (class _zone) (= (length (_zone . bv)) 1)) ;; big1
              (write-long (elt (_zone . bv) 0) s)
              (write-long (if (>= _zone 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long _zone s)(write-long (if (>= _zone 0) 0 #xffffffff) s)))
     ;; string _letter
       (write-long (length _letter) s) (princ _letter s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; float64 _latitude
     (setq _latitude (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _longitude
     (setq _longitude (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _altitude
     (setq _altitude (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; int64 _utm_easting
#+(or :alpha :irix6 :x86_64)
      (setf _utm_easting (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf _utm_easting (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
                  (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))
              (cond ((= b1 -1) b0)
                     ((and (= b1  0)
                           (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))
                      b0)
                    ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))
                    (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))
   ;; int64 _utm_northing
#+(or :alpha :irix6 :x86_64)
      (setf _utm_northing (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf _utm_northing (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
                  (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))
              (cond ((= b1 -1) b0)
                     ((and (= b1  0)
                           (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))
                      b0)
                    ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))
                    (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))
   ;; int64 _zone
#+(or :alpha :irix6 :x86_64)
      (setf _zone (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf _zone (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
                  (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))
              (cond ((= b1 -1) b0)
                     ((and (= b1  0)
                           (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))
                      b0)
                    ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))
                    (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))
   ;; string _letter
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _letter (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(setf (get gps::gps_data :md5sum-) "74ea169e4292230a2f91acbde1213ed4")
(setf (get gps::gps_data :datatype-) "gps/gps_data")
(setf (get gps::gps_data :definition-)
      "std_msgs/Header header

float64 latitude

float64 longitude

float64 altitude

int64 utm_easting

int64 utm_northing

int64 zone

string letter

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
string frame_id

")



(provide :gps/gps_data "74ea169e4292230a2f91acbde1213ed4")


