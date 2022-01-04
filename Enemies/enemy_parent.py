import arcade


class Enemy(arcade.Sprite):
    def __init__(self, max_health=100, attack_distance=1500, melee_attack_distance=None, points=10, damage=10, cooldown=3):
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
        self.cooldown = 3
        self.cooldown_timer = 0

    def draw_health_bar(self, x, y):
        if self.show_health_timer > 0:
            width = 50
            if self.cur_health < self.max_health:
                arcade.draw_rectangle_filled(center_x=x, center_y=y + 50, width=width, height=10, color=arcade.color.BLACK)

            health_width = width * (self.cur_health / self.max_health)
            arcade.draw_rectangle_filled(center_x=x - 0.5 * (width - health_width), center_y=y + 50, width=health_width, height=10, color=arcade.color.RED)
