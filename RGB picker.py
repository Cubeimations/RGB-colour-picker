import pygame
import random
import csv

pygame.init()
size = width,height = 1200,700
screen = pygame.display.set_mode((size))
clock = pygame.time.Clock()
x = width / 2
y = height / 2
delta_time = 60
running = True

red = 0
blue = 0
green = 0

change = 0
el_primo_img = pygame.image.load('Random_Asset.png').convert() # still calling it el primo lol
img_res = (350,100)
el_primo_img = pygame.transform.scale(el_primo_img, img_res)

el_primo_img.set_colorkey((255,255,255))

hex_code = '#000000'
offset = 120
programIcon = pygame.image.load('AdditiveColorMixing.png')
pygame.display.set_icon(programIcon)
pygame.display.set_caption('Hex Colour Picker')

def load_data(filename, entry, combine):
    mylist = []
    comb_list = []
    with open(filename, 'r') as strings:
        csv_reader = csv.reader(strings, delimiter=',')
        next(csv_reader)

        for row in csv_reader:
            if combine == 0:
                mylist.append(row[entry])
            else:
                for i in range(0,combine):
                    comb_list.append(row[entry+i])
                mylist.append(comb_list)
                comb_list = []
        return mylist
    
colour_val_list = load_data ('Colour Data.csv',0,6)
current_col = 'N/A'
clicky = False
def find_nearest_val(red,green,blue):
    least_difference = 1000
    val_list = []
    returner = ''
    for val in colour_val_list:
        val_list = []
        for j in val:
            val_list.append(j)
        current = val_list[1]
        val_red = int(val_list[3])
        val_green = int(val_list[4])
        val_blue = int(val_list[5])
        difference = abs(val_red - red) + abs(val_green - green) + abs(val_blue - blue)
        if difference < least_difference:
            least_difference = difference
            returner = current
    return returner                   

class slider:
    def __init__(self, pos: tuple, size:tuple, initial_val: float, min_x, max_x, slider_width):
        self.pos = pos
        self.size = size
        self.slider_width = slider_width

        self.slider_left = int(self.pos[0] - (size[0]//2))
        self.slider_right = int(self.pos[0] + (size[0]//2))
        self.slider_top = self.pos[1] - (size[1]//2)
        self.min = min_x
        self.max = max_x
        self.initial_val = (self.slider_right-self.slider_left)*initial_val # percentage

        self.container_rect = pygame.Rect(self.slider_left, self.slider_top, self.size[0], self.size[1])
        self.button_rect = pygame.Rect(self.slider_left + self.initial_val - 20, self.slider_top, self.slider_width, self.size[1])
    def move_slider(self, mouse_pos):
        self.button_rect.centerx = mouse_pos[0]
    def random(self):
        self.button_rect.centerx = random.randint(self.slider_left,self.slider_right)
    def render(self, screen, front_col, back_col):
        pygame.draw.rect(screen, back_col, self.container_rect, width = 0, border_radius = 5)
        pygame.draw.rect(screen, front_col, self.button_rect)
    def get_value(self):
        val_range = self.slider_right - self.slider_left - 2
        button_val = self.button_rect.centerx - self.slider_left
        return_val = (button_val/val_range)*(self.max-self.min)+self.min
            
        return return_val
      
def font(text, font, size, pos, num, colour):   
    my_font = pygame.font.SysFont(font, size)
    if num == 1:
        text_surface = my_font.render('red: '+ str(text) , True, colour)
    if num == 2:
        text_surface = my_font.render('green: '+ str(text) , True, colour)
    if num == 3:
        text_surface = my_font.render('blue: '+ str(text) , True, colour)
    if num == 4:
        text_surface = my_font.render('hex code: '+ str(text) , True, colour)
    if num == 5:
        text_surface = my_font.render('inverted hex code: '+ str(text) , True, colour)
    if num == 6:
        text_surface = my_font.render('50% desaturated hex code: '+ str(text) , True, colour)
    if num == 7:
        text_surface = my_font.render('Closest Colour: '+ str(text) , True, colour)
    text_rect = text_surface.get_rect()
    text_rect.midtop = pos
    screen.blit(text_surface, text_rect)

def hex_val(red,green,blue):
    hex_red = hex(red)[2:]
    hex_green = hex(green)[2:]
    hex_blue = hex(blue)[2:]
    if len(hex_red) == 1:
        hex_red = '0' + hex_red
    if len(hex_green) == 1:
        hex_green = '0' + hex_green
    if len(hex_blue) == 1:
        hex_blue = '0' + hex_blue
    hex_code = '#'+ hex_red+ hex_green+ hex_blue
    return hex_code
    
red_slider = slider((x,height/6-50), (width-40,50), (random.randint(0,255)/256), 0, 255, 30)
green_slider = slider((x,height/3-50), (width-40,50), (random.randint(0,255)/256), 0, 255, 30)
blue_slider = slider((x,height/2-50), (width-40,50), (random.randint(0,255)/256), 0, 255, 30)

random_button = pygame.Rect(900,height/1.6, 200, 150)
while running:
    screen.fill((255-red/10,255-green/10,255-blue/10))

    red = round(red_slider.get_value())
    blue = round(blue_slider.get_value())
    green = round(green_slider.get_value())
    
    mouse_pos = pygame.mouse.get_pos()
    mouse = pygame.mouse.get_pressed()
    current_col = find_nearest_val(red,green,blue)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # sliders
    if red_slider.container_rect.collidepoint(mouse_pos) and mouse[0]:
        red_slider.move_slider(mouse_pos)  
    red_slider.render(screen,'red','black')

    if green_slider.container_rect.collidepoint(mouse_pos) and mouse[0]:
        green_slider.move_slider(mouse_pos)  
    green_slider.render(screen,'green','black')
    
    if blue_slider.container_rect.collidepoint(mouse_pos) and mouse[0]:
        blue_slider.move_slider(mouse_pos)  
    blue_slider.render(screen,'blue','black')
    
    if not mouse[0]:
        clicky = True
    if random_button.collidepoint(mouse_pos):
        change = 30
        if mouse[0]:
            change = 0
            if clicky:
                red_slider.random()
                green_slider.random()
                blue_slider.random()
                clicky = False
    else:
        change = 0
        
    # colour vals
    hex_code = hex_val(red,green,blue)
    anti_red = 255 - red
    anti_green = 255 - blue
    anti_blue = 255 - green
    anti_hex_code = hex_val(anti_red,anti_green,anti_blue)
    red_50 = red // 2
    green_50 = green // 2
    blue_50 = blue // 2
    hex_code_50 = hex_val(red_50,green_50,blue_50)
    red_200 = red + (255 - red // 2)
    green_200 = green + (255 - green // 2)
    blue_200 = blue + ((255 - blue) // 2)
    hex_code_200 = hex_val(red_200,green_200,blue_200)
    #rects
    pygame.draw.rect(screen, (red,green,blue), (20,height/1.6-15, 400, 300), 0, 5)
    pygame.draw.rect(screen, (anti_red,anti_green,anti_blue), (470,height/1.6-70, 200, 150), 0, 5)
    pygame.draw.rect(screen, (red_50,green_50,blue_50), (470,height-120, 200, 150), 0, 5)
    pygame.draw.rect(screen, (20,200+change,100), (random_button),0,5)
    screen.blit(el_primo_img, (850,height/2.1))
    #pygame.draw.rect(screen, (red_200,green_200,blue_200), (690,height/1.6-70, 200, 150), 0, 5)
    # font
    font(red, 'Rockwell', 30, (120,height/6-offset), 1, (red,0,0))
    font(green, 'Rockwell', 30, (120,height/3-offset), 2, (0,green,0))
    font(blue, 'Rockwell', 30, (120,height/2-offset), 3, (0,0,blue))
    font(hex_code, 'Rockwell', 35, (180,height/2), 4, (0,0,0))
    font(anti_hex_code, 'Rockwell', 24, (560,height/1.6-110), 5, (0,0,0))
    font(hex_code_50, 'Rockwell', 16, (560,height-160), 6, (0,0,0))
    font(current_col, 'Rockwell', 30, (x+200,height/6-offset), 7, (0,0,0))
    pygame.display.flip()
    clock.tick(delta_time)
    
