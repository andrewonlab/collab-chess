#/user/bin/env python

import argparse
import random
import os, os.path
import cherrypy
import createChatHtml 
import clientHandle
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket
from ws4py.messaging import TextMessage

global voteCount
global moveTimer
global jsonBoard1
global jsonBoard2

voteCount = 0
jsonBoard1 = ('{'
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
            ']'
            '}'
    )
jsonBoard2 = ('{'
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
            ']'
            '}'
    )

class ChatWebSocketHandler(WebSocket):
    def received_message(self, m):
        global voteCount
        global jsonBoard1
        global jsonBoard2
        #TODO: parse received messages here and determine broadcast action
        # use a string 'key' for m to distinguish different messages
        if (str(m) == 'vote_button'):
            print "*****vote button pressed *****" 
            voteCount = voteCount + 1
            msg = "vote:"+str(voteCount)
            cherrypy.engine.publish('websocket-broadcast', msg)
        elif (str(m) == 'draw_button1'):
            print "*****draw button1 pressed ****"
            cherrypy.engine.publish('websocket-broadcast', jsonBoard1)
        elif (str(m) == 'draw_button2'):
            print "*****draw button2 pressed ****"
            cherrypy.engine.publish('websocket-broadcast', jsonBoard2)
        else:
            cherrypy.engine.publish('websocket-broadcast', m)

    def closed(self, code, reason="A client left the room without a proper explanation."):
        cherrypy.engine.publish('websocket-broadcast', TextMessage(reason))

class Root(object):
    def __init__(self, host, port, ssl=False):
        self.host = host
        self.port = port
        self.scheme = 'wss' if ssl else 'ws'

    @cherrypy.expose
    def index(self):
        clientId = random.randint(1,10000)
        # 0 = white
        # 1 = black
        clientTeam = random.randint(0,1) 
        client = clientHandle.ClientHandle(clientId, clientTeam)
        clientObj = client.createClient() 
        chat_server = createChatHtml.CreateChatHTML(clientObj,
                        str(self.scheme), str(self.host), str(self.port))
        html_string = chat_server.getString()
        
        #TODO: implement chess elements in here for updates
        return html_string

    @cherrypy.expose
    def ws(self):
        cherrypy.log("Handler created: %s" % repr(cherrypy.request.ws_handler))

if __name__ == '__main__':
    import logging
    from ws4py import configure_logger
    configure_logger(level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='Chess Server')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('-p', '--port', default=9000, type=int)
    parser.add_argument('--ssl', action='store_true')
    args = parser.parse_args()

    cherrypy.config.update({'server.socket_host': args.host,
                            'server.socket_port': args.port,
                            'tools.staticdir.root':\
                            os.path.abspath(
                                os.path.join(os.path.dirname(__file__), 'static'))})

    if args.ssl:
        cherrypy.config.update({'server.ssl_certificate': './server.crt',
                                'server.ssl_private_key': './server.key'})

    WebSocketPlugin(cherrypy.engine).subscribe()
    cherrypy.tools.websocket = WebSocketTool()

    cherrypy.quickstart(Root(args.host, args.port, args.ssl), '', config={
        '/ws': {
            'tools.websocket.on': True,
            'tools.websocket.handler_cls': ChatWebSocketHandler
            },
        '/js': {
              'tools.staticdir.on': True,
              'tools.staticdir.dir': 'js'
            },
        '/img': {
              'tools.staticdir.on': True,
              'tools.staticdir.dir': 'img'
            }
        }
    )

