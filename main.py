import os
import random
import arcade

# Constants
GRAVITY = 1
PLAYER_SPEED = 1
PLAYER_JUMP = 1
SCREEN_WIDTH = 1
SCREEN_HEIGHT = 1
LAYER_NAME_PLATFORMS = "Platforms"
LAYER_NAME_ITEMS = "Items"
LAYER_NAME_FOREGROUND = "Foreground"
LAYER_NAME_BACKGROUND = "Background"
LAYER_NAME_LAVA = "LAVA"
TILE_SCALING = 1
PLAYER_START_X = 1
PLAYER_START_Y = 1
CHARACTER_SCALING = 1



class game(arcade.Window):

    def __init__(self):

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.scene = None

        self.tile_map = None

        self.player_sprite = None

        self.physics_engine = None

        self.camera = None

        self.level = 1

        self.end_of_map = 0


    def setup(self):

        dir_path = os.path.dirname(os.path.realpath(__file__))
        map_name = f"/maps/map_level_{self.level}.tmx"

        layer_options = {
                LAYER_NAME_PLATFORMS: {
                    "use_spatial_hash": True,
                },
                LAYER_NAME_ITEMS: {
                    "use_spatial_hash": True,
                },
                LAYER_NAME_LAVA: {
                    "use_spatial_hash": True,
                },
            }
        
        self.scene.add_sprite_list_after("Player", LAYER_NAME_FOREGROUND)
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
                self.player_sprite,
                gravity_constant=GRAVITY,
                walls=self.scene[LAYER_NAME_PLATFORMS],
            )
        
        image_source = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.scene.add_sprite("Player", self.player_sprite)


    def on_key_press(self, key, modifiers):

            if key == arcade.key.UP or key == arcade.key.W:
                if self.physics_engine.can_jump():
                    self.player_sprite.change_y = PLAYER_SPEED
                    arcade.play_sound(self.jump_sound)
            elif key == arcade.key.LEFT or key == arcade.key.A:
                self.player_sprite.change_x = -PLAYER_SPEED
            elif key == arcade.key.RIGHT or key == arcade.key.D:
                self.player_sprite.change_x = PLAYER_SPEED
                

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Activate the game camera
        self.camera.use()

        # Draw our Scene
        self.scene.draw()

        # Activate the GUI camera before drawing GUI elements
        self.gui_camera.use()

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.WHITE,
            18,
        )