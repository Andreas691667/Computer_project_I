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
import time as t  # for sleep statements
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import numpy as np

LINEAR_VEL = 0.22
STOP_DISTANCE = 0.2
LIDAR_ERROR = 0.05
# radius of turtlebot is 10 cm and for safety measure LIDAR_ERROR is added.
SAFE_STOP_DISTANCE = STOP_DISTANCE + LIDAR_ERROR 
EMERGENCY_STOP_DISTANCE = 0.15
MAX_ANGLE = 2.84
DEFAULT_TURN_ANGLE = 3.14/2


class Obstacle():
    def __init__(self):
        self._cmd_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        self.obstacle()

    def get_scan(self):
        scan = rospy.wait_for_message('scan', LaserScan)
        scan_filter = []

        left_lidar_samples_ranges = 60
        right_lidar_samples_ranges = 345
        front_lidar_samples_ranges = 15

        front_lidar_samples1 = scan.ranges[0:front_lidar_samples_ranges]
        front_lidar_samples2 = scan.ranges[right_lidar_samples_ranges:360]
        left_lidar_samples = scan.ranges[front_lidar_samples_ranges:left_lidar_samples_ranges]
        right_lidar_samples = scan.ranges[300:right_lidar_samples_ranges]
        front_left_lidar_samples = scan.ranges[14:22]
        front_right_lidar_samples = scan.ranges[338:346]

        scan_filter.append(left_lidar_samples)
        scan_filter.append(front_lidar_samples1)
        scan_filter.append(front_lidar_samples2)
        scan_filter.append(right_lidar_samples)
        scan_filter.append(front_left_lidar_samples)
        scan_filter.append(front_right_lidar_samples)

        return scan_filter

    def obstacle(self):
        twist = Twist()
        turtlebot_moving = True

        def small_turns(dir, angle, vel):
            if(dir == 'left'):
                twist.linear.x = vel
                twist.angular.z = angle
                self._cmd_pub.publish(twist)
                rospy.loginfo('Turning left')
                turtlebot_moving = False

            elif (dir == 'right'):
                twist.linear.x = vel
                twist.angular.z = -angle
                self._cmd_pub.publish(twist)
                rospy.loginfo('Turning right')
                turtlebot_moving = False

        def emergency_check(l):
            # calculate mean of our slices:
            left_distance = np.mean((l[0]))
            front_distance = np.mean(l[1] + l[2])
            right_distance = np.mean(l[3])
            front_left_distance = np.mean(l[4])
            front_right_distance = np.mean(l[5])

            # calculate mean of special case slices
            special_case_right = np.mean(l[3][27:35])
            special_case_left = np.mean(l[0][10:18])

            if (front_distance < EMERGENCY_STOP_DISTANCE and left_distance < EMERGENCY_STOP_DISTANCE):
                small_turns('right', MAX_ANGLE, 0.0)

            elif (front_distance < EMERGENCY_STOP_DISTANCE and right_distance < EMERGENCY_STOP_DISTANCE):
                small_turns('left', MAX_ANGLE, 0.0)

            elif (front_distance < EMERGENCY_STOP_DISTANCE):
                if (left_distance < right_distance):
                    small_turns('right', MAX_ANGLE, 0.0)
                else:
                    small_turns('left', MAX_ANGLE, 0.0)

            elif(special_case_right < SAFE_STOP_DISTANCE and special_case_left < SAFE_STOP_DISTANCE):
                make_180()

            elif(front_left_distance < SAFE_STOP_DISTANCE):
                small_turns('right', MAX_ANGLE, 0.0)

            elif(front_right_distance < SAFE_STOP_DISTANCE):
                small_turns('left', MAX_ANGLE, 0.0)

        # turns 180 degrees to the left
        def make_180():
            twist.linear.x = 0.0
            twist.angular.z = MAX_ANGLE
            self._cmd_pub.publish(twist)
            rospy.loginfo('Turning 180 degrees')
            t.sleep(1.105634)
            turtlebot_moving = False

        # function converts list of tuples to list of lists and then converts zeros to 3.5:
        def non_zeros(l):
            # convert tuples to list
            for i in range(len(l)):
                l[i] = list(l[i])

            # if element zero, set to 3.5
            for i in range(len(l)):
                for j in range(len(l[i])):
                    if l[i][j] == 0:
                        l[i][j] = 3.5

        while not rospy.is_shutdown():

            lidar_distances = self.get_scan()
            non_zeros(lidar_distances)

            # calculate mean of our slices:
            left_distance = np.mean((lidar_distances[0]))
            front_distance = np.mean(lidar_distances[1] + lidar_distances[2])
            right_distance = np.mean(lidar_distances[3])
            front_left_distance = np.mean(lidar_distances[4])
            front_right_distance = np.mean(lidar_distances[5])

            emergency_check(lidar_distances)

            # case 1: obstacle in front
            if (front_distance < SAFE_STOP_DISTANCE + 0.08):
                print('obstacle in front')
                # look ahead:
                if turtlebot_moving:
                    if (right_distance < left_distance):
                        while(front_distance < SAFE_STOP_DISTANCE + 0.08):
                            small_turns('left', 1.44*front_distance **
                                        (-0.29), front_distance/2)
                            front_new = self.get_scan()
                            non_zeros(front_new)
                            emergency_check(front_new)
                            front_distance = np.mean(front_new[1] + front_new[2])

                    elif(left_distance < right_distance):
                        while(front_distance < SAFE_STOP_DISTANCE + 0.08):
                            small_turns('right', 1.44*front_distance **
                                        (-0.29), front_distance/2)
                            front_new = self.get_scan()
                            non_zeros(front_new)
                            emergency_check(front_new)
                            front_distance = np.mean(
                                front_new[1] + front_new[2])

            # case 2: obstacle to the left or right
            elif(left_distance < SAFE_STOP_DISTANCE or right_distance < SAFE_STOP_DISTANCE):
                if turtlebot_moving:
                    if(right_distance < left_distance):
                        small_turns('left', DEFAULT_TURN_ANGLE, 0.1)
                    else:
                        small_turns('right', DEFAULT_TURN_ANGLE, 0.1)

            # case 3: obstacle in "blindspot"
            elif(front_left_distance < SAFE_STOP_DISTANCE+0.15 or front_right_distance < SAFE_STOP_DISTANCE+0.15):
                if turtlebot_moving:
                    if (front_right_distance < front_left_distance):
                        print('blind vinkel hojre')
                        while(front_right_distance < SAFE_STOP_DISTANCE + 0.15):
                            small_turns('left', 0.34*front_right_distance **
                                        (-0.93), 1.7*front_right_distance**2.23)
                            front_right_new = self.get_scan()
                            non_zeros(front_right_new)
                            emergency_check(front_right_new)
                            front_right_distance = np.mean(front_right_new[5])

                    elif(front_left_distance < front_right_distance):
                        print('blind vinkel venstre')
                        while(front_left_distance < SAFE_STOP_DISTANCE + 0.15):
                            small_turns('right', 0.34*front_left_distance **
                                        (-0.93), 1.7*front_left_distance**2.23)
                            front_left_new = self.get_scan()
                            non_zeros(front_left_new)
                            emergency_check(front_left_new)
                            front_left_distance = np.mean(front_left_new[4])

            # case 4: obstacle in both "blindspots"
            elif (front_left_distance < SAFE_STOP_DISTANCE and front_right_distance < SAFE_STOP_DISTANCE):
                print('special case')
                if (right_distance < left_distance):
                    small_turns('left', DEFAULT_TURN_ANGLE, LINEAR_VEL)

                elif(left_distance < right_distance):
                    small_turns('right', DEFAULT_TURN_ANGLE, LINEAR_VEL)

            # case 5: no obstacles => go forward
            else:
                twist.linear.x = LINEAR_VEL
                twist.angular.z = 0.0
                turtlebot_moving = True
                self._cmd_pub.publish(twist)


def main():
    rospy.init_node('turtlebot3_obstacle')
    try:
        obstacle = Obstacle()
    except rospy.ROSInterruptException:
        pass


if __name__ == '__main__':
    main()
