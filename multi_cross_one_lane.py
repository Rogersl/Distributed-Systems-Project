'''
Logan Rogers
CS5800 class project
This file contains the functions for running a modified mutual exlusion
on a single lane bridge.  Mutliple people moving the same direction may
cross the bridge if they come immediately after the other.  Otherwise,
they must wait at the end of the bridge until acknowledged by all other
people.  Due the the use of timestamps, no person may be prevented from
crossing the bridge indefinitely.
'''

import sys
import pygame
import time
from misc import *

#Initiate times list, respective of people.  bignum = no timestamp (lazy way)
times = [bignum,bignum,bignum,bignum]

#Create empty check lists.  
people = []
#people_on_bridge = []
#times_on_bridge = []

clock = pygame.time.Clock()

#Container class for our "people"
class circle:
	def __init__(self, num, color, speed, direction, start_x, start_y, delta_x, delta_y):
		self.id = num
		self.color = color
		self.spd = speed
		self.dir = direction
		self.X = start_x
		self.Y = start_y
		self.dX = delta_x
		self.dY = delta_y
		self.timestamp = bignum
		self.wait = False
		self.other_people = []
		self.acks = []
		self.buffer = []
		self.on_bridge = False

	#Precondition: Person is at entrance to bridge.
	#Request access to the bridge.  Requesting person broadcasts request and
	#receives timestamp.  Timestamp is compared to that of other people.
	#If timestamp is lower, it gets ack from others.  If higher, it checks
	#if they are going in the same directions.  If yes, give ack.  If not,
	#send to buffer.  The same is done with people already on the bridge.
	def request_access(self):
		self.timestamp = time.time()
		print("{0} is requesting access to the bridge.".format(self.id))
		for p in self.other_people:
			if p.on_bridge == True and p.dir != self.dir:
				p.buffer.append(self)
			elif p.timestamp < self.timestamp and p.dir != self.dir:
				p.buffer.append(self)
			else:
				self.acks.append(p)
				print("{0} sends ack to {1}".format(p.id,self.id))

		times[self.id] = self.timestamp
		self.wait = True

	#Precondition: Person is at entrance to bridge.
	#Check that a person has received ack from all others.  Cross bridge if so.
	def try_enter_bridge(self):
		if set(self.acks) == set(self.other_people):
			print("{0} is crossing the bridge.".format(self.id))
			self.wait = False
			self.on_bridge = True

	#Precondition: Person is at exit to bridge.
	#Broadcast exit from bridge
	def exit_bridge(self):
		#people_on_bridge.remove(self)
		#times_on_bridge.remove(self.timestamp)
		print("{0} has exited the bridge.".format(self.id))
		for p in self.buffer:
			print("{0} sends ack to {1}".format(self.id, p.id))
			p.acks.append(self)
		self.timestamp = bignum
		del self.acks[:]
		del self.buffer[:]
		self.on_bridge = False
		times[self.id] = self.timestamp

#Draws the baseline display without the people represented.
def draw_stage(screen):
	screen.fill(white)
	pygame.draw.lines(screen, black, True, [NE, SE, bridge_E], 1)
	pygame.draw.lines(screen, black, True, [NW, SW, bridge_W], 1)
	pygame.draw.lines(screen, black, False, [bridge_W, bridge_E], 1)

#Clear variables that would be leftover in subsequent runs
def clear_vars():
	del people[:]
	times = [bignum,bignum,bignum,bignum]

#Main function for algorithm to let multiple people cross in the same directions.
#Mostly just a driver function that updates the GUI.
def multi_cross_one_lane(speed1, speed2, speed3, speed4):

	#Create our display and our people
	screen = pygame.display.set_mode((screen_x,screen_y))
	p1 = circle(0, blue, speed1, 'E', NW[0], NW[1], 1, 1)
	p2 = circle(1, red, speed2, 'E', SW[0], SW[1], 0, -1)
	p3 = circle(2, green, speed3, 'W', NE[0], NE[1], 0, 1)
	p4 = circle(3, pink, speed4, 'W', SE[0], SE[1], -1, -1)
	draw_stage(screen)

	#Set list of people and lists of others for every person
	people.extend([p1,p2,p3,p4])
	p1.other_people = [p2,p3,p4]
	p2.other_people = [p1,p3,p4]
	p3.other_people = [p1,p2,p4]
	p4.other_people = [p1,p2,p3]

	#Place each person at their initial position
	for person in people:
		pygame.draw.circle(screen, person.color, (person.X, person.Y), 20, 0)

	#Draw the initial display
	pygame.display.update()

	'''
	Display loop.
	This loop will run through the operations of the algorithm until the user
	exits.  It wipes the display clean, re-draws everything at the new position,
	and updates data as needed before updating the actualy display at 30 frames
	per second.
	'''
	while(True):
		clock.tick(30)
		screen.fill(white)
		draw_stage(screen)

		'''
		Check every person's position.  If needed, adjust their movement direction to stay
		on the path.  If at the entrance or exit to a bridge, communicate with other people 
		to see if they may pass over the bridge, or let others know they have crossed the bridge.
		'''
		for person in people:
			if person.X == NW[0] and person.Y == NW[1]:
				person.dX = person.spd
				person.dY = person.spd
				person.dir = 'E'
			elif person.X == SW[0] and person.Y == SW[1]:
				person.dX = 0
				person.dY = -person.spd
			elif person.X == bridge_W[0] and person.Y == bridge_W[1] and person.dir == 'W':
				person.dX = -person.spd
				person.dY = person.spd
				person.exit_bridge()
			elif person.X == bridge_W[0] and person.Y == bridge_W[1] and person.dir == 'E':
				person.dX = person.spd
				person.dY = 0
				if person.wait == False:
					person.request_access()
				if person.wait == True:
					person.try_enter_bridge()
			elif person.X == bridge_E[0] and person.Y == bridge_E[1] and person.dir == 'W':
				person.dX = -person.spd
				person.dY = 0
				if person.wait == False:
					person.request_access()
				if person.wait == True:
					person.try_enter_bridge()
			elif person.X == bridge_E[0] and person.Y == bridge_E[1] and person.dir == 'E':
				person.dX = person.spd
				person.dY = -person.spd
				person.exit_bridge()
			elif person.X == NE[0] and person.Y == NE[1]:
				person.dX = 0
				person.dY = person.spd
			elif person.X == SE[0] and person.Y == SE[1]:
				person.dX = -person.spd
				person.dY = -person.spd
				person.dir = 'W'

			#move people
			if(person.wait == False):
				person.X = person.X + person.dX
				person.Y = person.Y + person.dY

			pygame.draw.circle(screen, person.color, (person.X, person.Y), 20, 0)

		#update the display to reflect all changes made.
		pygame.display.update()

		#check for exit input from user (window close button)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				clear_vars()
				pygame.quit();
				return