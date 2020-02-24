# drone-scripts
Control and testing scripts for the Crazyflie drone.

# fig8_v3.py
Script that connects to crazyflie, runs a figure 8, and exports x and y position to a csv file
To run: Change OrigPath(line 18) variable to folder you want csv files loaded in. Change URI(line 15) variable to appropriate
radio for crazyflie. Change angle and speed to appropriate values(line 33,34). 

# ExcelExport.py
Script that compiles all csv's in listed folder and extrapolates some data
To run: Change PATH(line 7) variable to folder with csv's. First arg in ExcelWriter(line 9) will be final file name.
Note: Perfect Data is assuming .8 speed and 180 degree angle rate. Changes in the script are needed to account for other values,
especially if the looptime is different after changing those variables

# Fig8Speed.py
Script that connects to crazyflie, runs a figure 8, and exports x and y position to a csv file. 
Runs by setting position points, with loops based on time.
To run: Change OrigPath(line 39) to destination for csv's. Change TIME(line 18) to change runtime(manipulate speed)
NOTE: Seems to not finish if loop is too fast, will get closer to center as time is set to be longer.
NOTE2: At the moment does not change yaw
