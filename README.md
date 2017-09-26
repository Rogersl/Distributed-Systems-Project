# Distributed-Systems-Project
Project covering mutual exclusion on a single-lane bridge.  Includes gui using pygame.

This program was written and tested using Python 3.6.1
It relies on the PyGame 1.9.3 package.
You can get PyGame at https://www.pygame.org/ for the .whl file or just use pip to install it.
(In windows, in the CMD window, go to your python install directory and enter "python -m pip install pygame")

Once both of these are available on your machine, simply run
"main.py" through whatever Python interpreter you want with access 
to these, and it will take care of the rest.

Make sure that all files are in the same directory.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Exectuion: 

- The program opens up in a command line.  

- You will be prompted (with directions) to select which algorithm to run.

- When you select an algorithm, you will be prompted to input speeds for
  4 different people.

- Once all speeds are input, a window will open up to display the GUI.
  The command line will stay open and print the passage of acknowledgements
  between people, as well as when each person interacts with the bridge.

- Close the GUI window when finished, and the command line will prompt
  you to either close, or run another algorithm.  You can use this to
  go through multiple times, testing different speeds on each algorithm.

- When finished, either close the command console window or use the appropriate
  exit input in the command line.
