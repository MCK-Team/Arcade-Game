import arcade
import arcade.gui
import random
import math
from cat import Cat
from enemy import Rat, StormHead, NightBorne

WIDTH = 1920
HEIGHT = 1080
SCORE = 0
SKILLS = ["AOE", "BLOCK"]
WAVE = 0


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.COAL)

        self.cat = None
        self.sword = None
        self.stormhead = None
        self.nightborne = None
        self.enemy_list = None
        self.bullet_list = None
        self.wall_list = None
        self.texture_list = None
        self.ground_list = None
        self.waze_size = None

        self.scene = None
        self.camera = None
        self.camera_gui = None
        self.tile_map = None
        self.physics_engine = None
        self.wall = None
        self.change_screen_timer = None

        self.screen_center_x = None
        self.screen_center_y = None

    def setup(self):
        self.camera = arcade.Camera(WIDTH, HEIGHT)
        self.camera_gui = arcade.Camera(WIDTH, HEIGHT)
        self.change_screen_timer = 3

        self.waze_size = 0

        self.cat = Cat()
        self.stormhead = StormHead()
        self.nightborne = NightBorne()
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(is_static=True)
        self.ground_list = arcade.SpriteList(is_static=True)
        self.tile_map = arcade.load_tilemap("assets/map/Map1.json", scaling=5, use_spatial_hash=True)

        # PLAYER POSITION
        self.cat.center_x = 300
        self.cat.center_y = 1300

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.scene.add_sprite("StormHead", self.stormhead)
        self.scene.add_sprite("NightBorne", self.nightborne)
        self.scene.add_sprite_list("Enemies", sprite_list=self.enemy_list)
        self.scene.add_sprite("Cat", self.cat)
        self.scene.add_sprite_list("Bullets", sprite_list=self.bullet_list)
        self.scene.add_sprite_list("Bullets_Rats", sprite_list=arcade.SpriteList())

        if "BLOCK" in SKILLS:
            self.sword = arcade.Sprite("assets/sword/Sword1.png", scale=2)
            self.sword.center_x = self.cat.center_x
            self.sword.center_y = self.cat.center_y + 15
            self.sword.block_timer = 0
            self.sword.block_time = 10
            self.scene.add_sprite("Sword", self.sword)

        arcade.set_background_color((212, 240, 246))  # D4F0F6

        # for x in range(0, 15000, 64):
        #     wall = arcade.Sprite(":resources:images/tiles/grassMid.png", 0.5)
        #     wall.center_x = x
        #     wall.center_y = 0
        #     self.wall_list.append(wall)
        #
        #     for i in range(10):
        #         ground = arcade.Sprite(":resources:images/tiles/grassCenter.png", 0.5)
        #         ground.center_x = x
        #         ground.center_y = 64 * (-i - 1)
        #         self.ground_list.append(ground)
        #
        #     if x % (64 * random.randint(1, 10)) == 0:
        #         wall_2 = arcade.Sprite(":resources:images/tiles/dirtHalf.png", 1)
        #         wall_2.center_x = x
        #         wall_2.center_y = random.randrange(128, 512, 64)
        #         self.wall_list.append(wall_2)
        #
        # self.scene.add_sprite_list("Walls", use_spatial_hash=True, sprite_list=self.wall_list)
        # self.scene.add_sprite_list("Ground", use_spatial_hash=True, sprite_list=self.ground_list)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.cat,
            walls=self.scene["Block you can touch"],
            gravity_constant=0.5
        )

        self.physics_engine.enable_multi_jump(5)

        self.texture_list = []
        for i in list(range(2)):
            self.texture_list.append(arcade.load_texture(f"assets/sword/SwordAn{i + 1}.png", x=0, y=0, width=128, height=64))

    def on_draw(self):
        arcade.start_render()
        self.camera.use()
        self.scene.draw()
        self.scene["NightBorne"].draw_hit_boxes(color=arcade.color.RED, line_thickness=10)

        for rat in self.scene["Enemies"]:
            rat.draw_health_bar(rat.center_x, rat.center_y)  # TODO: The rectangles within here redraw from scratch which causes severe frame rate loss when > 10-20 health bars show.

        self.stormhead.draw_health_bar(self.stormhead.center_x, self.stormhead.center_y)

        self.nightborne.draw_health_bar(self.nightborne.center_x, self.nightborne.center_y)

        self.camera_gui.use()
        self.cat.draw_health_bar(WIDTH / 2, HEIGHT - 50)

        score = f"Score: {SCORE}"
        arcade.draw_text(score, WIDTH / 4, HEIGHT - 60, color=arcade.color.BLACK, font_size=20, font_name="Kenney Future")

        wave = f"Wave: {WAVE}"
        arcade.draw_text(wave, WIDTH - 650, HEIGHT - 60, color=arcade.color.BLACK, font_size=20, font_name="Kenney Future")

        number_of_enemies = len(self.scene["Enemies"])
        enemies = f"Enemies Left: {number_of_enemies}"
        arcade.draw_text(enemies, WIDTH - 650, HEIGHT - 100, color=arcade.color.BLACK, font_size=20, font_name="Kenney Future")

    def on_mouse_press(self, x, y, button, modifiers):
        radians = math.atan2((self.screen_center_y + y) - self.cat.center_y, (self.screen_center_x + x) - self.cat.center_x)

        if button == arcade.MOUSE_BUTTON_LEFT and self.cat.cur_health > 0:
            bullet = arcade.Sprite(texture=self.texture_list[0], scale=1.25)

            bullet.bullet_life = 1
            bullet.frame = random.randint(0, 4)

            speed = 40

            bullet.center_x = self.cat.center_x + math.cos(radians) * 50
            bullet.center_y = self.cat.center_y + math.sin(radians) * 50

            bullet.change_x = math.cos(radians) * speed
            bullet.change_y = math.sin(radians) * speed
            bullet.radians = radians

            self.scene.add_sprite("Bullets", bullet)

        if button == arcade.MOUSE_BUTTON_RIGHT and self.cat.cur_health > 0 and "BLOCK" in SKILLS:
            self.sword.block_timer = self.sword.block_time
            self.sword.block_radians = radians + math.pi

    def on_key_press(self, key, modifiers):
        if (key == arcade.key.RIGHT or key == arcade.key.D) and self.cat.cur_health > 0:
            self.cat.change_x = 8
        elif (key == arcade.key.LEFT or key == arcade.key.A) and self.cat.cur_health > 0:
            self.cat.change_x = -8
        elif (key == arcade.key.SPACE or key == arcade.key.W) and self.cat.cur_health > 0:
            if self.physics_engine.can_jump():
                self.cat.change_y = 12
                self.physics_engine.increment_jump_counter()

        elif key == arcade.key.E and self.cat.cur_health > 0 and "AOE" in SKILLS:

            number_of_bullets = 50
            angles = [(i + random.random()) * 2 * math.pi / number_of_bullets for i in range(number_of_bullets)]  # angle is in radians
            speed = 20

            for angle in angles:
                bullet = arcade.Sprite(texture=self.texture_list[0], scale=1)

                bullet.frame = random.randint(0, 4)
                bullet.bullet_life = 0.5

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

        camera_center = self.screen_center_x, self.screen_center_y  # TODO: consider not centering the cat; camera leads with cat's movement.
        self.camera.move_to(camera_center)

    def on_update(self, delta_time):
        self.physics_engine.update()
        self.center_camera_to_cat()
        self.scene["Enemies"].update_animation()
        self.scene["StormHead"].update_animation()
        self.scene["NightBorne"].update_animation()
        #self.scene["NightBorne"].update_hitbox()
        #self.scene["NightBorne"].draw_hit_boxes(color=arcade.color.RED, line_thickness=10)
        self.scene.update()
        if len(self.scene["NightBorne"]) > 0:
            self.scene["NightBorne"][0].update_sprite(self.cat.center_x, self.cat.center_y)

        if len(self.scene["Enemies"]) == 0:
            global WAVE
            WAVE += 1
            self.waze_size += 10
            for i in range(self.waze_size + 500):
                rat = Rat()
                rat.center_x = random.randrange(2000, 6500)
                rat.center_y = 505
                patrol_distance = random.randint(200, 750)  # TODO: Refactor patrol distance and boundaries into enemy class
                rand = random.randint(0, patrol_distance)
                rat.boundary_left = rat.center_x - (patrol_distance - rand)
                rat.boundary_right = rat.center_x + rand
                self.scene["Enemies"].append(rat)

                self.stormhead.center_x = 7000
                self.stormhead.center_y = 596

                self.nightborne.center_x = 6500
                self.nightborne.center_y = 560
                self.nightborne.boundary_left = self.nightborne.center_x - (patrol_distance - rand)
                self.nightborne.boundary_right = self.nightborne.center_x + rand

                rand = random.randint(0, patrol_distance)
                self.stormhead.boundary_left = self.stormhead.center_x - (patrol_distance - rand)
                self.stormhead.boundary_right = self.stormhead.center_x + rand
            self.scene["Enemies"].enable_spatial_hashing()
        sword_direction = 1 if self.cat.direction == 0 else -1

        if "BLOCK" in SKILLS:
            if self.sword.block_timer > 0:
                self.sword.block_x = self.cat.center_x + math.cos(self.sword.block_radians + math.pi) * 100
                self.sword.block_y = self.cat.center_y - 24 + math.sin(self.sword.block_radians + math.pi) * 100
                self.sword.change_x = (self.sword.block_x - self.sword.center_x) / 2
                self.sword.change_y = (self.sword.block_y - self.sword.center_y) / 2
                self.sword.radians = self.sword.block_radians + math.pi / 2
                self.sword.block_timer -= delta_time
            else:
                self.sword.change_x = ((self.cat.center_x - 50 * sword_direction) - self.sword.center_x) / 10
                self.sword.change_y = ((self.cat.center_y + 15) - self.sword.center_y) / 10
                self.sword.radians = math.atan2(self.sword.change_y, self.sword.change_x) + math.pi

            sword_block_collisions = arcade.check_for_collision_with_list(self.sword, self.scene["Bullets_Rats"])
            for collision in sword_block_collisions:
                collision.remove_from_sprite_lists()

        for rat in self.scene["Enemies"]:

            x_dist = self.cat.center_x - rat.center_x
            y_dist = self.cat.center_y - rat.center_y
            rat.current_distance = pow(x_dist * x_dist + y_dist * y_dist, 0.5)

            if rat.cooldown_timer <= 0 and rat.current_distance < rat.attack_distance:
                rat.cooldown_timer = rat.cooldown_time
                bullet_rats = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", scale=1)

                bullet_rats.bullet_life = 4

                radians = math.atan2(self.cat.center_y - rat.center_y, self.cat.center_x - rat.center_x)
                speed = 10

                bullet_rats.center_x = rat.center_x + math.cos(radians) * 50
                bullet_rats.center_y = rat.center_y + math.sin(radians) * 50

                aim_variability = (random.random() - 0.5) * 0.05
                bullet_rats.change_x = math.cos(radians + aim_variability) * speed
                bullet_rats.change_y = math.sin(radians + aim_variability) * speed
                bullet_rats.radians = radians

                self.scene.add_sprite("Bullets_Rats", bullet_rats)
            else:
                rat.cooldown_timer -= delta_time

            # TODO: Refactor this into the enemy class's update method.
            if rat.center_x < rat.boundary_left:
                rat.change_x *= -1
            elif rat.center_x > rat.boundary_right:
                rat.change_x *= -1

        # if self.nightborne.center_x < self.nightborne.boundary_left:
        #     self.nightborne.change_x *= -1
        # elif self.nightborne.center_x > self.nightborne.boundary_right:
        #     self.nightborne.change_x *= -1

        # Blocking sword damages rats.
        # sword_block_collisions = arcade.check_for_collision_with_list(self.sword, self.scene["Enemies"])
        # for collision in sword_block_collisions:
        #     if collision.cur_health >= 0:
        #         collision.cur_health -= 20
        #     if collision.cur_health <= 0:
        #         collision.remove_from_sprite_lists()
        #         self.score += 100

        cat_rat_bullet_collisions = arcade.check_for_collision_with_list(self.cat, self.scene["Bullets_Rats"])
        if self.cat.cur_health <= 0:
            self.cat.change_x = 0
            self.cat.death_animation(delta_time)

            # TODO: Uncomment after debugging
            # for _ in range(4):
            #     if self.change_screen_timer > 0:
            #         self.change_screen_timer -= 1 / (60 * 3)
            #     else:
            #         view = ShopView()
            #         self.window.show_view(view)
        elif cat_rat_bullet_collisions:
            for bullet in cat_rat_bullet_collisions:
                bullet.remove_from_sprite_lists()
            if self.cat.cur_health > 0:
                self.cat.cur_health -= 1  # RAT DAMAGE
                self.cat.hurt_animation(delta_time)  # hurt animation
                if self.cat.cur_health <= 0:
                    self.cat.current_animation_counter = 0
        elif arcade.check_for_collision_with_list(self.cat, self.scene["Enemies"]):
            if self.cat.cur_health > 0:
                self.cat.cur_health -= rat.damage  # RAT DAMAGE
                self.cat.hurt_animation(delta_time)  # hurt animation
                if self.cat.cur_health <= 0:
                    self.cat.current_animation_counter = 0
        elif arcade.check_for_collision_with_list(self.cat, self.scene["NightBorne"]):
            if self.cat.cur_health > 0:
                self.cat.cur_health -= self.scene["NightBorne"][0].damage
                self.cat.hurt_animation(delta_time)  # hurt animation
                if self.cat.cur_health <= 0:
                    self.cat.current_animation_counter = 0
        else:
            self.cat.update_animation()


        for bullet in self.scene["Bullets_Rats"]:
            bullet.bullet_life -= delta_time
            if bullet.bullet_life <= 0:
                bullet.remove_from_sprite_lists()

        # TODO: Update comment if this is not longer true: Damage from cat is handled only through bullets/swords
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
            collisions = arcade.check_for_collision_with_lists(bullet, [self.scene["Enemies"], self.scene["NightBorne"]])
            for collision in collisions:
                collision.show_health_timer = collision.show_health_time
                if collision.cur_health >= 0:
                    collision.cur_health -= 20
                if collision.cur_health <= 0:
                    collision.remove_from_sprite_lists()
                    global SCORE
                    SCORE += 100


class ShopView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.v_box = arcade.gui.UIBoxLayout()
        self.background = []
        for i in range(7):
            self.background.append(arcade.load_texture(f"assets/background/noonbackground{i + 1}.png", x=0, y=0, width=1024, height=768))
        self.texture = self.background[0]

        title_text = arcade.gui.UITextArea(text="Welcome to the shop!", width=600, height=50, font_size=20, font_name="Kenney Future")
        self.v_box.add(title_text.with_space_around(bottom=5))

        abilities = """
                Choose An ability you wish to Purchase:
                 
                500 Points for Radial Attack: 'E'
                1000 Points for Protective Sword """

        ability_text = arcade.gui.UITextArea(text=abilities, width=500, height=140, font_size=14, font_name="Arial")
        self.v_box.add(ability_text.with_space_around(bottom=2))

        aoe = arcade.gui.UIFlatButton(text='Radial Attack', width=150)
        self.v_box.add(aoe.with_space_around(bottom=10))

        @aoe.event('on_click')
        def on_click_aoe(event):
            global SCORE
            if SCORE >= 500 and "AOE" not in SKILLS:
                SKILLS.append('AOE')
                SCORE -= 500
            elif "AOE" in SKILLS:
                print("ALREADY PURCHASED")
                purchased = arcade.gui.UITextArea(text="already purchased!", width=600, height=50, font_size=20, font_name="Kenney Future", text_color=arcade.color.RED)
                self.v_box.add(purchased.with_space_around(bottom=5))
            else:
                print("NOT ENOUGH POINTS")
                not_enough = arcade.gui.UITextArea(text="not enough points!", width=600, height=50, font_size=20, font_name="Kenney Future", text_color=arcade.color.RED)
                self.v_box.add(not_enough.with_space_around(bottom=5))

        sword = arcade.gui.UIFlatButton(text='Protective Sword', width=150)
        self.v_box.add(sword.with_space_around(bottom=10))

        @sword.event('on_click')
        def on_click_sword(event):
            global SCORE
            if SCORE >= 1000 and "BLOCK" not in SKILLS:
                SKILLS.append('BLOCK')
                SCORE -= 1000
            elif "BLOCK" in SKILLS:
                print("ALREADY PURCHASED")
                purchased = arcade.gui.UITextArea(text="Already purchased!", width=600, height=50, font_size=20, font_name="Kenney Future", text_color=arcade.color.RED)
                self.v_box.add(purchased.with_space_around(bottom=5))
            else:
                print("NOT ENOUGH POINTS")
                not_enough = arcade.gui.UITextArea(text="Not enough points!", width=600, height=50, font_size=20, font_name="Kenney Future", text_color=arcade.color.RED)
                self.v_box.add(not_enough.with_space_around(bottom=5))

        play_again = arcade.gui.UIFlatButton(text="Play Again", width=150)
        self.v_box.add(play_again.with_space_around(top=50, bottom=10))

        @play_again.event('on_click')
        def on_click_start(event):
            self.manager.disable()
            game_view = GameView()
            self.window.show_view(game_view)
            game_view.setup()

        self.manager.add(
            arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", child=self.v_box))

    def on_show(self):
        arcade.set_background_color(arcade.color.AMETHYST)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        arcade.start_render()
        self.manager.draw()
        score = f"Score: {SCORE}"
        arcade.draw_text(score, WIDTH / 4, HEIGHT - 60, color=arcade.color.BLACK, font_size=20, font_name="Kenney Future")


def main():
    from menu import MenuView
    window = arcade.Window(WIDTH, HEIGHT, "Arcade Game", vsync=True, antialiasing=False)
    start_view = MenuView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
