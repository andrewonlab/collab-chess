class CreateChatHTML:
    def __init__(self, user, scheme, host, port):
        self.user = user
        self.scheme = scheme
        self.host = host
        self.port = port

    def getChessBoard(self):
        with open('/Users/Andrew/collab-chess/client/test.html', 'r') as myfile:
            data = myfile.read().replace('\n','')
        return data

    def getHeaderString(self):
        headerString = ("<html><head>"
                "<script type='application/javascript'" 
                        " src='https://ajax.googleapis.com/ajax/libs/jquery/"
                            "1.8.3/jquery.min.js'>"
                "</script>")
        
        return headerString

    def getJsString(self):
        jsString = \
            (
                "<script type='application/javascript'>"
                    "$(document).ready(function() {"
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
                            "ws.close(1000, '"+self.user+" left the room');"
                        
                            "if(!e) e = window.event;"
                            "e.stopPropagation();"
                            "e.preventDefault();"
                        "};"

                        #Received message evaluation
                        "ws.onmessage = function(evt) {"
                            #If messaged received is a vote message
                            "if(evt.data.indexOf('vote') !== -1) {"
                                #Update votecount field to value
                                "$('#voteCount').val(evt.data);"
                            "}"
                            #If chat message, update chat field
                            "else {"
                                "$('#chat').val($('#chat').val() + evt.data + '\\n');"
                            "}"
                        "};"
                        "ws.onopen = function() {"
                            "ws.send('"+self.user+" entered the game');" 
                        "};"
                        "ws.onclose = function(evt) {"
                            "$('#chat').val($('#chat').val() +"
                            "'Connection closed by server: ' +"
                            "evt.code + ' \"' + evt.reason + '\"\\n');"
                        "};"

                        "$('#send').click(function() {"
                            "console.log($('#message').val());"
                            "ws.send('"+self.user+": ' + $('#message').val());"
                            "$('#message').val('');"
                            "return false;"
                        "});"
                       
                        #If vote button is clicked, send key str 'vote_button'
                        "$('#voteButton').click(function() {"
                            "ws.send('vote_button');"
                        "});"
                    "});"
                    "</script>"
            "</head>" 
        )

        return jsString 
    
    def getHtmlString(self):
        htmlString =  \
            ("<body>"
             
            "<button type='button' id='voteButton'>sample</button>"
            "<input id='voteCount'></input>" 
             "<form action='#' id='chatform' method='get'>"
                "<textarea readonly id='chat' cols='35' rows='10'></textarea>"
                "<br />"
                "<label for='message'>"+self.user+":"
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

        chessBoard = self.getChessBoard()

        prepared = header+js+html

        return prepared
