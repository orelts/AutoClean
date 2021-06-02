"""!
@brief telemtry: class implementation for reading data out of sensors of the vehicle.
optional to connect either to sitl simulation or the real vehicle with uart
"""


from dronekit import connect, GPSInfo
import time
# import dronekit_sitl


def check_none(val):
    if val is None:
        return -1
    else:
        return val

## class for sensors info which saves the needed telem info.
# might alter information to suit to our needs
class SensorsInfo:
    def __init__(self, alt, heading, relative_alt, groundspeed, last_heartbeat):
        ## altitue of vehicle in meters
        self.alt_ = alt
        ## current heading in degrees - 0..360, where North = 0 (int).
        self.heading_ = heading
        self.relative_alt_ = relative_alt
        ## groundspeed of vehicle in meters/second
        self.groundspeed_ = groundspeed
        # self.home_location_ = home_location
        ## Time since last MAVLink heartbeat was received (in seconds).
        #The attribute can be used to monitor link activity and implement script-specific timeout handling.
        self.last_heartbeat_ = last_heartbeat


##
# @brief class to hold dronekit API vehicle handler and connect to it.
# this class connect either to vehicle or simulation and implement methods to read info from pixhawk
class Telemetry:
    ##
    # @brief constructor of telemetry which connects to vehicle or simulation
    # @param vehicle_connected True/False
    def __init__(self, vehicle_connected):
        ## holds True if we're running this on a TX2 connected to the Pixhawk by Uart (Telem2) and False otherwise
        self.vehicleConnected = vehicle_connected

        if not self.vehicleConnected:
            ## simulation handle if we don't use the pixhawk itself
            self.sitl = dronekit_sitl.start_default()  # (sitl.start)
            connection_string = self.sitl.connection_string()  # now we have the connection string (the ip and udp port)

        print("Connecting with the drone")
        if not self.vehicleConnected:
            ## vehicle is a dronekitAPI class for the connection to the vehicle
            self.vehicle = connect(connection_string,
                                   wait_ready=True)  # wait_ready flag hold the program until all the parameters have been read
        else:
            print("Trying to connect")
            self.vehicle = connect('/dev/ttyTHS2', wait_ready=True, # in j121 it was ttyTHS1
                                   baud=57600)  # this is the name of the Pixhawk/Telem2 as the TX2 sees it;
            # the same baud rate as configured in the Pixhawk using Mission Planner
        print("Connection success")


    ##
    # @brief Download the vehicle waypoints (commands) to acquire take-off parameters
    # @param indoor True/False
    # @return -
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

    ##
    # @brief One time read information from the Pixhawk flight computer
    # @param toPrint True/False (optional)
    # @return sensors_info class
    def read_information(self, toPrint=False):
        self.vehicle.wait_ready(True)  # waits for specified attributes to be populated from the vehicle (values are initially None).
        takeoff_alt_barom = self.vehicle.location.global_frame.alt

        # if toPrint:
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

        sensors_info = SensorsInfo(check_none(self.vehicle.location.global_relative_frame.lat),
                    check_none(self.vehicle.heading),
                    check_none(self.vehicle.location.global_frame.alt - takeoff_alt_barom),
                    check_none(self.vehicle.groundspeed),
                    # check_none(self.vehicle.home_location),
                    check_none(self.vehicle.last_heartbeat)
                    )
        return sensors_info

    ## Reads CH8IN (the drone operator can signal the TX2 through this channel). Used for reset the system
    def read_channel8(self):
        self.vehicle.wait_ready(True)
        return self.vehicle.channels['8']

    ##
    # @brief Reads armed status of the system (arm is ready to flight - motors are running) Disarm is while on ground
    # @param -
    # @return vehicle.armed True/False
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

    ##
    # @brief Closing interface & simulation (if there is)
    # @param -
    # @return -
    def close(self):
        self.vehicle.close()
        if not self.vehicleConnected:
            self.sitl.stop()

        print("Telemetry is closed")




# TODO: remove when done presenting it
##
# @brief example of an inheritence class to generate UML in doxygen
class Child(Telemetry):
    pass
