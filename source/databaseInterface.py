#!/usr/bin/env python
#Author: Nathanael Gordon
#Created: 2014-11-27

import mysql.connector
from mysql.connector import errorcode

#cnx = mysql.connector.connect(user='tournamenter', password='tournamenter', host='bismarck')

#curs = cnx.cursor()

DB_NAME = "tournamenter"

USE = "USE {0};".format(DB_NAME)

CREATE_TABLE = {}

CREATE_TABLE['tournaments'] = (
    "  CREATE TABLE `tournaments` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `gameName` varchar(40) NOT NULL,"
    "  `maxRacers` int(11) NOT NULL,"
    "  `timeStarted` datetime NOT NULL,"
    "  `timeEnded` datetime,"
    "  PRIMARY KEY (`id`)"
    "  )")

CREATE_TABLE['races'] = (
    "  CREATE TABLE `races` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `tournamentID` int(11) NOT NULL,"
    "  `timeStarted` datetime NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  CONSTRAINT `tournament_fk` FOREIGN KEY (`tournamentID`)"
    "  REFERENCES `tournaments` (`id`) ON DELETE CASCADE"
    "  )")

CREATE_TABLE['racers'] = (
    "  CREATE TABLE `racers` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `racerName` varchar(40) NOT NULL,"
    "  `created` datetime NOT NULL,"
    "  PRIMARY KEY (`id`), UNIQUE KEY `racerName` (`racerName`)"
    "  )")

CREATE_TABLE['racerInTournament'] = (
    "  CREATE TABLE `racerInTournament` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `tournamentID` int(11) NOT NULL,"
    "  `racerID` int(11) NOT NULL,"
    "  `entered` datetime NOT NULL,"
    "  `exited` datetime,"
    "  PRIMARY KEY (`id`),"
    "  KEY `racerID` (`racerID`),"
    "  CONSTRAINT `tournament_fk1` FOREIGN KEY (`tournamentID`)"
    "  REFERENCES `tournaments` (`id`) ON DELETE CASCADE,"
    "  CONSTRAINT `racer_fk` FOREIGN KEY (`racerID`)"
    "  REFERENCES `racers` (`id`) ON DELETE CASCADE"
    "  )")

CREATE_TABLE['racerInRace'] = (
    "  CREATE TABLE `racerInRace` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `raceID` int(11) NOT NULL,"
    "  `racerID` int(11) NOT NULL,"
    "  `position` int(11),"
    "  PRIMARY KEY (`id`),"
    "  KEY `racerID` (`racerID`),"
    "  KEY `raceID` (`raceID`),"
    "  CONSTRAINT `racer_fk1` FOREIGN KEY (`racerID`)"
    "  REFERENCES `racers` (`id`) ON DELETE CASCADE,"
    "  CONSTRAINT `race_fk` FOREIGN KEY (`raceID`)"
    "  REFERENCES `races` (`id`) ON DELETE CASCADE"
    "  )")

INSERT = {}

INSERT['tournaments'] = ("INSERT INTO tournaments "
    "  (gameName, maxRacers, timeStarted, timeEnded) "
    "  VALUES (%(gameName)s, %(maxRacers)s, %(timeStarted)s, %(timeEnded)s) ")

INSERT['races'] = ("INSERT INTO races"
    "  (tournamentID, timeStarted) "
    "  VALUES (%(tournamentID)s, %(timeStarted)s) ")

INSERT['racers'] = ("INSERT INTO racers"
    "  (racerName, created) "
    "  VALUES (%(racerName)s, %(created)s) ")

INSERT['racerInTournament'] = ("INSERT INTO racerInTournament"
    "  (tournamentID, racerID, entered, exited) "
    "  VALUES (%(tournamentID)s, %(racerID)s, %(entered)s, %(exited)s) ")

INSERT['racerInRace'] = ("INSERT INTO racerInRace"
    "  (raceID, racerID, position) "
    "  VALUES (%(raceID)s, %(racerID)s, %(position)s) ")

DELETE = {}

DELETE['tournaments'] = ("DELETE FROM tournaments"
    "  WHERE id = %(id)s")

DELETE['races'] = ("DELETE FROM races"
    "  WHERE id = %(id)s")

DELETE['racers'] = ("DELETE FROM racers"
    "  WHERE id = %(id)s")

DELETE['racerInTournament'] = ("DELETE FROM racerInTournament"
    "  WHERE id = %(id)s")

DELETE['racerInRace'] = ("DELETE FROM racerInRace"
    "  WHERE id = %(id)s")

SELECT_ALL = {}

SELECT_ALL['tournaments'] = ("SELECT * FROM tournaments")

SELECT_ALL['races'] = ("SELECT * FROM races")

SELECT_ALL['racers'] = ("SELECT * FROM racers")

SELECT_ALL['racerInTournament'] = ("SELECT * FROM racerInTournament")

SELECT_ALL['racerInRace'] = ("SELECT * FROM racerInRace")

SELECT = {}

SELECT['racerInTournament'] = ("SELECT * FROM racerInTournament WHERE racerID = %(racerID)s AND tournamentID = %(tournamentID)s")

SELECT['racerInRace'] = ("SELECT * FROM racerInRace WHERE racerID = %(racerID)s AND raceID = %(tournamentID)s")

QUERY = {}

QUERY['endTournament'] = ("UPDATE tournaments SET timeEnded = %(timeEnded)s WHERE id = %(id)s")

QUERY['openTournament'] = ("UPDATE tournaments SET timeEnded = NULL WHERE id = %(id)s")

QUERY['removeRacerFromTournament'] = ("UPDATE racerInTournament SET exited = %(exited)s WHERE tournamentID = %(tournamentID)s AND racerID = %(racerID)s")

QUERY['removeRacerFromRace'] = ("DELETE FROM racerInRace WHERE raceID = %(raceID)s AND racerID = %(racerID)s")

QUERY['reAddRacerInTournament'] = ("UPDATE racerInTournament SET exited = NULL WHERE tournamentID = %(tournamentID)s AND racerID = %(racerID)s")

QUERY['racersStillInTournament'] = ("SELECT racerID FROM racerInTournament WHERE tournamentID = %(tournamentID)s AND exited IS NULL")

QUERY['racersInRace'] = ("SELECT racerID, position FROM racerInRace WHERE raceID = %(raceID)s")

def createDatabase():
    cnx = mysql.connector.connect(user='tournamenter', password='tournamenter', host='bismarck')
    
    curs = cnx.cursor()
    
    try:
        curs.execute("CREATE DATABASE {0} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
        print("The database `tournamenter` was created")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_DB_CREATE_EXISTS:
            print("The database `tournament` already exists")
        else:
            print(err)
    
    curs.execute(USE)
    try:
        curs.execute(CREATE_TABLE['tournaments'])
        print("The table `tournaments` was created.")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("The table `tournaments` already exists")
        else:
            print(err)
    
    try:    
        curs.execute(CREATE_TABLE['races'])
        print("The table `races` was created.")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("The table `races` already exists")
        else:
            print(err)
            
    try:
        curs.execute(CREATE_TABLE['racers'])
        print("The table `racers` was created.")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("The table `racers` already exists")
        else:
            print(err)
            
    try:
        curs.execute(CREATE_TABLE['racerInTournament'])
        print("The table `racerInTournament` was created.")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("The table `racerInTournament` already exists")
        else:
            print(err)
            
    try:
        curs.execute(CREATE_TABLE['racerInRace'])
        print("The table `racerInRace` was created.")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("The table `racerInRace` already exists")
        else:
            print(err)
