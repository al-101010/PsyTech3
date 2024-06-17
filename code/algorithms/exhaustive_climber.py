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
    - figure out where to put the room capacity constraints method. 
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

    def switch_activities(self):
        """
        Experimental variation on method in Algorithm Class: 
        - only switches if no resulting overcapacity!  

        Switches the activities from two randomly chosen roomslots. Activity may
        also be None.
        """
        switch_enable = False 

        while not switch_enable:
        
            # store room, day, and time of roomslots
            random_roomslot1, random_roomslot2 = self.pick_roomslots_to_switch()
            room_1, day_1, time_1 = self.get_roomslot_info(random_roomslot1)
            room_2, day_2, time_2 = self.get_roomslot_info(random_roomslot2)

            # save activities in roomslots
            activity_1 = room_1.schedule[day_1][time_1]
            activity_2 = room_2.schedule[day_2][time_2]

            # if activity is Activity instance, schedule instance
            if activity_1:
                activity_1.schedule(room_2, day_2, time_2)
            if activity_2:
                activity_2.schedule(room_1, day_1, time_1)
            
            print(f' students in activity 2 {len(activity_2.students)} capacity room 1 {room_1.capacity}')
            print(f' students in activity 1 {len(activity_1.students)} capacity room 2 {room_2.capacity}')

            # make sure capacity is not violated 
            if len(activity_2.students) < room_1.capacity and len(activity_1.students) < room_2.capacity: 
                
                switch_enable = True 

            # switch the activities to the other roomslot in room instance
            room_1.schedule[day_1][time_1] = activity_2
            room_2.schedule[day_2][time_2] = activity_1

            self.update_student_schedules()
        

        
    
   
