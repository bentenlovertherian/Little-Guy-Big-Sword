
import arcade
import os
import random
import time

SCREEN_WIDTH = 1009
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Little Guy Big Sword"
#Feedback:
# add locked door
# make it so u stop moving 1nce dead

# Make so the player dies when the health is below zero using "<=" symbol instead of "="

#feature notes: have key unlock door to spawn point

CHARACTER_SCALING = 2
ENEMY_SCALING = 1.2
TILE_SCALING = 1.5
PLAYER_MOVEMENT_SPEED = 3
GRAVITY = 0.3
PLAYER_JUMP_SPEED = 12
PLAYER_START_X = 64
PLAYER_START_Y = 100
ENEMY_MOVEMENT_SPEED = 2
ENEMY_JUMP_SPEED = 7

LAYER_NAME_PLATFORMS = "Platforms"
LAYER_NAME_DOOR = "Door"
LAYER_NAME_ENEMIES = "Enemies"

RIGHT_FACING = 0
LEFT_FACING = 1

def load_texture_pair(filename):

    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]


class Key(arcade.Sprite):
    def __init__(self):
        super().__init__()

        filename = "./assets/key/key_"

        self.textures = []
        for i in range(1, 5):
            texture = arcade.load_texture(f"{filename}{i}.png")
            self.textures.append(texture)
        texture = arcade.load_texture(f"{filename}3.png")
        self.textures.append(texture)
        texture = arcade.load_texture(f"{filename}2.png")
        self.textures.append(texture)
        
        self.timer = 0
        self.cur_texture = 0

        self.scale = ENEMY_SCALING
        
        self.texture = self.textures[0]
        self.hit_box = self.texture.hit_box_points

    def update_animation(self):
        
        if self.timer > 20:
            self.cur_texture += 1
            if self.cur_texture > 5:
                self.cur_texture = 0
            self.texture = self.textures[self.cur_texture]
            self.timer = 0
        else:
            self.timer += 1


class Skeleton(arcade.Sprite):

    def __init__(self):
        super().__init__()

        filename = "./assets/creatures/Skeleton"

        self.idle_texture_pair = load_texture_pair(f"{filename}/idle/tile000.png")

        self.walk_textures = []
        for i in range(4):
            texture = load_texture_pair(f"{filename}/walk/tile00{i}.png")
            self.walk_textures.append(texture)

        self.idle_textures = []
        for i in range(4):
            texture = load_texture_pair(f"{filename}/idle/tile00{i}.png")
            self.idle_textures.append(texture)

        self.attack_textures = []
        for i in range(8):
            texture = load_texture_pair(f"{filename}/attack/tile00{i}.png")
            self.attack_textures.append(texture)
 
        self.death_textures = []
        for i in range(4):
            texture = load_texture_pair(f"{filename}/death/tile00{i}.png")
            self.death_textures.append(texture)

        self.hit_texture_pair = load_texture_pair(f"{filename}/take_hit/tile001.png")

        self.texture = self.idle_texture_pair[0]
        self.hit_box = self.texture.hit_box_points

        self.scale = ENEMY_SCALING
        self.sprite_face_direction = RIGHT_FACING

        self.cur_texture = 0
        self.state = ""
        self.timer = 0
        self.enemy_health = 50
        self.attacking = False
        self.play_sound = 0
        self.if_hit = False
        self.enemy_death_sound = arcade.load_sound("./assets/sounds/enemy_death.wav")
    
    def update_enemy_movement(self):
        
        if self.state == "":

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

        elif self.state == "attack" or self.state == "dead":
            self.change_x = 0
            self.change_y = 0

    def update_enemy_animation(self, delta_time: float = 1 / 60):

        if self.enemy_health > 0:

            if self.change_x < 0 and self.sprite_face_direction == RIGHT_FACING:
                self.sprite_face_direction = LEFT_FACING
            elif self.change_x > 0 and self.sprite_face_direction == LEFT_FACING:
                self.sprite_face_direction = RIGHT_FACING
            
            if self.if_hit == True:
                    self.texture = self.hit_texture_pair[self.sprite_face_direction]
                    self.if_hit = False
                    
            if self.state != "attack":

                self.attacking = False
                if self.change_x > 0 or self.change_x < 0:
                    if self.timer > 5:
                        self.cur_texture +=1 
                        if self.cur_texture > 3:
                            self.cur_texture = 0
                        self.texture = self.walk_textures[self.cur_texture][self.sprite_face_direction]
                        self.timer = 0
                    else:
                        self.timer += 1

                if self.change_x == 0:
                    i = random.randint(0, 10)
                    if i == 1:
                        self.cur_texture +=1 
                        if self.cur_texture > 3:
                            self.cur_texture = 0
                        self.texture = self.idle_textures[self.cur_texture][self.sprite_face_direction]

            if self.state == "attack":
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

        if self.enemy_health <= 0 and self.state != "dead":
                
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

                self.play_sound+= 1
                if self.play_sound < 2:
                    arcade.play_sound(self.enemy_death_sound)
                    self.play_sound += 1 

        if self.state == "dead":
            self.texture = self.death_textures[3][self.sprite_face_direction]

    def get_attack(self):
        return self.attacking


class PlayerSprite(arcade.Sprite):

    def __init__(self):

        super().__init__()

        self.character_face_direction = RIGHT_FACING
        self.scale = CHARACTER_SCALING

        self.path = "./assets/little_guy_big-sword"

        self.idle_texture = f"{self.path}_0.png"
        self.idle_texture_pair = load_texture_pair(self.idle_texture)

        self.death_texture = f"{self.path}_death.png"
        self.death_texture_pair = load_texture_pair(self.death_texture)

        self.texture = self.idle_texture_pair[0]
        self.hit_box = self.texture.hit_box_points

        self.hit_texture = f"{self.path}_hit.png"
        self.hit_texture_pair = load_texture_pair(self.hit_texture)
        

        self.hit_textures = []
        i = 0
        while i != 10:
            texture = load_texture_pair(f"{self.path}_hit.png")
            self.hit_textures.append(texture)
            texture = load_texture_pair(f"{self.path}_0.png")
            self.hit_textures.append(texture)
            i += 1
        

        self.fall_textures = []
        texture = load_texture_pair(f"{self.path}_slash_1.png")
        self.fall_textures.append(texture)
        texture = load_texture_pair(f"{self.path}_slash_2.png")
        self.fall_textures.append(texture)

        self.attack_textures = []
        for i in range(1, 5):
            texture = load_texture_pair(f"{self.path}_attack_{i}.png")
            self.attack_textures.append(texture)

        
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
        self.play_sound = 0
        self.door_unlock = False
        self.lives = 3

        self.player_death_sound = arcade.load_sound("./assets/sounds/player_death.wav")


    def update_animation(self, delta_time: float = 1 / 60):
        
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING
        
        if self.health <= 0:
            self.if_killed()
            return

        if self.attack == False:

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
            
            if self.change_y < 0:
                self.change_x = 0
                self.change_y = 0

            if self.timer > 1:
                self.cur_texture += 1
                if self.cur_texture > 3:
                    self.cur_texture = 0
                self.texture = self.attack_textures[self.cur_texture][self.character_face_direction]
                self.timer = 0
            else:
                self.timer += 1
        
    def if_killed(self):

        arcade.play_sound(self.player_death_sound)
        self.health = 10
        self.center_x = PLAYER_START_X
        self.center_y = PLAYER_START_Y
        self.lives -=1

class MyGame(arcade.Window):

    """
    Main application class.
    """

    def __init__(self):

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        FILE_PATH = os.path.dirname(os.path.abspath(__file__))
        os.chdir(FILE_PATH)

        self.tile_map = None

        self.scene = None

        self.player_sprite = None

        self.enemy_sprite_1 = None
        self.enemy_sprite_2 = None

        self.physics_engine_2 = None
        self.physics_engine_3 = None

        self.collision_strings = []

        self.physics_engine = None
        
        self.camera = None

        self.gui_camera = None

        self.end_of_map = 0

        self.character_face_direction = RIGHT_FACING
        self.left_pressed = False
        self.right_pressed = False

        self.counter = 0
        self.attack_counter = 0

        # List of enemy sprite objects.
        self.enemy_sprite_list = [self.enemy_sprite_1, self.enemy_sprite_2]

        # List of physics engines for each enemy
        self.enemy_physics_engines = [self.physics_engine_2, self.physics_engine_3]

        self.ouch = arcade.load_sound("./assets/sounds/ouch.wav")
        self.player_hit = arcade.load_sound("./assets/sounds/hit.wav")
        self.key_pickup = arcade.load_sound("./assets/sounds/key_pickup.wav")
        self.walk_sound = arcade.load_sound("./assets/sounds/move.wav")
        self.jump_sound = arcade.load_sound("./assets/sounds/jump.wav")

    def setup(self):


        self.camera = arcade.Camera(self.width, self.height)

        self.gui_camera = arcade.Camera(self.width, self.height)


        #map_name = f":resources:tiled_maps/map2_level_{self.level}.json"
        map_name = "maps/map1.tmx"

        layer_options = {LAYER_NAME_PLATFORMS: {"use_spatial_hash": True,}, LAYER_NAME_DOOR: {"use_spatial_hash": True},}

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
            self.new_enemy = Skeleton()

            self.new_enemy.center_x = 350
            self.new_enemy.center_y = 600

            self.enemy_sprite_list[a] = self.new_enemy
            self.scene.add_sprite(LAYER_NAME_ENEMIES, self.new_enemy)

        # Adds key sprite to the game.
        # Calls key class to create a key object.
        self.key = Key()
        self.key.center_x = 780
        self.key.center_y = 690
        self.scene.add_sprite("key", self.key)        

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, 
            gravity_constant=GRAVITY,
            walls=self.scene[LAYER_NAME_PLATFORMS],
        )
        
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

        draw_health = f"{self.player_sprite.health}"
        arcade.draw_text(draw_health, 40, 700, arcade.csscolor.WHITE, 18)

    def on_key_press(self, key, modifiers):
        
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

        # Updates the physics engines
        self.physics_engine.update()
        for i in self.enemy_physics_engines:
            i.update()

        self.player_sprite.update_animation()
        self.key.update_animation()

        # Updates the enemy movement and animation.
        for enemies in self.enemy_sprite_list:
            enemies.update_enemy_movement()
            enemies.update_enemy_animation()

        
        collision_list = arcade.check_for_collision_with_lists(self.player_sprite,[self.scene["key"]])
    
        for collision in collision_list:
        
            if self.scene["key"] in collision.sprite_lists:

                self.key.remove_from_sprite_lists()
                arcade.play_sound(self.key_pickup)

        enemy_hit_list = arcade.check_for_collision_with_lists(self.player_sprite,[self.scene[LAYER_NAME_ENEMIES]])

         # If player collides with enemy sprite.
        for enemy in enemy_hit_list:
            
            # Changes the state of enemy to attack when it collides with the player.
            enemy.state = "attack"

            # If the enemy manages to hit the player the player health decreases and sets the if_hit variable to True.
            if enemy.get_attack() == True:
                        self.player_sprite.if_hit = True
                        self.counter += 1
                        if self.counter == 7:
                            self.player_sprite.health -= 1
                            arcade.play_sound(self.ouch)
                            self.counter = 0

            # If the player hits the enemy sprite the enemy health decreases        
            if self.player_sprite.attack == True:
                        
                        enemy.if_hit = True
                        enemy.enemy_health -= 1
                        arcade.play_sound(self.player_hit)

                        self.attack_counter += 1
                        if self.attack_counter > 5:
                            self.player_sprite.attack = False
                            self.attack_counter = 0



def main():
    """Main function"""
    Window = MyGame()
    Window.setup()
    arcade.run()


if __name__ == "__main__":
    main()