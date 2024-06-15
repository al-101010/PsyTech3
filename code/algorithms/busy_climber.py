from .hillclimber import Hillclimber
from .busy_random import BusyRandom

# increase recursion limit for deepcopies
sys.setrecursionlimit(10**6)

class BusyClimber(Hillclimber):
    """ 
    Inherits from Hillclimber. 
    Uses BusyRandom instead of Random to initialise schedule. 
    Difference: Sorts courses by busiest first (so not randomly) before climbing. 

    TODOs:

    - when BusyRandom is ready: test 
    """

    def __init__(self, empty_schedule : Schedule):
        super().__init__(empty_schedule)
        self.busy_start = BusyRandom(empty_schedule)
        self.schedule = self.busy_start.schedule
        self.archive = self.busy_start.archive

   
