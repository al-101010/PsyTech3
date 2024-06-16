from .hillclimber import Hillclimber
from ..classes.schedule import Schedule
import copy 
import random 

class ExhaustiveClimber(Hillclimber):
    """ 
    Inherits from Hillclimber. 
    Difference: Uses all free slots in course schedule (exhausts schedule space). 

    TODOs:
    - test 
    """

    def __init__(self, empty_schedule : Schedule):
        super().__init__(empty_schedule)

        # fill all free slots in schedule 
        self.exhaust_schedule()  

    
    def exhaust_schedule(self):
        """ 
        If there are any rooms and timeslots still free, creates new groups for random
        activities and assigns them a new room. Relocates students to the new room.  

        TODO: 
        - need to exchange self.archive.remove with self.remove_roomslot() - for that 
        first self.remove_roomslot() needs to move to algorithm from random_alg

        """

        # loops over all still vacant room slots in schedule until none free
        while len(self.archive) > 0:
            
            # pick random room from still available 
            room, day, time = random.choice(self.archive)
            
            # make activity 
            self.add_extra_activity(room, day, time)
 
            # remove room from still available 
            self.archive.remove((room, day, time))

        

        
    
   
