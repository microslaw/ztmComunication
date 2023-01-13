# K01:	S  ← Ø	zbiór S ustawiamy jako pusty                                                                                       
# K02:	Q  ← wszystkie wierzchołki grafu	                                                                                       
# K03:	Utwórz n  elementową tablicę d	tablica na koszty dojścia                                                                  
# K04:	Utwórz n  elementową tablicę p	tablica poprzedników na ścieżkach                                                          
# K05	Tablicę d  wypełnij największą
# wartością dodatnią	                                                                                                           
# K06:	d [ v  ] ← 0	koszt dojścia do samego siebie jest zawsze zerowy                                                          
# K07:	Tablicę p  wypełnij wartościami -1	-1 oznacza brak poprzednika                                                            
# K08:	Dopóki Q  zawiera wierzchołki,
# wykonuj kroki K09...K12	 
# K09:	    Z Q  do S  przenieś wierzchołek u
#     o najmniejszym d [ u  ]	 
# K10:	    Dla każdego sąsiada w  wierzchołka u :
#     wykonuj kroki K11...K12	przeglądamy sąsiadów przeniesionego wierzchołka
# K11:	        Jeśli w  nie jest w Q,
#         to następny obieg pętli K10	szukamy sąsiadów obecnych w Q
# K12:	        Jeśli d [ w  ] > d [ u  ] + waga krawędzi u–w,
#         to:
#             d [ w  ] ← d [ u  ] + waga krawędzi u–w
#             p [ w  ] ← u	sprawdzamy koszt dojścia. Jeśli mamy niższy, to modyfikujemy koszt i zmieniamy poprzednika w na u
# K13:	Zakończ 

from ztmDatabaseControls import *

busStops = getBusStops()

for i in busStops:
    busStops

busLines = getBusLines()

def set_of_stops(recursion_level, start_stop, busStops):
    global busLines
    one_step_stops =set()
    if(recursion_level == 1):
        for line in busStops[start_stop].lines:
            one_step_stops.update(busLines[line].stops)
    else:
        for line in busStops[start_stop].lines:
            for stop in line.stops:
                one_step_stops.update(set_of_stops(recursion_level-1,stop, busStops))
    return one_step_stops
    


#removes stops with one line not being stop1 or stop2
def truncateStops(busStops, stop1,stop2):
    toDel = set()
    for busStop in busStops:
        if (busStop not in {stop1, stop2}) and 1== len(busStops[busStop].lines):
            toDel.add(busStop)
    for dictionary in toDel:
        del busStops[dictionary]

    return busStops
        

print(len(truncateStops(getBusStops(),32650,8101)))


def findDirections(directions, date):
    startStop, endStop = directions

    i = 1
    truncatedStops = truncateStops(busStops, startStop, endStop)
    if(len((truncatedStops[startStop].lines).intersection(truncatedStops[endStop].lines))):
        return directions
    
    
    while True:
        
        intersect = set_of_stops(i,startStop,truncatedStops).intersection(i,endStop,truncatedStops)
        if(len(intersect)>=1):
            midStop = intersect.pop()
            dir1 = findDirections([startStop, midStop])
            dir2 = findDirections([midStop, endStop])
            dir1.extend(dir2[1:])
            return dir1

        i+=1


def findLines(directions):
    truncatedStops = truncateStops(busStops, directions[0], directions[-1])
    busList = []
    for i in range(len(directions)-1):
        busList.append((truncatedStops[0].lines).intersection(truncatedStops[directions[-1]].lines).pop())


checked = set()
not_checked = set()

#for i in busStops:
#    print(i, busStops[i].lines)

dir = findDirections([8101,32260],0)
lines = findLines(dir)
print(dir,lines)
#while len(not_checked)>0:
    