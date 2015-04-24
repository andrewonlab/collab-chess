import json

class CreateChatHTML:
    def __init__(self, user, scheme, host, port):
        clientId = str(user['clientId'])
        clientId = json.dumps(clientId)
        self.clientId = clientId 
        self.scheme = scheme
        self.host = host
        self.port = port

    def getChessBoard(self):
        with open('/Users/Andrew/collab-chess/client/test.html', 'r') as myfile:
            data = myfile.read().replace('\n','')
        return data

    def getHeaderString(self):
        #NOTE: Important: local imports must be in ~/Public directory
        headerString = ("<html><head>"
                "<script type='application/javascript'" 
                        " src='https://ajax.googleapis.com/ajax/libs/jquery/"
                            "1.8.3/jquery.min.js'></script>"
                "<script src='js/GraphicsManager.js' type='text/javascript'>"
                "</script>"
                "<script src='js/Piece.js' type='text/javascript'></script>"
                "<script src='js/Board.js' type='text/javascript'></script>"
                "<script src='js/GameManager.js' type='text/javascript'></script>"
                "<script src='js/Counter.js type='text/javascript'></script>"
                )
        
        return headerString

    # Initial json to pass into GraphicsManager
    # The current board will be updated by the server
    def temp_json1(self):
        jsonString = (
        '{'
        '"black": ['
            '[0, 4, "k"],'
            '[0, 3, "q"],'
            '[0, 2, "b"], [0, 5, "b"],'
            '[0, 1, "h"], [0, 6, "h"],'
            '[0, 0, "r"], [0, 7, "r"],'
            '[1, 0, "p"], [1, 1, "p"], [1, 2, "p"], [1, 3, "p"], [1, 4, "p"], [1, 5, "p"], [1, 6, "p"], [1, 7, "p"]'
        '],'
        '"white": ['
            '[7, 4, "k"],'
            '[7, 3, "q"],'
            '[7, 2, "b"], [7, 5, "b"],'
            '[7, 1, "h"], [7, 6, "h"],'
            '[7, 0, "r"], [7, 7, "r"],'
            '[6, 0, "p"], [6, 1, "p"], [6, 2, "p"], [6, 3, "p"], [6, 4, "p"], [6, 5, "p"], [6, 6, "p"], [6, 7, "p"]'
            '],'
            '"victory": 1,'
            '"chat": "current chat messages"'
            '}'
         )
        
        return jsonString

    def getJsString(self):
        
        jsonStr1 = str(self.temp_json1())
   
        # TEAM: 0 = red 
        #       1 = black

        jsString = \
            (
                "<script type='application/javascript'>"
                    "$(document).ready(function() {"
                        # initialize board
                        "var board_size = Math.min("
                                "window.innerWidth,"
                                "window.innerHeight)*0.95;"
                                #"var gfx = new GraphicsManager("
                                #"document.getElementById("
                                #    "'canvas_container'),"
                                #    "board_size, board_size);"
                        "var json1 = "+jsonStr1+"; "
                        "var gm = new GameManager("
                                "document.getElementById("
                                "'canvas_container'),"
                                "board_size, board_size, json1);"

                        # TODO: gm.assignTeam(teamId 0 or 1)
                        "document.addEventListener('keypress',"
                        "function(event) {"
                            "if (event.keyCode == 117) {"
                                "gm.undoMove();"
                            "}"
                        "});"
                        
                        "window.setInterval(function() {"
                            "gm.update();"
                        "}, 100);"

                        "websocket = '"+self.scheme+"://"+
                                       self.host+":"+
                                       self.port+"/ws';"
                        "if(window.WebSocket) {"
                            "ws = new WebSocket(websocket);"
                        "}"
                        "else if(window.MozWebSocket) {"
                            "ws = MozWebSocket(websocket);"
                        "}"
                        "else {"
                            "console.log('WebSocket not supported');"
                            "return;"
                        "}"
                        
                        "window.onbeforeunload = function(e) {"
                            "$('#chat').val($('#chat').val()+'Exiting \\n');"
                            "ws.send('leave-"+str(self.clientId)+"');" 
                            "ws.close(1000, '"+str(self.clientId)+" left the room');"
                            "if(!e) e = window.event;"
                            "e.stopPropagation();"
                            "e.preventDefault();"
                        "};"

                        #Received message evaluation
                        "ws.onmessage = function(evt) {"
                            # Save board object from server data
                            #"var jsonBoard = jQuery.parseJSON(evt.data);"
                            #If messaged received is a vote message
                            "if(evt.data.indexOf('vote') !== -1) {"
                            "}"
                            "else if(evt.data.indexOf('move_timer') !== -1) {"
                                "var moveTimer = jQuery.parseJSON(evt.data);"
                                "$('#moveTimer').val(moveTimer['move_timer']);"
                            "}"
                            # Draw board state that we received from server
                            "else if(evt.data.indexOf('black') !== -1) {"
                                "var jsonBoard = jQuery.parseJSON(evt.data);"
                                "$('#gameDesc').val('Popular vote has been applied'); "
                                "gm.update(jsonBoard);" 
                                
                            "}"
                            
                            "else if(evt.data.indexOf('game_over') !== -1) {"
                                "alert('Game Over!');"
                                "ws.send('new_board');"
                            "}"

                            "else if(evt.data.indexOf('team') !== -1) {"
                                "var myTeam = jQuery.parseJSON(evt.data);"
                                "var myTeamNumber = myTeam.team;"
                                "var forId = myTeam.clientid;"
                                "var myId = "+str(self.clientId)+";" 
                                "if (myTeamNumber == 1 && myId == forId) {"
                                    "$('#myTeamColor').val('Black');"
                                    "$('#myTeamColor').css('background-color', 'black');"
                                    "gm.setTeam(myTeamNumber);"
                                "} else if (myId == forId) {"
                                    "$('#myTeamColor').val('Red');"
                                    "$('#myTeamColor').css('background-color', 'red');"
                                    "gm.setTeam(myTeamNumber);"
                                "}"
                            "}"
                            #If chat message, update chat field
                            "else {"
                                "$('#chat').val($('#chat').val() + evt.data + '\\n');"
                                "var pconsole = $('#chat');"
                                "if(pconsole.length) {"
                                    "pconsole.scrollTop(pconsole[0].scrollHeight - "
                                        "pconsole.height());"
                                "}"
                            "}"
                        "};"

                        # Get various information from server on load
                        "ws.onopen = function() {"
                            # TODO: Parse json object from self.user
                            
                            #"alert($('#chooseTeam').html());"
                            "ws.send('choose_team');"
                            "ws.send('get_time');"
                            "ws.send('load_board');"
                            "ws.send('set_team-"+str(self.clientId)+"');"
                            "ws.send('"+str(self.clientId)+" entered the game');" 
                        "};"
                        "ws.onclose = function(evt) {"
                            "$('#chat').val($('#chat').val() +"
                            "'Connection closed by server: ' +"
                            "evt.code + ' \"' + evt.reason + '\"\\n');"
                        "};"

                        "$('#send').click(function() {"
                            "console.log($('#message').val());"
                            "ws.send('"+str(self.clientId)+": ' + $('#message').val());"
                            "$('#message').val('');"
                            "return false;"
                        "});"
                       
                        #If vote button is clicked, send key str 'vote_button'
                        "$('#voteButton').click(function() {"
                            #"var clientJson = gm.getClientJson();" 
                            "var lastMove = gm.getLastMove();"
                            "var strLastMove = JSON.stringify(lastMove);"
                            "var clientId = "+str(self.clientId)+";"
                            "var teamName = gm.getTurn();"
                            "var myTeam = gm.getTeam();"
                            "if (teamName == myTeam && lastMove !== null) {"
                                "$('#gameDesc').val('Your vote has been submitted');"
                                "ws.send('last_move-'+strLastMove+'-'+clientId);"
                            "} else {"
                                "$('#gameDesc').val('It is not your turn.');"
                            "}"
                             
                            #"var team = gm.getTeam();"
                            #"alert('Your vote has been submitted');"
                            #"ws.send('client_vote-'+team+'-'+"
                            #    "clientJson[\"white\"]+'-'+"
                            #    "clientJson[\"black\"]);"
                        "});"
                    "});"
                    "</script>"
            "</head>" 
        )

        return jsString 
    
    def getHtmlString(self):
        htmlString =  \
            ("<body>"
                    "<div id='canvas_container' style='float:left;'></div>"
             
            "<div id='chatBox' style='float:left;'>"
             "<button type='button' id='voteButton'>SUBMIT VOTE</button><br>"
             "<textarea readonly id='gameDesc' cols='35' rows='2'></textarea>" 
             "<br><div style='float:left;'>Your team: </div>"
             "<div id='myTeamColor' style='width:20px; height:20px; float:left;'></div>"
             "<form action='#' id='chatform' method='get'>"
                "<textarea readonly id='chat' cols='35' rows='35'></textarea>"
                "<br />"
                "<label for='message'>"+str(self.clientId)+":"
                    "</label><input type='text' id='message' />"
                "<input id='send' type='submit' value='Send' />"
             "</form>"
            "</div>"

            # Team chooser popup box
            "<div id='chooseTeam' style='display:none;'>"
                "<input type='radio' name='Red' value=0>Red"
                "<br>"
                "<input type='radio' name='Black' value=1>Black"
                "<input type='button' value='Submit'>"
            "</div>"
             
            "<div id='preload' style='display:none'>"
             "<img id='king_img' src='/img/png/king_large.png' width='200' height='200' alt='king' />"
             "<img id='queen_img' src='/img/png/queen_large.png' width='200' height='200' alt='queen' />"
             "<img id='rook_img' src='/img/png/rook_large.png' width='200' height='200' alt='rook' />"
             "<img id='bishop_img' src='/img/png/bishop_large.png' width='200' height='200' alt='bishop' />"
             "<img id='knight_img' src='/img/png/knight_large.png' width='200' height='200' alt='knight' />"
             "<img id='pawn_img' src='/img/png/pawn_large.png' width='200' height='200' alt='pawn' />"
             "</div>" 

             "</body>"
             "</html>")
        return htmlString

    def getString(self):
        header = self.getHeaderString()
        js = self.getJsString()
        html = self.getHtmlString()

        chessBoard = self.getChessBoard()

        prepared = header+js+html

        return prepared
