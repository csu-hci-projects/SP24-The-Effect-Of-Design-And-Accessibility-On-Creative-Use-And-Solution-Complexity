Welcome to Maze Builder
   Program by Aspen Coates
   Class: CS 464
   Created: 03/18/2024
   Last Edited: 05/06/2024


Overview
   Program Description:
       In this project are two different executables:
           internal_menu.py
           external_menu.py
       Within is the same framework, each is a 20 by 20 table where the user can use
       different input keys to choice and manipulate different blocks in order to build
       the very vague prompt of "maze". Internal Menu lists the functions and commands on
       the left side of the screen, while external method uses the left shift to toggle an
       external menu open and closed. Details on the specific blocks and maneuvers can be
       seem as labeled in each program


Demo Video
   Video 1: (Broad Overview): https://youtu.be/yiZWgaKDnBI
   Video 2: (Program Step Through): https://youtu.be/mcOg05Aa1hE


Installation
   To run Maze builder you will need:
       Python (Version 3.9.6)


       Pygame Library
           pip install pygame


Github Access: https://github.com/csu-hci-projects/SP24-The-Effect-Of-Design-And-Accessibility-On-Creative-Use-And-Solution-Complexity.git


How to run:
   1. Clone repository to your local machine
       git clone https://github.com/csu-hci-projects/SP24-The-Effect-Of-Design-And-Accessibility-On-Creative-Use-And-Solution-Complexity.git
   2. Navigate to project directory
       cd SP24-The-Effect-Of-Design-And-Accessibility-On-Creative-Use-And-Solution-Complexity.git
   3. Navigate into the virtual environment
       cd venv
   4. Compile External or Internal prompt
       python3 Internal_menu.py
       or
       python3 External_menu.py
   5. Follow the prompts in the pygame pop-up


Controls:
   note: The block populates at the top of screen out of view so you have to "pull" it down
   Arrow Keys: Move block around the grid
   Right Shift: Rotate
   Return: Set Block
   1 key: 4 block line
   2 key: 3 block line
   3 key: 2 block line
   4 key: 4 block T
   5 key: Left corner
   6 key: Right corner


   (external) Left Shift: Opens and closes the menu
