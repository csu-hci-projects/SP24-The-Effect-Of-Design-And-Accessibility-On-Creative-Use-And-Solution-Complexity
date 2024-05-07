import pygame
import pygame_gui
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("GUI Test")

# Create a GUI manager
manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create a panel as an outer frame
frame_panel = pygame_gui.elements.UIPanel(
    relative_rect=pygame.Rect((50, 50), (700, 500)),
    starting_layer_height=0,
    manager=manager
)

# Create a panel for the menu
menu_panel = pygame_gui.elements.UIPanel(
    relative_rect=pygame.Rect((20, 20), (660, 460)),
    starting_layer_height=1,
    manager=manager,
    container=frame_panel  # Assign the frame panel as the container for the menu panel
)

# Add elements to the menu panel
# For example, a label
label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((10, 10), (200, 30)),
    text='Menu',
    manager=manager,
    container=menu_panel
)

# Create a button
button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((10, 50), (200, 50)),
    text='Click Me',
    manager=manager,
    container=menu_panel
)

# Main loop
running = True
while running:
    time_delta = pygame.time.Clock().tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == button:
                    print('Button clicked!')

        manager.process_events(event)

    manager.update(time_delta)
    screen.fill((255, 255, 255))
    manager.draw_ui(screen)
    pygame.display.update()

pygame.quit()
sys.exit()
