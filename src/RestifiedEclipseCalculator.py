import orekit
vm = orekit.initVM()

from org.hipparchus.util import Pair
from org.orekit.data import DataProvidersManager, DirectoryCrawler
from org.orekit.time import AbsoluteDate

import bottle
from bottle import request, response
import json

from EclipseCalculator import HAL_SatPos, EclipseCalculator
from datetime import datetime

app = application = bottle.default_app()

# the decorator
def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        # set CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

        if bottle.request.method != 'OPTIONS':
            # actual request; reply with the actual response
            return fn(*args, **kwargs)
    return _enable_cors

@app.route('propagation/eclipses', method=['OPTIONS','POST'])
@enable_cors
def EclipseCalculatorREST():
    response.content_type = 'application/json'
    
    data = request.json
    print(json.dumps(data))
    
    stringDateFormat = '%Y-%m-%dT%H:%M:%S%'

    try:
        header = data['header']
        sat = data['satellite']

        stringDate = str( header['timeStart'] )
        duration = float( header['duration'] )

        typeSat = str( sat['type'] )
        if 'keplerian' in typeSat:
            sma = float( sat['sma'] )
            if sma < 6371000:
                return ValueError('bad sma value')
            ecc = float( sat['ecc'] )
            inc = float( sat['inc'] )
            pa = float( sat['pa'] )
            raan = float( sat['raan'] )
            lv = float( sat['meanAnomaly'] )
            calculator = EclipseCalculator(HAL_SatPos(sma, ecc, inc, pa, raan, lv, 'keplerian'),
                datetime.strptime(stringDate, stringDateFormat), duration)
            return eclipseToJSON( calculator.getEclipse() )

        elif 'cartesian' in typeSat:
            x = float( sat['satellite.x'] )
            y = float( sat['satellite.y'] )
            z = float( sat['satellite.z'] )
            vx = float( sat['satellite.vx'] )
            vy = float( sat['satellite.vy'] )
            vz = float( sat['satellite.vz'] )
            calculator = EclipseCalculator(HAL_SatPos(x, y, z, vx, vy, vz, 'cartesian'), 
                datetime.strptime(stringDateFormat, stringDateFormat), duration)
            return eclipseToJSON( calculator.getEclipse() )

        else:
            return error('bad type')

    except Exception as e:
        return error(e.__name__)

def error(errorName):
    return '{"error": "' + errorName + '"}'

def eclipseToJSON(eclipse):
    eclipseDictionary = []

    for el in eclipse:
        obj = {}
        obj['start'] = el[0].toString()
        obj['end'] = el[1].toString()
        eclipseDictionary.append(obj)

    return json.dumps(eclipseDictionary)
        

if __name__ == '__main__':
    bottle.run(host = '127.0.0.1', port = 8000)