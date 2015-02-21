

class CreateChatHTML:
    def __init__(self, user, scheme, host, port):
        self.user = user
        self.scheme = scheme
        self.host = host
        self.port = port

    def getHeaderString(self):
        headerString = "<html><head>"
        return headerString

    def getJsTypeString(self):
        jsTypeString = \
                ("<script type='application/javascript'" 
                        " src='https://ajax.googleapis.com/ajax/libs/jquery/"
                            "1.8.3/jquery.min.js'>"
                "</script>")
        return jsTypeString

    def getFooterString(self):
        footerString = "</html>"
        return footerString

    def getHtmlString(self):
        htmlString =  \
            ("<body>"
             "<form action='#' id='chatform' method='get'>"
                "<textarea id='chat' cols='35' rows='10'></textarea>"
                "<br />"
                "<label for='message'>"+self.user+":"
                    "</label><input type='text' id='message' />"
                "<input id='send' type='submit' value='Send' />"
             "</form>"
             "</body>")
        return htmlString

    def getChatroomString(self):
        chatroomString = \
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
                        "ws.onmessage = function(evt) {"
                            "$('#chat').val($('#chat').val() + evt.data + '\\n');"
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
                    "});"
                    "</script>"
            "</head>" 
        )

        return chatroomString 

    def getString(self):
        header = self.getHeaderString()
        js = self.getJsTypeString()
        chat = self.getChatroomString()
        html = self.getHtmlString()
        footer = self.getFooterString()

        prepared = header+js+chat+html+footer

        return prepared
