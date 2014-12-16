#Author: Nathanael Gordon
#Created: 2014-11-19

import time
from datetime import datetime
from race import Race

class Tournament:

    def __init__(self, gameName, maxRacers, pk = -1, started = None, timeEnded = None):
        self.pk = pk
        self.gameName = gameName
        self.maxRacers = maxRacers
        self.races = []
        self.racers = []
        self.timeStarted = started
        if self.timeStarted is None:
            self.timeStarted = datetime.now()
        self.timeEnded = timeEnded
                
    # Generate and return a new race
    # TODO
    def generateRace(self):
        #create and init a new race pass self to the constructer
        #pick racers for the race with similar scores
        #pick racers for the race who haven't played recently
        #return new race
        newRace = Race()
        for index in range(0, self.maxRacers):
            if index < len(self.racers):
                newRace.addRacer(self.racers[index])
        return newRace
    
    # Automatically replace a racer with the next most appropriate racer
    # TODO
    def replaceRacerAuto(self, race, racer):
        #find next most appropriate racer
        
        #race.replaceRacer(racer, newRacer)
        pass
    
    # Generate a list of racers ordered by closeness of their scores
    # TODO
    def findRacersSimilarScore(self, racer):
        pass
    
    
    def getLeastRecentRacer(self):
        self.races.sort()
        for race in self.races:
            print(race)
                    
    
    #
    
    

    
    # Calculate score of passed racer based on the list of races
    def calculateScore(self, racer):
        score = 0
        for race in self.races:
            score += getPointsForRacer(racer)
        
        return score
    
    # Indicate the tournament has ended by setting the end time
    def endTournament(self):
        self.timeEnded = datetime.now()
        
    # Indicate the tournament has ended by setting the end time
    def openTournament(self):
        self.timeEnded = None
    
    # Add the passed racer to the list of racers
    def addRacer(self, racer):
        self.racers.append(racer)
        
    # Remove the passed racer
    def removeRacer(self, racer):
        for racerL in self.racers:
            if racerL.pk == racer.pk:
                self.racers.remove(racerL)
    
    # Add the passed race to the list of races
    def addRace(self, race):
        self.races.append(race)
        
    # Remove the passed race
    def removeRace(self, race):
        for raceL in self.races:
            if raceL.pk == race.pk:
                self.races.remove(raceL)
                
    # Replace the first racer with the second racer
    def replaceRacerManual(self, race, racer1, racer2):
        race.replaceRacer(racer1, racer2)
        
    def toString(self):
        toReturn = "{0} - Started: {1}, Closed: ".format(self.gameName,self.timeStarted.isoformat())
        if self.timeEnded is None:
            toReturn += "still open"
        else:
            toReturn += self.timeEnded.isoformat()
            
        return toReturn