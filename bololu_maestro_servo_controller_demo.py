import time
import maestro
servo = maestro.Controller()

# x = servo.getPosition(0) #get the current position of servo 1
# print('a: {}'.format(x))

# servo.setAccel(0,10)      #set servo 0 acceleration to 4
# servo.setTarget(0,6000)  #set servo to move to center position
# servo.setSpeed(0,30)     #set speed of servo 1
# print('b...')
# # # x = servo.getPosition(0) #get the current position of servo 1
# # # print('b: {}'.format(x))
# x = servo.getMin(0)
# print('min: {}'.format(x))
# x = servo.getMax(0)
# print('max: {}'.format(x))
# time.sleep(4)

servo.setAccel(0,10)      #set servo 0 acceleration to 4
servo.setTarget(0,2000)  #set servo to move to center position
servo.setSpeed(0,100)     #set speed of servo 1
# x = servo.getPosition(0) #get the current position of servo 1
# print('c: {}'.format(x))
print('2000')

time.sleep(10)

# servo.setAccel(0,40)      #set servo 0 acceleration to 4
# servo.setTarget(0,6000)  #set servo to move to center position
# servo.setSpeed(0,100)     #set speed of servo 1
# print('6000')
# time.sleep(5)


servo.setAccel(0,20)      #set servo 0 acceleration to 4
servo.setTarget(0,10000)  #set servo to move to center position
servo.setSpeed(0,100)     #set speed of servo 1
# x = servo.getPosition(0) #get the current position of servo 1
# print(x)
print('10000')
time.sleep(10)



servo.close()
print("Done!")