from .random_alg import Random

class FittedStart(Random):

    def schedule_courses(self, archive):
        """
        Schedule all activities on a random roomslot that is available.
        """
        activities = sorted(self.schedule.activities, key=lambda activity: activity.capacity, reverse=True)


        # loop over all activities
        for activity in activities:  
            lowest_space_left = float('inf')
            for roomslot in archive:
               space_left = roomslot[0].capacity - activity.capacity
               if space_left > 0 and space_left < lowest_space_left:
                   lowest_space_left = space_left
                   best_roomslot = roomslot
            self.schedule_activity(activity, best_roomslot, archive)
