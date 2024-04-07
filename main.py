
import arcade
import os
import random

# Screen constants.
SCREEN_WIDTH = 1009
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Little Guy Big Sword"

# Character sprite constants.
CHARACTER_SCALING = 2
PLAYER_MOVEMENT_SPEED = 3
GRAVITY = 0.3
PLAYER_JUMP_SPEED = 10
PLAYER_START_X = 64
PLAYER_START_Y = 100
MAX_DAMAGE_FRAMES = 7
MAX_LIVES = 3

# How much the tiles are upscaled by.
TILE_SCALING = 1.5

# Enemy sprite constants
ENEMY_SCALING = 1.2
ENEMY_MOVEMENT_SPEED = 2
ENEMY_JUMP_SPEED = 7
ENEMY_HEALTH = 20
RESPAWN_TIME = 300

# Amount of kills needed to complete a level.
SCORE_AMOUNT = 20

# Spawn point coordinates for each map.
MAP_ONE_SPAWN_POINTS = [171, 530, 417, 655, 718, 517.5]
MAP_TWO_SPAWN_POINTS = [277, 558, 555, 361, 718, 517]
MAP_THREE_SPAWN_POINTS = [474, 544, 816, 442, 313, 351]

# Layer names.
LAYER_NAME_PLATFORMS = "Platforms"
LAYER_NAME_ENEMIES = "Enemies"

RIGHT_FACING = 0
LEFT_FACING = 1

def load_texture_pair(filename):
    '''Loads texture and horizontally flipped texture for when sprites move in opposite direction'''

    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]



class Skeleton(arcade.Sprite):
    '''Class that loads enemies'''

    def __init__(self, level):
        super().__init__()

        self.level = level

        # String used adding textures.
        filename = "./assets/creatures/Skeleton"


        self.idle_texture_pair = load_texture_pair(f"{filename}/idle/tile000.png")

        # Loads walk textures.
        self.walk_textures = []
        for i in range(4):
            texture = load_texture_pair(f"{filename}/walk/tile00{i}.png")
            self.walk_textures.append(texture)

        # Loads idle textures.
        self.idle_textures = []
        for i in range(4):
            texture = load_texture_pair(f"{filename}/idle/tile00{i}.png")
            self.idle_textures.append(texture)

        # Loads attack textures.
        self.attack_textures = []
        for i in range(8):
            texture = load_texture_pair(f"{filename}/attack/tile00{i}.png")
            self.attack_textures.append(texture)

        # Loads death textures.
        self.death_textures = []
        for i in range(4):
            texture = load_texture_pair(f"{filename}/death/tile00{i}.png")
            self.death_textures.append(texture)

        # Loads hitbox.
        self.hit_texture_pair = load_texture_pair(f"{filename}/take_hit/tile001.png")
        self.texture = self.idle_texture_pair[0]
        self.hit_box = self.texture.hit_box_points

        # Sets scale of enemy and default facing direction.
        self.scale = ENEMY_SCALING
        self.sprite_face_direction = RIGHT_FACING

        self.cur_texture = 0
        self.state = "alive"
        self.timer = 0
        self.enemy_health = ENEMY_HEALTH
        self.attacking = False
        self.if_hit = False
        self.state = "alive"
        self.death_timer = 0
        self.play_sound = 0
        self.died = False

        # Loads sound when enemy dies.
        self.enemy_death_sound = arcade.load_sound("./assets/sounds/enemy_death.wav")
    
    def update_enemy_movement(self):
        '''When called updates the movement of the enemy sprite'''

        if self.state == "alive":
            
            # Chooses a random number that determines the movement
            #of the sprite, either left, right, idle or jump.
            i = random.randint(1, 20)
            if i == 1:
                self.direction =  random.randint(0, 12)
                if self.direction == 0:
                    if self.change_y == 0:
                        self.change_y += ENEMY_JUMP_SPEED
                elif self.direction >= 1 and self.direction <=4:
                    self.change_x = ENEMY_MOVEMENT_SPEED
                elif self.direction >= 5 and self.direction <= 8:
                    self.change_x = -ENEMY_MOVEMENT_SPEED
                elif self.direction >= 9:
                    self.change_x = 0

        # Movement is locked if the enemy is attacking or dead.
        elif self.state == "attack" or self.state == "dead":
            self.change_x = 0
            self.change_y = 0

    def update_enemy_animation(self, delta_time: float = 1 / 60):
        '''Updates the animation of the enemy sprite'''

        # Code only runs if the enemy's health is above 0.
        if self.enemy_health > 0:

            # Determines the facing direction depending on the movement of the sprite.
            if self.change_x < 0 and self.sprite_face_direction == RIGHT_FACING:
                self.sprite_face_direction = LEFT_FACING
            elif self.change_x > 0 and self.sprite_face_direction == LEFT_FACING:
                self.sprite_face_direction = RIGHT_FACING
            
            # If the if_hit variable is set to true then the hit animation runs.
            if self.if_hit == True:
                    self.texture = self.hit_texture_pair[self.sprite_face_direction]
                    self.if_hit = False

            # Runs if the enemy isn't attacking.        
            if self.state != "attack":

                self.attacking = False

                # Runs the walking animation with a timer that slows the speed of animation.
                if self.change_x > 0 or self.change_x < 0:
                    if self.timer > 5:
                        self.cur_texture +=1 
                        if self.cur_texture > 3:
                            self.cur_texture = 0
                        self.texture = self.walk_textures[self.cur_texture][self.sprite_face_direction]
                        self.timer = 0
                    else:
                        self.timer += 1

                # If the enemy is idle then the idle texture runs at random intervals.
                if self.change_x == 0:
                    i = random.randint(0, 10)
                    if i == 1:
                        self.cur_texture +=1 
                        if self.cur_texture > 3:
                            self.cur_texture = 0
                        self.texture = self.idle_textures[self.cur_texture][self.sprite_face_direction]

            # Only runs if the state of the enemy is "attack".
            if self.state == "attack":

                # Runs the attacking animation that sets the attacking variable when animation runs the final frame then
                # resets back to false.
                if self.timer > 5:
                    self.cur_texture += 1
                    if self.cur_texture > 7:
                        self.attacking = False
                        self.state = ""
                        self.cur_texture = 0
                    if self.cur_texture == 7:
                        self.attacking = True  
                    self.texture = self.attack_textures[self.cur_texture][self.sprite_face_direction]
                    self.timer = 0

                else:
                    self.timer += 1

        # Only runs if the enemy health is below and the enemy isn't already dead.
        if self.enemy_health <= 0 and self.state != "dead":
                

                # Once the animation has run the enemy state is dead.
                if self.timer > 6:
                    self.cur_texture += 1
                    if self.cur_texture > 3:
                        self.state = "dead"
                        self.attacking = False
                        self.cur_texture = 0
                    self.texture = self.death_textures[self.cur_texture][self.sprite_face_direction]
                    self.timer = 0
                else:
                    self.timer += 1

                # Play sound variable is used to make sure the sound is only played once when the enemy dies.
                self.play_sound += 1
                if self.play_sound < 2:
                    arcade.play_sound(self.enemy_death_sound)
                    self.play_sound += 1 

        # Only runs if enemy state is "dead".
        if self.state == "dead":

            self.texture = self.death_textures[3][self.sprite_face_direction]

            # Timer so the enemy doesn't immediatley respawn when they are killed.
            self.death_timer += 1
            if self.death_timer > RESPAWN_TIME:
                self.respawn()
           
    def get_attack(self):
        '''Returns attacking variable'''
        return self.attacking
    
    def respawn(self):
        '''Respawns the enemy when it is killed'''

        # Determines spawn location depending on the level.
        spawn_points = 0
        if self.level == 1:
            spawn_points = MAP_ONE_SPAWN_POINTS
        elif self.level == 2:
            spawn_points = MAP_TWO_SPAWN_POINTS
        else:
            spawn_points = MAP_THREE_SPAWN_POINTS

        # Resets enemy health and state.
        self.enemy_health = ENEMY_HEALTH
        self.state = "alive"
        self.death_timer = 0
        self.play_sound = 0

        # Selects from a random list of coordinates.
        random_num = random.randint(1, 3)
        if random_num == 1:
            self.center_x = spawn_points[0]
            self.center_y = spawn_points[1]
        elif random_num == 2:
            self.center_x = spawn_points[2]
            self.center_y = spawn_points[3]
        elif random_num == 3:
            self.center_x = spawn_points[4]
            self.center_y = spawn_points[5]
    
    def get_dead(self):
        '''Returns the state of the enemy.'''
        return self.state

class PlayerSprite(arcade.Sprite):
    '''Class that runs the player sprite'''
    def __init__(self):

        super().__init__()

        # Sets default direction of character and scaling.
        self.character_face_direction = RIGHT_FACING
        self.scale = CHARACTER_SCALING

        self.path = "./assets/little_guy_big-sword"

        # Sets idle texture as well as hitbox of player sprite.
        self.idle_texture = f"{self.path}_0.png"
        self.idle_texture_pair = load_texture_pair(self.idle_texture)
        self.texture = self.idle_texture_pair[0]
        self.hit_box = self.texture.hit_box_points
        self.hit_texture = f"{self.path}_hit.png"
        self.hit_texture_pair = load_texture_pair(self.hit_texture)
        
        # Loads hit duplicated hit textures so the textures run in a fast sequence for a while.
        self.hit_textures = []
        i = 0
        while i != 10:
            texture = load_texture_pair(f"{self.path}_hit.png")
            self.hit_textures.append(texture)
            texture = load_texture_pair(f"{self.path}_0.png")
            self.hit_textures.append(texture)
            i += 1
        
        # Loads fall textures.
        self.fall_textures = []
        texture = load_texture_pair(f"{self.path}_slash_1.png")
        self.fall_textures.append(texture)
        texture = load_texture_pair(f"{self.path}_slash_2.png")
        self.fall_textures.append(texture)

        # Loads attack textures.
        self.attack_textures = []
        for i in range(1, 5):
            texture = load_texture_pair(f"{self.path}_attack_{i}.png")
            self.attack_textures.append(texture)

        # Loads walk textures.
        self.walk_textures = []
        for i in range(2):
            x = 0
            while x != 5:
                texture = load_texture_pair(f"{self.path}_{i}.png")
                self.walk_textures.append(texture)
                x +=1

        self.attack = False
        self.timer = 0
        self.health = 10
        self.if_hit = False
        self.cur_texture = 0
        self.kills = 0

        # Loads death sound of player.
        self.player_death_sound = arcade.load_sound("./assets/sounds/player_death.wav")


    def update_animation(self, delta_time: float = 1 / 60):
        '''Update the animation of the player sprite.'''

        # Sets face direction depending on player movement.
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING
        
        # Calls if_killed function if healthh is below or equal to 0.
        if self.health <= 0:
            self.if_killed()
            return

        if self.attack == False:
            
            # Runs falling textures when falling.
            if self.change_y < 0 and self.change_y > -1:
                self.texture = self.fall_textures[0][self.character_face_direction]
                return
            if self.change_y < 0:
                self.texture = self.fall_textures[1][self.character_face_direction]
                return

            # Idle animation that only plays when the player is not being hit
            if self.change_x == 0 and self.if_hit != True:
                self.texture = self.idle_texture_pair[self.character_face_direction]

            # Walking animation plays when the player moves horizontally and the player isn't being hit.    
            if self.change_x > 0 or self.change_x < 0 and self.if_hit != True:
                self.cur_texture += 1
                if self.cur_texture > 9:
                    self.cur_texture = 0
                self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]

            # Plays hit animation while the player is being hit
            if self.if_hit == True:
                self.cur_texture += 1
                if self.cur_texture > 19:
                    self.cur_texture = 0
                    self.if_hit = False
                self.texture = self.hit_textures[self.cur_texture][self.character_face_direction]
        

        if self.attack == True:
            
            # Makes player hover in air while attacking.
            if self.change_y < 0:
                self.change_x = 0
                self.change_y = 0

            # Loads attacking animation.
            if self.timer > 1:
                self.cur_texture += 1
                if self.cur_texture > 3:
                    self.cur_texture = 0
                self.texture = self.attack_textures[self.cur_texture][self.character_face_direction]
                self.timer = 0
            else:
                self.timer += 1
        
    def if_killed(self):
        '''Resets player back to starting position when killed as well as plays death sound.'''

        arcade.play_sound(self.player_death_sound)
        self.health = 10
        self.center_x = PLAYER_START_X
        self.center_y = PLAYER_START_Y

class MyGame(arcade.Window):

    """
    Main application class.
    """

    def __init__(self):

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        FILE_PATH = os.path.dirname(os.path.abspath(__file__))
        os.chdir(FILE_PATH)

        self.tile_map = None

        self.level = 1

        self.scene = None

        self.spawn_points = None

        self.player_sprite = None

        self.lives = MAX_LIVES

        # All enemy sprites.
        self.enemy_sprite_1 = None
        self.enemy_sprite_2 = None
        self.enemy_sprite_3 = None
        self.enemy_sprite_4 = None
        self.enemy_sprite_5 = None
        self.enemy_sprite_6 = None
        self.enemy_sprite_7 = None
        self.enemy_sprite_8 = None

        # Enemy sprite engines.
        self.physics_engine_2 = None
        self.physics_engine_3 = None
        self.physics_engine_4 = None
        self.physics_engine_5 = None
        self.physics_engine_6 = None
        self.physics_engine_7 = None
        self.physics_engine_8 = None
        self.physics_engine_9 = None


        self.collision_strings = []

        # Player sprite engine.
        self.physics_engine = None
        
        self.camera = None

        self.gui_camera = None

        # Score of how many enemies are killed per level.
        self.kills = 0

        self.character_face_direction = RIGHT_FACING
        self.left_pressed = False
        self.right_pressed = False

        # Different counters used in on_update().
        self.counter = 0
        self.attack_counter = 0
        self.respawn_counter = 0

        # List of enemy sprite objects.
        self.enemy_sprite_list = [self.enemy_sprite_1, self.enemy_sprite_2,
                                  self.enemy_sprite_3, self.enemy_sprite_4,
                                  self.enemy_sprite_5, self.enemy_sprite_6,
                                  self.enemy_sprite_7, self.enemy_sprite_8
                                  ]

        # List of physics engines for each enemy
        self.enemy_physics_engines = [self.physics_engine_2, self.physics_engine_3,
                                      self.physics_engine_4, self.physics_engine_5,
                                      self.physics_engine_6, self.physics_engine_7,
                                       self.physics_engine_8,  self.physics_engine_9
                                      ]

        # Sounds pre loaded.
        self.ouch = arcade.load_sound("./assets/sounds/ouch.wav")
        self.player_hit = arcade.load_sound("./assets/sounds/hit.wav")
        self.key_pickup = arcade.load_sound("./assets/sounds/key_pickup.wav")
        self.walk_sound = arcade.load_sound("./assets/sounds/move.wav")
        self.jump_sound = arcade.load_sound("./assets/sounds/jump.wav")
        self.level_end = arcade.load_sound("./assets/sounds/complete_level.wav")
        self.end = arcade.load_sound("./assets/sounds/end.wav")

    def setup(self):
        '''Initializes all sprites and maps'''

        self.camera = arcade.Camera(self.width, self.height)

        self.gui_camera = arcade.Camera(self.width, self.height)

        map_name = f"./maps/map{self.level}.json"

        layer_options = {LAYER_NAME_PLATFORMS: {"use_spatial_hash": True,},}

        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Adds player sprite to scene.
        self.player_sprite = PlayerSprite()
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.scene.add_sprite("Player", self.player_sprite)
        

        # Uses list of sprite objects and calls the Skeleton function and adds them to the scene.
        for self.new_enemy in self.enemy_sprite_list:

            a = self.enemy_sprite_list.index(self.new_enemy)
            self.new_enemy = Skeleton(self.level)
            self.new_enemy.respawn()
            self.enemy_sprite_list[a] = self.new_enemy
            self.scene.add_sprite(LAYER_NAME_ENEMIES, self.new_enemy)    

        # Loads player sprite physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, 
            gravity_constant=GRAVITY,
            walls=self.scene[LAYER_NAME_PLATFORMS],
        )
        
        # Loads enemy physics engines
        for self.engine in self.enemy_physics_engines:
            index = self.enemy_physics_engines.index(self.engine)
            self.engine = arcade.PhysicsEnginePlatformer(
                self.enemy_sprite_list[index],
                gravity_constant= GRAVITY,
                walls=self.scene[LAYER_NAME_PLATFORMS])
            self.enemy_physics_engines[index] = self.engine

        
    def on_draw(self):

        self.clear()

        self.camera.use()

        self.scene.draw(pixelated = True)

        self.gui_camera.use()

        # Displays health.
        draw_health = f"HEALTH: {self.player_sprite.health}"
        arcade.draw_text(draw_health, 40, 700, arcade.csscolor.WHITE, 18)

        # Displays Score/amount kills per level
        draw_kills = f"SCORE: {self.kills}"
        arcade.draw_text(draw_kills, 40, 650, arcade.csscolor.WHITE, 18)
        
        # Displays lives.
        draw_lives = f"LIVES: {self.lives}"
        arcade.draw_text(draw_lives, 40, 600, arcade.csscolor.WHITE, 18)

    def on_key_press(self, key, modifiers):
        
        #Only runs if player is alive.
        if self.player_sprite.health > 0:

            if key == arcade.key.UP or key == arcade.key.W:
                if self.physics_engine.can_jump():
                    self.player_sprite.change_y = PLAYER_JUMP_SPEED
                    arcade.play_sound(self.jump_sound)
            elif key == arcade.key.LEFT or key == arcade.key.A:
                self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
                arcade.play_sound(self.walk_sound)
            elif key == arcade.key.RIGHT or key == arcade.key.D:
                self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
                arcade.play_sound(self.walk_sound)

            # Sets player attack variable to true when spaced is pressed.
            elif key == arcade.key.SPACE:
                self.player_sprite.attack = True
      
    
    def on_key_release(self, key, modifiers):

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0
        
        elif key == arcade.key.SPACE:
            self.player_sprite.attack = False

    def on_update(self, delta_time: float = 1 / 60):
        '''Updates the game 60 times per second'''

        # Updates the physics engines
        self.physics_engine.update()
        for i in self.enemy_physics_engines:
            i.update()

        self.player_sprite.update_animation()

        # Updates the enemy movement and animation.
        for enemies in self.enemy_sprite_list:
            enemies.update_enemy_movement()
            enemies.update_enemy_animation()

        # Updates the score once the enemy has respawned.
        for i in self.enemy_sprite_list:
            if i.state == "dead":
                self.respawn_counter += 1
                if self.respawn_counter == RESPAWN_TIME:
                    self.kills += 1
                    self.respawn_counter = 0


        enemy_hit_list = arcade.check_for_collision_with_lists(self.player_sprite,[self.scene[LAYER_NAME_ENEMIES]])

         # If player collides with enemy sprite.
        for enemy in enemy_hit_list:
            
            # Changes the state of enemy to attack when it collides with the player.
            if enemy.enemy_health > 0:
                enemy.state = "attack"

            # If the enemy manages to hit the player the player health decreases and sets the if_hit variable to True.
            if enemy.get_attack() == True:
                        self.player_sprite.if_hit = True
                        self.counter += 1
                        if self.counter > 7: #Make Constant
                            self.player_sprite.health -= 1
                            arcade.play_sound(self.ouch)
                            self.counter = 0
                        
                        if self.player_sprite.health <= 0:
                            self.lives -= 1

            # If the player hits the enemy sprite the enemy health decreases        
            if self.player_sprite.attack == True:
                        
                        enemy.if_hit = True
                        enemy.enemy_health -= 1
                        arcade.play_sound(self.player_hit)

                        # Timer so 
                        self.attack_counter += 1
                        if self.attack_counter > 5:
                            self.player_sprite.attack = False
                            self.attack_counter = 0

        # Resets score and player health and changes map and gives player a life if they have lost one
        if self.kills == SCORE_AMOUNT:
            arcade.play_sound(self.level_end)
            self.level += 1
            self.kills = 0
            self.player_sprite.health = 10

            # Only increases lives if lives is below three.
            if self.lives < MAX_LIVES:
                self.lives += 1

            # Plays winning sound when the player has completed level 3.
            if self.level == 4:
                self.level = 3
                arcade.play_sound(self.end)
            self.setup()

        # Resets player back to start.
        if self.lives == 0:
            self.kills = 0
            self.level = 1
            self.setup()
            self.lives = MAX_LIVES

def main():
    '''Main Function.'''

    Window = MyGame()
    Window.setup()
    arcade.run()


if __name__ == "__main__":
    main()