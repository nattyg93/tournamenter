#Author: Nathanael Gordon
#Created: 2014-11-29

from datetime import datetime
from databaseInterface import *
from tournament import Tournament
from racer import Racer
from race import Race

class TournamenterDatabase:
    
    def __init__(self):
        self.tournaments = []
        self.racers = []
        self.races = []
        self.cnx = mysql.connector.connect(user='tournamenter', password='tournamenter', host='localhost')
        createDatabase()
        self.cursor = self.cnx.cursor()
        self.cursor.execute(USE)
        
    def populateRacers(self):
        self.cursor.execute(SELECT_ALL['racers'])
        for result in self.cursor:
            racer = Racer(result[1], result[0], 0, result[2])
            self.racers.append(racer)
    
    def populateRaces(self):
        self.cursor.execute(SELECT_ALL['races'])
        for result in self.cursor:
            race = Race(result[0], result[2])
            self.races.append(race)
            
        for race in self.races:
            values = {'raceID':race.pk}
            self.cursor.execute(QUERY['racersInRace'], values)
            for result in self.cursor:
                for racer in self.racers:
                    if racer.pk == result[0]:
                        race.addRacer(racer, result[1])
            print("pk: {0}, LEN: {1}".format(race.pk, len(race.racers)))
    
    def populateTournaments(self):
        self.cursor.execute(SELECT_ALL['tournaments'])
        for result in self.cursor:
            tournament = Tournament(result[1], result[2], result[0], result[3], result[4])
            self.tournaments.append(tournament)
        
        for t in self.tournaments:
            values = {'tournamentID':t.pk}
            self.cursor.execute(QUERY['racersStillInTournament'], values)
            for result in self.cursor:
                for racer in self.racers:
                    if racer.pk == result[0]:
                        t.addRacer(racer)
            
            self.cursor.execute(SELECT_ALL['races'])
            for result in self.cursor:
                for race in self.races:
                    if race.pk == result[0] and tournament.pk == result[1]:
                        t.addRace(race)
    
    def populateDatabase(self):
        self.populateRacers()
        self.populateRaces()
        self.populateTournaments()
        
    def addTournament(self, t):
        if t is not None:
            values = {'gameName':t.gameName, 'maxRacers':t.maxRacers, 'timeStarted':t.timeStarted, 'timeEnded':t.timeEnded}
            self.cursor.execute(INSERT['tournaments'], values)
            t.pk = self.cursor.lastrowid
            self.cnx.commit()
            self.tournaments.append(t)
            
    def addRacer(self, racer):
        if racer is not None:
            values = {'racerName':racer.racerName, 'created':racer.created,}
            self.cursor.execute(INSERT['racers'], values)
            racer.pk = self.cursor.lastrowid
            self.cnx.commit()
            self.racers.append(racer)
            
    def addRace(self, race, t):
        if t is not None and race is not None:
            t.addRace(race)
            values = {'tournamentID':t.pk, 'timeStarted':race.timeStarted,}
            self.cursor.execute(INSERT['races'], values)
            race.pk = self.cursor.lastrowid

            for racer in race.racers:
                self.addRacerInRace(racer[0], race, racer[1])
            self.cnx.commit()
            self.races.append(race)
            
    def addRacerInRace(self, racer, race, position):
        if racer is not None and race is not None:
            values = {'racerID':racer.pk, 'raceID':race.pk, 'position':position}
            self.cursor.execute(INSERT['racerInRace'], values)
            self.cnx.commit()
            
    def addRacerInTournament(self, t, racer):
        if racer is not None and t is not None:
            values = {'tournamentID':t.pk, 'racerID':racer.pk}
            self.cursor.execute(SELECT['racerInTournament'], values)
            values = {'tournamentID':t.pk, 'racerID':racer.pk, 'entered':datetime.now(), 'exited':None}
            print("{0}, {1}".format(t.pk, racer.pk))
            if self.cursor.fetchone() is None:
                self.cursor.execute(INSERT['racerInTournament'], values)
            else:
                self.cursor.execute(QUERY['reAddRacerInTournament'], values)
            self.cnx.commit()
            t.addRacer(racer)
            
    def removeRacerFromTournament(self, t, racer):
        if racer is not None and t is not None:
            values = {'tournamentID':t.pk, 'racerID':racer.pk, 'exited':datetime.now()}
            self.cursor.execute(QUERY['removeRacerFromTournament'], values)
            self.cnx.commit()
            t.removeRacer(racer)
    
    def removeRace(self, t, race):
        if race is not None and t is not None:
            values = {'id':race.pk}
            self.cursor.execute(DELETE['races'], values)
            self.cnx.commit()
            t.removeRace(race)
    
    def endTournament(self, t):
        if t is not None:
            values = {'id':t.pk, 'timeEnded':t.timeEnded}
            self.cursor.execute(QUERY['endTournament'], values)
            self.cnx.commit()
            t.endTournament()
            
    def openTournament(self, t):
        if t is not None:
            values = {'id':t.pk, 'timeEnded':t.timeEnded}
            self.cursor.execute(QUERY['openTournament'], values)
            self.cnx.commit()
            t.openTournament()
