"""
file: telemetry
class implementation for reading data out of sensors of the vehicle
"""

from dronekit import connect, GPSInfo
import time
import dronekit_sitl
import math


def check_none(val):
    if val is None:
        return -1


## class for connection to vehicle sensors or simulation
# by connection and read information methods
class Telemetry:
    ## Connecting to drone
    def __init__(self, vehicle_connected):
        self.vehicleConnected = vehicle_connected  # if we're running this on a TX2 connected to the Pixhawk by Uart (Telem2) - put True. Otherwise, False

        if not self.vehicleConnected:
            self.sitl = dronekit_sitl.start_default()  # (sitl.start)
            connection_string = self.sitl.connection_string()  # now we have the connection string (the ip and udp port)

        print("Connecting with the drone")
        if not self.vehicleConnected:
            self.vehicle = connect(connection_string,
                                   wait_ready=True)  # wait_ready flag hold the program until all the parameters have been read
        else:
            self.vehicle = connect('/dev/ttyTHS1', wait_ready=True,
                                   baud=1500000)  # this is the name of the Pixhawk/Telem2 as the TX2 sees it;
            # the same baud rate as configured in the Pixhawk using Mission Planner
        print("Connection success")

    ## Download the vehicle waypoints (commands) to acquire take-off parameters
    def initialize(self, indoor):
        print("Initialization...")
        if indoor:
            cmds = self.vehicle.commands
            cmds.download()
            cmds.wait_ready()
            print("Indoor initialization completed")
        else:  # if there won't be a GPS signal, we will stuck here (self.vehicle.home_location will be None forever)
            num_satellites = 0
            GPSInfo(None, None, None, satellites_visible=num_satellites)
            while not self.vehicle.home_location:
                cmds = self.vehicle.commands
                cmds.download()
                cmds.wait_ready()
                if not self.vehicle.home_location:  # will be `None` until first set by autopilot and download completes
                    print("Waiting for home location...")
                    time.sleep(1)
            print("\n Home location: {}".format(self.vehicle.home_location))
            print("GPS info: {}".format(self.vehicle.gps_0))
            print("Visible satellites: {}".format(num_satellites))
            print("Outdoor initialization completed")

    ## One time read information from the Pixhawk flight computer
    def read_information(self, toPrint=False):
        self.vehicle.wait_ready(True)  # waits for specified attributes to be populated from the vehicle (values are initially None).
        takeoff_alt_barom = self.vehicle.location.global_frame.alt

        if toPrint:
            # print('Autopilot version: {}'.format(self.vehicle.version))
            # print('Home location (GPS, global WGS84): {}'.format(
            #     self.vehicle.home_location))  # location is set when the vehicle gets a first good location fix from the GPS
            # print('Mean sea level altitude (barometer) is: {:.3f}m'.format(
            #     takeoff_alt_barom))  # can take several seconds longer to populate (taken from the barometer).
            # # Relative to mean sea-level (MSL)
            # print('Current global latitude (GPS, WGS84): {}'.format(
            #     self.vehicle.location.global_relative_frame.lat))  # relative to the WGS84 coordinate system
            # print('Current global longitude (GPS, WGS84): {}'.format(
            #     self.vehicle.location.global_relative_frame.lon))  # relative to the WGS84 coordinate system
            # print('Current global altitude (GPS, WGS84): {}'.format(
            #     self.vehicle.location.global_relative_frame.alt))  # relative to home location
            # print('Current heading: {:.3f} deg ([0 360], north is 0)'.format(
            #     self.vehicle.heading))  # attitude information  # TODO: is this 'DroneCompass'?
            # print('Current relative altitude: {:.3f}m (barometer, from home location):'.format(
            #     self.vehicle.location.global_frame.alt - takeoff_alt_barom))  # relative to takeoff position # TODO PixhawkHeight
            # print('Current yaw: {:.3f} deg'.format(
            #     (180 / math.pi) * self.vehicle.attitude.yaw))
            # print('Current pitch: {:.3f} deg'.format(
            #     (180 / math.pi) * self.vehicle.attitude.pitch))
            # print('Current roll: {:.3f} deg'.format(
            #     (180 / math.pi) * self.vehicle.attitude.roll))
            # print('{})'.format(
            #     self.vehicle.gimbal))  # DroneKit-SITL does not automatically add a virtual gimbal, so this attribute will always report None
            # print('Last Heartbeat: {:.3f}s ago'.format(
            #     self.vehicle.last_heartbeat))  # when did we receive the last heartbeat



        return check_none(self.vehicle.location.global_relative_frame.lat),check_none(self.vehicle.location.global_relative_frame.lon),
               check_none(self.vehicle.location.global_relative_frame.alt,check_none(self.vehicle.heading),check_none(self.vehicle.location.global_frame.alt - takeoff_alt_barom),
               check_none(self.vehicle.gimbal.yaw),check_none(self.vehicle.gimbal.pitch),check_none(self.vehicle.gimbal.roll),check_none(self.vehicle.groundspeed),
               check_none(self.vehicle.home_location),check_none(self.vehicle.battery),check_none(self.vehicle.last_heartbeat)

            ## Reads CH8IN (the drone operator can signal the TX2 through this channel). Used for reset the system
    def read_channel8(self):
        self.vehicle.wait_ready(True)
        return self.vehicle.channels['8']

    ## Reads armed status of the system (arm is ready to flight - motors are running). Disarm is while on ground
    def is_arm(self):
        self.vehicle.wait_ready(True)
        return self.vehicle.armed

    """
    # Constantly show updates in parameters #
    def activeListeners(self):
        print("Adding listeners")
        self.vehicle.add_attribute_listener('attitude', _param_callback)

    # Disable constantly show updates in parameters #
    def deactiveListeners(self):
        print("Removing listeners")
        self.vehicle.remove_attribute_listener('attitude', _param_callback)
        # self.vehicle.remove_attribute_listener('global_relative_frame.lat', _param_callback)
    """

    ## Closing interface & simulation (if there is)
    def close(self):
        self.vehicle.close()
        if not self.vehicleConnected:
            self.sitl.stop()

        print("Telemetry is closed")


"""
# Callbacks function. Attributes that represent sensor values / used to monitor connection status are updated whenever a message is received from the vehicle. #
# Attributes which reflect vehicle “state” are only updated when their values change #
def _param_callback(self, attr_name, value):  # TODO: if not working (do not reflect actual drone params - send handle from 'main' instead of self)
    # print(value)
    return value
"""
