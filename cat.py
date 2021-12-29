import arcade


class Cat(arcade.Sprite):
    def __init__(self, max_health=100):
        super().__init__()

        self.max_health = max_health
        self.cur_health = max_health

        # IDLE TEXTURES
        self.idle_textures_pair = [[], []]
        for i in range(4):
            self.idle_textures_pair[0].append(arcade.load_texture("assets/cat/Idle.png", x=i * 48, y=0, width=48, height=48))
        self.texture = self.idle_textures_pair[0][0]

        for i in range(4):
            self.idle_textures_pair[1].append(arcade.load_texture("assets/cat/Idle.png", x=i * 48, y=0, width=48, height=48, mirrored=True))

        # RUNNING TEXTURES
        self.running_textures_pair = [[], []]
        for i in range(6):
            self.running_textures_pair[0].append(arcade.load_texture("assets/cat/Running.png", x=i * 48, y=0, width=48, height=48))
        for i in range(6):
            self.running_textures_pair[1].append(arcade.load_texture("assets/cat/Running.png", x=i * 48, y=0, width=48, height=48, mirrored=True))

        # HURT TEXTURES
        self.hurt_textures_pair = [[], []]
        for i in range(2):
            self.hurt_textures_pair[0].append(arcade.load_texture("assets/cat/Hurt.png", x=i * 48, y=0, width=48, height=48))
        for i in range(2):
            self.hurt_textures_pair[1].append(arcade.load_texture("assets/cat/Hurt.png", x=i * 48, y=0, width=48, height=48, mirrored=True))

        # DEATH TEXTURES
        self.death_textures_pair = [[], []]
        for i in range(4):
            self.death_textures_pair[0].append(arcade.load_texture("assets/cat/Death.png", x=i * 48, y=0, width=48, height=48))
        for i in range(4):
            self.death_textures_pair[1].append(arcade.load_texture("assets/cat/Death.png", x=i * 48, y=0, width=48, height=48, mirrored=True))

        self.current_animation_counter = 0
        self.direction = 0  # 0 represents right. 1 is left.
        self.scale = 2

    def draw_health_bar(self, x, y):
        width = 350
        if self.cur_health < self.max_health:
            arcade.draw_rectangle_filled(center_x=x, center_y=y, width=width, height=20, color=arcade.color.RED)

        health_width = width * (self.cur_health / self.max_health)
        arcade.draw_rectangle_filled(center_x=x - 0.5 * (width - health_width), center_y=y, width=health_width, height=20, color=arcade.color.GREEN)

    def update_animation(self, delta_time: float = 1 / 60):
        if self.change_x > 0:
            self.direction = 0  # Right
        if self.change_x < 0:
            self.direction = 1  # Left

        # Idle Animation
        if self.change_x == 0 and self.change_y == 0:

            self.current_animation_counter += 1
            if self.current_animation_counter >= 1/(delta_time*5)*4:  # [60 fps] * [4 frames] / [5 animation fps]
                self.current_animation_counter = 0
            current_animation_frame = self.current_animation_counter // (1/(delta_time*5))  # Todo refactor this

            if current_animation_frame == 0:
                self.texture = self.idle_textures_pair[self.direction][0]
            elif current_animation_frame == 1:
                self.texture = self.idle_textures_pair[self.direction][1]
            elif current_animation_frame == 2:
                self.texture = self.idle_textures_pair[self.direction][2]
            elif current_animation_frame == 3:
                self.texture = self.idle_textures_pair[self.direction][3]

        # Run Animation
        if abs(self.change_x) > 0:

            self.current_animation_counter += 1
            if self.current_animation_counter >= 1/(delta_time*20)*6:  # [60 fps] * [4 frames] / [5 animation fps]
                self.current_animation_counter = 0
            current_animation_frame = self.current_animation_counter // (1/(delta_time*20))  # Todo refactor this

            if current_animation_frame == 0:
                self.texture = self.running_textures_pair[self.direction][0]
            elif current_animation_frame == 1:
                self.texture = self.running_textures_pair[self.direction][1]
            elif current_animation_frame == 2:
                self.texture = self.running_textures_pair[self.direction][2]
            elif current_animation_frame == 3:
                self.texture = self.running_textures_pair[self.direction][3]
            elif current_animation_frame == 4:
                self.texture = self.running_textures_pair[self.direction][4]
            elif current_animation_frame == 5:
                self.texture = self.running_textures_pair[self.direction][5]

    def death_animation(self, delta_time):
        # Dead Animation
        self.current_animation_counter += 1
        current_animation_frame = self.current_animation_counter // (1/(delta_time*5))  # Todo refactor this

        if current_animation_frame == 0:
            self.texture = self.death_textures_pair[self.direction][0]
        elif current_animation_frame == 1:
            self.texture = self.death_textures_pair[self.direction][1]
        elif current_animation_frame == 2:
            self.texture = self.death_textures_pair[self.direction][2]
        elif current_animation_frame >= 3:
            self.texture = self.death_textures_pair[self.direction][3]

    # Hurt Animation
    def hurt_animation(self, delta_time):
        self.current_animation_counter += 1
        current_animation_frame = self.current_animation_counter // (1 / (delta_time * 5))  # Todo refactor this

        if current_animation_frame == 0:
            self.texture = self.hurt_textures_pair[self.direction][0]
        elif current_animation_frame == 1:
            self.texture = self.hurt_textures_pair[self.direction][1]
