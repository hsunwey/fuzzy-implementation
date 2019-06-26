#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from math import cos, sin, radians, sqrt
import random


# In[7]:


def x_distance(angle):
    rad = radians(angle)
    g = 9.81 # m/s square
    vx0 = v0*cos(rad)

    # time of flight
    t = 2*v0*sin(rad)/g

    # H distance
    x = vx0*t
    max_dist = int(x)
    return max_dist

def y_distance(angle):
    rad = radians(angle)
    g = 9.81 # m/s square

    y = v0 * sin(rad)**2
    return int(y)

def time(angle):
    rad = radians(angle)
    g = 9.81 # m/s square
    t = 2*v0*sin(rad)/g
    return t


# In[8]:


v0 = 30       # m/s
max_dist = x_distance(45)
human_dist = random.randint(int(max_dist*2/3), max_dist)

# print
print('Initial velocity: %d m/s' % v0)
print('Target distance: %d m' % human_dist)
print()
print('Time of flight: %2.2f s' % time(45))
print('Horizontal range: %d m' % x_distance(45))
print('Vertical range: %d m' % y_distance(45))
print('=========================')


# In[9]:


fall_range = max_dist - human_dist
fall_dist = ctrl.Antecedent(np.arange(-fall_range, fall_range+1, 1), 'fall_dist')

# Membership function
fall_dist.automf(5)
fall_dist.view()


# In[10]:


#fall_range = max_dist - human_dist
#print(fall_range)
#print(human_dist + fall_range)
#print(human_dist - fall_range)


# In[11]:


result = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'result')

# Very Small, Small, Medium, Big, Very Big
univ = result.universe
result['too near'] = fuzz.trimf(univ, [0, 0.1, 0.3])
result['near'] = fuzz.trimf(univ, [0.1, 0.3, 0.5])
result['hit'] = fuzz.trimf(univ, [0.3, 0.5, 0.7])
result['far'] = fuzz.trimf(univ, [0.5, 0.7, 0.9])
result['too far'] = fuzz.trimf(univ, [0.7, 0.9, 1])

result.view()


# #### Fuzzy rules
# 
# If the queue number of current red light phase is very short and the light duration of current red light phase is very short, so the urgency degree of current red light phase is very small.

# In[12]:


rule1 = ctrl.Rule(fall_dist['poor'], result['too near'])
rule2 = ctrl.Rule(fall_dist['mediocre'], result['near'])
rule3 = ctrl.Rule(fall_dist['average'], result['hit'])
rule4 = ctrl.Rule(fall_dist['decent'], result['far'])
rule5 = ctrl.Rule(fall_dist['good'], result['too far'])

rule1.view()


# #### Control System Creation and Simulation

# In[13]:


result_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
result_degree = ctrl.ControlSystemSimulation(result_ctrl)


# In[23]:


def shoot(my_angle):
    print('Current angle: %d' % my_angle)
    my_shoot = x_distance(my_angle)
    result_degree.input['fall_dist'] = my_shoot - human_dist

    # Crunch the numbers
    result_degree.compute()
    end = result_degree.output['result']
    print(end)
#     result.view(sim=result_degree)
    
    if 0.4 <= end <= 0.6:
        print('Hit!')
        return True
    elif end > 0.6:
        print("Need to decrease angle." + '\n')
        return shoot(my_angle-1)
    else:
        print("Need to increase angle." + '\n')
        return shoot(my_angle-1)


# In[24]:


shoot(45)


# In[ ]:





# In[ ]:





# In[ ]:




