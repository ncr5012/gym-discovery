import gym
from gym import error, spaces, utils
from gym.utils import seeding

import numpy as np

import random
from typing import List

#Stop notes 3/28 - great progress, built out an enviornment that allows probability based transitions between two states
#For tommorrow, need to fully build out the enviornment to 5 states. At that point, its ready for an agent!
#the simpliest nontrivial solution looks in reach! 
#gave it another shot 3/28 - enviornment appears to be working. looks like discovery is pretty hopeless with randomly
#picking actions. I think we need to introduce a little serendipity! 
#3/29 - optimized the enviornment for roughly a 1% success rate
#3/30 - attempted to construct the RL agent. Successfully implemented the NN and ptan agent. Failed to implement the
#experience source and optimizer. Next step is to implement the experience source. It is likely not working because
#the underlying enviornment is not structured correctly


class discoveryEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    
    #This block says initiates the self and says how long it has to live
    def __init__(self):
        self.steps_left = 600
        self.observation_state = 1

        #this block is the observation space (0 = UCO, 1 = OF, 2 = NUCO, 3 = VB, 4 = IB)
    def get_observation(self) -> float:
        return self.observation_state

        #this block is the action space (0 = wait, 1 = commit)
    def get_actions(self) -> List[int]:
        return [0, 1]

    #this block defines the end condition (time has run out)
    def is_done(self) -> bool:
        return self.steps_left <= 0

        #this block defines what happens on a given action. 
    def action(self, observation:int, action: int) -> float:
        if self.is_done():
            raise Exception("Game is over")
            
          #  all OF transitions
        elif observation == 1 and action == 0:
            self.steps_left -= 1
            if random.random() <= .5:
                self.observation_state = 0
                #print('W - OF to UCO')
            else:
                self.observation_state = 2
                #print('W - OF to NUCO')
            return 0
        
        elif observation == 1 and action == 1:
            self.steps_left -= 1
            if random.random() <= .99:
                self.observation_state = 4
                #print('C - OF to IB')
            else:
                self.observation_state = 3
                #print('C - OF to VB')
            return 0
        
        # UCO transitions 
        elif observation == 0 and action == 0:
            self.steps_left -= 6
            if random.random() <= .5:
                self.observation_state = 1
                #print('W - UCO to OF')
            else:
                self.observation_state = 2
                #print('W - UCO to NUCO')
            return 0
        
        elif observation == 0 and action == 1:
            self.steps_left -= 1
            if random.random() <= .98:
                self.observation_state = 4
                #print('C - UCO to IB')
            else:
                self.observation_state = 3
                #print('C - UCO to VB')
            return 0
        
        #NUCO transitions
        elif observation == 2 and action == 0:
            self.steps_left -= 6
            self.observation_state = 1
            #print('W - NUCO to OF')
            return 0
        
        elif observation == 2 and action == 1:
            self.steps_left -= 1
            self.observation_state = 4
            #print('C - NUCO to IB')
            return 0
        
        #VB transitions
        elif observation == 3 and action == 0:
                self.steps_left -= 1
                self.observation_state = 2
                #print('W - VB to NUCO')
                return 0
        
        #high probability indicates that things go wrong out of our control
        elif observation == 3 and action == 1:
            self.steps_left -= 120
            if random.random() <= .95:
                self.observation_state = 4
                #print('C - VB to IB')
                return 0
            else:
                self.observation_state = 1
                #print('C - VB to OF')
                return 100
        
        #IB transitions
        elif observation == 4 and action == 0:
            self.steps_left -= 1
            if random.random() <= .95:
                self.observation_state = 0
                #print('W - IB to UCO')
            else:
                self.observation_state = 1
                #print('W - IB to OF')
            return 0
        
        elif observation == 4 and action == 1:
            self.steps_left -= 60
            if random.random() <= .99:
                self.observation_state = 1
                #print('C - IB to OF')
                return 0
            else:
                self.observation_state = 3
                #print('C - IB to VB')
                return 0
