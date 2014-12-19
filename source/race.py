#Author: Nathanael Gordon
#Created: 2014-11-19

import time
from datetime import datetime

class Race:

    def __init__(self, pk = -1, started = None):
        self.pk = pk
        self.racers = []        # a list of lists where the first item is a racer and the second is the position
        self.timeStarted = started
        if self.timeStarted is None:
            self.timeStarted = datetime.now()
            
    def __lt__(self, other):
        if self.timeStarted < other.timeStarted:
            return True
    
    # Add the passed racer to the list of racers
    def addRacer(self, racer, position = 0):
        self.racers.append([racer, position])
        
    # Remove the passed racer
    def removeRacer(self, racer):
        for racerL in self.racers:
            if racerL[0].pk == racer[0].pk:
                self.racers.remove(racerL)
                
    # Replace the first racer with the second racer
    def replaceRacer(self, racer1, racer2):
        for racerL in self.racers:
            if racerL[0].pk == racer1.pk:
                racerL[0] = racer2
                
    # Returns the number of points the racer has (-1 is returned if racer was not in race)
    def getPointsForRacer(self, racer, maxRacers):
        for racerL in self.racers:
            if racerL[0].pk == racer.pk:
                return maxRacers + 1 - racerL[1]
        
        return -1
        
    # Set the position of that the racer return false if the racer is not in this race
    def setPositionForRacer(self, racer, position):
        for racerL in self.racers:
            if racerL[0].pk == racer.pk:
                racerL[1] = position
                return True
        
        return False
    
    def toString(self):
        stringRep = "PK: {0}, {1} Racers: ".format(self.pk, self.timeStarted.isoformat())
        
        for racer in self.racers:
            stringRep += "{0} pos: {1}, ".format(racer[0].racerName, racer[1])
        return stringRep
    
    def __lt__(self, other):
        return self.timeStarted < other.timeStarted
