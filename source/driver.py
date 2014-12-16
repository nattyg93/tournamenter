#!/usr/bin/env python
#Author: Nathanael Gordon
#Created: 2014-11-19

from tournament import Tournament
from race import Race
from racer import Racer
from databaseInterface import *
from tournamenterDatabase import TournamenterDatabase
from mysql.connector import errorcode

# prints the menu and validates the value entered by the user
# the first string in the list should be the title
# the rest of the strings will be the menu items
# all menus have a zero option appended to the end
# if topLevel is true it will print the last item as exit instead of return
def printMenu(strings = None, exitString = "Return to previous menu"):
    validResult = False
    
    while not validResult:
        count = 0
        result = 0
        for string in strings:
            if count == 0:
                print("{0}\n".format(string))
            else:
                print("{0} - {1}".format(count, string))
            count += 1
            
        print("0 - {0}\n".format(exitString))
        
        try:
            result = int(input("Selection: "))
            if result < 0 or result >= count: #must be >= since count with be one greater than the largest number printed
                raise ValueError()
            
            validResult = True
        except ValueError:
            print("\nPlease enter a number in the range of 0 - {0}\n".format(count-1))
        
    return result
        
def createNewRacer():
    racerName = input("Enter Racer Name: ")
    
    confirmMenu = []
    
    confirmMenu.append("Create racer with the name \"{0}\"?".format(racerName))
    confirmMenu.append("Yes")
    selection = printMenu(confirmMenu, "No")
    
    if selection == 1:
        racer = Racer(racerName)
    else:
        racer = None
        print("Cancelled")
        
    return racer

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
    
    confirmMenu = []
    
    confirmMenu.append("Create tournament with the name \"{0}\" and a maximum of {1} racers?".format(gameName, maxRacers))
    confirmMenu.append("Yes")
    selection = printMenu(confirmMenu, "No")
    
    if selection == 1:
        t = Tournament(gameName, maxRacers)
    else:
        t = None
        print("Cancelled")
    
    return t


def topMenu():
    while True:
        
        topMenu = []

        topMenu.append("Tournamenter:")                     # Menu Title
        topMenu.append("Create new tournament")             # 1
        topMenu.append("Select existing tournament")        # 2
        topMenu.append("Create new racer")                  # 3
        
        selection = printMenu(topMenu, "Exit")
        
        if selection == 0:
            # NTS: commit changes to db? or should I do that as soon as changes are made?? (probably the second option)
            return 0
        elif selection == 1:  # creat new tournament
            currentTournament = createNewTournament()
            if currentTournament is not None:
                tDB.addTournament(currentTournament)
                tournamentMenu(currentTournament)
        elif selection == 2:  # select existing tournament
            tournaments = tDB.tournaments
            existingTournamentMenu = []
            existingTournamentMenu.append("Select open or closed tournament?")
            existingTournamentMenu.append("Open")           # 1
            existingTournamentMenu.append("Closed")         # 2
            
            selection = printMenu(existingTournamentMenu, "Cancel")
            
            if selection > 0:
                if selection == 1:
                    selectedTournaments = [tournament for tournament in tournaments if tournament.timeEnded is None]
                else:
                    selectedTournaments = [tournament for tournament in tournaments if tournament.timeEnded is not None]
                
                existingTournamentMenu = []
                existingTournamentMenu.append("Select the tournament")
                for tournament in selectedTournaments:
                    existingTournamentMenu.append(tournament.toString())
                
                selection = printMenu(existingTournamentMenu, "Cancel")
                
                if selection > 0:
                    tournament = selectedTournaments[selection - 1]
                    if tournament.timeEnded is not None:
                        openTheTournamentMenu = []
                        openTheTournamentMenu.append("This tournament is closed. Do you want to open it?")
                        openTheTournamentMenu.append("Yes")
                        
                        selection = printMenu(openTheTournamentMenu, "No")
                        
                        if selection == 1:
                            tDB.openTournament(tournament)
                    
                    currentTournament = tournament
                    tournamentMenu(currentTournament)
                        
            if selection == 0:
                print("Cancelled")
                
            
        elif selection == 3:  # create new racer
            newRacer = createNewRacer()
            if newRacer is not None:
                try:
                    tDB.addRacer(newRacer)
                except mysql.connector.Error as err:
                    if err.errno == errorcode.ER_DUP_ENTRY:
                        print("\nRacer with the name \"{0}\" already exists.\n".format(newRacer.racerName))
                    else:
                        raise err

# @param t: Tournament
def tournamentMenu(t):
    while True:
        tournamentMenu = []
        tournamentMenu.append("Tournament Menu:\nGame - {0}".format(t.gameName))
        tournamentMenu.append("Add racer")                  # 1
        tournamentMenu.append("Remove racer")               # 2
        tournamentMenu.append("Generate race")              # 3
        tournamentMenu.append("Remove race")                # 4
        tournamentMenu.append("Show leader board")          # 5
        tournamentMenu.append("End Tournament")             # 6
        
        selection = printMenu(tournamentMenu)
    
        if selection == 0:
            return 0
        elif selection == 1:    # add an existing racer
            racers = [racer for racer in tDB.racers if racer not in t.racers] # racers will have the value as returned by the method that gets the racers
            addRacerMenu = []
            addRacerMenu.append("Select the racer to add")
            for racer in racers:
                addRacerMenu.append(racer.racerName)
            
            selection = printMenu(addRacerMenu, "Cancel")
            
            if selection > 0:
                tDB.addRacerInTournament(t,racers[selection - 1])
            else:
                print("Cancelled")
                
            
        elif selection == 2:    # remove a racer
            racers = t.racers   # racers will have the value as returned by the method that gets the racers
            removeRacerMenu = []
            removeRacerMenu.append("Select the racer to remove")
            
            for racer in racers:
                removeRacerMenu.append(racer.racerName)
            
            selection = printMenu(removeRacerMenu, "Cancel")
            
            if selection > 0:
                tDB.removeRacerFromTournament(t, racers[selection - 1])
            else:
                print("Cancelled\n")
            
        elif selection == 3:    # generate a new race
            race = t.generateRace()
            raceMenu(t, race)
            
        
        elif selection == 4:    # remove a race
            races = t.races
            
            removeRaceMenu = []
            removeRaceMenu.append("Select the race to remove")
            
            for race in races:
                removeRaceMenu.append(race.toString())
                
            selection = printMenu(removeRaceMenu, "Cancel")
            
            if selection > 0:
                t.removeRace(races[selection - 1])
            else:
                print("Cancelled\n")

        elif selection == 5:    # display the leader board
            pass
        elif selection == 6:    # end the current tournament
            tDB.endTournament(t)
            return 0


# @param t: Tournament
# @param r: Race
#NOTE: This needs to be broken up in MANY smaller functions.
def raceMenu(t, r):
    while True:
        raceMenu = []
        header = "Race Menu:\nGame - {0}".format(t.gameName)
        for racer in r.racers:
            header += "\n   * {0} - {1}pts".format(racer[0].racerName, racer[1])
        raceMenu.append(header)
        raceMenu.append("Replace racer")                    # 1
        raceMenu.append("Add racer")                        # 2
        raceMenu.append("Remove racer")                     # 3
        raceMenu.append("Start race")                       # 4
        
        selection = printMenu(raceMenu, "Cancel race")
        
        if selection == 0:
            return 0
                
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
                
        elif selection == 3:    # remove racer
            racers = r.racers
            
            replaceRacerMenu = []
            replaceRacerMenu.append("Select racer to remove")
            for racer in racers:
                replaceRacerMenu.append("{0} - {1}pts".format(racer[0].racerName, racer[1]))
            
            selection = printMenu(replaceRacerMenu, "Cancel")
            
            if selection > 0:
                r.removeRacer(r.racers[selection - 1])
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

if __name__ == "__main__":
    tDB = TournamenterDatabase()
    tDB.populateRacers()
    tDB.populateRaces()
    tDB.populateTournaments()
    topMenu()
    
