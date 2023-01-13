from flask import Flask, render_template, request
from datetime import datetime
from ztmDatabaseControls import getBusStops




busStops = getBusStops()

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
                                "%T-%m-%d")
        time = request.form["time"]


    else:
        return render_template("HACKATHON.html", BS = busStops)
     
@app.errorhandler(404)
def page_not_found_handler(e):
    return render_template("HACKATHON.html", BS = busStops)
       

if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port=80)


