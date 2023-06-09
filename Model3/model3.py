'''
The last model had many problems with complexity and overfitting.
This is a simpler model that tries to reward the car for staying in the center of the track and going fast.
Different changes are going to be applied to this model to see what improves the performance of the car.
'''

def reward_function(params):
    # Read input variables
    all_wheels_on_track = params['all_wheels_on_track']
    speed = params['speed']
    steering_angle = abs(params['steering_angle'])
    distance_from_center = params['distance_from_center']
    steps = params['steps']
    progress = params['progress']
    is_offtrack = params['is_offtrack']
    
    # Set the weights of each variable
    all_wheels_on_track_weight = 1
    speed_weight = 10
    steering_weight = 1
    center_weight = 1
    progress_weight = 3
    steps_penalty = 0.5
    off_track_penalty = 100
    
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
    
    return reward