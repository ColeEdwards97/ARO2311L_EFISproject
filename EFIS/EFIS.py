### IMPORTS
# general
import os
import time
import threading
# gpio libraries
import RPi.GPIO as GPIO
import board
import busio
os.system("sudo pigpiod")
time.sleep(1)
import pigpio
#sensor libraries
from adafruit_bno055 import BNO055
from hx711 import HX711
from strain_guage import LoadCell
from gpiozero import MCP3008
# gui
from HUD import *



### ==============
### INITIALIZATION
### ==============
GPIO.setmode(GPIO.BCM)



### ================
### CREATE PROTOCOLS
### ================
# i2c
i2c = busio.I2C(board.SCL, board.SDA)
# pwm
ESC=4
pi = pigpio.pi();
pi.set_servo_pulsewidth(ESC, 0)



### =======================
### CREATE SENSORS/SWITCHES
### =======================
# accelerometer
sens_acc = BNO055(i2c)
# load cell
sens_lc  = HX711(dout_pin=21, pd_sck_pin=20)
obj_lc = LoadCell(sens_lc)
obj_lc.start()
# dc motor
pwm_max = 2000
pwm_min = 1000
pot = MCP3008(0)
# switches
switch_1 = [26, 19]
switch_2 = [13, 6]
GPIO.setup(switch_1[0], GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch_1[1], GPIO.OUT)
GPIO.setup(switch_2[0], GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch_2[1], GPIO.OUT)


### =======
### METHODS
### =======
## accelerometer
# get heading in aircraft coords from euler rotation
def aircraft_heading(euler):
    (yaw,pitch,roll) = euler
    return (-pitch, -roll-90, yaw)

## load cell
# sets the tare for the load cell
def get_load():
    return sens_lc.get_weight_mean()

## dc motor
# sets pwm for servo
def get_throttle():
    pot = MCP3008(0)
    pwmout = int(round(1000 + pot.value*1000))
    pi.set_servo_pulsewidth(ESC, pwmout)
    return pot.value*100

## switches
# gets switch state
def update_switch(switch):
    button_state = GPIO.input(switch[0])
    if not button_state:
        GPIO.output(switch[1], True)
    else:
        GPIO.output(switch[1], False)




### INITIALIZE GUI

# Initialise screen.
pygame.init()
screen = pygame.display.set_mode((1024, 768))
screen.fill(0x222222)
myfont = pygame.font.SysFont('Courier New', 12, bold=True)
   
# Initialise Dials.
horizon = Horizon(300,180)
heading = Heading(600,180)
throttle = Throttle(0,180)



### =========
### MAIN LOOP
### =========
while True:

    ## accelerometer
    HEAD = aircraft_heading(sens_acc.euler)
    TEMP = sens_acc.temperature
    #print('heading (deg.): roll {:.3f}    pitch {:.3f}   yaw {:.3f}'.format(*HEAD))

    ## load cell
    LOAD = obj_lc.load
    LOAD_BIN = obj_lc.bin
    #print('load (g): {}'.format(LOAD))
    #print('load (bin): {}'.format(LOAD_BIN))

    ## dc motor
    THROT = get_throttle()
    #print('throttle: {:.3f}'.format(THROT))

    ## switches
    update_switch(switch_1)
    update_switch(switch_2)




    ## pygame events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
        if event.type == QUIT:
            print ("Exiting....")
            pygame.quit()

    screen.fill(0x222222)

    ## update dials
    horizon.update(screen, HEAD[0], HEAD[1])
    heading.update(screen, HEAD[2])
    throttle.update(screen, THROT)

    ## render text
    AA = False
    COLOR = (255, 255, 255)
    localtime = time.asctime( time.localtime(time.time()) )
    time_text = myfont.render('TIME    ' + localtime, AA, COLOR)
    roll_text = myfont.render('ROLL    %.3f' % HEAD[0], AA, COLOR)
    pitch_text = myfont.render('PITCH   %.3f' % HEAD[1], AA, COLOR)
    yaw_text = myfont.render('YAW     %.3f' % HEAD[2], AA, COLOR)
    temp_text = myfont.render('TEMP    %.3f' % TEMP, AA, COLOR)
    rpm_text = myfont.render('THROT    %i' % THROT, AA, COLOR)
    cargo_text = myfont.render('LOAD    %.3f' % LOAD, AA, COLOR)
    start = 25
    step = 20
    screen.blit(time_text,(10,start + 0*step))
    screen.blit(roll_text,(10,start + 1*step))
    screen.blit(pitch_text,(10,start + 2*step))
    screen.blit(yaw_text,(10,start + 3*step))
    screen.blit(temp_text,(10,start + 4*step))
    screen.blit(rpm_text,(10,start + 5*step))
    screen.blit(cargo_text,(10,start + 6*step))


    pygame.display.update()






