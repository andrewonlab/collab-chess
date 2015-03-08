import json

class ClientHandle:
    def __init__(self, clientId, clientTeam):
        self.clientId = clientId
        self.clientTeam = clientTeam

    def createClient(self):
        clientObj = \
            '{ "clientId" : '+str(self.clientId)+', "clientTeam" : '+str(self.clientTeam)+' }'
    
        clientJson = json.loads(clientObj)
        return clientJson

