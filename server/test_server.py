#/user/bin/env python

import argparse
import random
import os, os.path
import cherrypy
import createChatHtml 
import clientHandle
import json
import threading
import voteCounter
import chessengine
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket
from ws4py.messaging import TextMessage

global clientVote
global moveTimer
global jsonBoard1
global jsonBoard2
global currentBoard
global clientList
global clientVotedList
global voteCountRound
global vc
global engine

# Initialize vote counter
vc = voteCounter.VoteCounter()

clientVotedList = []
A1, H1, A8, H8 = 91, 98, 21, 28
initial = ( 
    '         \n'  #   0 -  9
    '         \n'  #  10 - 19
    ' rnbqkbnr\n'  #  20 - 29
    ' pppppppp\n'  #  30 - 39
    ' ........\n'  #  40 - 49
    ' ........\n'  #  50 - 59
    ' ........\n'  #  60 - 69
    ' ........\n'  #  70 - 79
    ' PPPPPPPP\n'  #  80 - 89
    ' RNBQKBNR\n'  #  90 - 99
    '         \n'  # 100 -109
    '          '   # 110 -119
)

N, E, S, W = -10, 1, 10, -1
directions = {
    'P': (N, 2*N, N+W, N+E), 
    'N': (2*N+E, N+2*E, S+2*E, 2*S+E, 2*S+W, S+2*W, N+2*W, 2*N+W),
    'B': (N+E, S+E, S+W, N+W),
    'R': (N, E, S, W),
    'Q': (N, E, S, W, N+E, S+E, S+W, N+W),
    'K': (N, E, S, W, N+E, S+E, S+W, N+W)
}

pst = {
    'P': (0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 198, 198, 198, 198, 198, 198, 198, 198, 0,
        0, 178, 198, 198, 198, 198, 198, 198, 178, 0,
        0, 178, 198, 198, 198, 198, 198, 198, 178, 0,
        0, 178, 198, 208, 218, 218, 208, 198, 178, 0,
        0, 178, 198, 218, 238, 238, 218, 198, 178, 0,
        0, 178, 198, 208, 218, 218, 208, 198, 178, 0,
        0, 178, 198, 198, 198, 198, 198, 198, 178, 0,
        0, 198, 198, 198, 198, 198, 198, 198, 198, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    'B': (
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 797, 824, 817, 808, 808, 817, 824, 797, 0,
        0, 814, 841, 834, 825, 825, 834, 841, 814, 0,
        0, 818, 845, 838, 829, 829, 838, 845, 818, 0,
        0, 824, 851, 844, 835, 835, 844, 851, 824, 0,
        0, 827, 854, 847, 838, 838, 847, 854, 827, 0,
        0, 826, 853, 846, 837, 837, 846, 853, 826, 0,
        0, 817, 844, 837, 828, 828, 837, 844, 817, 0,
        0, 792, 819, 812, 803, 803, 812, 819, 792, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    'N': (0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 627, 762, 786, 798, 798, 786, 762, 627, 0,
        0, 763, 798, 822, 834, 834, 822, 798, 763, 0,
        0, 817, 852, 876, 888, 888, 876, 852, 817, 0,
        0, 797, 832, 856, 868, 868, 856, 832, 797, 0,
        0, 799, 834, 858, 870, 870, 858, 834, 799, 0,
        0, 758, 793, 817, 829, 829, 817, 793, 758, 0,
        0, 739, 774, 798, 810, 810, 798, 774, 739, 0,
        0, 683, 718, 742, 754, 754, 742, 718, 683, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    'R': (0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 1258, 1263, 1268, 1272, 1272, 1268, 1263, 1258, 0,
        0, 1258, 1263, 1268, 1272, 1272, 1268, 1263, 1258, 0,
        0, 1258, 1263, 1268, 1272, 1272, 1268, 1263, 1258, 0,
        0, 1258, 1263, 1268, 1272, 1272, 1268, 1263, 1258, 0,
        0, 1258, 1263, 1268, 1272, 1272, 1268, 1263, 1258, 0,
        0, 1258, 1263, 1268, 1272, 1272, 1268, 1263, 1258, 0,
        0, 1258, 1263, 1268, 1272, 1272, 1268, 1263, 1258, 0,
        0, 1258, 1263, 1268, 1272, 1272, 1268, 1263, 1258, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    'Q': (0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 0,
        0, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 0,
        0, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 0,
        0, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 0,
        0, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 0,
        0, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 0,
        0, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 0,
        0, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 2529, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    'K': (0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 60098, 60132, 60073, 60025, 60025, 60073, 60132, 60098, 0,
        0, 60119, 60153, 60094, 60046, 60046, 60094, 60153, 60119, 0,
        0, 60146, 60180, 60121, 60073, 60073, 60121, 60180, 60146, 0,
        0, 60173, 60207, 60148, 60100, 60100, 60148, 60207, 60173, 0,
        0, 60196, 60230, 60171, 60123, 60123, 60171, 60230, 60196, 0,
        0, 60224, 60258, 60199, 60151, 60151, 60199, 60258, 60224, 0,
        0, 60287, 60321, 60262, 60214, 60214, 60262, 60321, 60287, 0,
        0, 60298, 60332, 60273, 60225, 60225, 60273, 60332, 60298, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
}


engine = chessengine.Position(initial, 0, (True,True), (True,True), 0, 0)

# Timer in seconds
moveTimer = '{ "move_timer": 15 }' 
clientVote = '' 
clientList = []
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
            '],'
            '"victory": 1,'
            '"chat": "current chat messages"'
            '}'
    )
jsonBoard2 = ('{'
        '"black": ['
            '[2, 4, "k"],'
            '[0, 3, "q"],'
            '[0, 2, "b"], [0, 5, "b"],'
            '[0, 1, "h"], [0, 6, "h"],'
            '[0, 0, "r"], [0, 7, "r"],'
            '[1, 0, "p"], [1, 1, "p"], [1, 2, "p"], [1, 3, "p"], [1, 4, "p"], [1, 5, "p"], [1, 6, "p"], [1, 7, "p"]'
        '],'
        '"white": ['
            '[5, 4, "k"],'
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

currentBoard = jsonBoard1
voteCountRound = 0

class ChatWebSocketHandler(WebSocket):
    def received_message(self, m):
        global voteCountRound
        global jsonBoard1
        global jsonBoard2
        global currentBoard
        global moveTimer
        global clientList
        global clientVotedList
        global vc
        global engine

        #pos = Position(initial, 0, (True,True), (True,True), 0, 0) 
        
        #TODO: parse received messages here and determine broadcast action
        # use a string 'key' for m to distinguish different messages
        print m
        if ('voteType' in str(m)):
            castVote = json.loads(str(m))
            print str(castVote) + "  *** Vote cast ***"
            #TODO: keep track of which clients have already voted

            clientVote = '{\"client\": '+castVote['clientId']+'}'
            msg = "vote:"+str(clientVote)
            cherrypy.engine.publish('websocket-broadcast', msg)
        
        # Draw button is a test version of a vote having completed.
        # A json object with the most votes should be cast.
        elif (str(m) == 'draw_button1'):
            print "*****draw button1 pressed ****"
            currentBoard = jsonBoard1
            cherrypy.engine.publish('websocket-broadcast', jsonBoard1)
        elif (str(m) == 'draw_button2'):
            print "*****draw button2 pressed ****"
            currentBoard = jsonBoard2
            cherrypy.engine.publish('websocket-broadcast', jsonBoard2)
        elif (str(m) == 'load_board'):
            cherrypy.engine.publish('websocket-broadcast', currentBoard)
        elif (str(m) == 'get_time' ):
            cherrypy.engine.publish('websocket-broadcast', moveTimer)
        elif ('set_team' in str(m) ):
            print "Current clients: "+ str(clientList)
            local_client = str(m).split('-')[1]
            #randTeam = random.randint(0, 1)
            randTeam = len(clientList) % 2
            print "Client length: " + str(randTeam)

            randTeamObj = (
                    "{\"team\": "+str(randTeam)+","
                    "\"clientid\": "+str(local_client)+"}"
                    )
            print "team assigned: "+str(randTeamObj) + \
                    "to client: "+str(local_client)
            cherrypy.engine.publish('websocket-broadcast', randTeamObj)   
        
        elif ('last_move' in str(m) ):
            m = str(m).split('-')
            clientCount = len(clientList)
            
            if m[2] not in clientVotedList:
                vc.add_vote(m[1])
                print "Client "+str(m[2])+" has voted"
                voteCountRound = voteCountRound + 1
                clientVotedList.append(m[2])
            
            print "Current round # of vote: " + str(voteCountRound)
            # Determine user percentage vote threshold
            # before executing json object
            if (voteCountRound >= 0.4 * clientCount):
                print "Round is over. Most popular move executed"
                most_popular = vc.get_next_popular_vote()
                print "Popular vote: "+str(most_popular)
                
                x = engine.makeMove(most_popular)
                jsonObj = x[0] 
                engine = x[1]
                  
                currentBoard = jsonObj
                clientVotedList = []
                vc.reset() 
                voteCountRound = 0
                cherrypy.engine.publish('websocket-broadcast',currentBoard)

        elif ('client_vote' in str(m) ):
            m = str(m).split('-') 
            
            
            #team = m[1]
            #if team == '1':
            #    print 'black assigned'
            #    client_vote_team = m[2]
            #    client_vote_enemy = m[3]
            #elif team == '0':
            #    print 'white assigned'
            #    client_vote_team = m[2]
            #    client_vote_enemy = m[3]

            #print "vote received: "+str(client_vote_team)+str(client_vote_enemy)

            #vote = vc.add_vote(client_vote)
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
        global clientList
        clientId = random.randint(1,10000)
        # 0 = white
        # 1 = black
        client = clientHandle.ClientHandle(clientId)
        clientObj = client.createClient() 
        clientList.append(clientId)
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
    parser.add_argument('--host', default='localhost')
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

