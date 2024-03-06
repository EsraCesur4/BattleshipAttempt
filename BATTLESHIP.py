# -*- coding: utf-8 -*-
"""
Created on Thu Dec 30 18:21:24 2021

@author: delll
"""

from graphics import Canvas
import random
from tkinter import messagebox
import time


#----------VARIABLES----------
CANVAS_SIZE = 400
BLOCK_SIZE = 40
WIN_SCORE = 100
TURNS = 50
#-----------------------------


# creates a screen before the game begins. 
def starting_screen(canvas):
    
    # FIRST TEXT
    start_rect = canvas.create_rectangle(80, 230, 320, 270) # JUST A BORDER
    label4 = canvas.create_text(200, 250, "STARTING!") # STARTING TEXT ON SCREEN
    canvas.set_font(label4, "Courier", 20) # FONT SIZE
    
    # SECOND TEXT
    label5 = canvas.create_text(200, 170, 'BATTLESHIP') # GAME NAME ON SCREEN
    canvas.set_font(label5, "Courier", 45) # FONT SIZE
    canvas.set_color(label5, 'DodgerBlue4') # TEXT COLOR (GAME NAME)
    
    # TIME STARTING SCREEN IS SEEN
    canvas.update()
    time.sleep(2) 
    
    # DELETE STARTING SCREEN
    canvas.delete(label4) 
    canvas.delete(start_rect)
    canvas.delete(label5)

    
# explains the gameplay    
def how_to_play_text(canvas):
    
    text1 = canvas.create_text(190, 510, 'How to play: Battleship is a strategy type guessing game. There')
    text2 = canvas.create_text(190, 525, 'are 10 ships marked on the map. You have to sunk them in order to')
    text3 = canvas.create_text(190, 540, "win. Click on the square to reveal what's behind. For each ship")
    text4 = canvas.create_text(190, 555, "you found hiding, you gain 10 points. You have 50 turns to win!")
    
    return text1, text2, text3, text4
        
    
# draws the square board
def draw_board(canvas,row,column):
    
    # CREATES THE MAP
    for j in range(row):
        y = j * BLOCK_SIZE
        
        for i in range(column):
            x = i * BLOCK_SIZE
            
            square = canvas.create_rectangle(x, y, x + BLOCK_SIZE, y + BLOCK_SIZE)
            canvas.set_color(square, 'DodgerBlue3')
            canvas.set_outline_color(square, 'DodgerBlue4')

            
# creates the ships            
def create_ships(canvas):
    
    ships_x = []

    # COORDS
    ship_x = [0,1,2,3,4,5,6,7,8,9]
    ship_y = [0,1,2,3,4,5,6,7,8,9]
    
    # LOOP THAT DRAWS THE SHIPS
    for i in range(len(ship_x)):
        
        # CREATE RANDOM COORDS
        x = random.choice(ship_x)
        y = random.choice(ship_y)
        x0 = x*BLOCK_SIZE
        y0 = y*BLOCK_SIZE
        
        ship = canvas.create_rectangle(x0, y0, x0+BLOCK_SIZE, y0+BLOCK_SIZE)
        
        # DELETE THE COORDS FROM THE LIST SO ANOTHER SHIP DOESN'T GET DRAWN IN THE SAME COORDS
        get_ship_x = canvas.get_left_x(ship)
        ships_x.append(get_ship_x)
        canvas.set_color(ship, 'gray25')
        if x in ship_x:
            ship_x.remove(x)    
 
            
# draw score label            
def add_score_label(canvas, score):
    
    label = canvas.create_text(0, 0, "")
    canvas.set_font(label, "Courier", 20)
    
    # UPDATE THE LABEL
    update_score_label(canvas, label, score)
    
    return label


# update score label
def update_score_label(canvas, score_label, score):
    canvas.set_text(score_label, "Score: " + str(score))
    canvas.moveto(score_label, 135, 460)
    
    
# REMOVE IF CLICKED          
def handle_clicks(canvas,score,score_label,turns,text1,text2,text3,text4):
    
    # LOOP FOR THE END
    while score < WIN_SCORE and turns < TURNS:
        clicks = canvas.get_new_mouse_clicks()
        for click in clicks:
            counter = 0 
            turns += 1
            clicked_object = canvas.find_element_at(click.x, click.y)
            
            # DELETE CLICKED OBJECT
            if clicked_object and clicked_object != score_label and clicked_object != text1 and clicked_object != text2 and clicked_object != text3 and clicked_object != text4:
                canvas.delete(clicked_object)
                
                # IF THERE IS A SHIP UNDERNEATH UPDATE THE SCORE LABEL
                mine = canvas.find_element_at(click.x, click.y)
                if mine:
                    counter += 1
                    if counter == 1:
                        score += 10
                        update_score_label(canvas, score_label, score)              
        canvas.update()
        
    return score


#------------------------------------------------------------------------------------------------------------ 
def main():
    # MAIN GAME
    canvas = Canvas(400,570) # CREATE CANVAS
    canvas.set_canvas_title("BATTLESHIP") # NAME CANVAS
    
    #canvas.create_image_with_size(0, 0, canvas.get_canvas_width(), canvas.get_canvas_height(), 'ocean.jpg')
    
    canvas.set_canvas_background_color('LightSkyBlue1') # SET COLOR
    starting_screen(canvas) # START SCREEN
    text1, text2, text3, text4 = how_to_play_text(canvas) # PLAYING GUIDE
    
    turns = 0
    score = 0
    score_label = add_score_label(canvas, score) # SCORE
    
    row = CANVAS_SIZE//BLOCK_SIZE # NUMBER OF ROWS
    column = CANVAS_SIZE//BLOCK_SIZE # NUMBER OF COLUMNS
    
    create_ships(canvas) # DRAW SHIPS
    draw_board(canvas,row,column) # DRAW BOARD
    game_score = handle_clicks(canvas,score,score_label,turns,text1,text2,text3,text4) # HANDLE CLICKS
    
    if game_score >= WIN_SCORE: # CHECK IF THE GAME IS WON OR LOST
        messagebox.showinfo('BATTLESHIP', 'ALL SHIPS SUNK\r  You Won!' ) # CREATE MESSAGEBOX
        time.sleep(1) 
        canvas.quit() # DESTROY THE PREVIOUS BOARD
        main() # START THE GAME AGAIN     
    else:
        messagebox.showinfo('BATTLESHIP', "RUN OUT OF TURNS!\r      You Lost!" ) # CREATE MESSAGE BOX
        time.sleep(1)
        canvas.quit() # DESTROY THE PREVIOUS BOARD
        main() # START THE GAME AGAIN
        
    canvas.mainloop()


    
if __name__ == "__main__":
    main()
    
