from .hillclimber import Hillclimber
from ..classes.schedule import Schedule

# increase recursion limit for deepcopies
#sys.setrecursionlimit(10**6)

class ExhaustiveClimber(Hillclimber):
    """ 
    Inherits from Hillclimber. 
    Difference: Uses all free slots in course schedule (exhausts schedule space). 

    TODOs:

    - implement add_extra_activity in Algorithm
    - test 
    """

    def __init__(self, empty_schedule : Schedule):
        super().__init__(empty_schedule)
        
        # fill all free slots in schedule 
        self.exhaust_schedule()    
    
    def exhaust_schedule(self):
        print(self.archive)
        # loops over all still vacant room slots in schedule until none free 
            # picks a random activity and splits it (use below function i think)     
            # self.add_extra_activity()
   
