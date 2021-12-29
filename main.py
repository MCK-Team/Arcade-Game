import arcade
import arcade.gui
import random
from cat import Cat
from enemy import Rat

WIDTH = 1280
HEIGHT = 720


class MenuView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.ALMOND)

        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text('Menu Screen', self.window.width / 2, self.window.height / 2, arcade.color.BLACK, font_size=40, anchor_x='center')

        arcade.draw_text('Click to begin', self.window.width / 2, self.window.height / 2-75, arcade.color.BLACK, font_size=20, anchor_x='center')

    def on_mouse_press(self, x, y, button, modifiers):
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.COAL)

        self.cat = None
        self.enemy_list = None

        self.scene = None
        self.camera = None
        self.tile_map = None
        self.physics_engine = None
        self.wall = None

    def setup(self):
        self.camera = arcade.Camera(WIDTH, HEIGHT)

        self.cat = Cat()

        self.enemy_list = arcade.SpriteList()
        for i in range(100):
            rat = Rat()
            rat.center_x = random.randrange(0, 10000)
            rat.center_y = 60
            self.enemy_list.append(rat)

        self.cat.center_x = 300
        self.cat.center_y = 300
        self.scene = arcade.Scene()
        self.scene.add_sprite("cat", self.cat)

        self.scene.add_sprite_list("rat", self.enemy_list)

        for x in range(0, 15000, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", 0.5)
            wall.center_x = x
            wall.center_y = 0
            self.scene.add_sprite("Walls", wall)

            if x % (64 * random.randint(1, 10)) == 0:
                wall_2 = arcade.Sprite(":resources:images/tiles/grassMid.png", 0.5)
                wall_2.center_x = x
                wall_2.center_y = random.randrange(64, 512, 64)
                self.scene.add_sprite("Walls", wall_2)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.cat,
            walls=self.scene["Walls"],
            gravity_constant=0.5
        )

    def on_draw(self):
        arcade.start_render()
        self.camera.use()
        self.scene.draw()
        self.enemy_list.draw()
        self.cat.draw_health_bar(self.cat.center_x - 450, self.cat.center_y + 330)

    def on_key_press(self, key, modifiers):

        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.cat.change_x = 12
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.cat.change_x = -12
        elif key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.cat.change_y = 15
                # Todo: Use enable_multi_jump(2) for double jump. Don't forget to increment_jump_counter() here also.
        elif key == arcade.key.K:
            if self.cat.cur_health > 0:
                self.cat.cur_health -= 5

    def on_key_release(self, key, modifiers):
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.cat.change_x = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.cat.change_x = 0

    def center_camera_to_cat(self):
        screen_center_x = self.cat.center_x - (WIDTH / 2)
        screen_center_y = self.cat.center_y - (HEIGHT / 2)

        camera_center = screen_center_x, screen_center_y
        self.camera.move_to(camera_center)

    def on_update(self, delta_time):
        self.physics_engine.update()
        self.center_camera_to_cat()
        self.cat.update_animation()


def main():
    window = arcade.Window(WIDTH, HEIGHT, "Arcade Game")
    start_view = MenuView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
