import arcade
import arcade.gui

WIDTH = 2560  # or 1920
HEIGHT = 1440  # or 1080


class HowTO(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.v_box = arcade.gui.UIBoxLayout()
        self.current_animation_counter = 0

        self.background = []
        for i in range(7):
            self.background.append(arcade.load_texture(f"assets/background/noonbackground{i + 1}.png", x=0, y=0, width=1024, height=768))
        self.texture = self.background[0]

        instructions = "The Goal is to kill all enemies and improve your skills throughout your journey"

        instruction_label = arcade.gui.UITextArea(text=instructions, width=1200, height=80, font_size=14, font_name="Kenney Future",  text_color=arcade.color.BLACK)
        self.v_box.add(instruction_label.with_space_around(bottom=10, left=200))

        keys = """
          Controls
        -------------------------
        Move Left: A / Left Arrow
        Move Right: D / Right Arrow
        Jump: W / Space
        Shoot: Left Click
        Protective Sword: Right Click
        Cone Shot: Right Click
        Radial Attack: E
        """

        key_text = arcade.gui.UITextArea(text=keys, width=500, height=240, font_size=14, font_name="Kenney Future", text_color=arcade.color.BLACK)
        self.v_box.add(key_text.with_space_around(bottom=20, left=100))

        back_button = arcade.gui.UIFlatButton(text="Back", width=150)
        self.v_box.add(back_button.with_space_around(bottom=10))

        @back_button.event('on_click')
        def on_click_how(event):
            from menu import MenuView
            self.manager.disable()
            menu_view = MenuView()
            self.window.show_view(menu_view)

        self.manager.add(
            arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", child=self.v_box))

    def on_show(self):
        arcade.set_background_color(arcade.color.AMETHYST)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, WIDTH, HEIGHT, self.texture)
        self.manager.draw()

    def on_update(self, delta_time):
        self.update_animation()

    def update_animation(self, delta_time: float = 1 / 60):
        self.current_animation_counter += 1
        if self.current_animation_counter >= 1/(delta_time*5)*7:  # [60 fps] * [7 frames] / [5 animation fps]
            self.current_animation_counter = 0
        current_animation_frame = int(self.current_animation_counter // (1/(delta_time*5)))  # Todo refactor this
        self.texture = self.background[current_animation_frame]
