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
