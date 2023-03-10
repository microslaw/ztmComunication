import requests
import json
from datetime import date, datetime


__busLinesUrl = "https://ckan.multimediagdansk.pl/dataset/c24aa637-3619-4dc2-a171-a23eec8f2172/resource/22313c56-5acf-41c7-a5fd-dc5dc72b3851/download"
__busStopsUrl = "https://ckan.multimediagdansk.pl/dataset/c24aa637-3619-4dc2-a171-a23eec8f2172/resource/4c4025f0-01bf-41f7-a39f-d156d201b82b/download"
__linesAndStopsUrl = "https://ckan.multimediagdansk.pl/dataset/c24aa637-3619-4dc2-a171-a23eec8f2172/resource/3115d29d-b763-4af5-93f6-763b835967d6/download"


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

__busLines = dict()
__busStops = dict()
today = (date.today()).strftime("%Y-%m-%d")


def update_database():
    global __busLines
    global __busStops

    response = json.loads(requests.get(__busLinesUrl).text)
    for newBusLine in response[today]["routes"]:
        newBusLine.pop("agencyId")
        newBusLine.pop("activationDate")
        newBusLine.pop("routeType")

        __busLines[newBusLine["routeId"]] = busLine(newBusLine["routeId"], newBusLine["routeLongName"], newBusLine["routeShortName"])
    
    #save("__busLiness", __busLines)


    response = json.loads(requests.get(__busStopsUrl).text) 

    for newBusStop in response[today]["stops"]:
        newBusStop.pop("activationDate")
        __busStops[newBusStop["stopId"]] = busStop(newBusStop["stopId"], newBusStop["stopCode"], newBusStop["stopDesc"], newBusStop["onDemand"] )

    
    response = json.loads(requests.get(__linesAndStopsUrl).text) 
    for newTripStop in response[today]["stopsInTrip"]:
        newTripStop.pop("agencyId")
        newTripStop.pop("topologyVersionId")
        newTripStop.pop("stopActivationDate")
        newTripStop.pop("tripActivationDate")
        newTripStop.pop("tripId")


    #__buslines.stops is a dictionary with key being stop number and value being stop id 
        __busStops[newTripStop["stopId"]].addLine(newTripStop["routeId"])
        __busLines[newTripStop["routeId"]].addStop(newTripStop["stopSequence"],newTripStop["stopId"])

def getBusStops():
    return __busStops

def getBusLines():
    return __busLines

def __isoToSeconds(iso):
    time = iso.split("-")[2]
    day = 31-int(time.split("T")[0])
    hour, minute, second = (time.split("T")[1]).split(":")
    hour = 24 - int(hour)
    minute = 60 - int(minute)
    second = 60-int(second)
    return (((day*24+hour)*60+minute)*60+second)
    

#returns fastest time the specified line will be at stop
#if none time is found returns -1
#if tripId is set, will look only for trip with set id
#if tripId isn't set won't take it into account
def getTimeAtStop(stopId, lineId, tripId = -1, dateTime = today):
    url = f"https://ckan2.multimediagdansk.pl/stopTimes?date={dateTime[:10]}&routeId={lineId}"
    response = json.loads(requests.get(url).text)
    fastestBusArrival = 0
    
    fastestTripId = -1
    for arrival in response["stopTimes"]:
        if arrival["stopId"] != stopId:
            continue
        if arrival["tripId"] != tripId and tripId != -1:
            continue

        arrival.pop("routeId")
        arrival.pop("agencyId")
        arrival.pop("topologyVersionId")
        arrival.pop("date")
        arrival.pop("variantId")
        arrival.pop("noteSymbol")
        arrival.pop("noteDescription")
        arrival.pop("busServiceName")
        arrival.pop("passenger")
        arrival.pop("nonpassenger")
        arrival.pop("ticketZoneBorder")
        arrival.pop("virtual")
        arrival.pop("pickupType")
        arrival.pop("dropOffType")
        arrival.pop("shapeDistTraveled")
        arrival.pop("timepoint")
        arrival.pop("islupek")
        arrival.pop("stopShortName")
        arrival.pop("stopHeadsign")
        if fastestBusArrival<__isoToSeconds(arrival["arrivalTime"]) or fastestBusArrival == 0:
            fastestBusArrival = __isoToSeconds(arrival["arrivalTime"])
            fastestTripId = arrival["tripId"]
    
        
    return (fastestBusArrival,fastestTripId)





#both stops have to be on the same line; returns how long it will take
#to move from stopA to stopB at given hour
#date has to be in format YYYY-MM-DD
#if no date is specified, current will be used
def getTimeBetweenStops(stopA, stopB, lineId, dateTime = today):
    secondsToBus,tripId = getTimeAtStop(stopA, lineId, dateTime=dateTime)
    secondsToDestination,tripId = getTimeAtStop(stopB, lineId, tripId,today)
    return (secondsToDestination-secondsToBus)/60


update_database()