import arcade


class Cat(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.idle_textures = []
        for i in range(4):
            self.idle_textures.append(arcade.load_texture("assets/Idle.png", x=i * 48, y=0, width=48, height=48))
        self.texture = self.idle_textures[0]

        self.running_textures_pair = [[], []]
        for i in range(6):
            self.running_textures_pair[0].append(arcade.load_texture("assets/Running.png", x=i * 48, y=0, width=48,
                                                                     height=48))
        for i in range(6):
            self.running_textures_pair[1].append(arcade.load_texture("assets/Running.png", x=i * 48, y=0, width=48,
                                                                     height=48, flipped_horizontally=True))

        self.current_idle_counter = 0
        self.scale = 2

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
            if self.current_idle_counter >= 60*6/20:
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
            elif current_running_frame == 4:
                self.texture = self.running_textures_pair[direction][4]
            elif current_running_frame == 5:
                self.texture = self.running_textures_pair[direction][5]
