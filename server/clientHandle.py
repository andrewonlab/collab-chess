import json

class ClientHandle:
    def __init__(self, clientId):
        self.clientId = clientId

    def createClient(self):
        clientObj = \
            '{ "clientId" : '+str(self.clientId)+' }'
    
        clientJson = json.loads(clientObj)
        return clientJson

