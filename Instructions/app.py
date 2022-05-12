import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

#Ref tables
measurement = Base.classes.measurement
station = Base.classes.station

################

@app.route("/")
def Welcome():
    """list all available api routes"""
    return(
        f'Available routes:<br/>'
        f'Precipitation: /api/v1.0/precipitation<br/>'
        f'Stations: /api/v1.0/stations<br/>'
        f'Temperature over previous year: /api/v1.0/tobs<br/>'
        f'Teperature Data for the start: /api/v1.0/yyyy-mm-dd<br/>'
        f'Temperature Data from start to end: /api/v1.0/yyyy-mm-dd/yyyy-mm-dd<br/>'
    )

@app.route('/api/v1.0/precipitation')
def Precipication():
    #create session engine
    session = Session(engine)
    
    query_results = session.query(measurement.date, measurement.prcp).all()
    
    session.close()
    
    precip = []
    
    for date, prcp in query_results:
        pre = {}
        pre["Date"] = date
        pre["Precipitation"] = prcp
        precip.append(pre)
        
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def Stations():
    #create session engine
    session = Session(engine)
    
    results = session.query(station.station, station.name).all()
    
    #close the session
    session.close()
    
    stat = []
    
    for result in results:
        stati = {}
        stati["Station"] = result[0]
        stati["Name"] = result[1]
        stat.append(stati)
    
    return jsonify(stat)

@app.route('/api/v1.0/tobs')
def TOBS():
    #create the session
    session = Session(engine)
    
    #query date
    recent_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    
    #Time delta date
    date = dt.date(2017,8,23) - dt.timedelta(days=365)
    
    #query the data
    precip_tob = session.query(measurement.date, measurement.prcp).filter(measurement.date >= date).all()
    
    #close the session
    session.close()
    
    tobs = []
    for result in precip_tob:
        tb = {}
        tb["date"] = result[0]
        tb["tobs"] = result[1]
        tobs.append(tb)
    
    return jsonify(tobs)

@app.route('/api/v1.0/<start_date>')
def Start(start_date):
    #create a session
    session = Session(engine)
    
#     start_dt = dt.datetime.strptime(start, '%Y-%m-%d')
    
    dates = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
                    filter(measurement.station>=start_date).all()
    
   #close the session
    session.close()
    
    tobstart = []
    for date in dates:
        tbstrt = {}
#         tbstrt["Start Date"] = start_dt
        tbstrt["Min"] = date[0]
        tbstrt["Average"] = date[1]
        tbstrt["Max"] = date[2]
        tobstart.append(tbstrt)
        
    return jsonify(tobstart)

@app.route('/api/v1.0/<start_date>/<end_date>')
def start_end_date(start_date, end_date):
    #create a session
    session = Session(engine)
    
    #query
    end_dates = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
                filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
    
    #close session
    session.close()
    
    start_end_list = []
    
    for end in end_dates:
        st_end_dic = {}
        st_end_dic["min"] = end[0]
        st_end_dic["avg"] = end[1]
        st_end_dic["max"] = end[2]
        start_end_list.append(st_end_dic)
        
        
    return jsonify(start_end_list)
                    
if __name__ == "__main__":
    app.run(debug=True)
        
        
        
        
    
    



