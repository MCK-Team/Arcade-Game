import arcade
import arcade.gui
import random
import math
from cat import Cat
from enemy import Rat

WIDTH = 1920
HEIGHT = 1080


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
        self.bullet_list = None
        self.wall_list = None
        self.texture_list = None

        self.scene = None
        self.camera = None
        self.tile_map = None
        self.physics_engine = None
        self.wall = None

        self.screen_center_x = None
        self.screen_center_y = None

    def setup(self):
        self.camera = arcade.Camera(WIDTH, HEIGHT)

        self.cat = Cat()
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        for i in range(100):
            rat = Rat()
            rat.center_x = random.randrange(0, 10000)
            rat.center_y = 60
            patrol_distance = random.randint(200, 750)
            rand = random.randint(0, patrol_distance)
            rat.boundary_left = rat.center_x - (patrol_distance - rand)
            rat.boundary_right = rat.center_x + rand
            self.enemy_list.append(rat)

        self.cat.center_x = 300
        self.cat.center_y = 300

        self.scene = arcade.Scene()
        self.scene.add_sprite("Cat", self.cat)
        self.scene.add_sprite_list("Rats", sprite_list=self.enemy_list)
        self.scene.add_sprite_list("Bullets", sprite_list=self.bullet_list)
        self.scene.add_sprite_list("Bullets_Rats", sprite_list=arcade.SpriteList())

        for x in range(0, 15000, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", 0.5)
            wall.center_x = x
            wall.center_y = 0
            self.wall_list.append(wall)

            if x % (64 * random.randint(1, 10)) == 0:
                wall_2 = arcade.Sprite(":resources:images/tiles/grassMid.png", 0.5)
                wall_2.center_x = x
                wall_2.center_y = random.randrange(128, 512, 32)
                self.wall_list.append(wall_2)

        self.scene.add_sprite_list("Walls", use_spatial_hash=True, sprite_list=self.wall_list)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.cat,
            walls=self.scene["Walls"],
            gravity_constant=0.5
        )
        self.texture_list = []
        for i in list(range(2)):
            self.texture_list.append(arcade.load_texture(f"assets/sword/SwordAn{i+1}.png", x=0, y=0, width=128, height=64))

    def on_draw(self):
        arcade.start_render()
        self.camera.use()
        self.scene.draw()
        self.cat.draw_health_bar(self.cat.center_x - 450, self.cat.center_y + 330)
        for rat in self.scene["Rats"]:
            rat.draw_health_bar(rat.center_x, rat.center_y)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            bullet = arcade.Sprite(texture=self.texture_list[0], scale=1.25)

            bullet.bullet_life = 5
            bullet.frame = random.randint(0, 4)

            radians = math.atan2((self.screen_center_y + y) - self.cat.center_y, (self.screen_center_x + x) - self.cat.center_x)
            speed = 40

            bullet.center_x = self.cat.center_x + math.cos(radians) * 50
            bullet.center_y = self.cat.center_y + math.sin(radians) * 50

            bullet.change_x = math.cos(radians) * speed
            bullet.change_y = math.sin(radians) * speed
            bullet.radians = radians

            self.scene.add_sprite("Bullets", bullet)

    def on_key_press(self, key, modifiers):
        if (key == arcade.key.RIGHT or key == arcade.key.D) and self.cat.cur_health > 0:
            self.cat.change_x = 8
        elif (key == arcade.key.LEFT or key == arcade.key.A) and self.cat.cur_health > 0:
            self.cat.change_x = -8
        elif (key == arcade.key.SPACE or key == arcade.key.W) and self.cat.cur_health > 0:
            if self.physics_engine.can_jump():
                self.cat.change_y = 12
                # Todo: use enable_multi_jump(2) for double jump. Don't forget to increment_jump_counter() here also.

        elif key == arcade.key.E and self.cat.cur_health > 0:

            number_of_bullets = 50
            angles = [i * 2*math.pi/number_of_bullets for i in range(number_of_bullets)]   # angle is in radians
            speed = 20

            for angle in angles:
                bullet = arcade.Sprite(texture=self.texture_list[0], scale=1)

                bullet.frame = random.randint(0, 4)
                bullet.bullet_life = 5

                bullet.center_x = self.cat.center_x + math.cos(angle) * 50
                bullet.center_y = self.cat.center_y + math.sin(angle) * 50

                bullet.change_x = math.cos(angle) * speed
                bullet.change_y = math.sin(angle) * speed
                bullet.radians = angle

                self.scene.add_sprite("Bullets", bullet)

        # FOR TESTING REMOVE LATER
        elif key == arcade.key.R:
            self.setup()
        elif key == arcade.key.ESCAPE:
            arcade.exit()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.cat.change_x = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.cat.change_x = 0

    def center_camera_to_cat(self):
        self.screen_center_x = self.cat.center_x - (WIDTH / 2)
        self.screen_center_y = self.cat.center_y - (HEIGHT / 2)

        camera_center = self.screen_center_x, self.screen_center_y
        self.camera.move_to(camera_center)

    def on_update(self, delta_time):
        print(delta_time)
        self.physics_engine.update()
        self.center_camera_to_cat()
        self.scene["Rats"].update_animation()
        # self.enemy_list.update()
        self.scene.update()

        for rat in self.enemy_list:
            if rat.cooldown_timer <= 0:
                rat.cooldown_timer = rat.cooldown_time
                bullet_rats = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", scale=1)

                bullet_rats.bullet_life = 4

                radians = math.atan2(self.cat.center_y - rat.center_y, self.cat.center_x - rat.center_x)
                speed = 5

                bullet_rats.center_x = rat.center_x + math.cos(radians) * 50
                bullet_rats.center_y = rat.center_y + math.sin(radians) * 50

                aim_variability = (random.random() - 0.5) * 0.2
                bullet_rats.change_x = math.cos(radians + aim_variability) * speed
                bullet_rats.change_y = math.sin(radians + aim_variability) * speed
                bullet_rats.radians = radians

                self.scene.add_sprite("Bullets_Rats", bullet_rats)
            else:
                rat.cooldown_timer -= delta_time

            if rat.center_x < rat.boundary_left:
                rat.change_x *= -1
            elif rat.center_x > rat.boundary_right:
                rat.change_x *= -1

        cat_rat_bullet_collisions = arcade.check_for_collision_with_list(self.cat, self.scene["Bullets_Rats"])
        if self.cat.cur_health <= 0:
            self.cat.change_x = 0
            self.cat.death_animation(delta_time)
        elif cat_rat_bullet_collisions:
            for bullet in cat_rat_bullet_collisions:
                bullet.remove_from_sprite_lists()
            if self.cat.cur_health > 0:
                self.cat.cur_health -= 1  # RAT DAMAGE
                self.cat.hurt_animation(delta_time)  # hurt animation
                if self.cat.cur_health <= 0:
                    self.cat.current_animation_counter = 0
        elif arcade.check_for_collision_with_list(self.cat, self.enemy_list):
            if self.cat.cur_health > 0:
                self.cat.cur_health -= 1  # RAT DAMAGE
                self.cat.hurt_animation(delta_time)  # hurt animation
                if self.cat.cur_health <= 0:
                    self.cat.current_animation_counter = 0
        else:
            self.cat.update_animation()

        for bullet in self.scene["Bullets_Rats"]:
            bullet.bullet_life -= delta_time
            if bullet.bullet_life <= 0:
                bullet.remove_from_sprite_lists()

        for bullet in self.scene["Bullets"]:
            bullet.bullet_life -= delta_time
            if bullet.alpha > 0:
                bullet.alpha -= 1
            if bullet.frame == 1:
                bullet.frame = 0
            else:
                bullet.frame = 1
            bullet.texture = self.texture_list[bullet.frame]

            if bullet.bullet_life <= 0:
                bullet.remove_from_sprite_lists()
            collisions = arcade.check_for_collision_with_list(bullet, self.scene["Rats"])
            for collision in collisions:
                if collision.cur_health >= 0:
                    collision.cur_health -= 20
                else:
                    collision.remove_from_sprite_lists()



def main():
    window = arcade.Window(WIDTH, HEIGHT, "Arcade Game")
    start_view = MenuView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
