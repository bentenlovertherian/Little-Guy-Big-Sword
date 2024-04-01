
import arcade
import os
import random
import time

SCREEN_WIDTH = 1009
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Little Guy Big Sword"

#feature notes: have key unlock door to spawn point

CHARACTER_SCALING = 2
ENEMY_SCALING = 1.2
TILE_SCALING = 1.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING
PLAYER_MOVEMENT_SPEED = 3
GRAVITY = 0.3
PLAYER_JUMP_SPEED = 12
PLAYER_START_X = 64
PLAYER_START_Y = 100
ENEMY_MOVEMENT_SPEED = 2
ENEMY_JUMP_SPEED = 7

LAYER_NAME_PLATFORMS = "Platforms"
LAYER_NAME_ENEMIES = "Enemies"

RIGHT_FACING = 0
LEFT_FACING = 1

def load_texture_pair(filename):

    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]

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


        self.texture = self.idle_texture_pair[0]
        self.hit_box = self.texture.hit_box_points

        self.scale = ENEMY_SCALING
        self.sprite_face_direction = RIGHT_FACING

        self.cur_texture = 0
        self.state = ""
        self.timer = 0
        self.enemy_health = 10
        self.attacking = False
        self.play_sound = 0
        self.enemy_death_sound = arcade.load_sound("./assets/sounds/enemy_death.wav")
    
    def update_enemy_movement(self):
        
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
                if self.timer > 10:
                    self.cur_texture += 1
                    if self.cur_texture > 7:
                        self.attacking = True
                        self.state = ""
                        self.cur_texture = 0     
                    self.texture = self.attack_textures[self.cur_texture][self.sprite_face_direction]
                    self.timer = 0

                else:
                    self.timer += 1

        if self.enemy_health <= 0:
                
                if self.timer > 6:
                    self.cur_texture += 1
                    if self.cur_texture > 3:
                        self.state = "dead"
                        self.cur_texture = 0
                    self.texture = self.death_textures[self.cur_texture][self.sprite_face_direction]
                    self.timer = 0
                else:
                    self.timer += 1

                self.play_sound+= 1
                if self.play_sound < 2:
                    arcade.play_sound(self.enemy_death_sound)
                    self.play_sound += 1            

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


    def update_animation(self, delta_time: float = 1 / 60):
        

        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        if self.attack != True:

            if self.health < 0:
                self.texture = self.death_texture_pair[self.character_face_direction]
                return
            

            if self.change_y < 0 and self.change_y > -1:
                self.texture = self.fall_textures[0][self.character_face_direction]
                return
            
            if self.change_y < 0:
                self.texture = self.fall_textures[1][self.character_face_direction]
                return


            # Idle animation that only plays when the player is not being hit
            if self.change_x == 0 and self.if_hit != True:
                self.texture = self.idle_texture_pair[self.character_face_direction]
                
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
            if self.timer > 1:
                self.cur_texture += 1
                if self.cur_texture > 3: 
                    self.attack = ""
                    self.cur_texture = 0        
                self.texture = self.attack_textures[self.cur_texture][self.character_face_direction]
                self.timer = 0
            else:
                self.timer += 1


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

        self.physics_engine = None

        self.camera = None

        self.gui_camera = None

        self.end_of_map = 0

        self.character_face_direction = RIGHT_FACING
        self.left_pressed = False
        self.right_pressed = False

        self.counter = 0

        self.enemy_sprite_list = [self.enemy_sprite_1, self.enemy_sprite_2]
        self.enemy_physics_engines = [self.physics_engine_2, self.physics_engine_3]

        self.player_slice = arcade.load_sound("./assets/sounds/player_slice.wav")
        self.player_hit = arcade.load_sound("./assets/sounds/hit.wav")

    def setup(self):


        self.camera = arcade.Camera(self.width, self.height)

        self.gui_camera = arcade.Camera(self.width, self.height)


        #map_name = f":resources:tiled_maps/map2_level_{self.level}.json"
        map_name = "maps/map1.tmx"

        layer_options = {LAYER_NAME_PLATFORMS: {"use_spatial_hash": True,},}

        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.player_sprite = PlayerSprite()
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.scene.add_sprite("Player", self.player_sprite)

        # Calls skeleton function to add a new sprite and adds them to sprite list.
        

        
        for self.new_enemy in self.enemy_sprite_list:
            a = self.enemy_sprite_list.index(self.new_enemy)
            self.new_enemy = Skeleton()
            self.new_enemy.center_x = 350
            self.new_enemy.center_y = 600
            self.enemy_sprite_list[a] = self.new_enemy
            sprite_string = f"enemy_{a + 1}"  
            self.scene.add_sprite(sprite_string, self.new_enemy)
        

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

    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

        elif key == arcade.key.SPACE:
            self.player_sprite.attack = True
      
    
    def on_key_release(self, key, modifiers):

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0


    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def on_update(self, delta_time: float = 1 / 60):

        self.physics_engine.update()
        for i in self.enemy_physics_engines:
            i.update()

        self.player_sprite.update_animation()
        
        for enemies in self.enemy_sprite_list:
            enemies.update_enemy_movement()
            enemies.update_enemy_animation()


        
        collision_list = arcade.check_for_collision_with_lists(self.player_sprite,[self.scene["enemy_1"], self.scene["enemy_2"]])

        # If player collides with enemy sprite.
        for collision in collision_list:

            if self.scene["enemy_1"] in collision.sprite_lists:

                # If the enemy hits the player the player health is decreased.
                self.enemy_sprite_list[0].state = "attack"
                if self.enemy_sprite_list[0].get_attack() == True:
                    self.player_sprite.if_hit = True
                    self.counter += 1
                    if self.counter > 10:
                        self.counter = 0
                        self.player_sprite.health -= 1

                if self.player_sprite.attack == True:
                    self.enemy_sprite_list[0].enemy_health -= 1
                    arcade.play_sound(self.player_hit)

            
            elif self.scene["enemy_2"] in collision.sprite_lists:

                self.enemy_sprite_list[1].state = "attack"
                if self.enemy_sprite_list[1].get_attack() == True:
                    self.player_sprite.if_hit = True
                    self.counter += 1
                    if self.counter > 10:
                        self.counter = 0
                        self.player_sprite.health -= 1

                if self.player_sprite.attack == True:
                    self.enemy_sprite_list[1].enemy_health -= 1
                    arcade.play_sound(self.player_hit)

            
        
def main():
    """Main function"""
    Window = MyGame()
    Window.setup()
    arcade.run()


if __name__ == "__main__":
    main()