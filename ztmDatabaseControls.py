import requests
import json
import pickle



busLinesUrl = "https://ckan.multimediagdansk.pl/dataset/c24aa637-3619-4dc2-a171-a23eec8f2172/resource/22313c56-5acf-41c7-a5fd-dc5dc72b3851/download"
busStopsUrl = "https://ckan.multimediagdansk.pl/dataset/c24aa637-3619-4dc2-a171-a23eec8f2172/resource/4c4025f0-01bf-41f7-a39f-d156d201b82b/download"
linesAndStopsUrl = "https://ckan.multimediagdansk.pl/dataset/c24aa637-3619-4dc2-a171-a23eec8f2172/resource/3115d29d-b763-4af5-93f6-763b835967d6/download"


class busStop:

    def __init__(self, id, number, name, onDemand):
        self.lines = set()
        self.number = number
        self.name = name
        self.onDemand = onDemand
        self.id = id

    def addLine(self, line):
        self.lines.add(line)


class busLine:

    def __init__(self, shortName, longName, id):
        self.shortName = shortName
        self.longName = longName
        self.stops = dict()
        self.trips = set()
        self.id = id

    def addStop(self, sequece, stopId):
        self.stops[sequece] = stopId


class busTrip:

    def __init__(self, line, startTime, id):
        self.line = line
        self.startTime = startTime
        self.id = id


def save( filename, object):
    with open(filename, 'wb') as saveFile:
        pickle.dump(object, saveFile)

def load(filename):
    with open(filename, 'rb') as loadFile:
        pickle.dump(object, loadFile)
    return object

busLines = dict()
busStops = dict()
busTrips = dict()


def update_database():
    global busLines

    response = json.loads(requests.get(busLinesUrl).text)
    for newBusLine in response["2023-01-12"]["routes"]:
        newBusLine.pop("agencyId")
        newBusLine.pop("activationDate")
        newBusLine.pop("routeType")

        busLines[newBusLine["routeId"]] = busLine(newBusLine["routeId"], newBusLine["routeLongName"], newBusLine["routeShortName"])
    
    #save("busLiness", busLines)


    response = json.loads(requests.get(busStopsUrl).text) 

    for newBusStop in response["2023-01-12"]["stops"]:
        newBusStop.pop("activationDate")
        busStops[newBusStop["stopId"]] = busStop(newBusStop["stopId"], newBusStop["stopCode"], newBusStop["stopDesc"], newBusStop["onDemand"] )

    #save("newBusStops", newBusStop)
    tmp = dict()
    
    response = json.loads(requests.get(linesAndStopsUrl).text) 
    for newTripStop in response["2023-01-12"]["stopsInTrip"]:
        newTripStop.pop("agencyId")
        newTripStop.pop("topologyVersionId")
        newTripStop.pop("stopActivationDate")
        newTripStop.pop("tripActivationDate")
        newTripStop.pop("tripId")

        #print(newTripStop)
        #print(newTripStop)

    #buslines.stops is a dictionary with key being stop number and value being stop id 
        busStops[newTripStop["stopId"]].addLine(newTripStop["routeId"])
        busLines[newTripStop["routeId"]].addStop(newTripStop["stopSequence"],newTripStop["stopId"])


    save("newBusStops", newBusStop)
update_database()
