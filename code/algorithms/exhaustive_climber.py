from .hillclimber import Hillclimber
from ..classes.schedule import Schedule
import copy 

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
        """

        # make deepcopy of archive as is now 
        archive_copy = copy.deepcopy(self.archive)

        # loops over all still vacant room slots in schedule until none free
        # change to while loop or use deepcopy 
        for slot in archive_copy:
            self.add_extra_activity(slot[0], slot[1], slot[2])
   
