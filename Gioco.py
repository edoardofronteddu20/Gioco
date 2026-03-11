import arcade
import arcade.future.background as background

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 800
CAMERA_SPEED = 0.1
PLAYER_SPEED = 300


class GameView(arcade.View):

    def __init__(self):
        super().__init__()

        self.background_color = (162, 84, 162, 255)

        # camera
        self.camera = arcade.Camera2D()

        # gruppo parallax
        self.backgrounds = background.ParallaxGroup()

        bg_size = (WINDOW_WIDTH, WINDOW_HEIGHT)

        # layer sfondo
        self.backgrounds.add_from_file("assets/layers/cielo.png", size=bg_size, depth=10.0)
        self.backgrounds.add_from_file("assets/layers/montagne.png", size=bg_size, depth=5.0)
        self.backgrounds.add_from_file("assets/layers/alberi.png", size=bg_size, depth=3.0)
        self.backgrounds.add_from_file("assets/layers/strada.png", size=bg_size, depth=1.0)

        # player
        self.player = arcade.Sprite("assets/player.png")
        self.player.center_x = 0
        self.player.bottom = 0

        self.x_velocity = 0

    def on_draw(self):
        self.clear()
        self.camera.use()

        bg = self.backgrounds

        bg.offset = self.camera.bottom_left
        bg.pos = self.camera.bottom_left

        bg.draw()

        self.player.draw()

    def pan_camera_to_player(self):

        self.camera.position = arcade.math.lerp_2d(
            self.camera.position,
            (self.player.center_x, WINDOW_HEIGHT // 2),
            CAMERA_SPEED
        )

    def on_update(self, delta_time: float):

        # movimento player
        self.player.center_x += self.x_velocity * delta_time

        # camera segue
        self.pan_camera_to_player()

    def on_key_press(self, symbol: int, modifiers: int):

        if symbol == arcade.key.A:
            self.x_velocity = -PLAYER_SPEED

        elif symbol == arcade.key.D:
            self.x_velocity = PLAYER_SPEED

    def on_key_release(self, symbol: int, modifiers: int):

        if symbol == arcade.key.A or symbol == arcade.key.D:
            self.x_velocity = 0


def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, "Parallax Example")
    view = GameView()
    window.show_view(view)
    arcade.run()


if __name__ == "__main__":
    main()