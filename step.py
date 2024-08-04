import pyxel
import random

SCENE_TITLE = 0
SCENE_PLAY = 1
SCENE_GAMEOVER = 2

class Game:
    def __init__(self):
        pyxel.init(128, 128, title="Maze Adventure Game")
        pyxel.load("my_resource.pyxres")
        pyxel.mouse(True)
    
        self.player = Player(10, 120, 24, 8, pyxel.tilemaps[0])  # Coordinates for the player sprite
        self.items= [Grogu(15, 25, 'grogu', 0, 0), Droid1(45,80, "droid1", 24, 24), Droid2(90,113, "droid2", 48,16) ]
        self.obstacles = [Stormtrooper(90, 90, 'patrol', 8, 16), Stormtrooper(50, 50, 'patrol', 8, 16), Stormtrooper(20, 30, 'patrol', 8, 16), Stormtrooper(20, 80, 'patrol', 8, 16)]  # Coordinates for the obstacle sprite
        self.maze = Maze(pyxel.tilemaps[0])
        self.ui = UI()
        self.lives = 3
        self.timer = 0.0
        self.game_state = "running"
        self.scene = SCENE_TITLE
        pyxel.playm(0, loop=True)
        pyxel.sounds[0].set("a3a2c1a1", "p", "7", "s", 5)
        pyxel.sounds[1].set("a3a2c2c2", "n", "7742", "s", 10)
        
        pyxel.run(self.update, self.draw)

    def handle_input(self):
        if pyxel.btn(pyxel.KEY_UP):
            self.player.move(0, -1)
        elif pyxel.btn(pyxel.KEY_DOWN):
            self.player.move(0, 1)
        elif pyxel.btn(pyxel.KEY_LEFT):
            self.player.move(-1, 0)
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.player.move(1, 0)
        
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.check_item_pickup()


    def check_item_pickup(self):
        mouse_x = pyxel.mouse_x
        mouse_y = pyxel.mouse_y
        
        for item in self.items:
            print(item.x, self.player.x)
            print(item.y, self.player.y)
            if item.is_clicked(mouse_x, mouse_y) and (item.x <= self.player.x <= item.x + 16 and
                item.y <= self.player.y <= item.y + 16):
                item.pick_up()
                

    def check_win_condition(self):
        all_picked_up = all(item.picked_up for item in self.items)
        if (self.player.x >= 105 and self.player.x <= 120) and (self.player.y >= 8 and self.player.y <= 15) and all_picked_up:
            self.game_state = "win"
            self.scene = SCENE_GAMEOVER

    def update(self):
        
        if self.scene == SCENE_TITLE:
            self.update_title_scene()
            
        elif self.scene == SCENE_PLAY:
            self.update_play_scene()
            
        elif self.scene == SCENE_GAMEOVER:
            self.update_gameover_scene()
            
    def update_title_scene(self):
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.scene = SCENE_PLAY
            pyxel.playm(1, loop=True)
        
    def update_play_scene(self):
        
        if self.game_state == "running":
            self.handle_input()
            for obstacle in self.obstacles:
                obstacle.move_randomly(self.maze)
                if self.player.check_collision(obstacle):
                    self.lives -= 1
                    print("lives;" , self.lives)
                    if self.lives == 0:
                        self.game_state = "game over" 
                        self.scene = SCENE_GAMEOVER
                  
            self.check_win_condition()
            self.timer += 1 / 60.0
            
    def update_gameover_scene(self):
        
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.scene = SCENE_PLAY
            self.player = Player(10, 120, 24, 8, pyxel.tilemaps[0])  # Coordinates for the player sprite
       
            self.items= [Grogu(15, 25, 'grogu', 0, 0), Droid1(50,50, "droid1", 32, 16), Droid2(100,100, "droid2", 48,16) ]
            self.obstacles = [Stormtrooper(90, 90, 'patrol', 8, 16), Stormtrooper(50, 50, 'patrol', 8, 16), Stormtrooper(20, 30, 'patrol', 8, 16), Stormtrooper(20, 80, 'patrol', 8, 16)]  # Coordinates for the obstacle sprite
            self.maze = Maze(pyxel.tilemaps[0])
            self.ui = UI()
            self.lives = 3
            self.timer = 0.0
            self.game_state = "running"
        
    def draw(self):
        pyxel.cls(0)
        
        if self.scene == SCENE_TITLE:
            self.draw_title_scene()
        elif self.scene == SCENE_PLAY:
            self.draw_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.draw_gameover_scene()
            
    def draw_title_scene(self):
        pyxel.text(30, 20, "Death Star Escape", pyxel.frame_count % 16)
        pyxel.text(25, 50, "Pick up Grogu, ", 10)
        pyxel.text(25, 60, "avoid Stormtroopers, ", 10)
        pyxel.text(25, 70, "& escape! ", 10)
        pyxel.text(31, 100, "- PRESS ENTER -", 13)
        
    
    def draw_play_scene(self):
         
        self.maze.draw()
        self.player.draw()
        
        for item in self.items:
            item.draw()
            
        for obstacle in self.obstacles:
            obstacle.draw()
        self.ui.update_timer(self.timer)
       
        
    def draw_gameover_scene(self):
        
        if self.game_state == "win":

            pyxel.text(50, 50, "You Won!", 3)
            self.player.draw_at(50, 60)  # Draw player at specified location
            self.items[0].draw_at(60, 60) 
            self.items[1].draw_at(70, 60)
            self.items[2].draw_at(80, 60)
            
        elif self.game_state == "game over":
            pyxel.text(40, 50, "GAME OVER! ", 8)
            pyxel.text(40, 60, "you lost :( ", 14)
           

class Player:
    def __init__(self, x, y, u, v, tilemap):
        self.x = x
        self.y = y
        self.u = u  # Sprite x-coordinate in the tilemap
        self.v = v  # Sprite y-coordinate in the tilemap
        self.tilemap = tilemap

    def move(self, dx, dy):
   
        new_x = self.x + dx
        new_y = self.y + dy
    
        if new_x >= 0 and new_x  <= 120: 
            self.x = new_x
            
        if new_y >= 13 and new_y <= 120:
            self.y = new_y
      
    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.u, self.v, 16, 16, pyxel.COLOR_BLACK)  # Adjust width and height as necessary


    def draw_at(self, x, y):
        pyxel.blt(x, y, 0, self.u, self.v, 16, 16, pyxel.COLOR_BLACK)  # Draw at specified coordinates


    def check_collision(self, other):
        return (self.x < other.x + 8 and
                self.x + 8 > other.x and
                self.y < other.y + 8 and
                self.y + 8 > other.y)

class Grogu:
    def __init__(self, x, y, type, u, v):
        self.x = x
        self.y = y
        self.type = type
        self.u = u  # Sprite x-coordinate in the tilemap
        self.v = v  # Sprite y-coordinate in the tilemap
        self.picked_up = False
        
    
    def is_clicked(self, mouse_x, mouse_y):
        return (self.x <= mouse_x <= self.x + 16 and
                self.y <= mouse_y <= self.y + 16)
         
    def pick_up(self):
        if not self.picked_up:
            self.x = 125
            self.y = 5
            self.picked_up = True
            pyxel.play(3, 1)

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.u, self.v, 16, 16, pyxel.COLOR_BLACK)  # Adjust width and height as necessary
        
    def draw_at(self, x, y):
        pyxel.blt(x, y, 0, self.u, self.v, 16, 16, pyxel.COLOR_BLACK)  # Draw at specified coordinates

class Droid1:
    def __init__(self, x, y, type, u, v):
        self.x = x
        self.y = y
        self.type = type
        self.u = u  # Sprite x-coordinate in the tilemap
        self.v = v  # Sprite y-coordinate in the tilemap
        self.picked_up = False
        
    def is_clicked(self, mouse_x, mouse_y):
        return (self.x <= mouse_x <= self.x + 16 and
                self.y <= mouse_y <= self.y + 16)
         
    def pick_up(self):
        if not self.picked_up:
            self.x = 120
            self.y = 5
            self.picked_up = True
            pyxel.play(3, 1)

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.u, self.v, 16, 16, pyxel.COLOR_BLACK)  # Adjust width and height as necessary
        
    def draw_at(self, x, y):
        pyxel.blt(x, y, 0, self.u, self.v, 16, 16, pyxel.COLOR_BLACK)  # Draw at specified coordinates

class Droid2:
    def __init__(self, x, y, type, u, v):
        self.x = x
        self.y = y
        self.type = type
        self.u = u  # Sprite x-coordinate in the tilemap
        self.v = v  # Sprite y-coordinate in the tilemap
        self.picked_up = False
        
    def is_clicked(self, mouse_x, mouse_y):
        return (self.x <= mouse_x <= self.x + 16 and
                self.y <= mouse_y <= self.y + 16)
         
    def pick_up(self):
        if not self.picked_up:
            self.x = 115
            self.y = 5
            self.picked_up = True
            pyxel.play(3, 1)

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.u, self.v, 16, 16, pyxel.COLOR_BLACK)  # Adjust width and height as necessary
        
    def draw_at(self, x, y):
        pyxel.blt(x, y, 0, self.u, self.v, 16, 16, pyxel.COLOR_BLACK)  # Draw at specified coordinates


class Stormtrooper:
    def __init__(self, x, y, pattern, u, v):
        self.x = x
        self.y = y
        self.pattern = pattern
        self.u = u  
        self.v = v  
  
        angle = pyxel.rndi(30, 150)
        self.dx = pyxel.cos(angle)
        self.dy = pyxel.sin(angle)
        
    def move_randomly(self, maze):
        
        if self.x < -10 or self.x + 16 > 150:
            self.dx *= -1
            
        if self.y < 20 or self.y+ 16 > 110:
            self.dy *= -1

        self.x += self.dx * 0.8
        self.y += self.dy * 0.8
    

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.u, self.v, 16, 16, pyxel.COLOR_BLACK)  # Adjust width and height as necessary
        

class Maze:
    def __init__(self, tilemap):
        self.tilemap = tilemap

    def draw(self):
        pyxel.bltm(0, 0, 0, 0, 0, 128, 128)  # Adjust width and height as necessary

class UI:
    def __init__(self):
        self.life_counter = 3
        self.timer = 0.0

    def update_timer(self, time):
        pyxel.text(10, 5, f"Timer: {int(time)}", 10)

Game()
