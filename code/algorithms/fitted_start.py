from .random_alg import Random

class FittedStart(Random):
    """
    A class to represent a fitted start algorithm which avoids starting with room overcapicity
    """
    def schedule_courses(self, archive):
        """
        Schedule all activities on a roomslot that is available and is just
        big enough so there is no overcapacity.
        """
        # sort activities on their capacity limit
        activities = sorted(self.schedule.activities, key=lambda activity: activity.capacity, reverse=True)

        # loop over all activities
        for activity in activities: 

            # initiate space left in room counter
            lowest_space_left = float('inf')
            
            # loop over all available roomslots
            for roomslot in archive:
               
               # calculate the space left if the activity would be scheduled in this room
               space_left = roomslot[0].capacity - activity.capacity

               # keep track of best fitting room
               if space_left > 0 and space_left < lowest_space_left:
                   lowest_space_left = space_left
                   best_roomslot = roomslot
            
            # schedule activity in the best fitting room
            self.schedule_activity(activity, best_roomslot, archive)
