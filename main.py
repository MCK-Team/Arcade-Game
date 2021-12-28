import arcade
import random
from cat import Cat


class GameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.set_location(400, 200)

        arcade.set_background_color(arcade.color.COAL)

        self.cat = None
        self.scene = None
        self.camera = None
        self.tile_map = None
        self.physics_engine = None
        self.wall = None

        self.tile_map = arcade.load_tilemap(":resources:tiled_maps/map_with_ladders.json", 1.0)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

    def setup(self):
        self.camera = arcade.Camera(self.width, self.height)

        self.cat = Cat()

        self.cat.center_x = 300
        self.cat.center_y = 800
        self.scene = arcade.Scene()
        self.scene.add_sprite("cat", self.cat)

        for x in range(0, 1500, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", 0.5)
            wall.center_x = x
            wall.center_y = 32
            self.scene.add_sprite("Walls", wall)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.cat,
            walls=self.scene["Walls"],
            gravity_constant=0.5
        )

    def on_draw(self):
        arcade.start_render()
        self.camera.use()
        self.scene.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.cat.change_x = 12
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.cat.change_x = -12
        if key == arcade.key.UP or key == arcade.key.W:
            self.cat.change_y = 5

    def on_key_release(self, key, modifiers):
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.cat.change_x = 0
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.cat.change_x = 0

    def center_camera_to_cat(self):
        screen_center_x = self.cat.center_x - (self.width / 2)
        screen_center_y = self.cat.center_y - (self.height / 2)

        camera_center = screen_center_x, screen_center_y
        self.camera.move_to(camera_center)

    def on_update(self, delta_time):
        self.physics_engine.update()
        self.center_camera_to_cat()
        self.cat.update_animation()


def main():
    window = GameWindow(1280, 720, "Arcade Game")
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
