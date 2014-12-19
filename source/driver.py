#!/usr/bin/env python
#Author: Nathanael Gordon
#Created: 2014-11-19

from tournament import Tournament
from constants import *
from menu import Menu
from menu import confirm
from race import Race
from racer import Racer
from databaseInterface import *
from tournamenterDatabase import TournamenterDatabase
from mysql.connector import errorcode


def createNewRacer():
    racerName = input("Enter Racer Name: ")
    
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
    gameName = input("Enter Game Name: ")
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
    t = values[TOURNAMENT]
    header = "Race Menu:\nGame - {0}".format(t.gameName)
    for racer in race.racers:
        header += "\n   * {0} - {1}pts".format(racer[0].racerName, racer[1])
    
    raceMenu.title = header
    
    values[RACE] = race

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
    race = t.generateRace()
    setCurrentRace(values, race)
    raceMenu.infinitePrintMenu(values)

def removeRace(values, result):
    t = values[TOURNAMENT] 
    races = t.races
    
    removeRaceMenu = Menu("Cancel", "Select the race to remove")
    
    for race in races:
        removeRaceMenu.append(race.toString(), SUBTRACT_ONE)
        
    selection = removeRaceMenu.printMenu(values)
    
    if selection >= 0:
        tDB.removeRace(t, races[selection])

def removeRacerFromRace(values, result):
    r = values[RACE]
    racers = r.racers
            
    replaceRacerMenu = Menu("Cancel", "Select racer to remove")
    
    for racer in racers:
        replaceRacerMenu.append("{0} - {1}pts".format(racer[0].racerName, racer[1]), SUBTRACT_ONE)
    
    selection = printMenu(values)
    
    if selection >= 0:
        r.removeRacer(r.racers[selection])

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
tournamentMenu.addOption("Show leader board", replaceMeWithAppropriateFunction)
tournamentMenu.addOption("End tournament", endTournament)

raceMenu = Menu("Cancel race")
raceMenu.addOption("Replace racer", replaceMeWithAppropriateFunction)
raceMenu.addOption("Add racer", replaceMeWithAppropriateFunction)
raceMenu.addOption("Remove racer", removeRacerFromRace)
raceMenu.addOption("Start race", replaceMeWithAppropriateFunction)


if __name__ == "__main__":
    tDB = TournamenterDatabase()
    tDB.populateRacers()
    tDB.populateRaces()
    tDB.populateTournaments()
    
    topMenu.infinitePrintMenu(values)
        


"""
# @param t: Tournament
# @param r: Race
#NOTE: This needs to be broken up in MANY smaller functions.
def raceMenu(t, r):
    while True:
       
        elif selection == 1:    # Replace
            replaceRacerMenu = []
            replaceRacerMenu.append("Select racer to replace")
            for racer in r.racers:
                replaceRacerMenu.append("{0} - {1}pts".format(racer[0].racerName, racer[1]))
            
            selection = printMenu(replaceRacerMenu, "Cancel")
            
            if selection > 0:
                toReplace = r.racers[selection - 1][0]
            else:
                print("Cancelled")
                
            replaceRacerMenu = []
            replaceRacerMenu.append("Select racer to add")
            # This allows adding duplicates to a race.
            racers = [racer for racer in t.racers if racer not in (racer2[0] for racer2 in r.racers)] #order this list so it is in order of who is most suitable for this race
            
            for racer in racers:
                print(racer)
                # I am not sure how score is been tracked in the tournament class.
                replaceRacerMenu.append("{0}".format(racer.racerName))
                
            selection = printMenu(replaceRacerMenu, "Cancel")
            
            if selection > 0:
                toAdd = racers[selection - 1]
                r.replaceRacer(toReplace, toAdd)
            else:
                print("Cancelled")
                

            
        elif selection == 2:    # add racer
            if len(r.racers) >= t.maxRacers:
                print("\nThis race already has a maximum of {0} racers.\n".format(t.maxRacers))
            else:
                racers = [racer for racer in t.racers if racer not in (racer2[0] for racer2 in r.racers)] #TODO:order this list so it is in order of who is most suitable for this race
                
                addRacerMenu = []
                addRacerMenu.append("Select racer to add")
                for racer in racers:
                    addRacerMenu.append("{0}".format(racer.racerName, racer))
                
                selection = printMenu(addRacerMenu, "Cancel")
                
                if selection > 0:
                    r.addRacer(racers[selection - 1])
                else:
                    print("Cancelled")
                
        elif selection == 4:    # start a race and get racer's positions and commit to db
            racers = r.racers.copy()
            for count in range(1, len(racers)+1):
                winnerMenu = []
                winnerMenu.append("Select racer that came in position {0}".format(count))
                for racer in racers:
                    winnerMenu.append(racer[0].racerName)
                
                selection = printMenu(winnerMenu, "Cancel")
                
                if selection > 0:
                    r.setPositionForRacer(racers[selection - 1][0], count)
                    del racers[selection - 1]
                    
            tDB.addRace(r, t)
"""