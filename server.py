import sys

from http.server import HTTPServer, BaseHTTPRequestHandler

from urllib.parse import urlparse
import os
import Physics
import json
import random


#imports above !

#decalring global variables to interact witht eh table states
global_table = Physics.Table()
global_table = global_table.initializeEntireTable()

#handler class
class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        #redeclaring global
        global global_table

        #creating thhe parsed path
        parsed = urlparse(self.path)

        #time based req
        if parsed.path.startswith('/table-at-time'):
            #splitting using query
            query_components = dict(qc.split("=") for qc in parsed.query.split("&"))

            #time elapse
            elapsed_time = float(query_components.get('time', '0')) / 1000.0

            #implementing the find tbale by id function
            table_id = self.findIDByTime(elapsed_time)  

            #if the tbale id is not none we proceed to send a response
            if table_id is not None:
                table = self.readTableId(table_id) 
                svg = global_table.svg()
                self.send_response(200)
                self.send_header('Content-type', 'image/svg+xml')
                self.end_headers()
                self.wfile.write(svg.encode('utf-8'))
            else:
                self.send_error(404, 'Table state not found for time: %s' % elapsed_time)
            return

        #path for name page
        elif parsed.path == '/names.html':
            #try catch
            try:
                #readint he html page
                with open('names.html', 'rb') as file:
                    content = file.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                self.send_error(404, 'File Not Found: names.html')

        #path for getting each svg
        elif "/get-svg" in parsed.path:

            #creating querys to parse through the elapsed tiem of svgs received
            query_params = dict(qc.split("=") for qc in parsed.query.split("&"))

            #steping trhought eh time retrived 
            time_step = query_params.get("time_step")

            #try catch block for the filename of the svg
            try:
                svg_filename = f"table_state_{time_step}.svg"
                with open(svg_filename, "r") as file:
                    svg_content = file.read()
                    self.send_response(200)
                    self.send_header('Content-type', 'image/svg+xml')
                    self.end_headers()
                    self.wfile.write(svg_content.encode('utf-8'))
                    
            except FileNotFoundError:
                self.send_error(404, "SVG not found for time_step: " + time_step)


        #creating a fetcher for my display.html file
        elif parsed.path == '/display.html':

            #setting a varibale to the current gloabl svg as the initia;
            global_table_svg = global_table.svg()

            try:
                #decoding it via file
                with open('index.html', 'rb') as file:
                    content = file.read().decode('utf-8')

                #replacing the commented block with the file code
                content = content.replace('<!-- REPLACE WITH SVG -->', global_table_svg)

                #sending response back
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            except FileNotFoundError:
                self.send_error(404, 'File Not Found: %s' % self.path)
            

        #checking for path symmetry, looking for the table svgs whihc are created
        elif parsed.path.startswith('/table-') and parsed.path.endswith('.svg'):
            #ensuring the path we are parsing is fitting the condiitons of a created table.svg file
            tableNum = parsed.path[len('/table-'):-len('.svg')]
            tableFile = f'table-{tableNum}.svg'
            #if a table exists
            if os.path.exists(tableFile):
                with open(tableFile, 'rb') as file:
                    #readig into varible
                    content = file.read()
                    #sending to client
                    self.send_response(200)
                    self.send_header('Content-type', 'image/svg+xml')
                    self.send_header('Content-length', len(content))
                    self.end_headers()
                    self.wfile.write(content)

            #else we send error response to client
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(bytes(f"404: File {tableFile} not found", "utf-8"))
        #if the shoot.html or table is not found we send error response to server
                    #parsing usingn the css path
        elif parsed.path.endswith(".css"):
            try:
                with open('.' + self.path, 'rb') as file:
                    content = file.read()
                self.send_response(200)
                self.send_header("Content-type", "text/css")
                self.send_header("Content-length", len(content))
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                self.send_error(404, 'File Not Found: %s' % self.path)

        #otherwise we parse with the javascript
        elif parsed.path.endswith(".js"):
            try:
                with open('.' + self.path, 'rb') as file:
                    content = file.read()
                self.send_response(200)
                self.send_header("Content-type", "application/javascript")
                self.send_header("Content-length", len(content))
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                self.send_error(404, 'File Not Found: %s' % self.path)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes(f"404: {parsed.path} not found", "utf-8"))

    def findIDByTime(self, requested_time, epsilon=0.1):
        db = Physics.Database()
        cursor = db.conn.cursor()
        try:
            # Query to find the nearest table state to the requested time within an epsilon range
            cursor.execute("SELECT TABLEID FROM TTable WHERE TIME BETWEEN ? AND ? ORDER BY ABS(TIME - ?) ASC LIMIT 1", (requested_time - epsilon, requested_time + epsilon, requested_time))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
        except Exception as e:
            print(f"Error finding table by time: {e}")
            return None
        finally:
            cursor.close()
            db.close()

    def readTableId(self, table_id):
        db = Physics.Database()
        return db.readTable(table_id) 


    #POST METHOD
    def do_POST(self):

        #restating the globa variable 
        global global_table


        parsed = urlparse(self.path)
        
        #if the path is the beginning of the game
        if self.path == '/start-game':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            #get the player names from javascript
            player1Name = data['player1Name']
            player2Name = data['player2Name']
            
            #decide ranodmely who will go frist
            if random.randint(0, 1) == 0:
                turn = player1Name
            else:
                turn = player2Name
                
            #respond to the users here.
            message = f"It's {turn}'s turn."
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'turn': turn, 'message': message}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        
        #if the sent path is a shot being processed
        elif parsed.path == '/process-shot':
            #reading data from JSON
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            #taking the shot data from the safety check
            dx_raw = data.get('dx')
            dy_raw = data.get('dy')
            velocity_raw = data.get('velocity')

            #ensuring for NO NONE VALUES
            #iddues earlier
            dx = float(dx_raw) if dx_raw is not None else 0.0
            dy = float(dy_raw) if dy_raw is not None else 0.0
            velocity = float(velocity_raw) if velocity_raw is not None else 0.0


            #setting the game name and player naems form the data retrieved
            gameName = "Game 01"
            playerName = data['playerName']

            #calling the game method
            game = Physics.Game(gameName=gameName, player1Name=playerName, player2Name="Opponenet")

            #setting local table to global table
            table = global_table

            #shot process ocurs heres, the array of svgs and the most last table is returned
            svg_array, segTable = game.shoot(gameName, playerName, table, dx, dy)

            #glbalt able is set to the msot last table
            global_table = segTable

            #the message for the assignmetn of ball balance is set here
            ball_assignment_msg = None

            #deoending on who sunk th eball
            if game.player1Balls and game.player2Balls:
                playerBallType = game.player1Balls if playerName == game.player1Name else game.player2Balls
                ball_assignment_msg = f"{playerName} plays {game.player1Balls if playerName == game.player1Name else game.player2Balls} balls."


            #rsponse sent to user
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'svgArray': svg_array, 'ballAssignmentMsg' : ball_assignment_msg}
            self.wfile.write(json.dumps(response).encode('utf-8'))

        else:
            #other stuff handled for errors
            self.send_response(404)
            self.end_headers()
            self.wfile.write("ERROR 404: Resource not found".encode('utf-8'))

    

if __name__ == "__main__":
    #local
    httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler );
    print( "Server listing in port:  ", int(sys.argv[1]) );
    httpd.serve_forever();
