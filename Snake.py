import pygame as pyg
import time, random, sys
pyg.init()
run = True
score = 0
gameover = False

# Game window
screenSize = 600
win = pyg.display.set_mode((screenSize, screenSize))

# Colors
black = (35, 35, 35)
white = (255, 255, 255)
red = (255, 0, 0)

# Snake attributes
size = 25
head_x = head_y = 0
vel = size
move_x = move_y = 0
up = down = left = right = True
body = []

# Snake food
food_x = food_y = screenSize/2

# Spawns new food
def spawnFood():
    global food_x, food_y
    # Assigning x  and y values not equal to player or body values and is within the window
    valid = False
    while valid == False:
        random.seed()
        food_x = random.randrange(0, screenSize - size, size)
        food_y = random.randrange(0, screenSize - size, size)
        if [food_x, food_y] != [head_x, head_y]:
            for i in body:
                if [food_x, food_y] != i:
                    valid = True
                else:
                    valid = False
                    break

# Adds food to body of snake    
def add2snake():
    body.append([food_x, food_y])

# Allows the body to follow the head
def shift():
    global body
    for i in range(score - 1):
        body[i][0] = body[i + 1][0]
        body[i][1] = body[i + 1][1]
    if score > 0:
        body[score - 1] = [head_x, head_y]

# Checks if head has collided with x,y
def collision(x, y):
    if head_x >= x and head_x < x + size or head_x + size > x and head_x <= x:
        if head_y >= y and head_y < y + size or head_y + size > y and head_y <= y:
            return True
        else:
            return False

# Draws everything in display
def draw():
    pyg.display.set_caption("Snake | Score: " + str(score))
    win.fill(black)
    
    # Draws body
    for i in body:
        pyg.draw.rect(win, white, (i[0], i[1], size, size))
    
    # Draws head
    pyg.draw.rect(win, white, (head_x, head_y, size, size))
    
    # Draws food
    pyg.draw.rect(win, red, (food_x, food_y, size, size))
    
    # Draws grid
    x = 0
    y = 0
    for i in range(screenSize//size):
        x += size
        y += size
        pyg.draw.line(win, black, (0, y), (screenSize, y))
        pyg.draw.line(win, black, (x, 0), (x, screenSize))

# Checks if player has died
def check_death():
    global run, gameover
    
    # Ends game if snake hits border
    if head_x < 0 or head_x > screenSize - size or head_y < 0 or head_y > screenSize - size:
        gameover = True
    
    # Ends game if snake hits body
    for i in body:
        if collision(i[0], i[1]):
            gameover = True
            break

# Generates text
def create_text(text, name, font_size, text_color, location):
    font = pyg.font.SysFont(name, font_size, bold = True)
    ren = font.render(text, True, text_color)
    win.blit(ren, (screenSize/2 - ren.get_rect().width/2, screenSize/2 - location))

# Pause menu
def pause():
    global run
    
    transparent = pyg.Surface((screenSize, screenSize))
    transparent.fill(black)
    transparent.set_alpha(175)
    
    paused = True
    while paused:
        for e in pyg.event.get():
            if e.type == pyg.QUIT:
                run = False
                pyg.quit()
                sys.exit()
            if e.type == pyg.KEYDOWN:
                if e.key == pyg.K_SPACE:
                    paused = False
                elif e.key == pyg.K_ESCAPE:
                    run = False
                    paused = False
        draw()
        win.blit(transparent, (0, 0))
        create_text("PAUSED", "Courier", 48, white, 50)
        create_text("Press SPACE to continue or ESCAPE to quit", "Courier", 24, white, 0)
        pyg.display.update()

# Game loop
def gameloop():
    global head_x, head_y, move_x, move_y
    global up, down, left, right
    global body, run, score, gameover
    
    # Resetting values
    head_x = head_y = 0
    move_x = move_y = 0
    up = down = left = right = True
    body = []
    score = 0
    gameover = False
    
    while run:
        pyg.time.delay(75)
        
        # GAME OVER SCREEN
        while gameover:
            win.fill(black)
            for e in pyg.event.get():
                if e.type == pyg.QUIT:
                    run = False
                    gameover = False
                    pyg.quit()
                    sys.exit()
                if e.type == pyg.KEYDOWN:
                    if e.key == pyg.K_ESCAPE:
                        run = False
                        gameover = False
                        pyg.quit()
                        sys.exit()
                    elif e.key == pyg.K_SPACE:
                        gameover = False
                        gameloop()
            create_text("GAME OVER", "Courier", 48, white, 150)
            create_text("Score: " + str(score), "Courier", 36, white, 60)
            create_text("Press SPACE to play again or ESCAPE to quit", "Courier", 18, white, -25)
            pyg.display.update()  
        
        # ACTUAL GAME
        shift()
        for e in pyg.event.get():
            # Clicking X to quit
            if e.type == pyg.QUIT:
                run = False
            
            # Player movement
            if e.type == pyg.KEYDOWN:
                if e.key == pyg.K_UP:
                    if score > 0:
                        if up:
                            move_x = 0
                            move_y = vel*(-1)
                            up = left = right = True
                            down = False
                    else:
                        move_x = 0
                        move_y = vel*(-1)
                elif e.key == pyg.K_DOWN:
                    if score > 0:
                        if down:
                            move_x = 0
                            move_y = vel
                            down = left = right = True
                            up = False
                    else:
                        move_x = 0
                        move_y = vel
                elif e.key == pyg.K_LEFT:
                    if score > 0:
                        if left:
                            move_x = vel*(-1)
                            move_y = 0
                            left = up = down = True
                            right = False
                    else:
                        move_x = vel*(-1)
                        move_y = 0
                elif e.key == pyg.K_RIGHT:
                    if score > 0:
                        if right:
                            move_x = vel
                            move_y = 0
                            right = up = down = True
                            left = False
                    else:
                        move_x = vel
                        move_y = 0
                elif e.key == pyg.K_SPACE:
                    pause()

        head_x += move_x
        head_y += move_y
        
        # Checking if player has died
        check_death()
        
        # Checking if food is eaten
        if collision(food_x, food_y):
            add2snake()
            spawnFood()
            score += 1
        
        # Updating display
        draw()
        pyg.display.update()

gameloop()