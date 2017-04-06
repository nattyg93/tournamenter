# Tournamenter
A Python project to schedule races in a tournament when the number of friends exceeds the number of controllers.

The basic idea came from the desire to host LANs focused around racing games (like Mario Kart). With 4 controllers and 10 friends I wanted a way to schedule races with the following 2 criteria in mind:

  1. On average everyone would get to be in the same number of races;
  2. Races would be organised such that each Racer in a given Race was of similar skill level.

To achieve this Tournamenter allows you to create Racers and Tournaments, add Racers to the Tournaments, and then automatically generate Races (i.e. which Racers should be in a given Race). At the end of the Race, you record which place the Racers finished in. Then based on these scores, further Races can be automatically scheduled.

If someone is eating pizza or just feels like sitting out for a round, the Racer can be removed from the Race and replaced with either the next most appropriate Racer, or anyone else. You can remove Races from the Tournament if you want, and can add and remove Racers from the Tournament at any time. You can also view a leaderboard with detailed information about each Racer. Then when a Tournament is finished you can close it.

### System Requirements:

 * Python 3;
 * [MySQL Connector/Python](https://dev.mysql.com/doc/connector-python/en/);
 * MySQL/MariaDB Server (by default it must be running on the same host as Tournamenter);
 * By default you need a MySQL user "tournamenter" with password "tournamenter".
 
 

### Instructions:
 
 To run the program navigate to source/ on the commandline and run "./driver". Hopefully it should work.


### Known Issues:

 * The current algorithm for determining which Racers should be in a Race is quite simple and as such does not currently satisfy the first criteria listed above.
