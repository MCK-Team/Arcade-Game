import arcade
import random
import math
from Enemies.enemy_parent import Enemy
import global_variables


class Executioner(Enemy):
    def __init__(self):
        super().__init__(max_health=1000, attack_distance=1000, melee_attack_distance=100, points=50, damage=0.2)

        self.current_animation_counter = 0
        self.change_x = 0
        self.walk_speed = 5
        self.attack_movement_speed = 20

        self.cooldown_time = 1  # in seconds
        self.cooldown_timer = random.random() * self.cooldown_time

        self.idle_textures_pair = [[], []]
        for i in range(4):
            self.idle_textures_pair[0].append(arcade.load_texture("assets/Undead_executioner_puppet/png/idle.png", x=i * 100, y=0, width=100, height=100, hit_box_algorithm="Simple"))
        for i in range(4):
            self.idle_textures_pair[1].append(arcade.load_texture("assets/Undead_executioner_puppet/png/idle.png", x=i * 100, y=0, width=100, height=100, flipped_horizontally=True, hit_box_algorithm="Simple"))

        self.texture = self.idle_textures_pair[0][0]

        self.attack_textures_pair = [[], []]
        for i in range(6):
            self.attack_textures_pair[0].append(arcade.load_texture("assets/Undead_executioner_puppet/png/attacking.png", x=i * 100, y=0, width=100, height=100, hit_box_algorithm="Simple"))
        for i in range(6):
            self.attack_textures_pair[1].append(arcade.load_texture("assets/Undead_executioner_puppet/png/attacking.png", x=i * 100, y=0, width=100, height=100, flipped_horizontally=True, hit_box_algorithm="Simple"))

        self.death_textures_pair = [[], []]
        for i in range(10):
            self.death_textures_pair[0].append(arcade.load_texture("assets/Undead_executioner_puppet/png/death.png", x=i * 100, y=0, width=100, height=100, hit_box_algorithm="Simple"))
        for i in range(10):
            self.death_textures_pair[1].append(arcade.load_texture("assets/Undead_executioner_puppet/png/death.png", x=i * 100, y=0, width=100, height=100, flipped_horizontally=True, hit_box_algorithm="Simple"))

        self.scale = 2

    def update_animation(self, delta_time: float = 1 / 60):

        if self.change_x > 0:
            self.direction = 0  # Right
        if self.change_x < 0:
            self.direction = 1  # Left

        if self.show_health_timer > 0:
            self.show_health_timer -= delta_time

        # Death Animation
        if self.cur_health <= 0:
            self.current_animation_counter += 1
            animation_speed = 10
            current_death_frame = int(self.current_animation_counter // (1 / (delta_time * animation_speed)))  # Todo refactor this

            if current_death_frame <= 9:
                self.texture = self.death_textures_pair[self.direction][current_death_frame]
            else:
                self.remove_from_sprite_lists()
                global_variables.SCORE += self.points

        # Attack Animation
        elif self.state == "Attack":
            self.current_animation_counter += 1
            animation_speed = 20
            attack_frames = 6
            if self.current_animation_counter >= 60 * attack_frames / animation_speed:
                self.current_animation_counter = 0
                self.state = "Idle"
                return
            current_attack_frame = int(self.current_animation_counter // (1 / (delta_time * animation_speed)))  # Todo refactor this

            self.texture = self.attack_textures_pair[self.direction][current_attack_frame]
            self.set_hit_box(self.texture.hit_box_points)  # Federinik33 on discord from some server comment a while ago.

        # Idle Animation
        else:
            animation_speed = 8
            self.current_animation_counter += 1
            if self.current_animation_counter >= 60 * 4 / animation_speed:  # [60 fps] * [frames] / [5 animation fps]
                self.current_animation_counter = 0
            current_idle_frame = int(self.current_animation_counter // (1 / (delta_time * animation_speed)))  # Todo refactor this

            self.texture = self.idle_textures_pair[self.direction][current_idle_frame]

    def update_sprite(self, x, y):
        self.draw_hit_box(color=arcade.color.RED, line_thickness=10)
        x_dist = abs(x - self.center_x)
        y_dist = abs(y - self.center_y)
        self.current_distance = pow(x_dist * x_dist + y_dist * y_dist, 0.5)

        if self.state == "Attack" or self.cur_health <= 0:
            self.change_x = 0
            self.change_y = 0
        elif self.state == "Idle":
            radians = math.atan2(y - self.center_y, x - self.center_x)
            if self.current_distance > self.melee_attack_distance:
                self.change_x = math.cos(radians) * self.walk_speed
                self.change_y = math.sin(radians) * self.walk_speed
            elif self.current_distance <= self.melee_attack_distance:
                self.state = "Attack"
