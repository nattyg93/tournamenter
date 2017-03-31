#!/usr/bin/env python
#Author: Nathanael Gordon
#Created: 2014-11-19

from tournament import Tournament
from constants import *
from menu import *
from race import Race
from racer import Racer
from databaseInterface import *
from tournamenterDatabase import TournamenterDatabase
from mysql.connector import errorcode


def createNewRacer():
    racerName = getInput("Enter Racer Name: ")
    
    if confirm("Create racer with the name \"{0}\"?".format(racerName)):
        racer = Racer(racerName)
    else:
        racer = None
        print("Cancelled")
        
    return racer

# @param values: a dictionary
# @param result: an integer indicating what the user entered
def createRacer(values, result):
    newRacer = createNewRacer()
    
    if newRacer is not None:
        try:
            tDB.addRacer(newRacer)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_DUP_ENTRY:
                print("\nRacer with the name \"{0}\" already exists.\n".format(newRacer.racerName))
            else:
                raise err

def listRacers(values, result):
    print("List of existing racers:")
    for racer in tDB.racers:
        print(racer.toString())
    print("\nNumber of racers: {0}".format(len(tDB.racers)))

def createNewTournament():
    gameName = getInput("Enter Game Name: ")
    maxRacers = 0
    while maxRacers < 1:
        try:
            maxRacers = int(input("Enter the maximum number of racers per race: "))
            if maxRacers < 1:
                raise ValueError()
        except ValueError:
            print("\nPlease enter a number greater than 0.\n")
    
    if confirm("Create tournament with the name \"{0}\" and a maximum of {1} racers?".format(gameName, maxRacers)):
        t = Tournament(gameName, maxRacers)
    else:
        t = None
        print("Cancelled")
    
    return t

# @param values: a dictionary
# @param result: an integer indicating what the user entered
def createTournament(values, result):
    currentTournament = createNewTournament()
    
    if currentTournament is not None:
        tDB.addTournament(currentTournament)
        setCurrentTournament(values, currentTournament)
        tournamentMenu.infinitePrintMenu(values)

def selectExistingTournament(values, result):
    tournaments = tDB.tournaments
    
    if confirm("Select open or closed tournament?", "Open", "Closed"):
        selectedTournaments = [tournament for tournament in tournaments if tournament.timeEnded is None] # returns list of open tournaments
    else:
        selectedTournaments = [tournament for tournament in tournaments if tournament.timeEnded is not None] # returns list of closed tournaments
        
    existingTournamentMenu = Menu("Cancel", "Select the tournament:")
    
    for tournament in selectedTournaments:
        existingTournamentMenu.addOption(tournament.toString(), SUBTRACT_ONE)
    
    selection = existingTournamentMenu.printMenu(values)
    
    if selection >= 0:
        tournament = selectedTournaments[selection]
        if tournament.timeEnded is not None:
            if confirm("This tournament is closed. Do you want to open it?"):
                tDB.openTournament(tournament)
            else:
                print('Cancelled')
                return

        setCurrentTournament(values, tournament)
        tournamentMenu.infinitePrintMenu(values)

def setCurrentTournament(values, tournament):
    values[TOURNAMENT] = tournament
    tournamentMenu.title = "Tournament Menu:\nGame - {0}".format(values[TOURNAMENT].gameName)

def setCurrentRace(values, race):
    values[RACE] = race
    updateRaceMenuHeader(values)

def updateRaceMenuHeader(values):
    t = values[TOURNAMENT]
    race = values[RACE]
    header = "Race Menu:\nGame - {0}".format(t.gameName)
    for racer in race.racers:
        header += "\n   * {0} - {1}/{2}pts".format(racer[0].racerName, racer[0].score, round(t.calculateAverageScore(racer[0]), 2))
    
    raceMenu.title = header

def addRacerToTournament(values, result):
    t = values[TOURNAMENT]
    racers = [racer for racer in tDB.racers if racer not in t.racers] # racers will have the value as returned by the method that gets the racers
    addRacerMenu = Menu("Cancel", "Select the racer to add")
    for racer in racers:
        addRacerMenu.addOption(racer.racerName, SUBTRACT_ONE)

    selection = addRacerMenu.printMenu(values)

    if selection >= 0:
        tDB.addRacerInTournament(t, racers[selection])

def removeRacerFromTournament(values, result):
    t = values[TOURNAMENT]
    racers = t.racers
    removeRacerMenu = Menu("Cancel", "Select the racer to remove")
    
    for racer in racers:
        removeRacerMenu.addOption(racer.racerName, SUBTRACT_ONE)
    
    selection = removeRacerMenu.printMenu(values)
    
    if selection >= 0:
        tDB.removeRacerFromTournament(t, racers[selection])

def endTournament(values, result):
    tDB.endTournament(values[TOURNAMENT])
    tournamentMenu._result = 0

def generateNewRace(values, result):
    t = values[TOURNAMENT]
    if len(t.racers) == 0:
        print("There are currently 0 racers in this tournament. There must be at least 1 racer entered in this tournament.")
    else:
        race = t.generateRace()
        setCurrentRace(values, race)
        raceMenu.infinitePrintMenu(values)

def removeRace(values, result):
    t = values[TOURNAMENT] 
    races = t.races
    
    removeRaceMenu = Menu("Cancel", "Select the race to remove")
    
    for race in races:
        removeRaceMenu.addOption(race.toString(), SUBTRACT_ONE)
        
    selection = removeRaceMenu.printMenu(values)
    
    if selection >= 0:
        tDB.removeRace(t, races[selection])

def removeRacerFromRace(values, result):
    r = values[RACE]
    t = values[TOURNAMENT]
    racers = r.racers
            
    replaceRacerMenu = Menu("Cancel", "Select racer to remove")
    
    for racer in racers:
        replaceRacerMenu.addOption("{0} - {1}/{2}pts".format(racer[0].racerName, racer[0].score, round(t.calculateAverageScore(racer[0]), 2)), SUBTRACT_ONE)
    
    selection = replaceRacerMenu.printMenu(values)
    
    if selection >= 0:
        r.removeRacer(r.racers[selection])
    
    updateRaceMenuHeader(values)

def addRacerToRace(values, result):
    r = values[RACE]
    t = values[TOURNAMENT]
    
    if len(r.racers) >= t.maxRacers:
        print("\nThis race already has a maximum of {0} racers.\n".format(t.maxRacers))
    else:
        racers = [racer for racer in t.racers if racer not in (racer2[0] for racer2 in r.racers)] #TODO:order this list so it is in order of who is most suitable for this race
        
        addRacerMenu = Menu("Cancel", "Select racer to add")
        
        for racer in racers:
            addRacerMenu.addOption("{0}".format(racer.racerName, racer), SUBTRACT_ONE)
        
        selection = addRacerMenu.printMenu(values)
        
        if selection >= 0:
            r.addRacer(racers[selection])
        
        updateRaceMenuHeader(values)

def startRace(values, result):
    r = values[RACE]
    t = values[TOURNAMENT]
    if len(r.racers) == 0:
        print("There are currently 0 racers in this race. There must be at least 1 racer in this race.")
    else:
        racers = r.racers.copy()
        for count in range(1, len(racers)+1):
            winnerMenu = Menu("Cancel", "Select racer that came in position {0}".format(count))
            for racer in racers:
                winnerMenu.addOption(racer[0].racerName, SUBTRACT_ONE)
            print("Len: {0}".format(len(r.racers)))
            selection = winnerMenu.printMenu(values)
            
            if selection >= 0:
                r.setPositionForRacer(racers[selection][0], count)
                del racers[selection]
            else:
                return
            
        tDB.addRace(r, t)
        raceMenu._result = 0

def replaceRacerInRace(values, result):
    r = values[RACE]
    t = values[TOURNAMENT]
    replaceRacerMenu = Menu("Cancel", "Select racer to replace")
    for racer in r.racers:
        replaceRacerMenu.addOption("{0} - {1}/{2}pts".format(racer[0].racerName, racer[0].score, round(t.calculateAverageScore(racer[0]), 2)), SUBTRACT_ONE)
    
    selection = replaceRacerMenu.printMenu(values)
    
    if selection >= 0:
        toReplace = r.racers[selection][0]
        
        replaceRacerMenu = Menu("Cancel", "Select racer to add")
        # This allows adding duplicates to a race.
        racers = [racer for racer in t.racers if racer not in (racer2[0] for racer2 in r.racers)]
        
        racers = t.sortOptimal(racers)
        
        for racer in racers:
            replaceRacerMenu.addOption("{0} - {1}/{2}pts".format(racer.racerName, racer.score, round(t.calculateAverageScore(racer), 2)), SUBTRACT_ONE)
            
        selection = replaceRacerMenu.printMenu(values)
        
        if selection >= 0:
            toAdd = racers[selection]
            r.replaceRacer(toReplace, toAdd)
        
        updateRaceMenuHeader(values)

def printLastRaced(values, result):
    for racer in values[TOURNAMENT].racers:
        print("{0}: {1}".format(racer.racerName, values[TOURNAMENT].racesSinceLastRaced(racer)))

def printLeaderBoard(values, result):
    t = values[TOURNAMENT]
    racers = sorted(t.racers, key = lambda x: (0-t.calculateAverageScore(x), 0-x.score))
    
    for racer in racers:
        score, numRaces = t.calculateScore(racer)
        print("{0} - Mean: {1}pts - Total: {2}pts - Been in {3} races - Raced {4} race(s) ago".format(racer.racerName, round(t.calculateAverageScore(racer),2), score, numRaces, t.racesSinceLastRaced(racer)))

def replaceMeWithAppropriateFunction(values, result):
    print("I need to replaced with an appropriate function")

values = {}

topMenu = Menu("Exit")
topMenu.addOption("Create new tournament", createTournament)
topMenu.addOption("Select existing tournament", selectExistingTournament)
topMenu.addOption("Create new racer", createRacer)
topMenu.addOption("List existing racers", listRacers)

tournamentMenu = Menu()
tournamentMenu.addOption("Add racer", addRacerToTournament)
tournamentMenu.addOption("Remove racer", removeRacerFromTournament)
tournamentMenu.addOption("Generate race", generateNewRace)
tournamentMenu.addOption("Remove race", removeRace)
tournamentMenu.addOption("Show leader board", printLeaderBoard)
tournamentMenu.addOption("End tournament", endTournament)

raceMenu = Menu("Cancel race")
raceMenu.addOption("Replace racer", replaceRacerInRace)
raceMenu.addOption("Add racer", addRacerToRace)
raceMenu.addOption("Remove racer", removeRacerFromRace)
raceMenu.addOption("Start race", startRace)


if __name__ == "__main__":
    tDB = TournamenterDatabase()
    tDB.populateRacers()
    tDB.populateRaces()
    tDB.populateTournaments()
    
    topMenu.infinitePrintMenu(values)
        



