import tkinter as tk
import random
import time

class Bird:
    _PLAYER_IMAGE_FILE = "sprites/bird.png"
    _GRAVITY_Y_SPEED =4           # used store the maximum downward falling speed of the player
    _JUMP_Y_SPEED = -5              # used to store the maximum upward jump
    _UPPER_WINDOW_BOUNDARY = 20     # used to store the y-coordinate of the upper window boundary
    _DOWNWARD_ACCELERATION = 0.25   # used to store the deceleration speed, which visually simulates the weight of the bird

    def __init__(self, root, canvas, window_width, window_height):
        #initializes 'brid' object with the following parameters
        self._root = root
        self._canvas = canvas
        self._window_width = window_width
        self._window_height = window_height
        self.window_center_x = self._window_width/2            # it stores the x-coordinate of the center of the window derived from its width
        self.window_center_y = self._window_height/2           # it stores the y-coordinate of the center of the window derived from its height
        self._player_sprite = tk.PhotoImage(file=self._PLAYER_IMAGE_FILE)          # it stores the player sprite
        self._player = self._canvas.create_image(self.window_center_x, self.window_center_y,
                                                 image=self._player_sprite, anchor="c", tag="player")
        self._y_speed = self._GRAVITY_Y_SPEED                  # it stores the player's current vertical (y) speed
        self._x_speed = 0                                      # it stores the player's current horizontal (x) speed
    
    def player_fall(self):
        if self.get_player_x_y_coords()[1] < self._UPPER_WINDOW_BOUNDARY:    # If the player hits the upper window boundary, make it bounce back down
            self._y_speed = self._GRAVITY_Y_SPEED

        self._canvas.move(self._player, self._x_speed, self._y_speed)        # Make the payer move downward
        self._y_speed += self._DOWNWARD_ACCELERATION

    def player_jump(self):
        self._y_speed = self._JUMP_Y_SPEED    # it makes the player to jump forward

    def get_player_x_y_coords(self):
        return self._canvas.coords(self._player)

class Pipe: 

   # this  manages the  pipe  and its motion
    _PIPE_WIDTH = 85
    _PIPE_SEPARATION_Y = 140       
    _MAX_X_SPEED = -8            # maximum horizontal speed constant for each pipe
    _PIPE_SPAWN_INTERVAL = 1.5     # frequency of generation of each pipe
    _PIPE_Y_OFFSET = 90            # maximum offset distance from the top and bottom window boundaries
    _PIPE_COLOR = "grey"           #color of the pipe

    def __init__(self, root, canvas, window_width, window_height):
        
           #initializes 'pipe' object with the following parameters
        
        self._root = root
        self._canvas = canvas
        self._window_width = window_width
        self._window_height = window_height

        self._pipe_bottom = None
        self._pipe_top = None
        self._origin_x = self._window_width        # stores the x-coordinate of the spawn origin of each pipe
        self.top_pipe_origin_y = 0                 # y-coordinate of the spawn origin of each upper pipe    
        self._pipe_drawn = False                   # used to indicate whenever a new pipe is drawn to allow for time-regulated generation
        self._x_speed = self._MAX_X_SPEED          # its stores the horizontal speed of each pipe
        self._y_speed = 0                          # it store a the vertical speed of each pipe

        self._pipe_generator_time_dp = 1                     # variable to store a constant the number of dp that the game run-time is rounded to
        self._min_length_from_top = self._PIPE_Y_OFFSET      # variable to store a derived constant for the smallest length of a pipe from the top
        self._max_length_from_top = self._window_height - self._PIPE_Y_OFFSET - self._PIPE_SEPARATION_Y    # variable to store a derived constant for the biggest length of a pipe from the top

    def pipe_generator(self):
        time_elapsed = round(time.time(), self._pipe_generator_time_dp)    # used to store the time elapse since the start of the game instance
        if time_elapsed % self._PIPE_SPAWN_INTERVAL == 0:
            if not self._pipe_drawn:                     # If a new pipe hasn't been drawn after the interval, generate a new pipe
                self._draw_pipe_on_canvas()
                self._pipe_drawn = True
        else:                                               # If the time interval since the last pipe generated is not met, set the _pipe_drawn attribute to False
            self._pipe_drawn = False

    def _draw_pipe_on_canvas(self):
        top_pipe_len_from_top = random.randrange(self._min_length_from_top, self._max_length_from_top)   # used to store a randomly-generated height-from-top of the top pipe
        bottom_pipe_len_from_top = top_pipe_len_from_top + self._PIPE_SEPARATION_Y                       # it is used to store the height-from-top for the bottom pipe derived from the previous var
        self._pipe_bottom = self._canvas.create_rectangle(self._origin_x, bottom_pipe_len_from_top,
                                                          self._origin_x + self._PIPE_WIDTH, self._window_height,
                                                          fill=self._PIPE_COLOR, tags=("pipe", "bottom_pipe"))
        # it Initialize top pipe object as a rectangle from the canvas class and store it in a private attribute
        self._pipe_top = self._canvas.create_rectangle(self._origin_x, self.top_pipe_origin_y,
                                                       self._origin_x + self._PIPE_WIDTH, top_pipe_len_from_top,
                                                       fill=self._PIPE_COLOR, tags=("pipe", "top_pipe"))

    def move_pipe(self):
        self._canvas.move("pipe", self._x_speed, self._y_speed)

class MainApplication:
    # controls the main game
    _BACKGROUND_IMAGE_FILE = "sprites/background.png"        # variable to store the file path for the game background image

    def __init__(self):
        self.root = tk.Tk()   
        self.root.title("FlappyBird")     # Title of the game
        self._width = 485        # it stores the width of the game window
        self._height = 640       # it stores the height of the game window
        self.window_center_x = self._width / 2       # it stores the x-coordinate of the center of the window derived from its width
        self.window_center_y = self._height / 2       # it stores the y-coordinate of the center of the window derived from its height
        self._background_color = "#03adfc"            # stores background color

        self._canvas = tk.Canvas(self.root, width=self._width, height=self._height, background=self._background_color)
        self._canvas.grid(row=0, column=0)

        self._background_image = tk.PhotoImage(file=self._BACKGROUND_IMAGE_FILE)    # it stores the game background PhotoImage
        self._canvas.create_image(self.window_center_x, self.window_center_y,       # Initialize the background image widget from the canvas class
                                  image=self._background_image, anchor="c", tag="background")

        self._player = None
        self._pipe = Pipe(self.root, self._canvas, self._width, self._height)
        self._scored_pipes = []         # used to store the id of the last pipe pair that the user has passed through

        self._canvas.bind("<KeyPress>", self._user_input_handler)
        self._canvas.bind("<Button>", self._user_input_handler)
        self._canvas.focus_set()             # Setting keyboard focus 

        self._best_score = 0                 #it stores user best score     
        self._player_score = 0               # it store the user's current score 
        self._score_counter_text = None      # it store the score counter widget

        # Call to the initialisation of the game
        self._start()
        self.root.mainloop()

    def _intro_menu(self):

        button_start_game = tk.Button(self._canvas, text="Start", anchor='c', font=("ROBOTO", 12, "bold"),       #  main menu's "start" button
                                      command=self._initialise_game_layout)
        button_start_game.configure(width=10, background="orange")
        self._canvas.create_window(self.window_center_x, self.window_center_y - 34, window=button_start_game,    # this host the "start" button
                                   tag="start_button") 

    def _user_input_handler(self, event):
        key_press = event.keysym      # used to stores the name of the key pressed by the user
        button_press = event.num

        if key_press in ("space", "Up") or button_press == 1:
            if self._NEW_GAME:
                self._NEW_GAME = False
                self._canvas.focus_set()
                self._player.player_jump()
                self._main()
            elif self._GAME_OVER and button_press != 1 and key_press == "space":   #if game ends restart the game 
                self._restart_game()
            else:
                if self._player:
                    self._player.player_jump()      # If the player exists, make it jump up

    def _initialise_game_layout(self):   
        # This function initialises the main game layout before each game session
        self._canvas.delete("all")      # This Remove all widgets present on the canvas
        self._canvas.create_image(self.window_center_x, self.window_center_y,
                                  image=self._background_image, anchor="c", tag="background")
        self._player = Bird(self.root, self._canvas, self._width, self._height)        # Initialise an instance of the Bird class and store in a private variable _player
        self._NEW_GAME = True          # Indicate that a new game has been initiated

    def _overlap_detection(self):
        pipe_objects = self._canvas.find_withtag("pipe")
        player_coords = self._player.get_player_x_y_coords()
        player_x = player_coords[0]     # it contains the x coordinate of the player 
        player_y = player_coords[1]     #it contains the y coordinate of the player   
        overlapping_objects = self._canvas.find_overlapping(player_x - 18, player_y - 18, player_x + 22,
                                                            player_y + 20)
        for pipe in pipe_objects:
            #this  Removes the pipes that have left the canvas window to maximise performance
            if self._canvas.coords(pipe)[2] < 0:
                if pipe in self._scored_pipes:
                    self._scored_pipes.remove(pipe)       # this Remove the redundant widget ID from the list
                self._canvas.delete(pipe)
           
            if "bottom_pipe" in self._canvas.gettags(pipe):    # this Check whether the chosen pipe object is a bottom pipe
              
                if self._canvas.coords(pipe)[0] < player_x:      # Check if the player has flown above the specified pipe without colliding with pipe
                    
                    if pipe not in self._scored_pipes:           # Check that the player hasn't yet been scored for passing through the given pipes
                       
                        self._scored_pipes.append(pipe)
                        self._player_score += 1       # this Give the player a point and update the score 
                        self._update_score()
           
            if pipe in overlapping_objects:                # this Indicates collision between the bird and a pipe
                return True                           
       
        if self._player.get_player_x_y_coords()[1] > self._height - 31:
            return True           # return true if collision has occurred
        else:
            return False          # return False if no collision had occurred

    def _update_score(self):
        self._canvas.delete("score_counter")    #clears the scoring board
        
    def _game_over_menu(self):
        self._GAME_OVER = True
        self._canvas.delete("score_counter")
    
        if self._player_score > self._best_score:
            self._best_score = self._player_score    # set the new high score
        # Create a canvas rectangle widget to serve as the menu's background
        self._canvas.create_rectangle(self.window_center_x - 50, self.window_center_y - 135, self.window_center_x + 50,
                                      self.window_center_y + 10, fill="white", tag="game_over_t")
        self._canvas.create_text(self.window_center_x, self.window_center_y - 110, text="Score", fill="black",
                                 font=("Arial", 20), justify="center", tag="game_over_t")       #it store and display the word "Score"
        self._canvas.create_text(self.window_center_x, self.window_center_y - 80, text=f"{self._player_score}", fill="red",
                                 font=("Arial", 20), justify="center", tag="game_over_t")       # it store and display the user's current score
        self._canvas.create_text(self.window_center_x, self.window_center_y - 45, text="Best", fill="black",
                                 font=("Arial", 20), justify="center", tag="game_over_t")        # it store and display the word "Best score"
        self._canvas.create_text(self.window_center_x, self.window_center_y - 15, text=f"{self._best_score}", fill="red",
                                 font=("Arial", 20), justify="center", tag="game_over_t")        # it store and display the user's best score
        # "restart" the game  button
        button_restart = tk.Button(self._canvas, text="Restart", anchor='c', font=("ROBOTO", 12, "bold"),
                                   command=self._restart_game)
        button_restart.configure(width=20, background="orange")
        # Create a  window to host the "restart" button
        self._canvas.create_window(self.window_center_x, self.window_center_y + 50, window=button_restart, tag="game_over_t")

    def _restart_game(self):
       # This restarts the game
        self._canvas.delete("all")
        self._GAME_OVER = False
        self._player_score = 0
        self._NEW_GAME = False
        self._initialise_game_layout()

    def _start(self):
         #This intiates new game process
        self._intro_menu()

    def _main(self):
       
       # This function carries out the primary game flow 
        if self._score_counter_text:
         self._canvas.tag_raise(self._score_counter_text)
        self._pipe.pipe_generator()             # this Generate a new pipe pair
        collision = self._overlap_detection()   # this Check the game window for collisions 
        self._player.player_fall()
        self._pipe.move_pipe()                  # it  Move the pipe objects towards the player
        
        if not collision:                       # If there is no collision it repeat the process
            self.root.after(15, self._main)
        else:                                   # If the player has collided with a pipe or the floor game over
            self._game_over_menu()


MainApplication()



