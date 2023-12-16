import pygame
import numpy as np
from base_functs import getAcc, getEnergy  # Import your custom functions

# Constants
pygame.init()
tEnd = 10.0
plotRealTime = True  #switch on for plotting as the simulation goes along

screen_width = 1200    
screen_height = 600

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Background")
font = pygame.font.SysFont("PixeloidSans-mLxMm.ttf", 40)

def draw_text(text, font, text_col, x, y):
  font_r = pygame.font.SysFont(font, 15)
  img = font_r.render(text, True, text_col)
  screen.blit(img, (x, y))

# Function to convert coordinates from simulation space to screen space
def sim_to_screen_x(val_x, rect_width):
    return ((val_x + 2) * rect_width / 4)

def sim_to_screen_y(val_y, rect_height):
    return ((val_y + 2) * rect_height / 4)

# Simulation Main Loop
def run_simulate(N, tEnd, screen, x_spawn, y_spawn, dt=0.01):
    clock = pygame.time.Clock()
    # rect surface
    rect_width = 500
    rect_height = 400
    rect_surface = pygame.Surface((rect_width, rect_height))

    # Simulation parameters
    t = 0
    # Nt = int(np.ceil(tEnd / dt))

    # Generate Initial Conditions
    np.random.seed(17)
    mass = 20.0 * np.ones((N, 1)) / N
    pos = np.random.randn(N, 3)
    vel = np.random.randn(N, 3)
    vel -= np.mean(mass * vel, 0) / np.mean(mass)

    softening = 0.1  # softening length
    G = 1  # Newton's Gravitational Constant

    run =  True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Calculate accelerations
        acc = getAcc(pos, mass, G, softening)

        # Update positions and velocities
        vel += acc * dt
        pos += vel * dt
        
        x_cm, y_cm = 0, 0
        
        # Update time
        t += dt

        # Clear the rectangular surface
        rect_surface.fill((255, 255, 255))

        # Plot the particles on the rectangular surface
        for p in range(N):
            x, y, _ = pos[p]
            x, y = sim_to_screen_x(x, rect_width), sim_to_screen_y(y, rect_height)
            pygame.draw.circle(rect_surface, (0, 0, 255), (int(x), int(y)), int(150*(1/(min(40,N)))))
            # print(N)
            
            if t >= tEnd*0.1:
                x_cm = np.mean(pos[:,0]) 
                y_cm = np.mean(pos[:,1]) 
                x_input, y_input = sim_to_screen_x(x_cm,rect_width), sim_to_screen_y(y_cm, rect_height)
                # print(x_input, y_input)
                pygame.draw.circle(rect_surface, (255, 0, 0), (int(x_input), int(y_input)), 4)

        # Blit the rectangular surface onto the main screen

        screen.blit(rect_surface, (x_spawn, y_spawn))
        pygame.display.flip()
        
        if t >= tEnd:
            run = False  
            return(screen)
        
        clock.tick(60)
             

    # Exit pygame
    pygame.quit()

# run_simulate(40, 30, screen, 650, 100)

import pygame
import math
import numpy as np
import matplotlib.pyplot as plt


def calculate_elliptical_orbit(eccentricity, semi_major_axis, num_points=100000):
    thetas = np.linspace(0, 2 * np.pi, num_points)
    radii = (semi_major_axis * (1 - eccentricity ** 2)) / (1 + eccentricity * np.cos(thetas))

    x_coords = radii * np.cos(thetas)
    y_coords = radii * np.sin(thetas)

    return x_coords, y_coords

def sim_to_screen_x_2(val_x, rect_width, ecc,semi_major_axis):
    return(val_x+semi_major_axis+rect_width+(200*ecc))
    # return (val_x+semi_major_axis+1)*rect_width/2*ecc

def sim_to_screen_y_2(val_y, rect_height,ecc,semi_minor_axis):
    return(val_y+semi_minor_axis+rect_height)
    # return (val_y+semi_minor_axis)*rect_height/2*ecc

def sim_M(x,y,rect_width,rect_height,ecc,semi_major_axis,semi_minor_axis, x_min, c):
    x_val = semi_major_axis*(1-ecc)
    x_sun = (x_min+semi_major_axis+rect_width+(200*ecc)) + x_val
    y_sun = y+semi_minor_axis+rect_height
    return(int(x_sun), int(y_sun))

def run_sim_2body(ecc, semi_major_axis, tEnd, dt, screen, x_spawn, y_spawn):
    clock = pygame.time.Clock()
    b = semi_major_axis*(math.sqrt(1-(ecc**2)))
    t = 0

    a = 130/(math.sqrt(1-(ecc**2)))
    b_scale = 130
    c = ecc*semi_major_axis

    rect_width = 500
    rect_height = 350
    rect_surface = pygame.Surface((rect_width, rect_height))
    scale_width = 1*rect_width/10
    scale_height = 1*rect_height/10
    x_cords, y_cords = calculate_elliptical_orbit(ecc, a)
    avg_x, avg_y = np.mean(x_cords),np.mean(y_cords)
    diam = np.max(x_cords)-np.min(x_cords)
    diam_v = sim_to_screen_y_2(np.min(y_cords),scale_height,ecc, b_scale)
    x_right = sim_to_screen_x_2(x_cords[1],scale_width,ecc,a)
    y_axis = sim_to_screen_y_2(y_cords[1],scale_height,ecc, b_scale)


    run =  True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        t += dt
        rect_surface.fill((255, 255, 255))

        # print(avg_x,avg_y)

        point_index = int((t/tEnd)*(len(x_cords)-1))
        
        x, y = x_cords[point_index], y_cords[point_index]
        x, y = sim_to_screen_x_2(x, scale_width,ecc,a), sim_to_screen_y_2(y, scale_height,ecc, b_scale)
        pygame.draw.circle(rect_surface, (0, 0, 255), (int(x), int(y)), 4)
        
        sun_cord = sim_M(np.mean(x_cords), np.mean(y_cords),scale_width,scale_height,ecc,a,b_scale, np.min(x_cords),c)
        pygame.draw.circle(rect_surface, "black", sun_cord, 20) #M>>m (180,165)

        # semi major axis
        pygame.draw.line(rect_surface, "red", (x_right-(diam/2),y_axis), (x_right, y_axis), 4)
        # semi minor y_axis
        pygame.draw.line(rect_surface, "cyan", (x_right-(diam/2),y_axis), (x_right-(diam/2), diam_v), 4)
        #sun to satellite
        pygame.draw.line(rect_surface, "grey", (x_right-(diam/2),y_axis), (x,y), 2)

        screen.blit(rect_surface, (x_spawn, y_spawn)) 
        #label
        draw_text("Semi-minor axis"+str(round(b,2))+"AU", "PixeloidSans-mLxMm.ttf", "black", x_right-(diam/2)+x_spawn+ 5, diam_v+10+y_spawn)     
        draw_text("Semi-Major axis "+ str(semi_major_axis) + "AU", "PixeloidSans-mLxMm.ttf", "red", x_right+x_spawn-100, y_axis+y_spawn+10)
        pygame.display.flip()
        clock.tick(60)


        if t >= tEnd:
            run = False   
            return(screen)

    # Exit pygame
    pygame.quit()


# screen = pygame.display.set_mode((700, 700))
# for _ in range(5):    
#     run_sim_2body(0.8, 1000, 20, 0.1, screen, 60, 60)

import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bordered Rectangle Example")

def border(x, y, width, height, color1, color2,border_thickness):
    pygame.draw.rect(screen, color1, (x, y, width, height))
    pygame.draw.rect(screen, color2, (x, y, width, height), border_thickness)
