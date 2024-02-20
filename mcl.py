
import math
import random
import time
from bot_control.PositionControl import PositionControlBot, Bot
from particleDataStructures import canvas, mymap
import brickpi3

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
motorR = BP.PORT_C # right motor
motorL = BP.PORT_B # left motor

from typing import Tuple, Dict

Coordinate = Tuple[int, int]
Wall = Tuple[Coordinate, Coordinate]

walls: Dict[int, Wall] = {
    1: ((210, 84), (210, 0)),
    2: ((168, 84), (210, 84)),
    3: ((0, 0), (0, 168)),
    4: ((84, 210), (168, 210)),
    5: ((84, 126), (84, 210)),
    6: ((210, 0), (0, 0)),
    7: ((0, 0), (0, 168)),
    8: ((210, 0), (0, 0))
}

wall = None
particles = [(float(84), float(30), float(0)) for _ in range(100)]
weights = [1 / len(particles) for _ in range(len(particles))]
forward_dist=833
turn_amount=256

def wall_dist(x, y, theta, wall: Wall):
    (a_x, a_y), (b_x, b_y) = wall
    return ((b_y - a_y)*(a_x - x) - (b_x - a_x)*(a_y - y)) / ((b_y - a_y)*math.degrees(math.cos(theta)) - (b_x - a_x)*math.degrees(math.sin(theta)))


def find_closest_wall(x, y, theta):
    # global current_wall
    # return walls[current_wall]
    # will change to code below
    min_m = float('inf')
    min_wall = None
    for wall in walls.values():
        m = wall_dist(x, y, theta, wall)
        if m < min_m:
            min_m = m
            min_wall = wall
            
    if min_m < 0:
        return None
    return min_wall



def calc_angle(theta, wall: Wall):
    (a_x, a_y), (b_x, b_y) = wall
    num = math.degrees(math.cos(theta))*(a_y - b_y) + math.degrees(math.sin(theta))*(b_x - a_x)
    den = math.sqrt((a_y - b_y)**2 + (b_x - a_x)**2)
    return math.degrees(math.acos(num/den))
    


def calculate_likelihood(x, y, theta, z):
    sigma = 0.02    
    global wall
    wall = find_closest_wall(x, y, theta)

    # didn't detect a valid wall, so likelihood here is 0
    if not wall:
        return 0
    
    m = wall_dist(x, y, theta, wall)
    return math.exp((-(-z-m)**2)/2*sigma**2) + 0


def norm():
    global weights
    total = sum(weights)
    for weight in weights:
        weight = weight / total

def resample():
    global weights
    global particles
    population = random.choices(list(zip(particles, weights)), weights=weights, k=100)
    [particles, weights] = list(zip(*population))


def update_weights(sonar):
    dist = 20
    for i in range(len(particles)):
        e = random.gauss(0, 0.02)
        f = random.gauss(0, 0.015)

        x, y, theta = particles[i]  # Unpack the tuple
        x += (dist + e) * math.cos(theta)
        y += (dist + e) * math.sin(theta)
        theta += f
        particles[i] = (x, y, theta)
        
        likelihood = calculate_likelihood(x, y, theta, sonar)
        if not wall:
            return
        if calc_angle(theta, wall) > 15:
            return
        weights[i] = likelihood * weights[i]
    norm()
    resample()
    print("drawParticles:" + str(particles))

try:
    bot = Bot()
    bot.reset_bp()
    posControlBot = PositionControlBot(bot, 200)
    mymap.draw()
    while True:    
        posControlBot.move_forward(833/2)
        time.sleep(3)
        sonars = [bot.get_ultrasonic_sensor_value() for _ in range(10)]
        print(sonars)
        sonar = sum(sonars) / len(sonars)
        update_weights(sonar)
        canvas.drawParticles(particles)
        time.sleep(3)
                
except KeyboardInterrupt:
    BP.reset_all()