#/user/bin/env python

import argparse
import random
import os
import cherrypy
import createChatHtml 
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket
from ws4py.messaging import TextMessage

global voteCount
global moveTimer

voteCount = 0

class ChatWebSocketHandler(WebSocket):
    def received_message(self, m):
        global voteCount
         
        #TODO: parse received messages here and determine broadcast action
        if (str(m) == 'vote_button'):
            print "*****vote button pressed *****" 
            voteCount = voteCount + 1
            msg = "vote:"+str(voteCount)
            cherrypy.engine.publish('websocket-broadcast', msg)
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
        random_user = "Guest"+str(random.randint(1,1000))
        chat_server = createChatHtml.CreateChatHTML(random_user,
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
            }
        }
    )

