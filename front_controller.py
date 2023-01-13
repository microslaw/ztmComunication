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
        time = datetime.strptime(request.form["time"],"%H-%M-%S")





    else:
        return render_template("HACKATHON.html", BS = busStops)
     
@app.errorhandler(404)
def page_not_found_handler(e):
    return render_template("HACKATHON.html", BS = busStops)
       

if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port=80)


