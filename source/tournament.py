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
    def generateRace(self):
        
        for racer in self.racers:
            racer.score, temp = self.calculateScore(racer)
        
        newRace = Race()
        racersSorted = self.sortOptimal(self.racers)
        averageScore = self.calculateAverageScore(racersSorted[0])
        newRace.addRacer(racersSorted[0])
        del racersSorted[0]
        
        racersSorted = self.orderBySimilarScore(averageScore, racersSorted)
        
        for racer in racersSorted:
            print("{0}, race: {1}, score: {2}".format(racer.racerName, self.racesSinceLastRaced(racer), self.calculateAverageScore(racer)))
        for index in range(0, self.maxRacers-1):
            if index < len(racersSorted):
                newRace.addRacer(racersSorted[index])
        return newRace
    
    # returns the number of races since the passed racer raced
    # 0 is returned if they were in the last race
    # 1 if they were in the race before last etc
    def racesSinceLastRaced(self, racer):
        self.races.sort()
        lastRaced = 0
        for race in self.races:
            lastRaced += 1
            racers = [racer[0] for racer in race.racers]
            if racer in racers:
                lastRaced = 0
                
        return lastRaced
    
    def sortOptimal(self, racers):
        return sorted(racers, key = lambda x: (0-self.racesSinceLastRaced(x), self.calculateAverageScore(x)))  #sorted by last raced in reverse order then by the score (least points first)
    
    # Generate a list of racers ordered by closeness of their scores
    def orderBySimilarScore(self, averageScore, racers):
        return sorted(racers, key = lambda x: (abs(averageScore-self.calculateAverageScore(x)), 0-self.racesSinceLastRaced(x)))    #sorted by closest score then by when they last raced
    
    # Calculate score of passed racer based on the list of races
    def calculateScore(self, racer):
        score = 0
        numberOfRaces = 0
        for race in self.races:
            points = race.getPointsForRacer(racer, self.maxRacers)
            score += points
            if points > 0:
                numberOfRaces += 1
        
        return score, numberOfRaces
    
    def calculateAverageScore(self, racer):
        score, num = self.calculateScore(racer)
        if num > 0:
            return score/num
        else:
            return 0
    
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