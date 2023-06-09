'''
First model for rewarding function.
General functions used:
* wheelsOnTrack() - returns an award value from -1.0 to 1.0 depending if the car is on the track or not.
* expectedOrientation(), 0.1-3.0 - returns a higher reward value if the car is oriented in the direction of the next waypoint.
* distanceFromCenter(), 0.0-3.0 - returns a higher reward value if the car is closer to the center of the track.
* speedReward(), 0.0-3.7 - returns a higher reward value if the car is going faster.
* steeringReward(), 0.0-2.0 - returns a higher reward value if the car is steering less.

In this version:
* More speed reward
'''

import math

# Thresholds
direction_threshold = 15.0

# List of straight waypoints for the current track (re:Invent 2018)
straight_waypoints=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,43,44,45,46,47,48,49,50,56,57,58,59,60,61,62,63,64,71,72,73,74,75,76,77,78,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,112,113,114,115,116,117]

# List of curve waypoints for the current track (re:Invent 2018)
curve_waypoints = [22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 65, 66, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 104, 105, 106, 107, 108, 109]

# List of waypoints where the car should open to the right
open_right_waypoints = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 53, 54, 55, 79]

# List of waypoints where the car should open to the left
open_left_waypoints = [34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 87, 88, 89, 90, 91, 92, 93, 94, 95, 104, 105, 106, 107, 108, 109, 110, 111]

def reward_function(params):
    # Read input parameters    
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    speed = params['speed']
    steps = params['steps']
    is_offtrack = params['is_offtrack']
    track_width = params['track_width']
    heading = params['heading']
    steering = abs(params['steering_angle']) # Only need the absolute steering angle
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    is_left_of_center = params['is_left_of_center']

    #### REWARD IF HEADING EXPECTED ORIENTATION ###
    num_of_correct_headings = 0
    heading_reward = 0.0
    for i in range(3):
        # Reward the car for heading in the right direction
        next_waypoint_idx = params['closest_waypoints'][1] + i + 2
        if next_waypoint_idx < len(waypoints):
            next_waypoint = waypoints[next_waypoint_idx]
            prev_waypoint_idx = params['closest_waypoints'][0] + i
            if prev_waypoint_idx < len(waypoints):
                prev_waypoint = waypoints[prev_waypoint_idx]
                track_direction = math.atan2(next_waypoint[1] - prev_waypoint[1], next_waypoint[0] - prev_waypoint[0])
                track_direction = math.degrees(track_direction)
                direction_diff = abs(track_direction - heading)
                if direction_diff > 180:
                    direction_diff = 360 - direction_diff
                if direction_diff < direction_threshold:
                    heading_reward += 2.0
                    num_of_correct_headings += 1
    correct_heading_ratio = num_of_correct_headings / 3.0

    if closest_waypoints[1] in open_right_waypoints:
        if not is_left_of_center:
            positioning_reward = 6 * correct_heading_ratio
    elif closest_waypoints[1] in open_left_waypoints:
        if is_left_of_center:
            positioning_reward = 6 * correct_heading_ratio
    else: 
        # Reward the car for staying close to the centerline
        positioning_reward = 6 * (1 - (distance_from_center / track_width))
    ### REWARD IF CAR IS CLOSE TO CENTER IN A STRAIGHT WAYPOINT ###
    ### REWARD IF CAR IS GOING FAST ###
    if not (closest_waypoints[0]) in curve_waypoints:
        speed_reward = 6 * (speed / 3.6) ** 2
    else:
        if speed < 2.8:
            speed_reward = 6 * (speed / 3.6) ** 2
        else:
            speed_reward = 2 * (speed / 3.6) ** 2

    ### REWARD IF CAR IS STEERING LESS ###  
    steering_reward = 2 * (1.0 - (steering / 30.0) ** 2)

    ### TOTAL REWARD ###
    reward = heading_reward + positioning_reward + speed_reward + steering_reward

    ### PENALTY IF CAR IS NOT ON TRACK ###
    if not all_wheels_on_track or is_offtrack:
        reward = 1e-3

    return float(reward)