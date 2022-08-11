import pyads

class ADSConnection():
    """GUI for demo PLC"""

    def __init__(self, 
        ams_net_id: str = "127.0.0.1.1.1",
        ams_net_port: int = 350,
        ip_address: str = None, ):
        
        self._port = ams_net_port
        self.ADSConnection = pyads.Connection(ams_net_id, ams_net_port, ip_address)
        self.ADSConnection.open()
        self.readVariableDictionary = {}
        self.writeVariableDictionary = {}
    
    def registerReadVariable(self, name, ADSName, value=0):
        self.readVariableDictionary[name] = { "ADSName" : ADSName, "value" : value}

    def registerWriteVariable(self, name, ADSName, value=0):
        self.writeVariableDictionary[name] = { "ADSName" : ADSName, "value" : value}

    def writeVariable(self, name, value):
        self.ADSConnection.write_by_name(name, value)

    def readVariable(self, name):
        self.readVariableDictionary[name]["value"] = self.ADSConnection.read_by_name(self.readVariableDictionary[name]["ADSName"])

    def getVariable(self, name):
        return self.readVariableDictionary[name]["value"]

    def setVariable(self, name, value):
        self.writeVariableDictionary[name]["value"] = value
    
    def updateAllVariables(self):
        for key in self.readVariableDictionary.keys():
            self.readVariable(key)
    
    def writeAllVariables(self):
        for key in self.writeVariableDictionary.keys():
            self.writeVariable(key, self.writeVariableDictionary[key]["value"])

    def __del__(self):
        self.disconnect()

    def disconnect(self):
        self.ADSConnection.close()