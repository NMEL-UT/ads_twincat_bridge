import pyads

class ADSConnection():
    """ADS connection class"""

    def __init__(self, 
        ams_net_id: str = "127.0.0.1.1.1",
        ams_net_port: int = 350,
        ip_address: str = None, ):
        
        self._port = ams_net_port
        self.ADSConnection = pyads.Connection(ams_net_id, ams_net_port, ip_address)
        self.ADSConnection.open()
        self.readVariableDictionary = {}
        self.writeVariableDictionary = {}
    
    def registerReadVariable(self, name, ADSName, value=0, arraySize=0, arrayType = pyads.PLCTYPE_LREAL):
        self.readVariableDictionary[name] = { "ADSName" : ADSName, "value" : value, "variablesSize" : arrayType * arraySize}

    def registerWriteVariable(self, name, ADSName, value=0, arraySize=0, arrayType = pyads.PLCTYPE_LREAL):
        self.writeVariableDictionary[name] = { "ADSName" : ADSName, "value" : value, "variablesSize" : arrayType * arraySize}

    def writeVariable(self, name, value):
        self.ADSConnection.write_by_name(self.writeVariableDictionary[name]["ADSName"], value)
        
    def writeVariableArray(self, name, value,):
        self.ADSConnection.write_by_name(self.writeVariableDictionary[name]["ADSName"], value, self.writeVariableDictionary[name]["variablesSize"])

    def readVariable(self, name):
        self.readVariableDictionary[name]["value"] = self.ADSConnection.read_by_name(self.readVariableDictionary[name]["ADSName"])
        return self.readVariableDictionary[name]["value"]
        
    def readVariableArray(self, name):
        self.readVariableDictionary[name]["value"] = self.ADSConnection.read_by_name(self.readVariableDictionary[name]["ADSName"], self.readVariableDictionary[name]["variablesSize"])
        return self.readVariableDictionary[name]["value"]
    
    def __del__(self):
        self.disconnect()

    def disconnect(self):
        self.ADSConnection.close()