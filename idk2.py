import pygame
import math
from pygame.locals import *

pygame.init()
def orbit():
    screen = pygame.display.set_mode((1000, 800))
    clock = pygame.time.Clock()

    

    class SpinningCircle(pygame.surface.Surface):

        '''
        Class which make a spinning circle
        Usage:
        >>> circle = SpinningCircle(100, (255, 0, 0))
        >>> circle.update()
        '''

        def __init__(self, radius, color, speed=0.5):

            self.color = color
            self.radius = radius
            self.angle = 1
            self.speed = speed
            self.thickness = int(self.radius / 25.)
            self.portion = 360
            self.update()

        def update(self):

            super(SpinningCircle, self).__init__((self.radius * 2, self.radius * 2), SRCALPHA)

            for i in range(self.portion):

                angle = math.radians(self.angle + i)
                pygame.draw.circle(self, [min(max(x * float(i) / self.radius, 0), 255) for x in self.color], (int(math.sin(angle) * (self.radius - self.thickness) + self.radius), int(math.cos(angle) * (self.radius - self.thickness) + self.radius)), self.thickness)

            self.angle += self.speed

    circle = SpinningCircle(100, (255, 0, 0), 10)

    def blitRotate(surf, image, pos, originPos, angle):

        # offset from pivot to center
        image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
        offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
        
        # rotated offset from pivot to center
        rotated_offset = offset_center_to_pivot.rotate(angle)

        # rotate image center
        rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

        # get a rotated image
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)

        # rotate and blit the image
        surf.blit(rotated_image, rotated_image_rect)
    
        # draw rectangle around the image
        #pygame.draw.rect(surf, (255, 0, 0), (*rotated_image_rect.topleft, *rotated_image.get_size()),2)

    text = pygame.font.SysFont('Times New Roman', 50).render('O', False, (255, 255, 0))
    image = pygame.Surface((text.get_width()+1, text.get_height()+1))
    #pygame.draw.rect(image, (0, 0, 255), (1, 1, *text.get_size()))
    #pygame.draw.circle(image, (255,0,0), [0,0], 20)
    image.blit(text, (1, 1))
    #image.blit(circle, (1, 1))
    w = 134
    h = 57
    angle = 0
    done = False
    while not done:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        pos = (screen.get_width()/2, screen.get_height()/2)
        
        screen.fill(0)
        blitRotate(screen, image, pos, (w/2+200, h/2+200), angle)
        angle += 1
        

        pygame.draw.circle(screen, (0, 0, 255), pos, 30, 0)

        pygame.display.flip()
    pygame.quit()
class Screen():

	# INITIALIZATION OF WINDOW HAVING TITLE,
	# WIDTH, HEIGHT AND COLOUR
	# HERE (0,0,255) IS A COLOUR CODE
	def __init__(self, title, width=440, height=445,
				fill=(0, 0, 255)):
		# HEIGHT OF A WINDOW
		self.height = height
		# TITLE OF A WINDOW
		self.title = title
		# WIDTH OF A WINDOW
		self.width = width
		# COLOUR CODE
		self.fill = fill
		# CURRENT STATE OF A SCREEN
		self.CurrentState = False

	# DISPLAY THE CURRENT SCREEN OF
	# A WINDOW AT THE CURRENT STATE
	def makeCurrentScreen(self):
	
		# SET THE TITLE FOR THE CURRENT STATE OF A SCREEN
		pygame.display.set_caption(self.title)
		# SET THE STATE TO ACTIVE
		self.CurrentState = True
		# ACTIVE SCREEN SIZE
		self.screen = pygame.display.set_mode((self.width,
										self.height))

	# THIS WILL SET THE STATE OF A CURRENT STATE TO OFF
	def endCurrentScreen(self):
		self.CurrentState = False

	# THIS WILL CONFIRM WHETHER THE NAVIGATION OCCURS
	def checkUpdate(self, fill):
		# HERE FILL IS THE COLOR CODE
		self.fill = fill
		return self.CurrentState

	# THIS WILL UPDATE THE SCREEN WITH
	# THE NEW NAVIGATION TAB
	def screenUpdate(self):
		if self.CurrentState:
			self.screen.fill(self.fill)

	# RETURNS THE TITLE OF THE SCREEN
	def returnTitle(self):
		return self.screen

# NAVIGATION BUTTON CLASS


class Button():

	# INITIALIZATION OF BUTTON
	# COMPONENTS LIKE POSITION OF BUTTON,
	# COLOR OF BUTTON, FONT COLOR OF BUTTON, FONT SIZE,
	# TEXT INSIDE THE BUTTON
	def __init__(self, x, y, sx, sy, bcolour,
				fbcolour, font, fcolour, text):
		# ORIGIN_X COORDINATE OF BUTTON
		self.x = x
		# ORIGIN_Y COORDINATE OF BUTTON
		self.y = y
		# LAST_X COORDINATE OF BUTTON
		self.sx = sx
		# LAST_Y COORDINATE OF BUTTON
		self.sy = sy
		# FONT SIZE FOR THE TEXT IN A BUTTON
		self.fontsize = 25
		# BUTTON COLOUR
		self.bcolour = bcolour
		# RECTANGLE COLOR USED TO DRAW THE BUTTON
		self.fbcolour = fbcolour
		# BUTTON FONT COLOR
		self.fcolour = fcolour
		# TEXT IN A BUTTON
		self.text = text
		# CURRENT IS OFF
		self.CurrentState = False
		# FONT OBJECT FROM THE SYSTEM FONTS
		self.buttonf = pygame.font.SysFont(font, self.fontsize)

	# DRAW THE BUTTON FOR THE TWO
	# TABS MENU_SCREEN AND CONTROL TABS MENU
	def showButton(self, display):
		if(self.CurrentState):
			pygame.draw.rect(display, self.fbcolour,
						(self.x, self.y,
						self.sx, self.sy))
		else:
			pygame.draw.rect(display, self.fbcolour, 
						(self.x, self.y,
						self.sx, self.sy))
		# RENDER THE FONT OBJECT FROM THE SYSTEM FONTS
		textsurface = self.buttonf.render(self.text,
										False, self.fcolour)

		# THIS LINE WILL DRAW THE SURF ONTO THE SCREEN
		display.blit(textsurface, 
					((self.x + (self.sx/2) -
					(self.fontsize/2)*(len(self.text)/2) -
					5, (self.y + (self.sy/2) -
						(self.fontsize/2)-4))))

	# THIS FUNCTION CAPTURE WHETHER 
	# ANY MOUSE EVENT OCCUR ON THE BUTTON
	def focusCheck(self, mousepos, mouseclick):
		if(mousepos[0] >= self.x and mousepos[0] <= self.x +
				self.sx and mousepos[1] >= self.y and mousepos[1]
				<= self.y + self.sy):
			self.CurrentState = True
			# IF MOUSE BUTTON CLICK THEN
			# NAVIGATE TO THE NEXT OR PREVIOUS TABS
			return mouseclick[0]

		else:
			# ELSE LET THE CURRENT STATE TO BE OFF
			self.CurrentState = False
			return False


# INITIALIZATION OF THE PYGAME
pygame.init()
# INITIALIZATION OF SYSTEM FONTS
pygame.font.init()

# CREATING THE OBJECT OF THE
# CLASS Screen FOR MENU SCREEN
menuScreen = Screen("Menu Screen")

# CREATING THE OBJECT OF THE
# CLASS Screen FOR CONTROL SCREEN
control_bar = Screen("Control Screen")

# CALLING OF THE FUNCTION TO
# MAKE THE SCREEN FOR THE WINDOW
win = menuScreen.makeCurrentScreen()

# MENU BUTTON
MENU_BUTTON = Button(150, 150, 150, 50, (255, 250, 250),
					(255, 0, 0), "TimesNewRoman",
					(255, 255, 255), "Main Menu")

done = False

toggle = False

#Define Input Area


#Define Mass & Velocity & Radius & Angular Momentum <-(Possibly?)
# def defvalue():
	
# MAIN LOOPING
while not done:
	# CALLING OF screenUpdate 
	# function FOR MENU SCREEN
	menuScreen.screenUpdate()
	
	# CALLING THE FUNCTION OF CONTROL BAR
	control_bar.screenUpdate()
	# STORING THE MOUSE EVENT TO
	# CHECK THE POSITION OF THE MOUSE
	mouse_pos = pygame.mouse.get_pos()
	# CHECKING THE MOUSE CLICK EVENT
	mouse_click = pygame.mouse.get_pressed()
	# KEY PRESSED OR NOT
	keys = pygame.key.get_pressed()

# MENU BAR CODE TO ACCESS
	# CHECKING MENU SCREEN FOR ITS UPDATE
	if menuScreen.checkUpdate((25, 0, 255)):
		control_barbutton = MENU_BUTTON.focusCheck(mouse_pos,
												mouse_click)
		MENU_BUTTON.showButton(menuScreen.returnTitle())

		if control_barbutton:
			win = control_bar.makeCurrentScreen()
			menuScreen.endCurrentScreen()

	# CONTROL BAR CODE TO ACCESS
	# CHECKING CONTROL SCREEN FOR ITS UPDATE
	elif control_bar.checkUpdate((255, 0, 255)):
		orbit()
			
	# CHECKING IF THE EXIT BUTTON HAS BEEN CLICKED OR NOT
	for event in pygame.event.get():
	
		# IF CLICKED THEN CLOSE THE WINDOW
		if(event.type == pygame.QUIT):
			done = True

	pygame.display.update()
	
# CLOSE THE PROGRAM
pygame.quit()
