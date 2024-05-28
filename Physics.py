import phylib;
import sqlite3;
import os;
import math
import random
import copy

import uuid

FRAME_RATE = 0.02

global_frame_counter = 0

HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-325 -325 2000 3475"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
            <defs>
              <clipPath id="tableClip">
                  <rect width="1350" height="2700" x="0" y="0"/>
              </clipPath>
            </defs>

<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />""";
FOOTER = """</svg>\n""";


################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER;
HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS;
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH;
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH;

SIM_RATE = phylib.PHYLIB_SIM_RATE;
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON;

DRAG = phylib.PHYLIB_DRAG;
MAX_TIME = phylib.PHYLIB_MAX_TIME;
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS;

STILL_BALL = phylib.PHYLIB_STILL_BALL;
ROLLING_BALL = phylib.PHYLIB_ROLLING_BALL

# add more here

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """
    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """
        self.number = number
        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;
    # add an svg method here
        ##SVG METHOD
    def svg( self ):
        #variable for ball colours
        ballColours = BALL_COLOURS[self.obj.still_ball.number]
        #the svg string to be returned 
        svgStillBall = """<circle id = "%d" cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.still_ball.number, self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, ballColours)
        #returning here
        #print(f"Generating SVG for StillBall at ({self.obj.still_ball.pos.x}, {self.obj.still_ball.pos.y})")

        return svgStillBall


################################################################################
class RollingBall(phylib.phylib_object):
    
    def __init__(self, number, pos, vel, acc):

        self.number = number

        phylib.phylib_object.__init__(self,
                                      phylib.PHYLIB_ROLLING_BALL,
                                      number,
                                      pos, vel, acc,
                                      0.0, 0.0)
        self.__class__ = RollingBall

    def svg( self ):
        #variable for ball colours
        ballColours = BALL_COLOURS[self.obj.rolling_ball.number]
        #the svg string to be returned 
        svgRollingBall = """<circle id = "%d" cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.rolling_ball.number, self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, BALL_RADIUS, ballColours)

        #print(f"Generating SVG for RollingBall at ({self.obj.rolling_ball.pos.x}, {self.obj.rolling_ball.pos.y})")
        #returning here
        return svgRollingBall

################################################################################
class Hole(phylib.phylib_object):

#*** NONE HAS TO BE 0?????
    
    #
    def __init__(self, pos):
        phylib.phylib_object.__init__(self,
                                      phylib.PHYLIB_HOLE,
                                      0,
                                      pos, None, None,
                                      0.0, 0.0)
        self.__class__ = Hole
    
    def svg( self ):
        holePosX = self.obj.hole.pos.x
        holePosY = self.obj.hole.pos.y
    
        #the svg string to be returned 
        svgHole = """ <circle cx="%d" cy="%d" r="%d" fill="black" clip-path="url(#tableClip)"/>\n""" % (holePosX, holePosY, HOLE_RADIUS)
       # svgHole = f'<circle cx="{holePosX}" cy="{holePosY}" r="{HOLE_RADIUS}" fill="black" />\n'
        #print(f"Generating SVG for hole at {holePosX}, {holePosY})")
        #returning here
        return svgHole

################################################################################
class HCushion(phylib.phylib_object):

    def __init__(self, y):
        #making pos variable
        pos = phylib.phylib_coord(0, y)
        phylib.phylib_object.__init__(self,
                                      phylib.PHYLIB_HCUSHION,
                                      0,
                                      pos, None, None,
                                      0.0, 0.0)
        self.__class__ = HCushion
    
    def svg( self ):

        yCushionPlacement = self.obj.hcushion.y
        
        if yCushionPlacement == 0:
            yPos = -25
        else:
            yPos = 2700

        #the svg string to be returned 
        svgHCushion = """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % (yPos)
        #print(f"Generating SVG for hHcushion at {yPos}")

        #returning here
        return svgHCushion

################################################################################
class VCushion(phylib.phylib_object):

    def __init__(self, x):
        pos = phylib.phylib_coord(x, 0)
        phylib.phylib_object.__init__(self,
                                      phylib.PHYLIB_VCUSHION,
                                      0,
                                      pos, None, None,
                                      0.0, 0.0)
        self.__class__ = VCushion
        
    def svg( self ):
        #defining variblae to be equal to the phylib.c full struct access, using current instantiation
        xCushionPlacement = self.obj.vcushion.x
        
        if xCushionPlacement == 0:
            xPos = -25
        else :
            xPos = 1350

        #the svg string to be returned 
        svgHCushion = """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % (xPos)

       # print(f"Generating SVG for vHcushion at {xPos}")
        #returning here
        return svgHCushion

################################################################################
class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    # add svg method here

    def svg( self ):
        #variable set to the header
        svgString = HEADER

        #for each value in curr method
        for val in self:
            #if a value exists
            if val is not None:

                #add on the svg string o the val varibale and sum it into svgString as a full string
                svgString += val.svg()
            if val is None:
                continue

        svgString += '<line id="line" x1="0" y1="0" x2="0" y2="0" stroke="black" stroke-width="4"></line>'


        #end the string with a footer
        svgString += FOOTER
        #return the new string
        return svgString
    
    def roll( self, t ):
        new = Table();
        
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                Coordinate(0,0),
                Coordinate(0,0),
                Coordinate(0,0) );
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );
                # add ball to table
                new += new_ball;
            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                Coordinate( ball.obj.still_ball.pos.x,
                ball.obj.still_ball.pos.y ) );
                # add ball to table
                new += new_ball;

        # return table
        return new;


    def cueBall(self):

        #print("is cue ball being searched")
        for ball in self:
            #ensuring ball is proper
            if ball is not None and ball.obj is not None:
                if ball.type == ROLLING_BALL and ball.obj.rolling_ball.number == 0:
                    #returnign the ball
                    return ball
                elif ball.type == STILL_BALL and ball.obj.still_ball.number == 0:
                    #retuning ball
                    return ball

        return None
    
  #  def numBall(self):

   #     count = 0

    #    for ball in self:

     #       if ball.type == ROLLING_BALL || ball.type == STILL_BALL && ball.obj.still_ball.number == 0 || ball.obj.rolling_ball.number == 0:
      #          count = count + 1
        
      #  return count

    def resetCueBall(self) :
        reset_position = Coordinate(677, 2025)

        cueBall = self.cueBall()

        if cueBall:
            cueBall.obj.still_ball.pos = reset_position
        else:
            newCueBall = StillBall(0, reset_position)
            self += newCueBall


    def initializeEntireTable(self):
        table = Table()

        #numebr of balls
        count = 15

       #rows of the balls
        rows = [5, 4, 3, 2, 1]
        #loop for the other balls
        for i, row in enumerate(rows):
            for j in range(row):
                if i % 2 == 0:
                    x = TABLE_WIDTH / 2.0 - (row - 1) * (BALL_DIAMETER + 4.0) / 2 + j * (BALL_DIAMETER + 4.0) + self.nudge()
                else:
                    x = TABLE_WIDTH / 2.0 - j * (BALL_DIAMETER + 4.0) + (row - 1) * (BALL_DIAMETER + 4.0) / 2 + self.nudge()
                y = TABLE_WIDTH / 2.0 + i * math.sqrt(3.0) / 2.0 * (BALL_DIAMETER + 4.0) + self.nudge()

                pos = Coordinate(x, y)
                sb = StillBall(count, pos)
                table += sb
                count -= 1

        # Cue ball
        pos = Coordinate(TABLE_WIDTH / 2.0 + random.uniform(-3.0, 3.0), TABLE_LENGTH - TABLE_WIDTH / 2.0)
        vel = Coordinate(0.0, -1000.0)
        acc = Coordinate(0.0, 150.0)
        rb = RollingBall(0, pos, vel, acc)
        table += rb
        
        return table
    

    def nudge(self):
        return random.uniform(-1.5, 1.5)


#A3 SQL DATABASE HERE
   
class Database:

    #constructor
    def __init__( self, reset=False ) :

        #database name is set to phylib..db
        self.sqlDbName = 'phylib.db'

        #if reset is false, it means a database exists so we delete it
        if reset : 
            #try catch block to
            try :
                os.remove(self.sqlDbName)

            except FileNotFoundError :
                pass

        try :
            self.conn = sqlite3.connect(self.sqlDbName)

        except sqlite3.Error as e :
            self.conn = None


    def createDB(self) :

        #creating table queries here. 
        create_ball_db = '''
            CREATE TABLE IF NOT EXISTS Ball (
                BALLID  INTEGER  PRIMARY KEY    AUTOINCREMENT,
                BALLNO  INTEGER  NOT NULL, 
                XPOS    FLOAT    NOT NULL,
                YPOS    FLOAT    NOT NULL,
                XVEL    FLOAT,
                YVEL    FLOAT
            );
        '''

        create_ttable = '''
            CREATE TABLE IF NOT EXISTS TTable (
                TABLEID     INTEGER     PRIMARY KEY AUTOINCREMENT,
                TIME        FLOAT       NOT NULL
            );
        '''

        create_ball_table = '''
            CREATE TABLE IF NOT EXISTS BallTable (
                BALLID  INTEGER NOT NULL,
                TABLEID INTEGER NOT NULL,
                FOREIGN KEY (BALLID) REFERENCES Ball(BALLID),
                FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID)
            );
        '''

        create_shot = '''
            CREATE TABLE IF NOT EXISTS Shot (
                SHOTID INTEGER PRIMARY KEY AUTOINCREMENT,
                PLAYERID INTEGER NOT NULL,
                GAMEID INTEGER NOT NULL,
                FOREIGN KEY (PLAYERID) REFERENCES Player(PLAYERID),
                FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID)
            );
        '''

        create_table_shot = '''
            CREATE TABLE IF NOT EXISTS TableShot (
                TABLEID INTEGER NOT NULL,
                SHOTID INTEGER NOT NULL,
                FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID),
                FOREIGN KEY (SHOTID) REFERENCES Shot(SHOTID)
            );
        '''

        create_game = '''
            CREATE TABLE IF NOT EXISTS Game (
                GAMEID      INTEGER PRIMARY KEY AUTOINCREMENT,
                GAMENAME    VARCHAR(64) NOT NULL
            );
        '''

        create_player = '''
            CREATE TABLE IF NOT EXISTS Player (
                PLAYERID    INTEGER PRIMARY KEY AUTOINCREMENT,
                GAMEID      INTEGER NOT NULL,
                PLAYERNAME  VARCHAR(64) NOT NULL,
                FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID)
            );
        '''
        
        try :
            #setting up the cursor
            cursor = self.conn.cursor()

            #executing the creation of each sql table
            cursor.execute(create_ball_db)
            cursor.execute(create_ttable)
            cursor.execute(create_ball_table)
            cursor.execute(create_shot)
            cursor.execute(create_table_shot)
            cursor.execute(create_game)
            cursor.execute(create_player)

            #calling commut on my conn
            self.conn.commit()

        #catching exceptio from the try and catch block
        except sqlite3.Error as e :
            raise

        finally :
            #calling close on my cursor
            cursor.close()


    def readTable (self, tableID ) :

        newTable = Table()

        #here i am retriving the time from the table
        try :
            cursor = self.conn.cursor()

            cursor.execute('''
                SELECT TIME FROM TTable
                    WHERE TABLEID = ?

            ''', (tableID + 1,))

            timeReceived = cursor.fetchone()

            if timeReceived :

                newTable.time = timeReceived[0]
            else :

                cursor.close()
                return None

            #here i am retrieving and adding balls to the table

            #retriving all fo the balls for this table
            cursor.execute('''

                SELECT Ball.BALLNO, Ball.XPOS, Ball.YPOS, Ball.XVEL, Ball.YVEL
                    FROM Ball INNER JOIN BallTable ON Ball.BALLID = BallTable.BALLID
                        WHERE BallTable.TABLEID = ?
            ''', (tableID + 1,))

            allBalls = cursor.fetchall()

            #if theres no balls. 
            if not allBalls:

                cursor.close()
                #in the case that there are no balls found for this tableID
                return None #we simply return None as specified 
            
            for eachBall in allBalls :

                number = eachBall[0]
                xpos = eachBall[1]
                ypos = eachBall[2]
                xvel = eachBall[3]
                yvel = eachBall[4]

                if yvel is None and xvel is None :
                    currBall = StillBall(number, Coordinate(xpos, ypos))
                else :
                    #recalcualting acceration here 
                    mag = math.sqrt((xvel) * (xvel) + (yvel) * (yvel))
                    #if the magnitude is not 0 we go by the normal formula
                    if mag != 0 :
                        xacc = -DRAG * (xvel/mag)
                        yacc = -DRAG * (yvel/mag)
                    #else we manually set the accelerations to 0
                    else :
                        xacc = 0
                        yacc = 0
                    #calling rolling ball and setting it to a variable
                    currBall = RollingBall(number, Coordinate(xpos, ypos), Coordinate(xvel, yvel), Coordinate(xacc, yacc))
                #adding the current ball to the table
                newTable += currBall

            #closing the cursor
            cursor.close()
            self.conn.commit()
            return newTable
    
        except Exception as e :
            cursor.close()
            return None

    def writeTable(self, table) :

        try :
            cursor = self.conn.cursor()

            #insert statements
            cursor.execute('''
                INSERT INTO TTable (TIME) VALUES (?)
                           
            ''', (table.time,))

            self.conn.commit()

           # cursor.execute ('''
           #     SELECT MAX(TABLEID) FROM TTable    
           #  ''')
            
           # maxTableId = cursor.fetchone()[0]

           # tableId = maxTableId
            
            tableId = cursor.lastrowid

            #for the objects int he table, we are looking for ball so we specify
            for ball in table :

                #if the ball is non existent just skip it!
                if ball is None :

                    continue

                #ensuring both ball types are still or rolling. 
                if ball.type == STILL_BALL or ball.type == ROLLING_BALL :
                    #attributes through `obj` for both StillBall and RollingBall
                    
                    #dependignon the type of ball we generate differnt atributes
                    if ball.type == ROLLING_BALL :
                        number = ball.obj.rolling_ball.number
                        xPos = ball.obj.rolling_ball.pos.x
                        yPos = ball.obj.rolling_ball.pos.y
                    else :
                        #this is for STILL BALS
                        number = ball.obj.still_ball.number
                        xPos = ball.obj.still_ball.pos.x
                        yPos = ball.obj.still_ball.pos.y

                    #setting velocity attributes depending on if its rolling
                    if isinstance(ball, RollingBall):
                        xVel = ball.obj.rolling_ball.vel.x
                        yVel = ball.obj.rolling_ball.vel.y
                    else:
                        xVel = None
                        yVel = None

                    #putting the ball into table with its attributes
                    cursor.execute('''
                        INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) VALUES (?, ?, ?, ?, ?)
                    ''', (number, xPos, yPos, xVel, yVel))

                    ballId = cursor.lastrowid

                    cursor.execute('''
                        INSERT INTO BallTable (BALLID, TABLEID) VALUES (?, ?)
                    ''', (ballId, tableId))

            self.conn.commit()

            cursor.close()
            #return the autoincremented TABLEID value minus 1 because we like to start numbering tableID at zero
            return tableId - 1
        
        except Exception as e:

            if cursor:

                cursor.close()
            return None
        
    def close(self):

        if self.conn :
            self.conn.commit()
            self.conn.close()

    
    def getPlayerID(self, playerName):
        #generating cursor
        cursor = self.conn.cursor()
        #executing the sql statement to get player id from palyer name
        cursor.execute('''
            SELECT PLAYERID FROM Player WHERE PLAYERNAME = ?
        ''', (playerName,))

        #fetching the latest one
        playerID = cursor.fetchone()
        #closing cursor
        cursor.close()
        
        #falsey evalution
        if playerID:
            return playerID[0]
        else:
            return None
    
    def getGameID(self, gameName) :

        #cursor start
        cursor = self.conn.cursor()

        #sql string to select the game id from the game name
        cursor.execute('''
            SELECT GAMEID FROM Game WHERE GAMENAME = ?
        ''', (gameName,))

        #game id set to the found row
        gameID = cursor.fetchone()
        #closing cursor
        cursor.close()

        #game id falsey evaluation
        if gameID:
            return gameID[0]
        else:
            return None
        
    #game and player id, retnirng the id of the newest shot
    def newShot(self, gameID, playerID) :
        #creating cursor
        cursor = self.conn.cursor()

        #inserting into shot the game id and the palyer id that is sent. 
        cursor.execute('''
            INSERT INTO Shot (GAMEID, PLAYERID) VALUES (?, ?)
        ''',(gameID, playerID))

        #variable is the latest row
        shotID = cursor.lastrowid

        #commiting and closing
        self.conn.commit()
        cursor.close()

        return shotID



class Game:

    def __init__( self, gameID=None, gameName=None, player1Name=None, player2Name=None ):

        #creating connection with database
        self.conn = sqlite3.connect('phylib.db')
        #setting up a cursor
        cursor = self.conn.cursor()

        self.player1Balls = None
        self.player2Balls = None
        self.sunkBalls = []

        #if the game id is an integer, and the rest are none, we have 
        #1ST possible condiiton
        if type(gameID) is int and gameName is None and player1Name is None and player2Name is None :
            #setting game id to parameter val
            self.gameID = gameID

            #incrementing gameID each tiem a new game is created
            gameID += 1

            #try catch block to find the game id
            try :
                #sql statement to get the game id from player and from Game. 
                cursor.execute('''
                    SELECT Game.GAMENAME, group_concat(Player.PLAYERNAME ORDER BY Player.PLAYERID ASC)
                        FROM Game
                        JOIN Player ON Game.GAMEID = Player.GAMEID
                        WHERE Game.GAMEID = ?
                        GROUP BY Game.GAMEID;                        
                ''', (gameID,)) #variabel game id

                #the game info is going to fetch the one game id we need
                gameInfo = cursor.fetchone()

                #if the game info exists and is not false
                if gameInfo:
                    #then we set the corresponding vairbales
                    self.gameID = gameID
                    self.gameName, playerNames = gameInfo
                    #we find the two player names via a string split. 
                    self.player1Name, self.player2Name = playerNames.split(',')

                #else we raise an error
                else:
                    raise ValueError("The game could not be retrived.");
            #exception block to handle in case database is no retrieved
            except sqlite3.Error as e:
                self.conn.rollback()
                raise
            finally:
                cursor.close()

        #the second possibility, if the other vals exist and gameID is none
        elif gameID is None and gameName and player1Name and player2Name :
            #try catch block for it
            try :
                #here we put the game into the sql database
                cursor.execute('''
                    INSERT INTO Game (GAMENAME) VALUES (?)
                ''', (gameName,))
                #retriving the latest
                self.gameID = cursor.lastrowid
                self.gameName = gameName

                #here we are inserting teh new players with the new game id 
                cursor.execute('''
                    INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?)
                ''', (self.gameID, player1Name))
                #executing string to inser teh player anem and game id
                cursor.execute('''
                    INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?)
                ''', (self.gameID, player2Name))
                
                #setting teh correspinding varibaels
                self.player1Name = player1Name
                self.player2Name = player2Name

                self.conn.commit()

            #catching exception. 
            except sqlite3.Error as e :
                self.conn.rollback()
                raise
            #finally block
            finally:
                cursor.close()

        else :
            cursor.close()
            self.conn.close()
            raise TypeError("Invalid parameter types :(")
        #final connection close to ensure everything is properly shut. 
        self.conn.close()

    def save_svg(self, svg_content, frameCounter):
       # global global_frame_counter
        filename = f"table_state_{frameCounter}.svg"
        with open(filename, "w") as file:
            file.write(svg_content)
        # Increment the global frame counter after saving
       # global_frame_counter += 1

    def assign_balls(self, playerName, ball_number):
        if ball_number <= 7:
            ball_set = "low"
        else:
            ball_set = "high"
        
        if playerName == self.player1Name:
            self.player1Balls = ball_set
            self.player2Balls = "high" if ball_set == "low" else "low"
        else:
            self.player2Balls = ball_set
            self.player1Balls = "high" if ball_set == "low" else "low"

    def check_for_sunk_ball(self, prev_table, current_table):

        #array of rpeciosu balls
        prev_balls = {
            ball.obj.still_ball.number if ball.type == STILL_BALL else ball.obj.rolling_ball.number
            for ball in prev_table
            if ball and (ball.type == STILL_BALL or ball.type == ROLLING_BALL)
        }
        #and array of current balls
        current_balls = {
            ball.obj.still_ball.number if ball.type == STILL_BALL else ball.obj.rolling_ball.number
            for ball in current_table
            if ball and (ball.type == STILL_BALL or ball.type == ROLLING_BALL)
        }


        #finding the balls that aarent in either
        sunk_balls = prev_balls - current_balls
        
        if sunk_balls:
            #we wnat to know aboutt he lowest ball sunk. 
            return min(sunk_balls)
        return None




    def shoot(self, gameName, playerName, table, xvel, yvel):

        tableID = None
        print("ENTERING SHOOT")
        print(table)
        #creating an object of the database
        db = Database()

        #setting variable gameId equal to the game id associated witht eh current name via 
        #function clal
        gameID = db.getGameID(gameName)

        #ensuring no values are none
        if not gameID:
            return None
        
        playerID = db.getPlayerID(playerName)
        
        if not playerID:
            return None

        svg_array = []

        prev_table_state = table
   
        shotID = db.newShot(gameID, playerID)
        cursor = None


    #    gameOver = winner()

   #     if gameOver = True:

        #here im trying to find the cue ball
        cueBall = table.cueBall()
        if cueBall is None:
            print("cueball is none again")
            table.resetCueBall()
            cueBall = table.cueBall()


       # print(f"Before setting velocity and acceleration: {cueBall}")

        # Assuming cueBall is correctly retrieved as a RollingBall or converted to one
        pos_x = cueBall.obj.still_ball.pos.x if cueBall.type == phylib.PHYLIB_STILL_BALL else cueBall.obj.rolling_ball.pos.x
        pos_y = cueBall.obj.still_ball.pos.y if cueBall.type == phylib.PHYLIB_STILL_BALL else cueBall.obj.rolling_ball.pos.y

        #updating the cue ball to turn it to a rolling ball
        cueBall.type = phylib.PHYLIB_ROLLING_BALL
        
        #storig the values of the ball as the variabels 
        cueBall.obj.rolling_ball.number = 0
        cueBall.obj.rolling_ball.pos.x = pos_x
        cueBall.obj.rolling_ball.pos.y = pos_y
        cueBall.obj.rolling_ball.vel.x = xvel
        cueBall.obj.rolling_ball.vel.y = yvel

        #recalcuakting the acceleration of the ball
        mag = math.sqrt((xvel) * (xvel) + (yvel) * (yvel))

        if mag != 0:
            cueBall.obj.rolling_ball.acc.x = -DRAG * (xvel / mag) 
            cueBall.obj.rolling_ball.acc.y = -DRAG * (yvel / mag) 
        else :
            cueBall.obj.rolling_ball.acc.x = 0
            cueBall.obj.rolling_ball.acc.y = 0

       # print(f"After setting velocity and acceleration: {cueBall}")
        #storing the segments into variable seg
        seg = table.segment()

        #while we still have table segments
        while seg is not None:

            #table time will be stored in variable start
            start = table.time

            #subtracting the end of the time with the beginning
            difference = seg.time - start
            #dividing here. 
            frameCount = int(difference / FRAME_RATE)

            current_table_state = seg
            sunk_ball_number = self.check_for_sunk_ball(prev_table_state, current_table_state)

            if sunk_ball_number:
                # If a ball is sunk, assign ball sets if not already assigned
                if not self.player1Balls or not self.player2Balls:
                    self.assign_balls(playerName, sunk_ball_number)
                    print(f"{playerName} has been assigned {'low' if sunk_ball_number <= 7 else 'high'} balls.")

            
            #for i in the range of all of the frame counts we found
            for i in range(frameCount):

                #the frame time is going to be each frame multiplied by the frame rate
                frameTime = i * FRAME_RATE
                

                #creating a new table and calling the roll function so we cna instantiate movement
                newTable = table.roll(frameTime)
                #the time of the new table is going to be the start time added by the time of each frame
                newTable.time = start + frameTime

                #we take the table database and wrtie it into varibale table id
                tableID = db.writeTable(newTable)

                # Print the updated table
                updated_db_table = db.readTable(tableID)

                if updated_db_table is not None:
                    print("Updated Database Table:")
                    print(updated_db_table)

                    svg_content = updated_db_table.svg()

                    print("NOW PRINTING THE SVG_CONTENT BEFORE SAVING TO FILE")
                    print(svg_content)

                    svg_array.append(svg_content)

                    self.save_svg(svg_content, i)


                else:
                    print("Error: Updated database table not found.")


            if tableID is not None:
                #try catch block to insert table id and the shot id
                try :
                    #creating cursor 
                    cursor = db.conn.cursor()
                #executing the insert
                    cursor.execute('''
                        INSERT INTO TableShot (TABLEID, SHOTID) VALUES (?, ?)

                    ''', (tableID, shotID))

                    #commiting 
                    db.conn.commit()
                        

                    
                    #throwing exception
                except sqlite3.Error as e:
                    raise
                    #finally block
                finally :
                    if cursor :
                        cursor.close()
            #updating the current table so it is the newest segment
            table = seg 
            #now we get the next
            seg = table.segment() 
        
        return svg_array, table

  #  def winner(self) :

   #     table = Table();

    #    ballNum = table.numBall()

     #   if ballNum == 0:
       #     return True
      #  

       # return False;


