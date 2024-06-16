from .random_alg import Random

class BusyRandom(Random):
    """ 
    Inherits from Random schedule. Difference: Activities are selected on a busy-comes-first 
    basis and not randomly. 

    TODOs: 

    - Implement get_busy_index()
    - Implement sort_activities_by_busy()
    
     """
    
    # TODO: remove random seed comments
    
    # random.seed(1)

    def __init__(self, empty_schedule) -> None:
        super().__init__(empty_schedule)

    def get_busy_index(self):
        """ Labels activities by - define all criteria - into busy and not busy"""
        pass
        # loop over courses
            # get number activities in course: int 
            # get number students enrolled in course: int  
            # get number courses of each enrolled student: int 
            # sum all up to index  
            # add busy index label to course 
        
        
    def sort_activities_by_busy(self):
        """ Sorts activities by index of busyness."""
        pass
        # sort courses by busyest index 

    def schedule_courses(self, archive):
        """
        Schedule sorted activities on a random roomslot that is available.
        """
        # random.seed(1)
        
        # sort activities so that busy ones are scheduled first  
        self.sort_activities_by_busy(self.schedule.activities)

        # loop over all activities
        for activity in self.schedule.activities:  
           roomslot = self.pick_random_roomslot(archive)
           self.schedule_activity(activity, roomslot, archive)



