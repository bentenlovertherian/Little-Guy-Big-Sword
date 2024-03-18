
import arcade
import os

SCREEN_WIDTH = 1009
SCREEN_HEIGHT = 680
SCREEN_TITLE = "Little Guy Big Sword"


CHARACTER_SCALING = 2
TILE_SCALING = 1.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING
PLAYER_MOVEMENT_SPEED = 3
GRAVITY = 0.3
PLAYER_JUMP_SPEED = 8
PLAYER_START_X = 64
PLAYER_START_Y = 100


LAYER_NAME_PLATFORMS = "Platforms"

RIGHT_FACING = 0
LEFT_FACING = 1

def load_texture_pair(filename):

    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]
        

class player_sprite(arcade.Sprite):

    def __init__(self):

        super().__init__()

        self.character_face_direction = RIGHT_FACING
        self.scale = CHARACTER_SCALING

        self.idle_texture = "assets/little_guy_big-sword_0.png"
        self.idle_texture_pair = load_texture_pair(self.idle_texture)

        self.texture = self.idle_texture_pair[0]
        self.hit_box = self.texture.hit_box_points

        self.cur_texture = 0

        path = "./assets/little_guy_big-sword"

        
        self.fall_textures = []
        texture = load_texture_pair(f"{path}_slash_0.png")
        self.fall_textures.append(texture)
        texture = load_texture_pair(f"{path}_slash_1.png")
        self.fall_textures.append(texture)
        
        self.walk_textures = []
        for i in range(2):
            texture = load_texture_pair(f"{path}_{i}.png")
            self.walk_textures.append(texture)
            texture = load_texture_pair(f"{path}_{i}.png")
            self.walk_textures.append(texture)
            texture = load_texture_pair(f"{path}_{i}.png")
            self.walk_textures.append(texture)
            texture = load_texture_pair(f"{path}_{i}.png")
            self.walk_textures.append(texture)
            texture = load_texture_pair(f"{path}_{i}.png")
            self.walk_textures.append(texture)
        

    def update_animation(self, delta_time: float = 1 / 60):
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        if self.change_y < 0 and self.change_y > -1:
            self.texture = self.fall_textures[1][self.character_face_direction]
            return
        
        if self.change_y < 0:
            self.texture = self.fall_textures[0][self.character_face_direction]
            return
    
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return
        
        if self.change_x > 0 or self.change_x < 0:
            self.cur_texture += 1
            if self.cur_texture > 9:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]
                
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

        self.physics_engine = None

        self.camera = None

        self.gui_camera = None

        self.end_of_map = 0

        self.character_face_direction = RIGHT_FACING
        self.left_pressed = False
        self.right_pressed = False


    def setup(self):


        self.camera = arcade.Camera(self.width, self.height)

        self.gui_camera = arcade.Camera(self.width, self.height)


        #map_name = f":resources:tiled_maps/map2_level_{self.level}.json"
        map_name = "maps/map1.tmx"



        layer_options = {LAYER_NAME_PLATFORMS: {"use_spatial_hash": True,},}

        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        self.scene = arcade.Scene.from_tilemap(self.tile_map)


        #image_source = "assets/little_guy_big-sword_0.png"
        #self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite = player_sprite()
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.scene.add_sprite("Player", self.player_sprite)


        self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE

    
        if self.tile_map.background_color:

            arcade.set_background_color(self.tile_map.background_color)


        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            gravity_constant=GRAVITY,
            walls=self.scene[LAYER_NAME_PLATFORMS],
        )

    def on_draw(self):

        self.clear()

        self.camera.use()

        self.scene.draw()

        self.gui_camera.use()

    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

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

    def on_update(self, delta_time):

        self.physics_engine.update()
        self.player_sprite.update_animation()

def main():
    """Main function"""
    Window = MyGame()
    Window.setup()
    arcade.run()


if __name__ == "__main__":
    main()