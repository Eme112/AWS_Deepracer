'''
The last model had many problems with complexity and overfitting.
This is a simpler model that tries to reward the car for staying in the center of the track and going fast.

This version adds the consideration of the 3 next waypoints and previous waypoint to the reward function.
'''

import math

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
    steering_weight = 1
    center_weight = 1
    progress_weight = 3
    heading_weight = 1.5
    steps_penalty = 0.5
    off_track_penalty = 100

    # Thresholds
    direction_threshold = 10.0
    
    # Initialize the reward
    reward = 1e-3
    
    # Give a high reward if the car stays on track and goes fast
    if all_wheels_on_track and not is_offtrack:
        reward += all_wheels_on_track_weight * speed_weight * speed
        
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
                    reward *= heading_weight
    
    return reward