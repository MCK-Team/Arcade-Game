import arcade
import arcade.gui

WIDTH = 1920
HEIGHT = 1080


class MenuView(arcade.View):
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

        arcade.set_background_color(arcade.color.AMETHYST)

        title_text = arcade.gui.UITextArea(text="Arcade Cat", font_size=30, font_name="Kenney Rocket", text_color=arcade.color.BLACK)
        self.v_box.add(title_text.with_space_around(bottom=55, left=50))

        start_button = arcade.gui.UIFlatButton(text="Begin Journey", width=150)
        self.v_box.add(start_button.with_space_around(bottom=10))

        how_button = arcade.gui.UIFlatButton(text="How To Play", width=150)
        self.v_box.add(how_button.with_space_around(bottom=10))

        quit_button = arcade.gui.UIFlatButton(text="Exit Game", width=150)
        self.v_box.add(quit_button.with_space_around(bottom=10))

        @start_button.event('on_click')
        def on_click_start(event):
            from main import GameView
            self.manager.disable()
            game_view = GameView()
            self.window.show_view(game_view)
            self.window.set_mouse_visible(False)
            game_view.setup()

        @how_button.event('on_click')
        def on_click_how(event):
            from how_to import HowTO
            self.manager.disable()
            how_view = HowTO()
            self.window.show_view(how_view)

        @quit_button.event("on_click")
        def on_click_quit(event):
            arcade.exit()

        self.manager.add(
            arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", child=self.v_box))

    def on_show(self):
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

