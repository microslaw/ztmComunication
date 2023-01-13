from flask import Flask, render_template, request
from datetime import datetime
from ztmDatabaseControls import *



dic = getBusStops()
busStops = []
for i in dic:
    busStops.append(str(dic[i].name))

app=Flask(__name__)

@app.route("/")

def main():
    return render_template("HACKATHON.html", BS = busStops)

@app.route("/pass_args" ,methods=['GET', 'POST'])

def pass_args():
    if request.method == 'POST':
        first_stop = request.form['first_stop']
        last_stop = request.form['last_stop']
        date = datetime.strptime(request.form['date'],
                                "%Y-%m-%d")
        time = datetime.strptime(request.form["time"],"%H:%M")
        busLines = getBusLines()
        busStops = getBusStops()
        
        for stop in busStops:
            if first_stop == busStops[stop].name:
                first_stop = busStops[stop].id
                break

        for stop in busStops:
            if last_stop == busStops[stop].name:
                last_stop = busStops[stop].id
                break
        
        matchingLine = {}

        for line in busLines:
            if first_stop and last_stop in busLines[line].stops:
                matchingLine= busLines[line]
                break
        if(matchingLine == {}):
            return render_template("no_output.html")

        eta, tripId= getTimeAtStop(first_stop, matchingLine.id, dateTime=date+time)
        etd, tripId = getTimeAtStop(last_stop, matchingLine.id, tripId)
        delta = etd-eta
        name = matchingLine.shortName
        
        return render_template("output.html", eta = eta, etd =etd, delta = delta, sname = name)

        

            




    else:
        return render_template("HACKATHON.html", BS = busStops)
     
@app.errorhandler(404)
def page_not_found_handler(e):
    return render_template("HACKATHON.html", BS = busStops)
       

if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port=80)


