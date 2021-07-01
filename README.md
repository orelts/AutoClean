# AutoClean

<h1 align="center">
  <img src="./assets/Driver.gif" height="200" width="400">
</h1>
  <p align="center">
    <a href="mailto:oreltsioni@gmail.com">Orel Tsioni</a> •
    <a href="mailto:itamar.meyer@campus.technion.ac.il">Itamar Meyer</a>
  </p>

Welcome to AutoClean. Number 1 autonomous world cleaner in the world
in this project we implemented the basic infrastructure for the world cleaner robot. 
this was done by different modules we will elaborate about.


- [AutoClean](#autoclean)
  * [SQL database](#sql-database)
  * [Sensors](#sensors)
  * [Driver](#driver)
  * [Communication](#communication)
  * [Crane](#crane)
  * [Further Work](#further-work)


## SQL database
The center of all data transmission. all modules commuinicate with the sql server by writing and reading from it when needed.
this way we create modularity in our software and we create an easy environment for future development.
the sql server is Azure SQL Edge which runs on the ubuntu of the TX2 nvidia device via docker. We are using it for sensors and driver module use cases such as driver need to operate based on sensors information or driver need to execute a driving command. The SQL database holds those commands and sensors info in different tables and all the modules communicate through them.
## Sensors
This module is all about getting the info from the pixhawk(sensors device) and deliver it to the sql server
## Driver
<h1 align="center">
  <img src="./assets/Driver.gif" height="200" width="400">
</h1>
The driver modules gets a string of driving instructions which he can parse. those instructions are coming from the instructions list in the sql db
this way we can control the driving while creating the base for future module to send the instructions itself.
Driver uses 4 motors that gets command from sabertooth controller 2x12 which gets commands from the nvidia TX2.
## Communication
This module role is to be the mediator between groundstation and the world cleaner. also if needed to communicate between devices on robot itself
## Crane
<h1 align="center">
  <img src="./assets/Crane.gif" height="200" width="400">
</h1>
The world Cleaner uses a 3D printed claw with 3 axis. Each of the 3 axis is moving using 2 servo motors which conrolled by lynxmotion controller. the linxmotion gets commands from the crane sql table that is on nvidia TX2
## Further Work
Implement Computer Vision based module for navigation controll. Also, implement and add a CNN for Trash classification and recognition for Crane operation.
