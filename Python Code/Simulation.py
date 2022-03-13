from pickle import FALSE
from re import S
from turtle import distance
import pygame
import math 

pygame.init()

WIDTH, HEIGHT = 800, 800

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Planet Simulation')

WHITE = (255, 255, 255) #RGB value for white
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)

FONT = pygame.font.SysFont("comicsans", 16)

class Planet:
    AU = 149.6e6 * 1000 #Represents Austronomical Units multiple by 1000 to get distance in metres. 
    G = 6.67428e-11 #Represents gravitaitional constant
    SCALE = 250 / AU #1 AU = 100 Pixels. Reduces scale of Visualisation. 
    TIMESTEP = 3600*24 #Represents time in one day.

    #x and y are positions of planets. 
    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False #Tells us if Planet is Sun. we want orbit around sun and not Sun.
        self.distance_to_sun = 0


        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH/2
        y = self.y * self.SCALE + HEIGHT/2

        if len(self.orbit) > 2:
        #Obtaining a list of all the updated points which will contain the x, y coordinates to Scale
            updated_points = []
            for point in self.orbit:
                x, y = point 
                x = x* self.SCALE + WIDTH/2
                y = y * self.SCALE + HEIGHT/2
                updated_points.append((x,y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)


        pygame.draw.circle(win, self.color, (x,y), self.radius)
        #This code is after the draw circle to avoid circle overalpping text. 
        if not self.sun:
            #Place text onto graph simulation
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 2)}km", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width()/2, y- distance_text.get_height()/2))

    def attraction(self, other):
        #We begin by clauclating the distance between the two objects.
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        #If the distance is the Sun we want to sttore it as a property since we want to determin what the value is.
        if other.sun:
            self.distance_to_sun = distance

        #Calulcate force of attraction
        force = self.G * self.mass *other.mass / distance**2
        
        #Breaking down the denominator into the 2 forces. 
        theta = math.atan2(distance_y,distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        #Obtaining total forces exerted on planet that is not itslef. 
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
        
        #Calculate x and y velocities. 
        self.x_vel += total_fx/self.mass * self.TIMESTEP
        self.y_vel += total_fy/self.mass * self.TIMESTEP

        #Update x and y position using TIMESTEP to maintain correct time
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        
        #Appending the x and y position to help with drawing the orbit. 
        self.orbit.append((self.x, self.y))



#Setting up event loop to enter and exit pygame window
def main():
    run = True

    #Regulates frame rate for game. Important to maintain time 
    clock = pygame.time.Clock()

    #Creating the sun and planets
    sun = Planet(0,0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True #=> This is to make sure we don't draw orbit of Sun and distance from sun

    #Velocity varibales are converted from km/s to m/s
    #If x parameter in Planet is postive, y needs to be negative and vice versa

    earth = Planet(-1 *Planet.AU, 0, 16, BLUE, 5.9742 *10**24) #-ve means to the left of the sun and +ve is right of the sun
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 *Planet.AU, 0, 12, RED, 6.39 * 10 **23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 *10**23)
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000

    planets = [sun,earth, mars, mercury, venus]
    #Loops through Frames and Updates the screen with White background
    while run:
        clock.tick(60)
        WIN.fill((0,0,0))
        #pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()
    pygame.quit()

main()
