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
                "</script>")
        
        return headerString

    def temp_json1(self, json2):
        if not json2:
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
            '}'
         )

        if json2:
            jsonString = ('{'
        '"black": ['
            '[0, 4, "q"],'
            '[0, 3, "q"],'
            '[0, 2, "b"], [0, 5, "b"],'
            '[0, 1, "h"], [0, 6, "h"],'
            '[0, 0, "r"], [0, 7, "r"],'
            '[1, 0, "p"], [1, 1, "p"], [1, 2, "p"], [1, 3, "p"], [1, 4, "p"], [1, 5, "p"], [1, 6, "p"], [1, 7, "p"]'
        '],'
        '"white": ['
            '[7, 4, "q"],'
            '[7, 3, "q"],'
            '[7, 2, "b"], [7, 5, "b"],'
            '[7, 1, "h"], [7, 6, "h"],'
            '[7, 0, "r"], [7, 7, "r"],'
            '[6, 0, "p"], [6, 1, "p"], [6, 2, "p"], [6, 3, "p"], [6, 4, "p"], [6, 5, "p"], [6, 6, "p"], [6, 7, "p"]'
            '],'
            '}'
        )
        
        return jsonString

    def getJsString(self):
        
        jsonStr1 = str(self.temp_json1(json2 = False))
        jsonStr2 = str(self.temp_json1(json2 = True))
    
        jsString = \
            (
                "<script type='application/javascript'>"
                    "$(document).ready(function() {"
                        # initialize board
                        "var board_size = Math.min("
                                "window.innerWidth,"
                                "window.innerHeight)*0.95;"
                        "var gfx = new GraphicsManager("
                                "document.getElementById("
                                    "'canvas_container'),"
                                    "board_size, board_size);"
                        "var json1 = "+jsonStr1+"; "
                        "var json2 = "+jsonStr2+"; "
        
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
                                #Update votecount field to value
                                "$('#voteCount').val(evt.data);"
                            "}"
                            # Draw board state that we received
                            "else if(evt.data.indexOf('black') !== -1) {"
                                "var jsonBoard = jQuery.parseJSON(evt.data);"
                                "gfx.draw(jsonBoard);" 
                            "}"
                            #If chat message, update chat field
                            "else {"
                                "$('#chat').val($('#chat').val() + evt.data + '\\n');"
                            "}"
                        "};"
                        "ws.onopen = function() {"
                            # TODO: Parse json object from self.user
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
                            "ws.send('vote_button');"
                        "});"
                        "$('#drawButton1').click(function() {"
                            "ws.send('draw_button1');"
                        "});"
                        "$('#drawButton2').click(function() {"
                            "ws.send('draw_button2');"
                        "});"
                    "});"
                    "</script>"
            "</head>" 
        )

        return jsString 
    
    def getHtmlString(self):
        htmlString =  \
            ("<body>"
             "<div id='canvas_container'></div>"
             "<div id='preload' style='display:none'>"
             "<img id='king_img' src='/img/png/king_large.png' width='200' height='200' alt='king' />"
             "<img id='queen_img' src='/img/png/queen_large.png' width='200' height='200' alt='queen' />"
             "<img id='rook_img' src='/img/png/rook_large.png' width='200' height='200' alt='rook' />"
             "<img id='bishop_img' src='/img/png/bishop_large.png' width='200' height='200' alt='bishop' />"
             "<img id='knight_img' src='/img/png/knight_large.png' width='200' height='200' alt='knight' />"
             "<img id='pawn_img' src='/img/png/pawn_large.png' width='200' height='200' alt='pawn' />"
             "</div>" 
            "<button type='button' id='voteButton'>vote</button>"
            "<button type='button' id='drawButton1'>draw1</button>"
            "<button type='button' id='drawButton2'>draw2</button>"
            "<input id='voteCount'></input>" 
             "<form action='#' id='chatform' method='get'>"
                "<textarea readonly id='chat' cols='35' rows='10'></textarea>"
                "<br />"
                "<label for='message'>"+str(self.clientId)+":"
                    "</label><input type='text' id='message' />"
                "<input id='send' type='submit' value='Send' />"
             "</form>"
             "</body>"
             "</html>")
        return htmlString

    def getString(self):
        header = self.getHeaderString()
        js = self.getJsString()
        html = self.getHtmlString()

        print "HEADER: "+header
        print "JS: "+js
        print "HTML: "+html

        chessBoard = self.getChessBoard()

        prepared = header+js+html

        return prepared
