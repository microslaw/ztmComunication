from ztmDatabaseControls import *

busStops = getBusStops()

for i in busStops:
    busStops

busLines = getBusLines()

def set_of_stops(recursion_level, start_stop, busStops :dict):
    global busLines
    one_step_stops =set()
    if(recursion_level == 1):
        for line in busStops[start_stop].lines:
            for stop in busLines[line].stops and busStops:
                one_step_stops.add(busStops[stop])
    else:
        for line in busStops[start_stop].lines:
            for stop in line.stops:
                one_step_stops.update(set_of_stops(recursion_level-1,stop, busStops))
    return one_step_stops
    


#removes stops with one line not being stop1 or stop2
def truncateStops(busStops, stop1,stop2):
    global busLines
    toDel = set()
    for busStop in busStops:
        if (busStop not in {stop1, stop2}) and 1== len(busStops[busStop].lines):
            toDel.add(busStop)
            for line in busLines:
                if busStop in busLines[line].stops:
                    busLines[line].stops.pop(busStop)
                    


    for dictionary in toDel:
        del busStops[dictionary]

    return busStops
        



def findDirections(directions):
    startStop, endStop = directions

    i = 1
    truncatedStops = truncateStops(busStops, startStop, endStop)
    linesAtStartStop = (truncatedStops[startStop]).lines
    
    linesAtEndStop = (truncatedStops[endStop]).lines

    if(len((linesAtStartStop).intersection(linesAtEndStop)) == 1):
        return directions
    
    
    while True:
        intersect = set_of_stops(i,startStop,truncatedStops).intersection(set_of_stops(i,endStop,truncatedStops))
        if(len(intersect)>=1):
            midStop = (intersect.pop()).id
            if midStop == endStop or midStop == startStop:
                return [startStop,endStop]
            dir1 = findDirections([startStop, midStop])
            dir2 = findDirections([midStop, endStop])
            dir1.extend(dir2[1:])
            return dir1

        i+=1


def findLines(directions):
    truncatedStops = truncateStops(busStops, directions[0], directions[-1])
    busList = []
    for i in range(len(directions)-1):
        busList.append((truncatedStops[directions[i]].lines).intersection(truncatedStops[directions[i+1]].lines).pop())

    