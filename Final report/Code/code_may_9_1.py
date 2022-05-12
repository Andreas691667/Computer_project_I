#!/usr/bin/env python
#################################################################################
# Copyright 2018 ROBOTIS CO., LTD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#################################################################################

# Authors: Gilbert #

import rospy
import time as t
import math
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import random
import numpy as np

LINEAR_VEL = 0.13
STOP_DISTANCE = 0.2
LIDAR_ERROR = 0.05
SAFE_STOP_DISTANCE = STOP_DISTANCE + LIDAR_ERROR
MAX_ANGLE = 1.0


class Obstacle():
    def __init__(self):
        self._cmd_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        self.obstacle()

    def get_scan(self):
        scan = rospy.wait_for_message('scan', LaserScan)
        scan_filter = []

        samples = len(scan.ranges)  # The number of samples is defined in
        # turtlebot3_<model>.gazebo.xacro file,
        # the default is 360.
        samples_view = 120          # 1 <= samples_view <= samples

        if samples_view > samples:
            samples_view = samples

        if samples_view is 1:
            scan_filter.append(scan.ranges[0])

        else:
            left_lidar_samples_ranges = 60
            right_lidar_samples_ranges = 345
            front_lidar_samples_ranges = 15

            front_lidar_samples1 = scan.ranges[0:front_lidar_samples_ranges]
            front_lidar_samples2 = scan.ranges[right_lidar_samples_ranges:360]
            left_lidar_samples = scan.ranges[front_lidar_samples_ranges:left_lidar_samples_ranges]
            right_lidar_samples = scan.ranges[300:right_lidar_samples_ranges]
#	    print(test)
          #  print(right_lidar_samples)
          #  print(front_lidar_samples2)

            scan_filter.append(left_lidar_samples)
            scan_filter.append(front_lidar_samples1)
            scan_filter.append(front_lidar_samples2)
            scan_filter.append(right_lidar_samples)

#        for i in range(samples_view):
 #           if scan_filter[i] == float('Inf'):
  #              scan_filter[i] = 3.5
   #         elif math.isnan(scan_filter[i]):
    #            scan_filter[i] = 1

        return scan_filter

    def obstacle(self):
        twist = Twist()
        turtlebot_moving = True
        COLLISION_COUNTER = 0
        COLLISION_DISTANCE = 0.05
        # 0 for right, 1 for left

        def small_turns(dir, angle):
            if(dir == 'left'):
                twist.linear.x = 0.1
                twist.angular.z = angle
                self._cmd_pub.publish(twist)
                rospy.loginfo('Turning left')
                turtlebot_moving = False
            elif (dir == 'right'):
                twist.linear.x = 0.1
                twist.angular.z = -angle
                self._cmd_pub.publish(twist)
                rospy.loginfo('Turning right')
                turtlebot_moving = False

        while not rospy.is_shutdown():

            lidar_distances = self.get_scan()

            left_distance = np.mean((lidar_distances[0]))
            front_distance = np.mean(lidar_distances[1] + lidar_distances[2])
            right_distance = np.mean(lidar_distances[3])

            if(left_distance == 0.0):
                left_distance = 3.5
            if(right_distance == 0.0):
                right_distance = 3.5
            if(front_distance == 0.0):
                front_distance = 3.5

        #	turn_angle = MAX_ANGLE - min(left_distance, right_distance, front_distance)
            turn_angle = 3.14/2

           # print('left =', left_distance)
           # print('right =', right_distance)
           # print('front =', front_distance)

            if (right_distance < SAFE_STOP_DISTANCE and left_distance < SAFE_STOP_DISTANCE and front_distance < SAFE_STOP_DISTANCE):
                if turtlebot_moving:
                    twist.linear.x = -LINEAR_VEL
                    twist.angular.z = 0.0
                    self._cmd_pub.publish(twist)
                    rospy.loginfo('Turning backwards for 1 second')
                    t.sleep(2.0)
                    twist.linear.x = 0.0
                    twist.angular.z = 3.14/2
                    self._cmd_pub.publish(twist)
                    rospy.loginfo('Turning 180 degrees')
                    t.sleep(1.0)
                    turtlebot_moving = False

#					while(right_distance < SAFE_STOP_DISTANCE or left_distance < SAFE_STOP_DISTANCE):
#						while(right_distance < SAFE_STOP_DISTANCE and left_distance < SAFE_STOP_DISTANCE):
#							small_turns(1)
#							twist.linear.x = -0.10
#							twist.angular.z = 0.0
#							self._cmd_pub.publish(twist)
#							rospy.loginfo('Continue turning backwards')
#							turtlebot_moving = False
#							break

#						if (right_distance < SAFE_STOP_DISTANCE):
#							small_turns(1)
#							break
#						else:
#							small_turns(0)
#							break
            elif (front_distance < SAFE_STOP_DISTANCE + 0.05):
                if turtlebot_moving:
                    if (right_distance < left_distance):
                        small_turns('left', turn_angle + 0.2)
                    elif(left_distance < right_distance):
                        small_turns('right', turn_angle + 0.2)

            elif(left_distance < SAFE_STOP_DISTANCE or right_distance < SAFE_STOP_DISTANCE):
                if turtlebot_moving:
                    if(right_distance < left_distance):
                        small_turns('left', turn_angle)
                    else:
                        small_turns('right', turn_angle)

        #	elif (left_distance < SAFE_STOP_DISTANCE):
                 #      		 if turtlebot_moving:
        #			small_turns('right', turn_angle)

                 #       elif (right_distance < SAFE_STOP_DISTANCE):
                  #  		 if turtlebot_moving:
        #			small_turns('left', turn_angle)

            else:
                twist.linear.x = LINEAR_VEL
                twist.angular.z = 0.0
                turtlebot_moving = True
                self._cmd_pub.publish(twist)

            if(min(lidar_distances) < COLLISION_DISTANCE):
                COLLISION_COUNTER += 1
                print('Number of collision:', COLLISION_COUNTER)


def main():
    rospy.init_node('turtlebot3_obstacle')
    try:
        obstacle = Obstacle()
    except rospy.ROSInterruptException:
        pass


if __name__ == '__main__':
    main()
