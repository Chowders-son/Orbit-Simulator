import pygame
import numpy as np
from base_functs import getAcc, getEnergy  # Import your custom functions
from pygame_menu import Menu
from Button import Button
from N_body import run_simulate, run_sim_2body, border
from QuestionAnswer import InputBox, Input_n_part,input_run_time, Input_ecc, Input_sm_axis
import math


pygame.init()

#create game window
screen_width = 1200
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Celestial Orbitpy")
#image background
background_img = pygame.image.load("space.png")
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

#define fonts
font = pygame.font.SysFont("arialblack", 40)

#define colours
TEXT_COL = (255, 255, 255)

#load button images
npart_img = pygame.image.load("N_Body_System.png").convert_alpha()
body2_img = pygame.image.load("2_Body_System.png").convert_alpha()
back_img = pygame.image.load("Back.png").convert_alpha()
run_img = pygame.image.load("Run.png").convert_alpha()

body_bio = pygame.image.load("2body_bio.png").convert_alpha()
Npart_bio = pygame.image.load("nbody_bio.png").convert_alpha()
cel_title = pygame.image.load("Celestial_Orbit.png").convert_alpha()


npart_img_tit = pygame.transform.scale(npart_img, (int(npart_img.get_width())/2, int(npart_img.get_height())/2))
body2_img_tit = pygame.transform.scale(body2_img, (int(body2_img .get_width())/2, int(body2_img .get_height())/2))

#create button instances
y_cent = (screen_height/2)
x_cent = (screen_width/2)
npart_button = Button(x_cent - (npart_img.get_width()), y_cent, npart_img, 3/4)
body2_button = Button(x_cent + (body2_img.get_width()/4), y_cent, body2_img, 3/4)
back_button = Button(screen_width/10, (screen_height - (screen_height/8)), back_img, 1/3)
run_w, run_h = run_img.get_size()
run_button = Button((screen_width-run_w/3)/2 , (screen_height - (screen_height/8)), run_img, 1/3)

#width/heights
scale_factor = 0.55
tit_width = int(cel_title.get_width() * scale_factor)
tit_height = int(cel_title.get_height() * scale_factor)
body_width = int(body_bio.get_width()*0.65)
body_height = int(body_bio.get_height()*0.65)
npart_width = int(Npart_bio.get_width()*0.5)
npart_height = int(Npart_bio.get_height()*0.5)

# Scale the images
scaled_tit = pygame.transform.scale(cel_title, (tit_width, tit_height))
cel_title_rect = scaled_tit.get_rect()
cel_title_rect.x = (screen_width - tit_width)// 2
cel_title_rect.y = screen_height - 2*tit_height- 70

scaled_nbody_bio = pygame.transform.scale(Npart_bio, (npart_width, npart_height))
nbody_bio_rect = scaled_nbody_bio.get_rect()
nbody_bio_rect.x = x_cent - (npart_img.get_width())- 20
nbody_bio_rect.y = y_cent+(npart_img.get_width())/4

scaled_2body_bio = pygame.transform.scale(body_bio, (body_width, body_height))
body_bio_rect = scaled_2body_bio.get_rect()
body_bio_rect.x = x_cent + (body2_img.get_width()/4)-60
body_bio_rect.y = y_cent+(body2_img.get_width())/4


def draw_text(text, font, text_col, x, y):
  font_r = pygame.font.SysFont(font, 24)
  img = font_r.render(text, True, text_col)
  screen.blit(img, (x, y))

#user text
base_font = pygame.font.Font(None, 32)
user_txt = "N body yody"

#box instances
input_box_particles = Input_n_part("Number of particles:", 100, 200, 230, 70)
input_duration = input_run_time("Duration:", 100, 300, 200, 70)
input_ecc = Input_ecc("Eccentricity:", 100, 200, 240, 70)
input_sm_axis = Input_sm_axis("Semi-Major Axis:", 100, 300, 200, 70)

#game varibles for decision making
game_state = True
state = "main_menu"
val = 0

clock = pygame.time.Clock()
input_values_valid = True

run = True
#game loop
while run:

  screen.fill((0,0,0))
  screen.blit(background_img, (0, 0))

  mouse_x, mouse_y = pygame.mouse.get_pos()

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
        run = False

    #input handler
    input_box_particles.handle_events(event)
    input_duration.handle_events(event)
    input_ecc.handle_events(event)
    input_sm_axis.handle_events(event)

  if state == "npart":

    border(100-5, 200-5, 250, 200, "white","blue",5)
    text_surface = base_font.render(user_txt, True, (255, 255, 255))
    val = input_box_particles.draw(screen)
    t_val = input_duration.draw(screen)
    screen.blit(npart_img_tit, (screen_width/2 - npart_height/2-20, 20))
    border(650-5, 100-5, 500+10, 400+15, "white","green",5)
    draw_text("Between 2 and 200", "PixeloidSans-mLxMm.ttf", "black", 100+10, 200+70)
    draw_text("Between 10 and 30 seconds", "PixeloidSans-mLxMm.ttf", "black", 100+10, 300+70)

    if run_button.draw(screen):
      if val == "" or t_val == "" or not input_box_particles.check(screen) or not input_duration.check(screen):
        input_values_valid = False
      else:  
        input_values_valid = True
        screen.blit(run_simulate(int(val), int(t_val), screen, 650, 100), (screen_width / 2, screen_height / 2))
        state = "npart"
      
    if back_button.draw(screen):
      input_values_valid = True
      state = "main_menu"
      

  if state == "main_menu":
    screen.fill((0,0,0))
    screen.blit(background_img, (0, 0))
    screen.blit(scaled_tit, cel_title_rect)

    npart_hovered = npart_button.rect.collidepoint(mouse_x, mouse_y)
    body_hovered = body2_button.rect.collidepoint(mouse_x, mouse_y)
    if body_hovered:
      screen.blit(scaled_2body_bio, body_bio_rect)

    if npart_hovered:
      screen.blit(scaled_nbody_bio, nbody_bio_rect)

    if npart_button.draw(screen):
      print("now") 
      state = "npart"
    if body2_button.draw(screen):
      print("2 celestial objects")
      state = "body2"

  if state == "body2":

    border(100-5, 200-5, 250, 200, "white","blue",5)
    a = input_sm_axis.draw(screen)
    ecc = input_ecc.draw(screen)
    screen.blit(body2_img_tit, (screen_width/2 - body_height/2-20, 20))
    border(650-5, 100-5, 500+10, 350+10, "white","green",5)
    draw_text("Greater than 0-Less than 0.8", "PixeloidSans-mLxMm.ttf", "black", 100+10, 200+70)
    draw_text("More than 1AU", "PixeloidSans-mLxMm.ttf", "black", 100+10, 300+70)
    
    if run_button.draw(screen):
      if a == "" or ecc == "" or not input_ecc.check(screen) or not input_sm_axis.check(screen):
        input_values_valid = False
      else:
        input_values_valid = True
        for _ in range(5):  
          run_sim_2body(float(ecc), int(a), 20, 0.1, screen, 650, 100)
    
    if back_button.draw(screen):
      input_values_valid = True
      state = "main_menu"
  
  if not input_values_valid:
    # border(650-5, 100-5, 500+10, 350+15, "white","green",5)
    draw_text("Please enter valid input values", "PixeloidSans-mLxMm.ttf", "red", (screen_width-run_w/3)/2-80 , (screen_height - (screen_height/7)))
  
  clock.tick(60)    

  pygame.display.update()

pygame.quit()
