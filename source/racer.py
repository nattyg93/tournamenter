#Author: Nathanael Gordon
#Created: 2014-11-19

import time
from datetime import datetime

class Racer:

    def __init__(self, racerName, pk = -1, score = 0, created = None):
        self.pk = pk
        self.score = score
        self.racerName = racerName
        self.created = created
        if self.created is None:
            self.created = datetime.now()
            
    # Method to insert passed racer (or this racer if None) into database
    # TODO
    def createRacer(self, racer = None):
        pass
    
    # Method to remove passed racer (or this racer if None) from database
    # TODO
    def removeRacer(self, racer = None):
        pass
    
    # Get and return uniqueID of Racer that has the passed name
    # TODO
    def findUniqueIDs(self, name):
        pass