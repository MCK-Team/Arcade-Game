import arcade
import random


class Enemy(arcade.Sprite):
    def __init__(self, max_health=100):
        super().__init__()
        self.max_health = max_health
        self.cur_health = max_health

    def draw_health_bar(self, x, y):
        width = 50
        if self.cur_health < self.max_health:
            arcade.draw_rectangle_filled(center_x=x, center_y=y + 50, width=width, height=10, color=arcade.color.BLACK)

        health_width = width * (self.cur_health / self.max_health)
        arcade.draw_rectangle_filled(center_x=x - 0.5 * (width - health_width), center_y=y + 50, width=health_width, height=10, color=arcade.color.RED)


class Rat(Enemy):
    def __init__(self):
        super().__init__()
        # self.max_health = max_health
        # self.cur_health = max_health

        self.current_idle_counter = 0
        self.change_x = random.random() * 4 + 2

        self.cooldown_time = 2    # in seconds
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

    #def update(self, delta_time: float = 1 / 60):
    #    self.center_x += random.randint(-10, 10)

    def update_animation(self, delta_time: float = 1 / 60):

        # Idle Animation
        if self.change_x == 0 and self.change_y == 0:

            self.current_idle_counter += 1
            if self.current_idle_counter >= 60*4/5:  # [60 fps] * [4 frames] / [5 animation fps]
                self.current_idle_counter = 0
            current_idle_frame = self.current_idle_counter // (1/(delta_time*5)) # Todo refactor this

            if current_idle_frame == 0:
                self.texture = self.idle_textures[0]
            elif current_idle_frame == 1:
                self.texture = self.idle_textures[1]
            elif current_idle_frame == 2:
                self.texture = self.idle_textures[2]
            elif current_idle_frame == 3:
                self.texture = self.idle_textures[3]

        # Run Animation
        if abs(self.change_x) > 0:
            if self.change_x > 0:
                direction = 0   # Right
            if self.change_x < 0:
                direction = 1   # Left

            self.current_idle_counter += 1
            if self.current_idle_counter >= 60*4/20:
                self.current_idle_counter = 0
            current_running_frame = self.current_idle_counter // (1/(delta_time*20))  # Todo refactor this

            if current_running_frame == 0:
                self.texture = self.running_textures_pair[direction][0]
            elif current_running_frame == 1:
                self.texture = self.running_textures_pair[direction][1]
            elif current_running_frame == 2:
                self.texture = self.running_textures_pair[direction][2]
            elif current_running_frame == 3:
                self.texture = self.running_textures_pair[direction][3]
