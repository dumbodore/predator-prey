import libpyAI as ai
import math
import sys 

class Predator:

	def __init__(self, name, chromosome):
		self.grid = [["", (200, 200)], ["", (500, 200)], ["", (800, 200)], ["", (1100, 200)], ["", (1400, 200)], ["", (1700, 200)], ["", (2000, 200)],
					["", (200, 500)], ["", (500, 500)], ["", (800, 500)], ["", (1100, 500)], ["", (1400, 500)], ["", (1700, 500)], ["", (2000, 500)],
					["", (200, 800)], ["", (500, 800)], ["", (800, 800)], ["", (1100, 800)], ["", (1400, 800)], ["", (1700, 800)], ["", (2000, 800)],
					["", (200, 1100)], ["", (500, 1100)], ["", (800, 1100)], ["", (1100, 1100)], ["", (1400, 1100)], ["", (1700, 1100)], ["", (2000, 1100)],
					["", (200, 1400)], ["", (500, 1400)], ["", (800, 1400)], ["", (1100, 1400)], ["", (1400, 1400)], ["", (1700, 1400)], ["", (2000, 1400)],
					["", (200, 1700)], ["", (500, 1700)], ["", (800, 1700)], ["", (1100, 1700)], ["", (1400, 1700)], ["", (1700, 1700)], ["", (2000, 1700)],
					["", (200, 2000)], ["", (500, 2000)], ["", (800, 2000)], ["", (1100, 2000)], ["", (1400, 2000)], ["", (1700, 2000)], ["", (2000, 2000)]]
		
		self.gridLength = len(self.grid)

		# stores name of bot 
		self.name = name  

		# used for grid sweeping
		self.counter = 0
		self.checking = False

		# frame counter
		self.frames = 0

		# fitness
		self.fitness = 0

		# used to send bots to opposite ends of grid
		if self.name == "Dumbodore":
			self.grid = self.grid[::-1]

		# stores messages from game
		self.MessageBuffer = ["Blah blah blah"]
		
		# catching the prey
		self.foundPreyFlag = False
		self.parterFoundPreyFlag = False
		self.caughtPreyFlag = False
		self.quitFlag = False
		self.preyLocation = (500, 500)
		self.preyID = -1 

		#-------------------- Extract info from chromosome --------------------#
		self.chromosome = []
		tempGene = []
		for bit in chromosome:
			if len(tempGene) == 8:
				self.chromosome.append(tempGene)
				tempGene = []
			tempGene.append(int(bit))
		self.chromosome.append(tempGene)

		self.gene0 = self.binaryToDecimal(self.chromosome[0])
		self.gene1 = self.binaryToDecimal(self.chromosome[1])
		self.gene2 = self.binaryToDecimal(self.chromosome[2])
		self.gene3 = self.binaryToDecimal(self.chromosome[3])
		self.gene4 = self.binaryToDecimal(self.chromosome[4])
		self.gene5 = self.binaryToDecimal(self.chromosome[5])
		self.gene6 = self.binaryToDecimal(self.chromosome[6])
		self.gene7 = self.binaryToDecimal(self.chromosome[7])
		self.gene8 = self.binaryToDecimal(self.chromosome[8])
		self.gene9 = self.binaryToDecimal(self.chromosome[9])
		self.gene10 = self.binaryToDecimal(self.chromosome[10])
		self.gene11 = self.binaryToDecimal(self.chromosome[11])
		self.gene12 = self.binaryToDecimal(self.chromosome[12])
		self.gene13 = self.binaryToDecimal(self.chromosome[13])
		self.gene14 = self.binaryToDecimal(self.chromosome[14])
		self.gene15 = self.binaryToDecimal(self.chromosome[15])
		self.gene16 = self.binaryToDecimal(self.chromosome[16])
		self.gene17 = self.binaryToDecimal(self.chromosome[17])
		self.gene18 = self.binaryToDecimal(self.chromosome[18])
		self.gene19 = self.binaryToDecimal(self.chromosome[19])
		self.gene20 = self.binaryToDecimal(self.chromosome[20])
		self.gene21 = self.binaryToDecimal(self.chromosome[21])
		self.gene22 = self.binaryToDecimal(self.chromosome[22])
		self.gene23 = self.binaryToDecimal(self.chromosome[23])

		ai.start(self.AI_loop,["-name",name,"-join","136.244.14.6", "-team", "2"])

	def checkSearchComplete(self):
		counter = 0
		for spot in self.grid:
			if spot[0] == "checked!" or spot[0] == "checking!":
				counter = counter + 1
		if counter == self.gridLength or counter == self.gridLength - 1:
			ai.talk("clear!")
			self.counter = 0			
			for spot in self.grid:
				spot[0] = ""
			return True
		else: 
			return False

	def binaryToDecimal(self, gene):

		builder = ""
		for bit in gene:
			builder = builder + str(bit)
			decimal = int(builder, 2)

		return decimal

	def markSpotChecked(self, coordinate, flag):
		for spot in self.grid:
			if spot[1] == coordinate:
				spot[0] = "checked!"
				finished = self.checkSearchComplete()
				
				if finished != True and flag == "me":
					# send message that coordinate is checked 
					ai.talk("checked! " + str(coordinate))
					
					# get new spot
					while self.grid[self.counter][0] == "checked!" or self.grid[self.counter][0] == "checking!":
						self.counter = (self.counter + 1) % self.gridLength
					
					# mark as checking 
					newSpot = self.grid[self.counter][1]
					self.grid[self.counter][0] = "checking!"
					self.checking = False
			
	def setChecking(self, coordinate):
		for spot in self.grid:
			if spot[1] == coordinate:
				spot[0] = "checking!"

	def foundPrey(self, coordinate):
		message = "*** " + str(coordinate)
		ai.talk(message)

	def lostPrey(self):
		message = "--- Lost the enemy!"
		ai.talk(message)

	def caughtPrey(self, coordinate, distance):
		message = "caught! " + str(coordinate)
		ai.talk(message)
		
		if distance <= 100:
			self.caughtPreyFlag = True
		else:
			# get last two messages sent
			lastMessage = self.MessageBuffer[-1]
			secLastMessage = self.MessageBuffer[-2]

			# flags for later
			caught1 = False
			caught2 = False 

			split1 = lastMessage.split(" ")
			split2 = secLastMessage.split(" ")
			sender1 = ""
			sender2 = ""
			
			if "[" in split1[-1]:
				sender1 = split1[-1][1:-1]

			if "[" in split2[-1]:
				sender2 = split2[-1][1:-1]

			if sender1 != "" and sender2 != "" and sender1 != sender2:
				if split1[0] == "caught!" and split2[0] == "caught!":
					self.fitness = self.fitness + 100
					with open('fitness.txt', 'a') as inFile:
						outString = str(self.fitness) + "\n"
						inFile.write(outString)
					ai.quitAI()
																								
	def checkMessage(self, message):

		splitMessage = message.split(" ")
		
		# Checks if message is sent by one of the predators
		if "[" in splitMessage[-1]:
			sender = splitMessage[-1][1:-1]

			# Checks if message wasn't sent by itself
			if sender != self.name:

				# Another grid coordinate checked
				if splitMessage[0] == "checked!":
					coordinate = eval(message[message.find("(")+1:message.find(")")])
					self.markSpotChecked(coordinate, "not me")
					self.checkSearchComplete()

				# Checking sector of grid
				elif splitMessage[0] == "checking!":
					coordinate = eval(message[message.find("(")+1:message.find(")")])
					self.setChecking(coordinate)

				# Grid sweep complete - restart sweep
				elif splitMessage[0] == "clear!":
					self.checkSearchComplete()

				# Parter found enemy 
				elif splitMessage[0] == "***" or splitMessage[0] == "caught!":
					coordinate = eval(message[message.find("(")+1:message.find(")")])
					self.parterFoundPreyFlag = True
					self.preyLocation = coordinate

				# Partner lost enemy 
				elif splitMessage[0] == "---":
					self.parterFoundPreyFlag = False
				
				elif splitMessage[0] == "preyid":
					self.preyID = int(splitMessage[1])

				elif splitMessage[0] == "quit!":
					with open('fitness.txt', 'a') as inFile:
						outString = str(self.fitness) + "\n"
						inFile.write(outString)
					ai.quitAI()

		self.MessageBuffer.append(message)

	def angleDiff(self, a1, a2):
		return 180 - abs( abs(a1 - a2) - 180)

	def distance(self, xi, xii, yi, yii):
	    sq1 = (xi-xii)*(xi-xii)
	    sq2 = (yi-yii)*(yi-yii)
	    return math.sqrt(sq1 + sq2)

	def angleToPoint(self, x, y, targetX, targetY, heading):
		differenceX = targetX - x
		differenceY = targetY - y
		angleDiffRad = math.atan2(differenceY, differenceX)
		angleDiffDegrees = math.degrees(angleDiffRad)
		toTurn = ai.angleDiff(heading, int(angleDiffDegrees))
		return toTurn

	def AI_loop(self):

		# Release keys
		ai.thrust(0)
		ai.turnLeft(0)
		ai.turnRight(0)

		if self.quitFlag == True:
			with open('fitness.txt', 'a') as inFile:
				outString = str(self.fitness) + "\n"
				inFile.write(outString)
			ai.quitAI()
		
		if ai.selfAlive() == 0 or self.frames > 3000:
			self.foundPreyFlag = False
			self.parterFoundPreyFlag = False
			self.checking = False

		if self.foundPreyFlag == True and self.parterFoundPreyFlag == True:
			self.fitness = self.fitness + 2

		#-------------------- Set variables --------------------#
		heading = int(ai.selfHeadingDeg())
		tracking = int(ai.selfTrackingDeg())
		frontWall = ai.wallFeeler(500,heading)
		leftWall = ai.wallFeeler(500,heading+45)
		rightWall = ai.wallFeeler(500,heading-45)
		leftWallStraight = ai.wallFeeler(500,heading+90)
		rightWallStraight = ai.wallFeeler(500,heading-90)
		leftBack = ai.wallFeeler(500,heading+135)
		rightBack = ai.wallFeeler(500,heading-135)
		backWall = ai.wallFeeler(500,heading-180)
		trackWall = ai.wallFeeler(500,tracking)
		R = (heading-90)%360
		L = (heading+90)%360
		aim = ai.aimdir(0)
		bullet = ai.shotAlert(0)
		speed = ai.selfSpeed()
		x = ai.selfX()
		y = ai.selfY()
		enemyX = -1
		enemyY = -1 
		enemyTeam = -1

		if self.preyID != -1:
			enemyX = ai.screenEnemyXId(self.preyID)
			enemyY = ai.screenEnemyYId(self.preyID)
			enemyTeam = ai.enemyTeamId(self.preyID)
		else:
			enemyX = ai.screenEnemyXId(ai.closestShipId())
			enemyY = ai.screenEnemyYId(ai.closestShipId())
			enemyTeam = ai.enemyTeamId(ai.closestShipId())

		myTeam = ai.selfTeam()
		coordinate = self.grid[self.counter][1]
		message = ai.scanMsg(0)

		# Continually check messages 
		if message != self.MessageBuffer[-1]:
			self.checkMessage(message)

		# Check if enemy is on screen 
		# If it is: broadcast location of enemy 	
		if enemyX != -1 and enemyY != -1 and enemyTeam != 2:
			coordinate = (enemyX, enemyY)
			self.foundPreyFlag = True
			self.foundPrey(coordinate)
			self.fitness += 1
		elif self.foundPreyFlag == True:
			self.foundPreyFlag = False
			ai.talk("--- " + "Lost prey!")
		
		if self.parterFoundPreyFlag == True:
			coordinate = self.preyLocation
	
		# Calculate most efficient way to turn to get where we want to
		targetX = coordinate[0]
		targetY = coordinate[1]
		toTurn = self.angleToPoint(x,y,targetX,targetY,heading)
		distance = self.distance(x,targetX,y,targetY)

		
		if self.checking == False and self.foundPreyFlag == False:
			ai.talk("checking! " + str(coordinate))
			self.checking = True

		# If speed is too fast, turn around and thrust to negate velocity
		if speed > self.gene0:
			turning = ai.angleDiff(heading, tracking)
			if abs(turning) > self.gene1 and abs(turning) <= self.gene2:
				ai.turnLeft(0)
				ai.turnRight(0)
				if self.frames % self.gene3 == 0:
					ai.thrust(1)
			elif turning <= self.gene4 and turning > self.gene5:
				ai.turnRight(1)
			else:
				ai.turnLeft(1)

			if self.foundPreyFlag == True and distance <= 150:
				self.caughtPrey(coordinate, distance)

		else: 

			#-------------------- Go to coordinate / enemy --------------------#
			if abs(toTurn) < self.gene6 and distance > self.gene7:
				ai.turnLeft(0)
				ai.turnRight(0)
				if self.frames % self.gene8 == 0:
					ai.thrust(1)
			elif toTurn >= self.gene9:
				ai.turnLeft(1)
			elif toTurn <= -self.gene10:
				ai.turnRight(1)

			if self.foundPreyFlag == True and distance <= 150:
				self.caughtPrey(coordinate, distance)
			elif self.foundPreyFlag == True and distance > 150:
				self.foundPrey(coordinate)
			elif distance < 150:
				self.markSpotChecked(coordinate, "me")


		#-------------------- Old turn and thrust rules --------------------#
		if speed <= self.gene14 and frontWall >= self.gene15:
			ai.thrust(1)
		elif trackWall < self.gene16:
			ai.thrust(1)
		elif backWall < self.gene17:
			ai.thrust(1)
		if (backWall < self.gene18) and (rightWallStraight < self.gene19):
			ai.turnLeft(1)
		elif backWall < self.gene20 and (leftWallStraight < self.gene21):
			ai.turnRight(1)
		elif leftWallStraight < rightWallStraight and trackWall < self.gene22:
			ai.turnRight(1)
		elif leftWallStraight > rightWallStraight and trackWall < self.gene23:
			ai.turnLeft(1)


		self.frames = self.frames + 1

		if self.caughtPreyFlag == True and self.quitFlag == False:
			ai.talk("quit!")
			self.quitFlag = True

		if ai.selfAlive() == 0 or self.frames > 1800:
			self.quitFlag = True
		

def main(*args):
	agent = Predator(sys.argv[2], sys.argv[3])

if __name__ == "__main__":
	main()
