import arcade
import arcade.gui
import random
import math

from pyglet.gl.gl import GL_NEAREST
from cat import Cat
from Enemies.rat import Rat
from Enemies.stormhead import StormHead
from Enemies.nightborne import NightBorne
from Enemies.excutioner import Executioner
import global_variables

WIDTH = 1920
HEIGHT = 1080
SKILLS = []
WAVE = 0


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.COAL)


        self.mouse_x = None
        self.mouse_y = None

        self.cat = None
        self.sword = None
        self.rat_list = None
        self.bullet_list = None
        self.wall_list = None
        self.texture_list = None
        self.ground_list = None
        self.wave_size = None
        self.cursor_texture = None

        self.aoe_cooldown_time = 0.2
        self.aoe_cooldown_timer = None

        self.scene = None
        self.camera = None
        self.camera_gui = None
        self.camera_shake_cooldown_time = None
        self.camera_shake_cooldown_timer = None
        self.tile_map = None
        self.physics_engine = None
        self.wall = None
        self.change_screen_timer = None

        self.screen_center_x = None
        self.screen_center_y = None
        self.center_x_last_cycle = None # For parallax

    def setup(self):
        self.camera = arcade.Camera(WIDTH, HEIGHT)
        self.camera_gui = arcade.Camera(WIDTH, HEIGHT)
        self.camera_shake_cooldown_time = 0.2
        self.camera_shake_cooldown_timer = 0
        self.change_screen_timer = 3
        self.mouse_x = 0
        self.mouse_y = 0

        self.wave_size = 0

        # TODO: Uncomment to reset waves to start after dying.
        # global WAVE
        # WAVE = 0

        self.aoe_cooldown_timer = 0

        self.cursor_texture = arcade.load_texture(file_name="assets/crosshair159dark.png", x=0, y=0, width=128, height=128, hit_box_algorithm="None")

        self.cat = Cat()
        self.bullet_list = arcade.SpriteList()
        self.rat_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(is_static=True)
        self.ground_list = arcade.SpriteList(is_static=True)
        self.tile_map = arcade.load_tilemap("assets/map/Map1.json", scaling=5, use_spatial_hash=True)

        # PLAYER POSITION
        self.cat.center_x = 1000
        self.cat.center_y = 1300

        self.center_x_last_cycle = self.cat.center_x

        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.scene.add_sprite_list("Rats", sprite_list=self.rat_list)
        self.scene.add_sprite_list("NightBorne", arcade.SpriteList())
        self.scene.add_sprite_list("StormHead", arcade.SpriteList())
        self.scene.add_sprite_list("Executioner", arcade.SpriteList())
        self.scene.add_sprite("Cat", self.cat)
        self.scene.add_sprite_list("Bullets", sprite_list=self.bullet_list)
        self.scene.add_sprite_list("Bullets_Rats", sprite_list=arcade.SpriteList())

        # Procedural generation.
        procedural_scale = 4
        for x in range(0, 5000, 48*procedural_scale):
            for y in range(1000, 5000, 48*procedural_scale):
                if random.randint(0, 20) == 0:
                    tile_texture_number = random.randint(1, 4)
                    wall = arcade.Sprite(f"assets/map/tile{tile_texture_number}.png", scale=procedural_scale)
                    wall.center_x = x
                    wall.center_y = y
                    self.wall_list.append(wall)

        self.scene.add_sprite_list("Walls", use_spatial_hash=True, sprite_list=self.wall_list)

        if "BLOCK" in SKILLS:
            self.sword = arcade.Sprite("assets/sword/Sword1.png", scale=2)
            self.sword.center_x = self.cat.center_x
            self.sword.center_y = self.cat.center_y + 15
            self.sword.block_timer = 0
            self.sword.block_time = 10
            self.scene.add_sprite("Sword", self.sword)

        arcade.set_background_color((212, 240, 246))  # D4F0F6

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.cat,
            walls=[self.scene["Block you can touch"], self.scene["Walls"]],
            gravity_constant=0.5
        )

        if "MULTIJUMP" in SKILLS:
            self.physics_engine.enable_multi_jump(5)
        else:
            self.physics_engine.enable_multi_jump(1)

        self.texture_list = []
        for i in list(range(2)):
            self.texture_list.append(arcade.load_texture(f"assets/sword/SwordAn{i + 1}.png", x=0, y=0, width=128, height=64))

    def on_draw(self):
        arcade.start_render()
        self.camera.use()
        self.scene.draw(filter=GL_NEAREST)
        # self.scene["NightBorne"].draw_hit_boxes(color=arcade.color.RED, line_thickness=10)
        self.scene["StormHead"].draw_hit_boxes(color=arcade.color.RED, line_thickness=10)

        for rat in self.scene["Rats"]:
            rat.draw_health_bar(rat.center_x, rat.center_y)  # TODO: The rectangles within here redraw from scratch which causes severe frame rate loss when > 10-20 health bars show.

        for stormhead in self.scene["StormHead"]:
            stormhead.draw_health_bar(stormhead.center_x, stormhead.center_y)

        for nightborne in self.scene["NightBorne"]:
            nightborne.draw_health_bar(nightborne.center_x, nightborne.center_y)

        for executioner in self.scene["Executioner"]:
            executioner.draw_health_bar(executioner.center_x, executioner.center_y)

        self.camera_gui.use()
        self.cat.draw_health_bar(WIDTH / 2, HEIGHT - 50)

        arcade.draw_texture_rectangle(center_x=self.mouse_x, center_y=self.mouse_y, texture=self.cursor_texture, width=64, height=64)

        score = f"Score: {global_variables.SCORE}"
        arcade.draw_text(score, WIDTH / 4, HEIGHT - 60, color=arcade.color.BLACK, font_size=20, font_name="Kenney Future")

        wave = f"Wave: {WAVE}"
        arcade.draw_text(wave, WIDTH - 650, HEIGHT - 60, color=arcade.color.BLACK, font_size=20, font_name="Kenney Future")

        number_of_enemies = len(self.scene["Rats"]) + len(self.scene["StormHead"]) + len(self.scene["NightBorne"]) + len(self.scene["Executioner"])
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

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.mouse_x = x
        self.mouse_y = y

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

            if self.aoe_cooldown_timer <= 0:
                self.aoe_cooldown_timer = self.aoe_cooldown_time
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

    def update_enemies(self, delta_time):
        if len(self.scene["StormHead"]) > 0:
            self.scene["StormHead"][0].update_sprite(self.cat.center_x, self.cat.center_y)
            for stormhead in self.scene["StormHead"]:
                stormhead.update_sprite(self.cat.center_x, self.cat.center_y)
        if len(self.scene["NightBorne"]) > 0:
            self.scene["NightBorne"][0].update_sprite(self.cat.center_x, self.cat.center_y)
            for nightborne in self.scene["NightBorne"]:
                nightborne.update_sprite(self.cat.center_x, self.cat.center_y)
        if len(self.scene["Executioner"]) > 0:
            for executioner in self.scene["Executioner"]:
                executioner.update_sprite(self.cat.center_x, self.cat.center_y)
        self.update_rats(delta_time)
        self.update_enemy_animations()

    def update_enemy_animations(self):
        self.scene["Rats"].update_animation()
        self.scene["StormHead"].update_animation()
        self.scene["NightBorne"].update_animation()
        self.scene["Executioner"].update_animation()

    def update_rats(self, delta_time):
        for rat in self.scene["Rats"]:
            x_dist = self.cat.center_x - rat.center_x
            y_dist = self.cat.center_y - rat.center_y
            rat.current_distance = pow(x_dist * x_dist + y_dist * y_dist, 0.5)

            if rat.cooldown_timer <= 0 and rat.current_distance < rat.attack_distance:
                rat.cooldown_timer = rat.cooldown_time
                bullet_rats = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", scale=1)

                bullet_rats.bullet_life = 4

                radians = math.atan2(self.cat.center_y - rat.center_y, self.cat.center_x - rat.center_x)
                speed = 5

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

    def update_cat_sword(self, delta_time):
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

    def damage_to_cat(self, delta_time):
        starting_health = self.cat.cur_health

        cat_rat_bullet_collisions = arcade.check_for_collision_with_list(self.cat, self.scene["Bullets_Rats"])
        if self.cat.cur_health <= 0:
            self.cat.change_x = 0
            self.cat.death_animation(delta_time)

            # TODO: Uncomment after debugging
            for _ in range(4):
                if self.change_screen_timer > 0:
                    self.change_screen_timer -= delta_time    # Untested, switch back to this if doesn't work: 1 / (60 * 3)
                else:
                    view = ShopView()
                    self.window.show_view(view)
                    self.window.set_mouse_visible(True)
        elif cat_rat_bullet_collisions:
            for bullet in cat_rat_bullet_collisions:
                bullet.remove_from_sprite_lists()
                self.cat.cur_health -= 1  # Damage from rat bullets
                self.cat.hurt_animation(delta_time)  # hurt animation
                if self.cat.cur_health <= 0:
                    self.cat.current_animation_counter = 0
        elif arcade.check_for_collision_with_list(self.cat, self.scene["Rats"]):
            if self.cat.cur_health > 0:
                self.cat.cur_health -= self.scene["Rats"][0].damage * delta_time * 60 # Damage from rat melee
                self.cat.hurt_animation(delta_time)  # hurt animation
                if self.cat.cur_health <= 0:
                    self.cat.current_animation_counter = 0
        elif arcade.check_for_collision_with_list(self.cat, self.scene["NightBorne"]):
            if self.cat.cur_health > 0:
                self.cat.cur_health -= self.scene["NightBorne"][0].damage * delta_time * 60
                self.cat.hurt_animation(delta_time)  # hurt animation
                if self.cat.cur_health <= 0:
                    self.cat.current_animation_counter = 0
        elif arcade.check_for_collision_with_list(self.cat, self.scene["StormHead"]):
            if self.cat.cur_health > 0:
                self.cat.cur_health -= self.scene["StormHead"][0].damage * delta_time * 60
                self.cat.hurt_animation(delta_time)  # hurt animation
                if self.cat.cur_health <= 0:
                    self.cat.current_animation_counter = 0
        elif arcade.check_for_collision_with_list(self.cat, self.scene["Executioner"]):
            if self.cat.cur_health > 0:
                self.cat.cur_health -= self.scene["Executioner"][0].damage * delta_time * 60
                self.cat.hurt_animation(delta_time)  # hurt animation
                if self.cat.cur_health <= 0:
                    self.cat.current_animation_counter = 0
        elif self.cat.cur_health > 0:
            self.cat.update_animation()

        ending_health = self.cat.cur_health

        damage_taken = starting_health - ending_health if starting_health - ending_health > 0 else 0
        if self.camera_shake_cooldown_timer > 0:
            self.camera_shake_cooldown_timer -= delta_time
        
        if damage_taken > 0 and self.camera_shake_cooldown_timer <= 0: # If damage was taken
            self.camera_shake_cooldown_timer = self.camera_shake_cooldown_time
            # Sample random shake code from documentation: https://api.arcade.academy/en/2.6.2/examples/sprite_move_scrolling_shake.html
            shake_direction = 2 * math.pi * random.random()
            shake_amplitude = 10.0
            shake_speed = 10.0
            shake_damping = 0.8
            shake_vector = math.cos(shake_direction) * shake_amplitude, math.sin(shake_direction) * shake_amplitude
            self.camera.shake(shake_vector, speed=shake_speed, damping=shake_damping)

        if self.cat.cur_health < 0:
            self.cat.cur_health = 0

    def update_enemy_projectiles(self, delta_time):
        for bullet in self.scene["Bullets_Rats"]:
            bullet.bullet_life -= delta_time
            if bullet.bullet_life <= 0:
                bullet.remove_from_sprite_lists()

    def update_cat_projectiles(self, delta_time):
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
            collisions = arcade.check_for_collision_with_lists(bullet, [self.scene["Rats"], self.scene["StormHead"], self.scene["NightBorne"], self.scene["Executioner"]])
            for collision in collisions:
                collision.show_health_timer = collision.show_health_time
                if collision.cur_health >= 0:
                    collision.cur_health -= 5
                if collision.cur_health <= 0:
                    if not isinstance(collision, NightBorne) and not isinstance(collision, StormHead) and not isinstance(collision, Executioner):
                        collision.remove_from_sprite_lists()
                        #global SCORE
                        global_variables.SCORE += collision.points

    def spawn_wave(self):
        if len(self.scene["Rats"]) == 0 and len(self.scene["StormHead"]) == 0 and len(self.scene["NightBorne"]) == 0 and len(self.scene["Executioner"]) == 0:
            global WAVE
            WAVE += 1

            if WAVE > 0:
                if WAVE > 5:
                    self.wave_size == 200
                else:
                    self.wave_size += 1 + (WAVE - 1) * (WAVE - 1) * 5
                for i in range(self.wave_size):
                    rat = Rat()
                    rat.center_x = random.randrange(2000, 6500)
                    rat.center_y = 507
                    patrol_distance = random.randint(200, 750)  # TODO: Refactor patrol distance and boundaries into enemy class
                    rand = random.randint(0, patrol_distance)
                    rat.boundary_left = rat.center_x - (patrol_distance - rand)
                    rat.boundary_right = rat.center_x + rand
                    if WAVE > 3:
                        rat.attack_distance = 2000
                    self.scene["Rats"].append(rat)
                self.scene["Rats"].enable_spatial_hashing()

            if WAVE == 5:
                    for i in range(1):
                        nightborne = NightBorne()

                        nightborne.center_x = 6500
                        nightborne.center_y = 560
                        rand = random.randint(0, patrol_distance)
                        patrol_distance = 500
                        nightborne.boundary_left = nightborne.center_x - (patrol_distance - rand) # center_x - (patrol_distance - rand)
                        nightborne.boundary_right = nightborne.center_x + rand
                    self.scene.add_sprite("NightBorne", nightborne)    # TODO: Uncomment to enable nightborne

            elif WAVE > 10:
                self.wave_size = (WAVE - 10) * (WAVE - 10)
                for i in range(self.wave_size):
                    executioner = Executioner()
                    executioner.center_x = random.randint(0, 10000)
                    executioner.center_y = random.randint(1000, 5000)
                    self.scene["Executioner"].append(executioner)
                self.scene["Executioner"].enable_spatial_hashing()

                # executioner = Executioner()
                #
                # stormhead.center_x = 700
                # stormhead.center_y = 694
                # stormhead.boundary_left = stormhead.center_x - (patrol_distance - rand)
                # stormhead.boundary_right = stormhead.center_x + rand
                #
                # nightborne.center_x = 1500
                # nightborne.center_y = 560
                # nightborne.boundary_left = nightborne.center_x - (patrol_distance - rand)
                # nightborne.boundary_right = nightborne.center_x + rand
                #
                # executioner.center_x = 1000
                # executioner.center_y = 1200
                # executioner.boundary_left = executioner.center_x - (patrol_distance - rand)
                # executioner.boundary_right = executioner.center_x + rand
                #
                # # self.scene.add_sprite("StormHead", stormhead)
                # # self.scene.add_sprite("Executioner", executioner)
                # # self.scene.add_sprite("NightBorne", nightborne)    # TODO: Uncomment to enable nightborne
    
    def update_cat_cooldowns(self, delta_time):
        if self.aoe_cooldown_timer > 0:
            self.aoe_cooldown_timer -= delta_time

    def update_parallax(self):
        movement_since_last_cycle = self.center_x_last_cycle - self.cat.center_x

        change_x_inifinity = self.cat.change_x * 0.95 if movement_since_last_cycle else 0
        self.scene["Mountains"].move(change_x=change_x_inifinity, change_y=0)
        self.scene["Moon"].move(change_x=change_x_inifinity, change_y=0)

        change_x_sand_dune = self.cat.change_x * 0.7 if movement_since_last_cycle else 0
        self.scene["Sand Dune"].move(change_x=change_x_sand_dune, change_y=0)

        change_x_clouds_crosses = self.cat.change_x * 0.7 if movement_since_last_cycle else 0
        self.scene["Clouds"].move(change_x=change_x_clouds_crosses, change_y=0)

        change_x_foreground = self.cat.change_x * -.2 if movement_since_last_cycle else 0
        self.scene["Tile Layer 5"].move(change_x=change_x_foreground, change_y=0)

        self.center_x_last_cycle = self.cat.center_x

    def utility_code(self):
        # Draw hitbox.
        # self.scene["StormHead"].update_hitbox()
        # self.scene["StormHead"].draw_hit_boxes(color=arcade.color.RED, line_thickness=10)

        # Procedural generation.
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
        pass

    def on_update(self, delta_time):
        self.physics_engine.update()
        self.center_camera_to_cat()

        self.scene.update()
        self.spawn_wave()
        self.update_enemies(delta_time)
        self.update_cat_sword(delta_time)
        self.update_cat_projectiles(delta_time)
        self.update_cat_cooldowns(delta_time)
        self.update_enemy_projectiles(delta_time)
        self.damage_to_cat(delta_time)
        self.update_parallax()

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
            if global_variables.SCORE >= 500 and "AOE" not in SKILLS:
                SKILLS.append('AOE')
                global_variables.SCORE -= 500
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
            if global_variables.SCORE >= 1000 and "BLOCK" not in SKILLS:
                SKILLS.append('BLOCK')
                global_variables.SCORE -= 1000
            elif "BLOCK" in SKILLS:
                print("ALREADY PURCHASED")
                purchased = arcade.gui.UITextArea(text="Already purchased!", width=600, height=50, font_size=20, font_name="Kenney Future", text_color=arcade.color.RED)
                self.v_box.add(purchased.with_space_around(bottom=5))
            else:
                print("NOT ENOUGH POINTS")
                not_enough = arcade.gui.UITextArea(text="Not enough points!", width=600, height=50, font_size=20, font_name="Kenney Future", text_color=arcade.color.RED)
                self.v_box.add(not_enough.with_space_around(bottom=5))

        multijump = arcade.gui.UIFlatButton(text='Multi-Jump', width=150)
        self.v_box.add(multijump.with_space_around(bottom=10))

        @multijump.event('on_click')
        def on_click_multijump(event):
            if global_variables.SCORE >= 1000 and "MULTIJUMP" not in SKILLS:
                SKILLS.append('MULTIJUMP')
                global_variables.SCORE -= 1000
            elif "MULTIJUMP" in SKILLS:
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
            game_view.setup()
            self.window.show_view(game_view)
            self.window.set_mouse_visible(False)

        self.manager.add(
            arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", child=self.v_box))

    def on_show(self):
        arcade.set_background_color(arcade.color.AMETHYST)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        arcade.start_render()
        self.manager.draw()
        score = f"Score: {global_variables.SCORE}"
        arcade.draw_text(score, WIDTH / 4, HEIGHT - 60, color=arcade.color.BLACK, font_size=20, font_name="Kenney Future")


def main():
    from menu import MenuView
    window = arcade.Window(WIDTH, HEIGHT, "Arcade Game", vsync=True, antialiasing=False)
    start_view = MenuView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
