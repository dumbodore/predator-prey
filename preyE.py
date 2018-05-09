## Prey for final project
## Mike Riley
## Marcus Vincius
## Jigar Dhimar
import libpyAI as ai
import math

frames = 0

def angleDiff(a1, a2):
  return 180 - abs( abs(a1 - a2) - 180)

def distance(xi, xii, yi, yii):
  sq1 = (xi-xii)*(xi-xii)
  sq2 = (yi-yii)*(yi-yii)
  return math.sqrt(sq1 + sq2)

def angleToPoint(x, y, targetX, targetY, heading):
  differenceX = targetX - x
  differenceY = targetY - y
  angleDiffRad = math.atan2(differenceY, differenceX)
  angleDiffDegrees = math.degrees(angleDiffRad)
  toTurn = ai.angleDiff(heading, int(angleDiffDegrees))
  return toTurn

def checkAngle(angle1, angle2):
  if abs(ai.angleDiff(angle1, angle2))<30:
    return 0.5
  elif abs(ai.angleDiff(angle1, angle2))<60:
    return 0.75
  else:
    return 1

def AI_loop():
  
  # #Release keys
  ai.thrust(0)
  ai.turnLeft(0)
  ai.turnRight(0)

  global frames
  frames+=1

  #Set variables
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
  rightBWall = ai.wallFeeler(500,heading+220)
  leftBWall = ai.wallFeeler(500,heading+140)
  R = (heading-90)%360
  L = (heading+90)%360
  aim = ai.aimdir(0)
  bullet = ai.shotAlert(0)
  speed = ai.selfSpeed()
  enemyX = ai.screenEnemyXId(ai.closestShipId())
  enemyY = ai.screenEnemyYId(ai.closestShipId())
  X= ai.selfX()
  Y= ai.selfY()
  wallBetweenBotEnemy= 1
  distEnemy= -1
  toTurn=-1
  
  if enemyX != -1 and enemyY!= -1:
    distEnemy= distance(X,Y, enemyX, enemyY)
    toTurn = angleToPoint(X,Y, enemyX, enemyY,heading)
  

  if enemyX != -1 and enemyY != -1 :
    wallBetweenBotEnemy = ai.wallBetween(X, Y, enemyX, enemyY)

  #---------------- Thrust rules ----------------#
  if ai.selfSpeed() <= 5 and frontWall >= 98:
    ai.thrust(1)
  elif distEnemy>0 and wallBetweenBotEnemy ==-1 and distEnemy < 180:
    ai.thrust(1)
  elif trackWall < 74 and backWall <=36 and frontWall >= 232: 
    ai.thrust(1)
  elif backWall < 95:
    ai.thrust(1)
  elif leftBWall<160: 
    ai.thrust(1)
  elif rightBWall <146:
    ai.thrust(1)
  

  #---------------- Turn rules ----------------#
  ai.setTurnSpeed(35.0)  
  
  if distEnemy>0 and wallBetweenBotEnemy ==-1:

    #-------initiate wall sensors-----------#
    enemyangle= angleToPoint(X, Y, enemyX, enemyY, heading)
    frontWall = ai.wallFeeler(500,heading) * checkAngle(enemyangle,0)
    leftWall = ai.wallFeeler(500,heading+45) * checkAngle(enemyangle,45)
    rightWall = ai.wallFeeler(500,heading-45) * checkAngle(enemyangle,-45)
    backWall = ai.wallFeeler(500,heading-180) * checkAngle(enemyangle,-180)
    left2 = ai.wallFeeler(500,heading+75) * checkAngle(enemyangle,75)
    right2 = ai.wallFeeler(500,heading-75) * checkAngle(enemyangle,-75)
    left3 = ai.wallFeeler(500,heading+105)  * checkAngle(enemyangle,105)
    right3 = ai.wallFeeler(500,heading-105) * checkAngle(enemyangle,-105)
    left4 = ai.wallFeeler(500,heading+135)  * checkAngle(enemyangle,135)
    right4 = ai.wallFeeler(500,heading-135)  * checkAngle(enemyangle,-135)
    left5 = ai.wallFeeler(500,heading+165)  * checkAngle(enemyangle,165)
    right5 = ai.wallFeeler(500,heading-165) * checkAngle(enemyangle,-165)

    # Creates a list of feelers and check the distance from walls and enemy
    lista=[0, 45,-45,75,-75,105,-105,135,-135,165,-165,-180]
    listb=[frontWall, leftWall, rightWall, left2,right2,left3,right3,left4,right4,left5,right5,backWall]
    mini=max(listb)
    indixm=listb.index(mini)

    if lista[indixm]< 0:
      ai.turnRight(1)
    elif lista[indixm]> 0:
      ai.turnLeft(1)
  
  # Wall avoidance rules! 
  else:  
    if leftBWall <= rightBWall and leftBWall < 184:
      ai.turnRight(1)
    elif rightBWall <= leftBWall and rightBWall < 236:
      ai.turnLeft(1)
    elif leftWallStraight <= rightWallStraight and leftWallStraight <10:
      ai.turnRight(1)
    elif rightWallStraight <= leftWallStraight and rightWallStraight <140:
      ai.turnLeft(1)
    elif leftWall <= rightWall and leftWall<13:
      ai.turnRight(1)
    elif rightWallStraight <= leftWallStraight and rightWallStraight<63:
      ai.turnLeft(1)    
    elif leftWallStraight < rightWallStraight and trackWall < 100:
      ai.turnRight(1)
    elif leftWallStraight > rightWallStraight and trackWall < 243:
      ai.turnLeft(1)

    elif leftWall < rightWall:
      ai.turnRight(1)
    elif rightWall < leftWall:
      ai.turnLeft(1)

  # if we are going too fast, then slow down
  
  if speed > 8:
    turning = ai.angleDiff(heading, tracking)
    if abs(turning) > 125 and abs(turning) <= 187:
      ai.turnLeft(0)
      ai.turnRight(0)
      if frames % 10 == 0:
        ai.thrust(1)
    elif abs(turning) <= 165:
      ai.turnRight(1)

  if distEnemy >0 and distEnemy <100:
    ai.thrust(1)

ai.start(AI_loop,["-name","prey", "-join", "localhost"])