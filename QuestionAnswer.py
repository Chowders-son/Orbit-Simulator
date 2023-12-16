import pygame

class InputBox():
    def __init__(self, question, x, y, width, height, font_size=20):
        """This function takes in the parameters and converts them into a question displayed above an input box.
        question, 
        x, y = left top of parent rect
        width, height = width, height of parent rect
        font_size=20 is the default font size used
        This itereation covers number based inputs in handled events and outputs the number whilst displying on the window"""
        pygame.font.init()

        self.font_custom = "PixeloidSans-mLxMm.ttf"
        self.pixel_font = pygame.font.Font(self.font_custom, font_size)
        self.base_font = pygame.font.Font(self.font_custom, font_size)

        self.question = question
        self.user_text = ""

        #parent rect
        self.rect = pygame.Rect(x, y, width, height)

        self.input_rect = pygame.Rect(self.rect.x + 10, self.rect.y + 30, 100, 32)
        self.color_active = pygame.Color("black")
        self.color_passive = pygame.Color("lightgrey")

        self.color = self.color_passive
        self.active = False

        self.error_message = ""
                        
    def draw(self, screen):
        #draw the parent rect
        pygame.draw.rect(screen, (255, 255, 255), self.rect)

        if self.active:
            self.color = self.color_active
        else:
            self.color = self.color_passive

        #draw the input box inside the parent rect
        pygame.draw.rect(screen, self.color, self.input_rect, 2)

        text_surface = self.base_font.render(self.user_text, True, (0, 0, 0))
        screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))

        #draw question
        question_surface = self.pixel_font.render(self.question, True, (0, 0, 0))
        screen.blit(question_surface, (self.input_rect.x,self.input_rect.y - 30))

        #error message
        # if self.error_message:
        #     error_font = pygame.font.Font(None, 18)
        #     error_surface = error_font.render(self.error_message, True, (255, 0, 0))
        #     screen.blit(error_surface, (self.rect.x + 5, self.rect.y + self.rect.h + 5))
        
        return self.user_text


class Input_n_part(InputBox):
    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            if not self.rect.collidepoint(event.pos):
                self.active = False
    
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    try: #valid inputs
                        num = int(self.user_text)
                        if 2 <= num <= 200:
                            return num
                        elif num == "" :
                            self.error_message = "Between 2 and 200"
                        else:
                            self.error_message = "Between 2 and 200"
                    except ValueError:
                        self.error_message = "Please enter a valid number"
                elif event.unicode.isnumeric():
                    self.user_text += event.unicode

    def check(self, screen):
        num = int(self.user_text)
        if 2 <= num <= 200:
            return True        
        else:
            return False

        

class input_run_time(InputBox):
    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            if not self.rect.collidepoint(event.pos):
                self.active = False

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    try: #valid inputs
                        num = int(self.user_text)
                        if 10 <= num:
                            return num
                        elif num == "" :
                            self.error_message = "More than 10 seconds"
                        else:
                            self.error_message =  "More than 10 seconds"
                    except ValueError:
                        self.error_message = "Please enter a valid number"
                elif event.unicode.isnumeric():
                    self.user_text += event.unicode
    def check(self, screen):
        num = int(self.user_text)
        if 10 <= num <= 30:
            return True        
        else:
            return False


##### change handlers
class Input_ecc(InputBox):
    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            if not self.rect.collidepoint(event.pos):
                self.active = False

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER) or self.active != self.active:
                    try: #valid inputs
                        num = float(self.user_text)
                        if 0 <= num <= 0.8:
                            return num
                        elif num == "" :
                            self.error_message = "Between 0 and 0.8"
                        else:
                            self.error_message = "Between 0 and 0.8"
                    except ValueError:
                        self.error_message = "Please enter a valid decimal number"
                elif event.unicode.isnumeric() or event.unicode == ".":
                    self.user_text += event.unicode
    def check(self, screen):
        num = float(self.user_text)
        if 0.0 <= num <= 0.8:
            return True        
        else:
            return False

class Input_sm_axis(InputBox):
    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            if not self.rect.collidepoint(event.pos):
                self.active = False

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    try: #valid inputs
                        num = int(self.user_text)
                        if 1 <= num:
                            return num
                        elif num == "" :
                            self.error_message = "Atleast 1 AU"
                        else:
                            self.error_message = "Atleast 1AU"
                    except ValueError:
                        self.error_message = "Please enter a valid number"
                elif event.unicode.isnumeric():
                    self.user_text += event.unicode
    def check(self, screen):
        num = int(self.user_text)
        if 1 <= num:
            return True        
        else:
            return False
