'''
The last model had many problems with complexity and overfitting.
This is a simpler model that tries to reward the car for staying in the center of the track and going fast.

This version adds the consideration of next waypoint and previous waypoint to the reward function.
'''

import math

# List of straigh waypoints for the current track (re:Invent 2018)
straight_waypoints=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,43,44,45,46,47,48,49,50,56,57,58,59,60,61,62,63,64,71,72,73,74,75,76,77,78,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,112,113,114,115,116,117]

def reward_function(params):
    # Read input variables
    all_wheels_on_track = params['all_wheels_on_track']
    speed = params['speed']
    heading = params['heading']
    steering_angle = abs(params['steering_angle'])
    distance_from_center = params['distance_from_center']
    steps = params['steps']
    progress = params['progress']
    is_offtrack = params['is_offtrack']
    waypoints = params['waypoints']
    
    # Set the weights of each variable
    all_wheels_on_track_weight = 1
    speed_weight = 10
    steering_weight = 2
    center_weight = 1
    progress_weight = 5
    heading_weight = 1.5
    steps_penalty = 0.5
    high_speed_penalty = 0.5
    off_track_penalty = 100

    # Thresholds
    direction_threshold = 10.0
    
    # Initialize the reward
    reward = 1e-3
    
    # Give a high reward if the car stays on track and goes fast
    if all_wheels_on_track and not is_offtrack:
        # Reward if curves are taken slower than straight sections
        if params['closest_waypoints'][1] in straight_waypoints:
            reward += all_wheels_on_track_weight * speed_weight * speed
        else: 
            if speed < 1.6:
                reward += all_wheels_on_track_weight * speed_weight * speed
            else:
                reward += all_wheels_on_track_weight * speed_weight * speed * high_speed_penalty
        # Penalize the steering angle to encourage smooth driving
        reward -= steering_weight * steering_angle
        # Reward the car for staying close to the centerline
        reward += center_weight * (1 - (distance_from_center / params['track_width']))
        # Reward progress made in the race
        reward += progress_weight * progress
    else:
        # Penalize the car heavily for going off track
        reward -= off_track_penalty

    # Penalize for taking too many steps to complete the lap
    if steps > 300:
        reward *= steps_penalty

    # Reward for completing the lap with less than 450 steps
    if progress == 100:
        if steps < 450:
            reward += 100
        else:
            reward *= 0.5

    # Reward the car for heading to the next waypoint
    next_waypoint = waypoints[params['closest_waypoints'][1]]
    prev_waypoint = waypoints[params['closest_waypoints'][0]]
    track_direction = math.atan2(next_waypoint[1] - prev_waypoint[1], next_waypoint[0] - prev_waypoint[0])
    track_direction = math.degrees(track_direction)
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff
    if direction_diff < direction_threshold:
        reward *= 1.5

    return reward