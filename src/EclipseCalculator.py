from datetime import datetime

import orekit
vm = orekit.initVM()

from org.hipparchus.geometry.euclidean.threed import RotationOrder, Vector3D
from org.hipparchus.util import FastMath, Pair

from org.orekit.attitudes import AttitudeProvider, AttitudesSequence, LofOffset
from org.orekit.bodies import CelestialBodyFactory
from org.orekit.errors import OrekitException
from org.orekit.frames import FramesFactory, LOFType
from org.orekit.orbits import CartesianOrbit, KeplerianOrbit, Orbit, PositionAngle
from org.orekit.propagation import Propagator, SpacecraftState
from org.orekit.propagation.analytical import KeplerianPropagator
from org.orekit.propagation.events import EclipseDetector, EventDetector
from org.orekit.propagation.events.handlers import ContinueOnEvent
from org.orekit.time import AbsoluteDate, TimeScalesFactory
from org.orekit.utils import AngularDerivativesFilter, Constants, PVCoordinates, PVCoordinatesProvider

class HAL_SatPos:

    def __init__(self, param1, param2, param3, param4, param5, param6, typeSat):
        self.param1, self.param2, self.param3 = param1, param2, param3
        self.param4, self.param5, self.param6 = param4, param5, param6
        self.typeSat = typeSat


# Class needed in class EclipseCalculator to replace SwitchHandler
class SwitchHandlerPython:

    def __init__(self, output):
        self.output = output

    def switchOcurred(self, preceding, following, s):
        if preceding == dayObservationLaw:
            self.output.append((s.getDate(), True))
        else:
            self.output.append((s.getDate(), False))


class EclipseCalculator:
    
    # Attributes: duration, date, orbit, mu, output
    mu =  3.986004415e+14

    '''
    Initiate with a HAL_SatPos kepOrCartPos, an initial date and a float duration
    '''
    def __init__(self, kepOrCartPos, initialDateTime, duration):
        self.duration = duration

        initialDate = initialDateTime.date
        initialTime = initialDateTime.time
        self.date = AbsoluteDate(initialDate.year+1900, initialDate.month+1,
            initialDate.day, initialTime.hour, initialTime.minute,
            initialTime.second, TimeScalesFactory.getUTC())

        if kepOrCartPos.typeSat == 'keplerian':
            self.orbit = KeplerianOrbit(kepOrCartPos.param1, 
                kepOrCartPos.param2, kepOrCartPos.param3, kepOrCartPos.param4,
                kepOrCartPos.param5, kepOrCartPos.param6, PositionAngle.MEAN,
                FramesFactory.getEME2000(), self.date, self.mu)
        elif kepOrCartPos.typeSat == 'cartesian':
            pos = Vector3D(kepOrCartPos.param1, kepOrCartPos.param2, kepOrCartPos.param3)
            speed = Vector3D(kepOrCartPos.param4, kepOrCartPos.param5, kepOrCartPos.param6)
            self.orbit = CartesianOrbit(PVCoordinates(pos, speed),
                FramesFactory.getEME2000(), self.date, self.mu)

        # Output will be a list of tuples
        self.output = []

    def getEclipse:
        try:
            # Attitudes sequence definition
            dayObservationLaw = LofOffset(self.orbit.getFrame(), LOFType.VVLH,
                RotationOrder.XYZ, FastMath.toRadians(20), FastMath.toRadians(40),
                0)
            nightRestingLaw = LofOffset(self.orbit.getFrame(), LOFType.VVLH)
            sun = CelestialBodyFactory.getSun()
            earth = CelestialBodyFactory.getEarth()

            # Creation des events trigger
            dayNightEvent = EclipseDetector(sun, 696000000., earth, 
                Constants.WGS84_EARTH_EQUATORIAL_RADIUS).withHandler(ContinueOnEvent<EclipseDetector>())
            nightDayEvent = EclipseDetector(sun, 696000000., earth,
                Constants.WGS84_EARTH_EQUATORIAL_RADIUS).withHandler(new ContinueOnEvent<EclipseDetector>())

            attitudesSequence = AttitudesSequence()
            switchHandler = SwitchHandlerPython(self.output)
            
            # Add the swithchHandler as callback
            attitudesSequence.addSwitchingCondition(dayObservationLaw, 
                nightRestingLaw, dayNightEvent, False, True, 10.0,
                AngularDerivativesFilter.USE_R, switchHandler)
            attitudesSequence.addSwitchingCondition(nightRestingLaw,
                dayObservationLaw, nightDayEvent, True, False, 10.0,
                AngularDerivativesFilter.USE_R, switchHandler)
            if dayNightEvent.g(SpacecraftState(self.orbit)) >= 0:
                attitudesSequence.resetActiveProvider(dayObservationLaw)
            else:
                attitudesSequence.resetActiveProvider(nightRestingLaw)

            propagator = KeplerianPropagator(self.orbit, attitudesSequence)

            attitudesSequence.registerSwitchEvents(propagator)

            propagator.propagate(self.date.shiftedBy(self.duration))

        except OrekitException as oe:
            print(oe.getMessage())

        result = []
        tempTrueDate = None
        for el in self.output:
            if el[1] == True:
                tempTrueDate = el[0]
            elif tempTrueDate != None:
                result.append((tempTrueDate, el[0]))

        return result
