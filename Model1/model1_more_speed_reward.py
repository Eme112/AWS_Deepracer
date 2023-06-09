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

# Constants
HEADING_THRESHOLD_1 = 10.0
HEADING_THRESHOLD_2 = 20.0
HEADING_THRESHOLD_3 = 30.0

# List of straigh waypoints for the current track (re:Invent 2018)
straight_waypoints=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,43,44,45,46,47,48,49,50,56,57,58,59,60,61,62,63,64,71,72,73,74,75,76,77,78,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,112,113,114,115,116,117]

def reward_function(params):
    # Read input parameters    
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    speed = params['speed']
    steps = params['steps']
    track_width = params['track_width']
    heading = params['heading']
    steering = abs(params['steering_angle']) # Only need the absolute steering angle
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']

    #### REWARD IF HEADING EXPECTED ORIENTATION ###
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]
    
    # Calculate the expected heading based on the closest waypoints
    expected_heading = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    expected_heading = math.degrees(expected_heading)

    # Calculate the difference between the track heading and the current heading
    heading_diff = abs(expected_heading - heading)

    heading_reward = 0.1
    if heading_diff < HEADING_THRESHOLD_1:
        heading_reward = 3.0
    elif heading_diff < HEADING_THRESHOLD_2:
        heading_reward = 2.0
    elif heading_diff < HEADING_THRESHOLD_3:
        heading_reward = 1.0

    ### REWARD IF CAR IS CLOSE TO CENTER IN A STRAIGHT WAYPOINT ###
    ### REWARD IF CAR IS GOING FAST ###
    if closest_waypoints[0] in straight_waypoints:
        close_to_center_reward = 3 * (1.0 - (distance_from_center / (track_width / 2.0)))
        speed_reward = 6 * (speed / 3.6) ** 2
    else:
        close_to_center_reward = 1.0
        speed_reward = 1.0

    ### REWARD IF CAR IS STEERING LESS ###  
    steering_reward = 2 * (1.0 - (steering / 30.0) ** 2)

    ### TOTAL REWARD ###
    reward = heading_reward + close_to_center_reward + speed_reward + steering_reward

    ### PENALTY IF CAR IS NOT ON TRACK ###
    if not all_wheels_on_track:
        reward = 1e-3

    return float(reward)