import pygame
import sys

"""
20 x 20 grid
play_height = 2 * play_width
"""

pygame.font.init()

# global variables

col = 20  # 10 columns
row = 20  # 20 rows
s_width = 1000  # window width
s_height = 750  # window height
play_width = 600  # play window width; 300/10 = 30 width per block
play_height = 600  # play window height; 600/20 = 20 height per block
block_size = 30  # size of block

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height - 50

fontpath = './AovelSansRounded-rdDL.ttf'
#fontpath_mario = './ChrustyRock-ORLA.ttf'

# shapes formats (Includes the Rotation)

#4 Block Line
A = [['.....',
      '..0..',
      '..0..',
      '..0..',
      '..0..'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

#3 Block Line
B = [['.....',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.000.',
      '.....',
      '.....',
      '.....']]

#2 Block line
C = [['.....',
      '.....',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '..00.',
      '.....',
      '.....',
      '.....']]

#4 Block T
D = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

#5 3 Block Left Corner
E = [['.....',
      '.0...',
      '.00..',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '.....',
      '.....'],
     ['.....',
      '.....',
      '..00.',
      '...0.',
      '.....'],
     ['.....',
      '.....',
      '..0..',
      '.00..',
      '.....']]

# 3 Block Right Corner
F = [['.....',
      '...0.',
      '..00.',
      '.....',
      '.....'],
     ['.....',
      '.....',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.00..',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '.....',
      '.....']]

X = [['.....',
      '....',
      '..0..',
      '.....',
      '.....']]

# index represents the shape
shapes = [A, B, C, D, E, F, X]
shape_colors = [(255,0,255),(255, 165, 0),(255,255,0),(0,255,255),(0,255,255),(128,0,128),(255,255,255)]

# class to represent each of the pieces
#TESTED
class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]  # choose color from the shape_color list
        self.rotation = 0  # chooses the rotation according to index

#TESTED
def create_grid(locked_pos={}):
    grid = [[(0, 0, 0) for x in range(col)] for y in range(row)]  # grid represented rgb tuples

    # locked_positions dictionary
    # (x,y):(r,g,b)
    for y in range(row):
        for x in range(col):
            if (x, y) in locked_pos:
                color = locked_pos[
                    (x, y)]  # get the value color (r,g,b) from the locked_positions dictionary using key (x,y)
                grid[y][x] = color  # set grid position to color

    return grid

#SET
#TESTED
def convert_shape_format(piece):
    positions = []
    shape_format = piece.shape[piece.rotation % len(piece.shape)]  # get the desired rotated shape from piece

    '''
    e.g.
       ['.....',
        '.....',
        '..00.',
        '.00..',
        '.....']
    '''
    for i, line in enumerate(shape_format):  # i gives index; line gives string
        row = list(line)  # makes a list of char from string
        for j, column in enumerate(row):  # j gives index of char; column gives char
            if column == '0':
                positions.append((piece.x + j, piece.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)  # offset according to the input given with dot and zero

    return positions


# checks if current position of piece in grid is valid ~ Collision detection 
#TEST
def valid_space(piece, grid):
    # makes a 2D list of all the possible (x,y)
    accepted_pos = [[(x, y) for x in range(col) if grid[y][x] == (0, 0, 0)] for y in range(row)]
    # removes sub lists and puts (x,y) in one list; easier to search
    accepted_pos = [x for item in accepted_pos for x in item]

    formatted_shape = convert_shape_format(piece)

    for pos in formatted_shape:
        if pos not in accepted_pos:
            if pos[1] >= 0:
                return False
    return True


# check if piece is out of board
#TEST
def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

# draws text in the middle (TITLE)
#TESTED
def draw_text_middle(text, size, color, surface):
    font = pygame.font.Font(fontpath, size) #bold=False, italic=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width/2 - (label.get_width()/2), top_left_y + play_height/2 - (label.get_height()/2)))


# draws the lines of the grid for the game
#TESTED
def draw_grid(surface):
    r = g = b = 0
    grid_color = (r, g, b)

    for i in range(row):
        # draw grey horizontal lines
        pygame.draw.line(surface, grid_color, (top_left_x, top_left_y + i * block_size),
                         (top_left_x + play_width, top_left_y + i * block_size))
        for j in range(col):
            # draw grey vertical lines
            pygame.draw.line(surface, grid_color, (top_left_x + j * block_size, top_left_y),
                             (top_left_x + j * block_size, top_left_y + play_height))



# draws the upcoming piece
#Link to the adjusted generator
def draw_next_shape(piece, surface):
    font = pygame.font.Font(fontpath, 30)
    label = font.render('Next shape', 1, (255, 255, 255))

    start_x = top_left_x + play_width + 50
    start_y = top_left_y + (play_height / 2 - 100)

    shape_format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(shape_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, piece.color, (start_x + j*block_size, start_y + i*block_size, block_size, block_size), 0)

    surface.blit(label, (start_x, start_y - 30))

    # pygame.display.update()


# draws the content of the window
#ADJUST
def draw_window(surface, grid):
    surface.fill((0, 0, 0))  # fill the surface with black

    pygame.font.init()  # initialise font
    font = pygame.font.Font(fontpath, 65) #bold=True)
    label = font.render('MAZE BUILDER', 1, (255, 255, 255))  # Initialize with the title

    surface.blit(label, ((top_left_x + play_width / 2) - (label.get_width() / 2), 30))  # put surface on the center of the window

    font = pygame.font.Font(fontpath, 25)
    game_key = font.render('Game Key', 1, (255, 255, 255))
    surface.blit(game_key, (15,90))

    font = pygame.font.Font(fontpath, 18)
    start = font.render('Down Arrow To Reveal', 1, (255, 255, 255))
    surface.blit(start, (20,130))

    move = font.render('Arrow Keys to Move', 1, (255, 255, 255))
    surface.blit(move, (20,150))

    rotate = font.render('Shift to Rotate', 1, (255, 255, 255))
    surface.blit(rotate, (20,170))

    lock = font.render('Enter To Place', 1, (255, 255, 255))
    surface.blit(lock, (20,190))

    select = font.render('Number 1-6 to Select', 1, (255, 255, 255))
    surface.blit(select,(20,210))

    block_key = font.render('Block Key', 1, (255, 255, 255))
    surface.blit(block_key,(20,230))

    four_line = font.render('1: 4 Block Line', 1, (255, 255, 255))
    surface.blit(four_line,(25,250))
    
    three_line = font.render('2: 3 Block Line', 1, (255, 255, 255))
    surface.blit(three_line,(25,270))

    two_line = font.render('3: 2 Block Line', 1, (255, 255, 255))
    surface.blit(two_line,(25,290))

    the_t = font.render('4: 4 Block T', 1, (255, 255, 255))
    surface.blit(the_t,(25,310))

    left_corner = font.render('5: Left Corner', 1, (255, 255, 255))
    surface.blit(left_corner,(25,330))

    right_corner = font.render('6: Right Corner ', 1, (255, 255, 255))
    surface.blit(right_corner,(25,350))

    game_play = font.render('Game Play', 1, (255, 255, 255))
    surface.blit(game_play,(20,400))

    font = pygame.font.Font(fontpath, 15)

    start_end = font.render('The Beginning 2 Blocks \n are the start and end \n points of the maze,\nthey are interchangeable \n but once set cannot \n be moved.',1,(255, 255, 255))
    surface.blit(start_end,(25,430))

    time = font.render('You have ten minutes \n to create your maze.',1,(255, 255, 255))
    surface.blit(time,(25,550))

    think_ahead = font.render('Select your next piece \nbefore placing the prior.',1,(255, 255, 255))
    surface.blit(think_ahead,(25,600))

    have_fun= font.render('Have Fun!',1,(255, 255, 255))
    surface.blit(have_fun,(25,650))

    # draw content of the grid
    for i in range(row):
        for j in range(col):
            # pygame.draw.rect()
            # draw a rectangle shape
            # rect(Surface, color, Rect, width=0) -> Rect
            pygame.draw.rect(surface, grid[i][j],
                             (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)

    # draw vertical and horizontal grid lines
    draw_grid(surface)

    # draw rectangular border around play area
    border_color = (255, 255, 255)
    pygame.draw.rect(surface, border_color, (top_left_x, top_left_y, play_width, play_height), 4)

    # pygame.display.update()

def main(window):
    locked_positions = {}
    create_grid(locked_positions)

    change_piece = False #determine if you can move onto the next peice
    run = True
    current_piece = Piece(5, 0, shapes[6]) #White block to indicate the start/end
    next_shape_ready = True
    next_piece = Piece(5, 0, shapes[6]) 
    max_game_duration = 60 # 1 minute for testing, ten for trials
    elapsed_time = 0
    clock = pygame.time.Clock()

    while run:
        # need to constantly make new grid as locked positions always change
        grid = create_grid(locked_positions)
        clock.tick()  # updates clock

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()
            
            #menu_button.hand_event(event)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1  # move x position left
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1

                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1  # move x position right
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1

                elif event.key == pygame.K_DOWN:
                    # move shape down
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

                elif event.key == pygame.K_UP:
                   current_piece.y -= 1
                   if not valid_space(current_piece, grid):
                       current_piece.y +=1
                
                elif event.key == pygame.K_RSHIFT:
                    #rotate shape
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)

                elif not next_shape_ready:
                    if event.type == pygame.KEYDOWN:
                        if pygame.K_1 <= event.key <= pygame.K_6:
                            chosen_shape_index = event.key - pygame.K_1
                            next_piece = Piece(5, 0, shapes[chosen_shape_index])
                            next_shape_ready = True
              
                #If the user presses enter --> Locking the piece and changing to the next_piece
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and current_piece:
                        #current_piece.y += 1
                        change_piece = True
                        #if not valid_space(current_piece, grid) and current_piece.y > 0: #condition might be an error here
                        #    change_piece = True
        
        piece_pos = convert_shape_format(current_piece)

        # draw the piece on the grid by giving color in the piece locations
        for i in range(len(piece_pos)):
            x, y = piece_pos[i]
            if y >= 0:
                grid[y][x] = current_piece.color

        if change_piece and next_shape_ready:  # if the piece is locked by the user AND they've entered the next value they want
            for pos in piece_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color       # add the key and value in the dictionary
            current_piece = next_piece
            change_piece = False
            next_shape_ready = False

        draw_window(window, grid)
        draw_next_shape(next_piece, window)
        pygame.display.update()

        if elapsed_time >= max_game_duration: 
            run = False
        
        clock.tick(30)
    
    pygame.quit()



# Function to display the main menu
def main_menu(window):
    global player_name
    run = True
    name_entered = False
    input_text = ''
    while run:
        window.fill((0, 0, 0))  # Fill the screen with black
        draw_text_middle('Enter Your Name', 40, (255, 255, 255), window)
        
        # Display the input box
        pygame.draw.rect(window, (255, 255, 255), (s_width//2 - 150, s_height//2 + 50, 300, 40))
        font = pygame.font.SysFont(None, 32)
        input_surface = font.render(input_text, True, (0, 0, 0))
        window.blit(input_surface, (s_width//2 - 140, s_height//2 + 60))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if not name_entered:
                    if event.key == pygame.K_RETURN:
                        player_name = input_text
                        name_entered = True
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode
                else:
                    print('internal trial: ', input_text)
                    main(window)


if __name__ == '__main__':
    win = pygame.display.set_mode((s_width, s_height))
    pygame.display.set_caption('Maze Builder')

    main_menu(win)  # start game