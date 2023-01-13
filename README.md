## Table of contents
* [General info](#General-info)
* [Used languages and tools](#Used-languages-and-tools)
* [Setup](#Setup)
* [Functions](#Functions)
* [Authors](#Authors)


## General info
Website using ztm api to find bus line between two bus stops

## Used languages and packages:
* Python 3.10.7
*   requests
*   json
*   datetime
*   flask
	
## Setup

## Functions
* updateDatabase() - pulls the data from ztmApi. Is called on initialization of ztmDatabaseControls.py
* getBusLines() - returns dictionary with all bus lines in form {lineId:lineObject}
* getBusStops() - returns dictionary with all bus stops in form {stopId:stopObject}
* getTimeAtStop() returns fastest time the specified line will be at stop; if none time is found returns -1; if tripId is set, will look only for trip with set id; if tripId isn't set won't take it into account
## Authors
BEST Gdansk hackaton team "Natural stupidity"
* microslaw
* mszablewski
* sgolebiewska
* IwsonHd