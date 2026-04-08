import arcade

# --- Costanti ---
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Gioco"

WORLD_WIDTH = 5000  # larghezza mondo
GRAVITA = 0.8
PLAYER_JUMP_SPEED = 16
PLAYER_MOVEMENT_SPEED = 7

# Altezza del terreno (misura della strada nel background)
ALTEZZA_TERRENO = 100  


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__(scale=1.5, hit_box_algorithm="Simple")

        self.anim_idle = self._carica("assets/idle.png", 128, 128, 8, 8)
        self.anim_walk = self._carica("assets/walk.png", 128, 128, 7, 7)
        self.anim_jump = self._carica("assets/jump.png", 128, 128, 8, 8)

        self.anim_idle_f = [t.flip_left_right() for t in self.anim_idle]
        self.anim_walk_f = [t.flip_left_right() for t in self.anim_walk]
        self.anim_jump_f = [t.flip_left_right() for t in self.anim_jump]

        self.texture = self.anim_idle[0]

        self.flippato = False
        self.a_terra = False
        self.cur_frame = 0
        self.tempo_anim = 0.0
        self.stato_attuale = "IDLE"

    def _carica(self, percorso, fw, fh, num, col):
        try:
            sheet = arcade.load_spritesheet(percorso)
            return sheet.get_texture_grid(size=(fw, fh), columns=col, count=num)
        except:
            return [arcade.Texture.create_empty("fall", (fw, fh))]

    def update_animation(self, delta_time: float = 1/60):
        if self.change_x < -0.1:
            self.flippato = True
        elif self.change_x > 0.1:
            self.flippato = False

        nuovo_stato = "IDLE"
        if not self.a_terra:
            nuovo_stato = "JUMP"
        elif abs(self.change_x) > 0.1:
            nuovo_stato = "WALK"

        if nuovo_stato != self.stato_attuale:
            self.stato_attuale = nuovo_stato
            self.cur_frame = 0

        if self.stato_attuale == "JUMP":
            frames = self.anim_jump_f if self.flippato else self.anim_jump
        elif self.stato_attuale == "WALK":
            frames = self.anim_walk_f if self.flippato else self.anim_walk
        else:
            frames = self.anim_idle_f if self.flippato else self.anim_idle

        self.tempo_anim += delta_time
        if self.tempo_anim >= 0.1:
            self.tempo_anim = 0
            self.cur_frame = (self.cur_frame + 1) % len(frames)
            self.texture = frames[self.cur_frame]


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.player_list = arcade.SpriteList()
        self.sfondo_list = arcade.SpriteList()

        self.camera_mondo = arcade.camera.Camera2D()
        self.camera_ui = arcade.camera.Camera2D()

        self.sinistra_premuto = False
        self.destra_premuto = False
        self.player = None

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.sfondo_list = arcade.SpriteList()

        try:
            sfondo = arcade.Sprite("assets/background.png")
            sfondo.width = SCREEN_WIDTH
            sfondo.height = SCREEN_HEIGHT
            sfondo.position = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            self.sfondo_list.append(sfondo)
        except:
            pass

        self.player = Player()

        # 🔹 Spawn iniziale sulla strada (a sinistra)
        self.player.left = 50  # distanza dal bordo sinistro
        self.player.bottom = ALTEZZA_TERRENO  # allineato con la strada

        self.player_list.append(self.player)

    def on_draw(self):
        self.clear()

        self.camera_ui.use()
        self.sfondo_list.draw()

        self.camera_mondo.use()
        self.player_list.draw()

    def on_update(self, delta_time):
        self.player.change_x = 0
        if self.sinistra_premuto:
            self.player.change_x = -PLAYER_MOVEMENT_SPEED
        if self.destra_premuto:
            self.player.change_x = PLAYER_MOVEMENT_SPEED

        # Fisica
        self.player.change_y -= GRAVITA
        self.player.center_x += self.player.change_x
        self.player.center_y += self.player.change_y

        # Terreno
        if self.player.bottom <= ALTEZZA_TERRENO:
            self.player.bottom = ALTEZZA_TERRENO
            self.player.change_y = 0
            self.player.a_terra = True
        else:
            self.player.a_terra = False

        # Limiti orizzontali
        if self.player.left < 0:
            self.player.left = 0
        if self.player.right > WORLD_WIDTH:
            self.player.right = WORLD_WIDTH

        # Camera segue il player, ma non blocca a sinistra
        cam_x = self.player.center_x - SCREEN_WIDTH / 2
        if cam_x < 0:
            cam_x = 0
        if cam_x > WORLD_WIDTH - SCREEN_WIDTH:
            cam_x = WORLD_WIDTH - SCREEN_WIDTH

        self.camera_mondo.position = (cam_x, 0)

        self.player.update_animation(delta_time)

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.A):
            self.sinistra_premuto = True
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.destra_premuto = True
        elif key in (arcade.key.SPACE, arcade.key.W, arcade.key.UP) and self.player.a_terra:
            self.player.change_y = PLAYER_JUMP_SPEED

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.A):
            self.sinistra_premuto = False
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.destra_premuto = False


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    view = GameView()
    view.setup()
    window.show_view(view)
    arcade.run()


if __name__ == "__main__":
    main()