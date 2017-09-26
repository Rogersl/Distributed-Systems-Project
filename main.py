'''
Logan Rogers
CS 5800
Main function for class Project (Single Lane Bridge)
Directs the user through command line input to display the GUI for
both Ricart and Agrawala's algorithm and the multiple people crossing
algorithm.  
User may input custom speeds from an available set of speeds and repeat
as desired.
'''

import sys
import pygame
import time

from misc import *
import ricart_agrawala
import multi_cross_one_lane

speeds = [1,1,1,1]	#Holder list for speeds of the 4 people

pygame.init()

clock = pygame.time.Clock()

#Loop through options to run different algorithms, set speeds, etc.
def main():
	loop = True
	cont = 0

	while(loop == True):
		#promp user for algorithm selection
		print("Please select which alogirthm you would like to run.")
		print("1. Ricart and Agrawala's one-at-a-time bridge crossing.")
		print("2. Multiple people, same direction algorithm.")
		print("3. Exit.")
		mode = input("Enter option 1 or 2 or 3: ")

		while(True):
			try:
				mode = int(mode)
				if mode < 0 or mode > 3:
					raise ValueError()
				break
			except ValueError:
				mode = input("Please enter valid input: ")

		if(mode == 1):
			get_speeds()
			ricart_agrawala.ricart_agrawala(speeds[0],speeds[1],speeds[2],speeds[3])

		elif(mode == 2):
			get_speeds()
			multi_cross_one_lane.multi_cross_one_lane(speeds[0],speeds[1],speeds[2],speeds[3])

		elif(mode == 3):
			sys.exit()


		#Promp user for continue or not
		print("Would you like to run another algorithm?")
		cont = input("1 = Yes, 0 = No: ")
		while(True):
			try:
				cont = int(cont)
				if cont != 0 and cont != 1:
					raise ValueError()
				break
			except ValueError:
				cont = input("Please enter valid input: ")

		if(cont == 1):
			loop = True
		elif(cont == 0):
			loop = False
			print("Exiting.")

#Function to get speeds of each person.  Will loop for 4 people until
#given 4 valid inputs.  
def get_speeds():
	print("Please enter speeds for the 4 people.")
	print("1 = Slow, 2 = Medium, 3 = Fast, 4 = Very Fast.")
	for i in range(4):
		s = input("{0}: ".format(i))
		while(True):
			try:
				s = int(s)
				if s < 1 or s > 4:
					raise ValueError()
				break
			except ValueError:
				s = input("Please enter valid input for speed {0}: ".format(i))
		if(s == 3):
			speeds[i] = 5
		elif(s == 4):
			speeds[i] = 10
		else:
			speeds[i] = s

if __name__ == '__main__':
	main()


