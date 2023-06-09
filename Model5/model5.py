"""
Focuses on opening to curves.
"""

import math

# List of straight waypoints for the current track (re:Invent 2018)
straight_waypoints=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,43,44,45,46,47,48,49,50,56,57,58,59,60,61,62,63,64,71,72,73,74,75,76,77,78,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,112,113,114,115,116,117]

# List of curve waypoints for the current track (re:Invent 2018)
curve_waypoints = [22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 65, 66, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 104, 105, 106, 107, 108, 109]

# List of waypoints where the car should open to the right
open_right_waypoints = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 53, 54, 55, 79]

# List of waypoints where the car should open to the left
open_left_waypoints = [34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 87, 88, 89, 90, 91, 92, 93, 94, 95, 104, 105, 106, 107, 108, 109, 110, 111]

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
    closest_waypoints = params['closest_waypoints']
    is_left_of_center = params['is_left_of_center']
    
    # Set the weights of each variable
    all_wheels_on_track_weight = 2
    speed_weight = 10
    steering_weight = 2
    center_weight = 5
    opening_weight = 6
    progress_weight = 7
    steps_penalty = 0.9
    high_speed_penalty = 0.2
    off_track_penalty = 0.01
    
    # Thresholds
    direction_threshold = 10.0
    
    # Initialize the reward
    reward = 1

    num_of_correct_headings = 0
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
                    reward *= 1 + (i + 1) * 0.15
                    num_of_correct_headings += 1
    correct_heading_ratio = num_of_correct_headings / 3
    
    # Give a high reward if the car stays on track and goes fast
    if all_wheels_on_track and not is_offtrack:
        # Reward if curves are taken slower than straight sections
        if not (closest_waypoints[0]) in curve_waypoints:
            reward *= all_wheels_on_track_weight * speed_weight * speed
        else: 
            if speed < 2.8:
                reward *= all_wheels_on_track_weight * speed_weight * speed
            else:
                reward *= all_wheels_on_track_weight * speed_weight * speed * high_speed_penalty
        # Penalize the steering angle to encourage smooth driving
        reward *= steering_weight * (1 - steering_angle / 30)
        # Reward progress made in the race
        reward += progress_weight * progress
        # Reward the car for opening to the right direction
        if closest_waypoints[1] in open_right_waypoints:
            if not is_left_of_center:
                reward *= opening_weight * correct_heading_ratio
        elif closest_waypoints[1] in open_left_waypoints:
            if is_left_of_center:
                reward *= opening_weight * correct_heading_ratio
        else: 
            # Reward the car for staying close to the centerline
            reward *= center_weight * (1 - (distance_from_center / params['track_width']))
    else:
        # Penalize the car heavily for going off track
        reward *= off_track_penalty

    # Penalize for taking too many steps to complete the lap
    if steps > 185:
        reward *= steps_penalty

    # Reward for completing the lap with less than 160 steps
    if progress == 100:
        if steps < 180:
            reward *= 2
        else:
            reward *= 0.5

    return reward