import arcade

# Costanti
WORLD_WIDTH = 5000
WORLD_HEIGHT = 800
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 800
CAMERA_SPEED = 0.1

ALTEZZA_TERRENO = 245
FORZA_SALTO = 15

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__(scale=1.5)

        self.anim_idle = self._carica("assets/idle.png", 128, 128, 8, 8)
        self.anim_walk = self._carica("assets/walk.png", 128, 128, 7, 7)
        self.anim_jump = self._carica("assets/jump.png", 128, 128, 8, 8)
        self.anim_walk_flip = [t.flip_left_right() for t in self.anim_walk]
        self.anim_idle_flip = [t.flip_left_right() for t in self.anim_idle]
        self.anim_jump_flip = [t.flip_left_right() for t in self.anim_jump]

        self.textures_correnti = self.anim_idle
        self.texture = self.textures_correnti[0]

        self.indice = 0
        self.tempo = 0.0
        self.durata_frame = 0.15
        self.anim_precedente = "idle"

        self.sinistra = False
        self.destra = False
        self.flippato = False
        self.vel_y = 0.0
        self.a_terra = False

    def _carica(self, percorso, fw, fh, num, col):
        try:
            sheet = arcade.load_spritesheet(percorso)
            return sheet.get_texture_grid(size=(fw, fh), columns=col, count=num)
        except Exception as e:
            print(f"Errore: {e}")
            return [arcade.Texture.create_empty("vuota", (fw, fh))]

    def _cambia_anim(self, nuove_textures, durata, nome):
        if nome != self.anim_precedente:
            self.textures_correnti = nuove_textures
            self.durata_frame = durata
            self.indice = 0
            self.tempo = 0.0
            self.anim_precedente = nome

    def salta(self):
        if self.a_terra:
            self.vel_y = FORZA_SALTO
            self.a_terra = False

    def update_animation(self, delta_time=1/60):
        dx = 0
        if self.sinistra: dx -= 1
        if self.destra: dx += 1

        if dx < 0:
            self.flippato = True
        elif dx > 0:
            self.flippato = False

        if not self.a_terra:
            if self.flippato:
                self._cambia_anim(self.anim_jump_flip, 0.06, "jump_flip")
            else:
                self._cambia_anim(self.anim_jump, 0.06, "jump")
        elif dx != 0:
            if self.flippato:
                self._cambia_anim(self.anim_walk_flip, 0.15, "walk_flip")
            else:
                self._cambia_anim(self.anim_walk, 0.15, "walk")
        else:
            if self.flippato:
                self._cambia_anim(self.anim_idle_flip, 0.15, "idle_flip")
            else:
                self._cambia_anim(self.anim_idle, 0.15, "idle")

        self.tempo += delta_time
        if self.tempo >= self.durata_frame:
            self.tempo -= self.durata_frame
            self.indice = (self.indice + 1) % len(self.textures_correnti)

        self.texture = self.textures_correnti[self.indice]


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.sfondo_list = arcade.SpriteList()
        self.lista_player = arcade.SpriteList()
        self.player = None
        self.camera_mondo = arcade.Camera2D()
        self.camera_ui = arcade.Camera2D()
        self.velocita = 4
        self.setup()

    def setup(self):
        # Sfondo 1
        try:
            sfondo1 = arcade.Sprite("assets/background.png")
            sfondo1.scale = max(SCREEN_WIDTH / sfondo1.texture.width, SCREEN_HEIGHT / sfondo1.texture.height)
            sfondo1.left = 0
            sfondo1.bottom = 0
        except Exception as e:
            print(f"Errore sfondo1: {e}")
            sfondo1 = arcade.SpriteSolidColor(SCREEN_WIDTH, SCREEN_HEIGHT, arcade.color.AZURE)
            sfondo1.left = 0
            sfondo1.bottom = 0
        self.sfondo_list.append(sfondo1)

        # Sfondo 2
        try:
            sfondo2 = arcade.Sprite("assets/background2.png")
            sfondo2.scale = max(SCREEN_WIDTH / sfondo2.texture.width, SCREEN_HEIGHT / sfondo2.texture.height)
            sfondo2.left = SCREEN_WIDTH
            sfondo2.bottom = 0
        except Exception as e:
            print(f"Errore sfondo2: {e}")
            sfondo2 = arcade.SpriteSolidColor(SCREEN_WIDTH, SCREEN_HEIGHT, arcade.color.GREEN)
            sfondo2.left = SCREEN_WIDTH
            sfondo2.bottom = 0
        self.sfondo_list.append(sfondo2)

        # Player
        self.player = Player()
        self.player.center_x = 200
        self.player.center_y = ALTEZZA_TERRENO + 150
        self.lista_player.append(self.player)

    def aggiorna_camera(self):
        cam_x, cam_y = self.camera_mondo.position

        target_x = cam_x + (self.player.center_x - cam_x) * CAMERA_SPEED
        target_y = cam_y + (self.player.center_y - cam_y) * CAMERA_SPEED

        target_x = max(SCREEN_WIDTH / 2, min(target_x, WORLD_WIDTH - SCREEN_WIDTH / 2))
        target_y = max(SCREEN_HEIGHT / 2, min(target_y, WORLD_HEIGHT - SCREEN_HEIGHT / 2))

        self.camera_mondo.position = (target_x, target_y)

    def on_draw(self):
        self.clear()

        self.camera_mondo.use()
        self.sfondo_list.draw()
        self.lista_player.draw()

        self.camera_ui.use()

    def on_update(self, delta_time):
        if self.player.sinistra:
            self.player.center_x -= self.velocita
        if self.player.destra:
            self.player.center_x += self.velocita

        self.player.vel_y -= 0.8
        self.player.center_y += self.player.vel_y

        if self.player.center_y <= ALTEZZA_TERRENO:
            self.player.center_y = ALTEZZA_TERRENO
            self.player.vel_y = 0
            self.player.a_terra = True
        else:
            self.player.a_terra = False

        if self.player.center_x < 0:
            self.player.center_x = 0

        if self.player.center_y > WORLD_HEIGHT:
            self.player.center_y = WORLD_HEIGHT
            self.player.vel_y = 0

        self.player.update_animation(delta_time)
        self.aggiorna_camera()

    def on_key_press(self, tasto, modificatori):
        if tasto in (arcade.key.LEFT, arcade.key.A):
            self.player.sinistra = True
        elif tasto in (arcade.key.RIGHT, arcade.key.D):
            self.player.destra = True
        elif tasto in (arcade.key.UP, arcade.key.W, arcade.key.SPACE):
            self.player.salta()

    def on_key_release(self, tasto, modificatori):
        if tasto in (arcade.key.LEFT, arcade.key.A):
            self.player.sinistra = False
        elif tasto in (arcade.key.RIGHT, arcade.key.D):
            self.player.destra = False


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Gioco")
    view = GameView()
    window.show_view(view)
    arcade.run()

if __name__ == "__main__":
    main()