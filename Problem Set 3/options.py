# This file contains the options that you should modify to solve Question 2

# IMPORTANT NOTE:
# Comment your code explaining why you chose the values you chose.
# Uncommented code will be penalized.





# discount_factor: close to 0 -> future rewards are ignored (+1)
#                  close to 1 -> future rewards are highly valued (+10)

# Noise: close to 0 -> agent takes shorter but riskier paths
#        close to 1 -> highly stocastic (agent avoids risky areas like -10)

# Living reward: > 0 -> avoid terminal states so take longer paths
#                < 0 -> reach a terminal state quickly
def question2_1():
    #TODO: Choose options that would lead to the desired results 
    # noise = 0 to make the agent not afraid to take risky short path
    # low discount factor to make future rewards ignored so go to near low reward (+1)
    # living reward = -1 to be penalized for moving alot and want reach the terminal state as quickly
    return {
        "noise": 0,
        "discount_factor": 0.2,
        "living_reward": -1
    }

def question2_2():
    #TODO: Choose options that would lead to the desired results
    # adding some noise to not go into risky path
    # Slightly increase discount factor to consider short-term rewards
    # living reward = -0.3 to encourage shorter (not stuck forever) but also safe paths in the same time
    return {
        "noise": 0.2,
        "discount_factor": 0.4,
        "living_reward": -0.3
    }

def question2_3():
    #TODO: Choose options that would lead to the desired results
    # noise = 0 to make the agent not afraid to take risky short path
    # high discount factor to make future rewards highly valued so go to far high reward (+10)
    # living reward = -1 to be penalized for moving alot and want reach the terminal state as quickly
    return {
        "noise": 0,
        "discount_factor": 1,
        "living_reward": -1
    }

def question2_4(): 
    #TODO: Choose options that would lead to the desired results
    # adding some noise to not go into risky path
    # living reward = -0.3 to encourage shorter (not stuck forever) but also safe paths in the same time
        return {
        "noise": 0.2,
        "discount_factor": 1,
        "living_reward": -0.3
    }

def question2_5():
    #TODO: Choose options that would lead to the desired results
    # living reward = large positive value larger than any terminal state reward to make the robot doen't want to finish
    return {
        "noise": 0,
        "discount_factor": 0.2,
        "living_reward": 100
    }

def question2_6():
    #TODO: Choose options that would lead to the desired results
    # living reward = large negative value larger than any terminal state reward to make the robot trying to finish in the shortest time possible
    return {
        "noise": 0,
        "discount_factor": 1,
        "living_reward": -100
    }