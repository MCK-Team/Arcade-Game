import arcade
import random
from Enemies.enemy_parent import Enemy
import global_variables


class StormHead(Enemy):
    def __init__(self):
        super().__init__(max_health=1000, attack_distance=1000, melee_attack_distance=300, points=100, damage=5)

        self.current_animation_counter = 0
        self.change_x = 0
        self.walk_speed = 10
        self.attack_movement_speed = 20

        self.cooldown_time = 1  # in seconds
        self.cooldown_timer = random.random() * self.cooldown_time

        self.idle_textures = []
        for i in range(9):
            self.idle_textures.append(arcade.load_texture("assets/stormhead/idle.png", x=0, y=i * 124, width=119, height=124, hit_box_algorithm="Simple"))
        self.texture = self.idle_textures[0]

        self.running_textures_pair = [[], []]
        for i in range(10):
            self.running_textures_pair[0].append(arcade.load_texture("assets/stormhead/run.png", x=0, y=i * 124, width=119, height=124, hit_box_algorithm="Simple"))
        for i in range(10):
            self.running_textures_pair[1].append(arcade.load_texture("assets/stormhead/run.png", x=0, y=i * 124, width=119, height=124, flipped_horizontally=True, hit_box_algorithm="Simple"))

        self.attack_textures_pair = [[], []]
        for i in range(21):
            self.attack_textures_pair[0].append(arcade.load_texture("assets/stormhead/attack.png", x=0, y=i * 124, width=119, height=124, hit_box_algorithm="Simple"))
        for i in range(21):
            self.attack_textures_pair[1].append(arcade.load_texture("assets/stormhead/attack.png", x=0, y=i * 124, width=119, height=124, flipped_horizontally=True, hit_box_algorithm="Simple"))
        self.texture = self.attack_textures_pair[0][9]

        self.death_textures_pair = [[], []]
        for i in range(8):
            self.death_textures_pair[0].append(arcade.load_texture("assets/stormhead/death.png", x=0, y=i * 124, width=119, height=124, hit_box_algorithm="Simple"))
        for i in range(8):
            self.death_textures_pair[1].append(arcade.load_texture("assets/stormhead/death.png", x=0, y=i * 124, width=119, height=124, flipped_horizontally=True, hit_box_algorithm="Simple"))

        self.scale = 3.5

    def update_animation(self, delta_time: float = 1 / 60):

        if self.show_health_timer > 0:
            self.show_health_timer -= delta_time

        # Death Animation
        if self.cur_health <= 0:
            if self.change_x > 0:
                self.direction = 0   # Right
            if self.change_x < 0:
                self.direction = 1   # Left
            self.change_x = 0
            self.current_animation_counter += 1
            animation_speed = 5
            current_death_frame = int(self.current_animation_counter // (1 / (delta_time * animation_speed)))  # Todo refactor this

            if current_death_frame <= 7:
                self.texture = self.death_textures_pair[self.direction][current_death_frame]
            else:
                self.remove_from_sprite_lists()
                global_variables.SCORE += self.points

        # Attack Animation
        elif self.state == "Attack":
            if self.change_x > 0:
                self.direction = 0   # Right
            if self.change_x < 0:
                self.direction = 1   # Left

            self.current_animation_counter += 1
            animation_speed = 20
            attack_frames = 21
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
            if self.current_animation_counter >= 60*10/animation_speed:
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
                self.cooldown_timer = self.cooldown
            else:
                self.change_x = 0

    def on_update(self, delta_time: float = 1 / 60):
        print('on_update')
        if self.cooldown_timer > 0:
            self.cooldown_timer -= delta_time
