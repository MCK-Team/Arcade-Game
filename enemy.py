import arcade
import random


class Enemy(arcade.Sprite):
    def __init__(self, max_health=100, attack_distance=1500, melee_attack_distance=None, points=100, damage=10):
        super().__init__()
        self.max_health = max_health
        self.cur_health = max_health
        self.attack_distance = attack_distance
        self.melee_attack_distance = melee_attack_distance
        self.current_distance = None
        self.points = points
        self.damage = damage
        self.show_health_time = 3
        self.show_health_timer = 0
        self.state = "Idle"
        self.direction = 0

    def draw_health_bar(self, x, y):
        if self.show_health_timer > 0:
            width = 50
            if self.cur_health < self.max_health:
                arcade.draw_rectangle_filled(center_x=x, center_y=y + 50, width=width, height=10, color=arcade.color.BLACK)

            health_width = width * (self.cur_health / self.max_health)
            arcade.draw_rectangle_filled(center_x=x - 0.5 * (width - health_width), center_y=y + 50, width=health_width, height=10, color=arcade.color.RED)


class StormHead(Enemy):
    def __init__(self):
        super().__init__(max_health=1000, points=1000)

        self.current_animation_counter = 0
        #self.change_x = random.random() * 4 + 2

        self.current_animation_counter = 0
        self.cooldown_time = 5
        self.cooldown_timer = random.random() * self.cooldown_time

        self.idle_textures = []
        for i in range(9):
            self.idle_textures.append(arcade.load_texture("assets/stormhead/idle.png", x=0, y=i * 124, width=119, height=124))
        self.texture = self.idle_textures[0]

        self.scale = 2

    def update_animation(self, delta_time: float = 1 / 60):
        if self.show_health_timer > 0:
            self.show_health_timer -= delta_time

        # Idle Animation
        if self.change_x == 0 and self.change_y == 0:

            self.current_animation_counter += 1
            animation_speed = 5
            if self.current_animation_counter >= 60*4/animation_speed:  # [60 fps] * [4 frames] / [5 animation fps]
                self.current_animation_counter = 0
            current_idle_frame = int(self.current_animation_counter // (1 / (delta_time * animation_speed)))    # Todo refactor this

            self.texture = self.idle_textures[current_idle_frame]


class Rat(Enemy):
    def __init__(self):
        super().__init__(max_health=50, attack_distance=500, points=50)

        self.current_animation_counter = 0
        self.change_x = random.random() * 4 + 2

        self.cooldown_time = 1    # in seconds
        self.cooldown_timer = random.random() * self.cooldown_time

        self.idle_textures = []
        for i in range(4):
            self.idle_textures.append(arcade.load_texture("assets/rat/Idle.png", x=i * 32, y=0, width=32, height=32))
        self.texture = self.idle_textures[0]

        self.running_textures_pair = [[], []]
        for i in range(4):
            self.running_textures_pair[0].append(arcade.load_texture("assets/rat/Running.png", x=i * 32, y=0, width=32,
                                                                     height=32))
        for i in range(4):
            self.running_textures_pair[1].append(arcade.load_texture("assets/rat/Running.png", x=i * 32, y=0, width=32,
                                                                     height=32, flipped_horizontally=True))

        self.scale = 1.7

    # def update(self, delta_time: float = 1 / 60):
    #    self.center_x += random.randint(-10, 10)

    def update_animation(self, delta_time: float = 1 / 60):
        if self.show_health_timer > 0:
            self.show_health_timer -= delta_time

        # Idle Animation
        if self.change_x == 0 and self.change_y == 0:

            self.current_animation_counter += 1
            animation_speed = 5
            if self.current_animation_counter >= 60*4/animation_speed:  # [60 fps] * [4 frames] / [5 animation fps]
                self.current_animation_counter = 0
            current_idle_frame = int(self.current_animation_counter // (1 / (delta_time * animation_speed)))    # Todo refactor this

            self.texture = self.idle_textures[current_idle_frame]

        # Run Animation
        if abs(self.change_x) > 0:
            if self.change_x > 0:
                self.direction = 0   # Right
            if self.change_x < 0:
                self.direction = 1   # Left

            self.current_animation_counter += 1
            animation_speed = 20
            if self.current_animation_counter >= 60*4/animation_speed:
                self.current_animation_counter = 0
            current_running_frame = int(self.current_animation_counter // (1 / (delta_time * animation_speed)))  # Todo refactor this
            self.texture = self.running_textures_pair[self.direction][current_running_frame]


class NightBorne(Enemy):
    def __init__(self):
        super().__init__(max_health=1000, attack_distance=1000, melee_attack_distance=200, points=1000, damage=50)

        self.current_animation_counter = 0
        self.change_x = 0
        self.walk_speed = 10
        self.attack_movement_speed = 100

        arcade.hitbox

        self.cooldown_time = 1    # in seconds
        self.cooldown_timer = random.random() * self.cooldown_time

        self.idle_textures = []
        for i in range(9):
            self.idle_textures.append(arcade.load_texture("assets/NightBorne/NightBorne.png", x=i * 80, y=0, width=80, height=80, hit_box_algorithm="Simple"))

        self.running_textures_pair = [[], []]
        for i in range(6):
            self.running_textures_pair[0].append(arcade.load_texture("assets/NightBorne/NightBorne.png", x=i * 80, y=80, width=80, height=80, hit_box_algorithm="Simple"))
        for i in range(6):
            self.running_textures_pair[1].append(arcade.load_texture("assets/NightBorne/NightBorne.png", x=i * 80, y=80, width=80, height=80, flipped_horizontally=True, hit_box_algorithm="Simple"))

        self.attack_textures_pair = [[], []]
        for i in range(12):
            self.attack_textures_pair[0].append(arcade.load_texture("assets/NightBorne/NightBorne.png", x=i * 80, y=80 * 2, width=80, height=80, hit_box_algorithm="Simple"))
        for i in range(12):
            self.attack_textures_pair[1].append(arcade.load_texture("assets/NightBorne/NightBorne.png", x=i * 80, y=80 * 2, width=80, height=80, flipped_horizontally=True, hit_box_algorithm="Simple"))
        self.texture = self.attack_textures_pair[0][9]

        self.scale = 3.5

    # def update(self, delta_time: float = 1 / 60):
    #    self.center_x += random.randint(-10, 10)

    def update_animation(self, delta_time: float = 1 / 60):

        if self.show_health_timer > 0:
            self.show_health_timer -= delta_time

        # Attack Animation
        if self.state == "Attack":
            if self.change_x > 0:
                self.direction = 0   # Right
            if self.change_x < 0:
                self.direction = 1   # Left

            self.current_animation_counter += 1
            animation_speed = 20
            attack_frames = 12
            if self.current_animation_counter >= 60*attack_frames/animation_speed:
                self.current_animation_counter = 0
                self.state = "Idle"
                return
            current_attack_frame = int(self.current_animation_counter // (1 / (delta_time * animation_speed)))  # Todo refactor this

            self.texture = self.attack_textures_pair[self.direction][current_attack_frame]
            self.set_hit_box(self.texture.hit_box_points)   # Federinik33 on discord from some server comment a while ago.

        # Idle Animation
        elif self.change_x == 0 and self.change_y == 0:
            animation_speed = 8
            self.current_animation_counter += 1
            if self.current_animation_counter >= 60*9/animation_speed:  # [60 fps] * [5 frames] / [5 animation fps]
                self.current_animation_counter = 0
            current_idle_frame = int(self.current_animation_counter // (1 / (delta_time * animation_speed)))    # Todo refactor this

            self.texture = self.idle_textures[current_idle_frame]

        # Run Animation
        elif abs(self.change_x) > 0:
            if self.change_x > 0:
                self.direction = 0   # Right
            if self.change_x < 0:
                self.direction = 1   # Left

            self.current_animation_counter += 1
            animation_speed = 20
            if self.current_animation_counter >= 60*6/animation_speed:
                self.current_animation_counter = 0
            current_running_frame = int(self.current_animation_counter // (1 / (delta_time * animation_speed)))  # Todo refactor this

            self.texture = self.running_textures_pair[self.direction][current_running_frame]

    def update_sprite(self, x, y):
        self.draw_hit_box(color=arcade.color.RED, line_thickness=10)
        x_dist = abs(x - self.center_x)
        y_dist = abs(y - self.center_y)
        self.current_distance = pow(x_dist * x_dist + y_dist * y_dist, 0.5)

        if self.state == "Attack":
            self.change_x = 0

        # if self.nightborne.state == "Cooldown":
        #     if self.cat.center_x < self.nightborne.center_x:
        #         self.nightborne.change_x = 1 * self.nightborne.attack_movement_speed
        #     elif self.cat.center_x > self.nightborne.center_x:
        #         self.nightborne.change_x = -1 * self.nightborne.attack_movement_speed
        #     self.nightborne.state == "Idle"

        elif self.state == "Idle":
            if abs(self.center_y - y) > self.melee_attack_distance and abs(self.center_x - x) < self.melee_attack_distance / 2:
                self.change_x = 0
            elif self.attack_distance > self.current_distance > self.melee_attack_distance:
                if x < self.center_x:
                    self.change_x = -1 * self.walk_speed
                elif x > self.center_x:
                    self.change_x = 1 * self.walk_speed
            elif self.current_distance <= self.melee_attack_distance:
                if x + self.melee_attack_distance < self.center_x:
                    self.change_x = -1 * self.attack_movement_speed
                elif x - self.melee_attack_distance > self.center_x:
                    self.change_x = 1 * self.attack_movement_speed
                self.state = "Attack"
            else:
                self.change_x = 0

