import arcade
import random
from Enemies.enemy_parent import Enemy


class Rat(Enemy):
    def __init__(self):
        super().__init__(max_health=50, attack_distance=500, points=50, damage=0.2)

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
