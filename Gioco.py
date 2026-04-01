import arcade

# Costanti
WORLD_WIDTH = 5000
WORLD_HEIGHT = 800  
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 650

GRAVITA = 0.8
ALTEZZA_TERRENO = 130

class SpriteAnimato(arcade.Sprite):
    def __init__(self, scala: float = 1.0):
        super().__init__(scale=scala)
        self.animazioni = {}
        self.animazione_corrente = None
        self.animazione_default = None
        self.tempo_frame = 0.0
        self.indice_frame = 0

    def aggiungi_animazione(self, nome, percorso, frame_width, frame_height, num_frame, colonne, durata, loop=True, default=False):
        try:
            sheet = arcade.load_spritesheet(percorso)
            tutti = sheet.get_texture_grid(size=(frame_width, frame_height), columns=colonne, count=num_frame)
            # Salva anche versione flippata
            flippati = [t.flip_left_right() for t in tutti]
            self._registra(nome, tutti, durata, loop, default)
            self._registra(nome + "_flip", flippati, durata, loop, False)
        except Exception as e:
            print(f"Errore caricando {nome}: {e}")

    def _registra(self, nome, textures, durata, loop, default=False):
        self.animazioni[nome] = {
            "textures": textures,
            "durata_frame": durata / len(textures),
            "loop": loop,
        }
        if default or self.animazione_default is None:
            self.animazione_default = nome
        if self.animazione_corrente is None:
            self._vai(nome)

    def imposta_animazione(self, nome: str):
        if nome in self.animazioni and nome != self.animazione_corrente:
            self._vai(nome)

    def _vai(self, nome: str):
        self.animazione_corrente = nome
        self.indice_frame = 0
        self.tempo_frame = 0.0
        self.texture = self.animazioni[nome]["textures"][0]

    def update_animation(self, delta_time: float = 1 / 60):
        if not self.animazione_corrente:
            return
        anim = self.animazioni[self.animazione_corrente]
        self.tempo_frame += delta_time
        if self.tempo_frame < anim["durata_frame"]:
            return
        self.tempo_frame -= anim["durata_frame"]
        self.indice_frame = (self.indice_frame + 1) % len(anim["textures"])
        self.texture = anim["textures"][self.indice_frame]

class Player(SpriteAnimato):
    def __init__(self):
        super().__init__(scala=1.5)
        direzioni = ["su", "sinistra", "giu", "destra"]
        for d in direzioni:
            self.aggiungi_animazione(f"idle_{d}", "assets/idle.png", 128, 128, 2, 2, 0.8, default=(d == "giu"))
            self.aggiungi_animazione(f"walk_{d}", "assets/walk.png", 128, 128, 8, 8, 0.6)

        self.direzione = "destra"
        self.sinistra = self.destra = False
        self.vel_y = 0.0
        self.a_terra = False
        self.flippato = False

    def update_animation(self, delta_time: float = 1 / 60):
        dx = 0
        if self.sinistra: dx -= 1
        if self.destra: dx += 1

        if dx < 0:
            self.direzione = "sinistra"
            self.flippato = True
        elif dx > 0:
            self.direzione = "destra"
            self.flippato = False

        if not self.a_terra:
            if self.vel_y > 0:
                self.direzione = "su"
            else:
                self.direzione = "giu"

        nome_anim = f"walk_{self.direzione}" if (dx != 0 or not self.a_terra) else f"idle_{self.direzione}"
        nome_anim_flip = nome_anim + ("_flip" if self.flippato else "")

        self.imposta_animazione(nome_anim_flip)
        super().update_animation(delta_time)

class Gioco(arcade.Window):
    def __init__(self, larghezza, altezza, titolo):
        super().__init__(larghezza, altezza, titolo)

        self.player = None
        self.lista_player = arcade.SpriteList()
        self.sfondo_list = arcade.SpriteList()

        self.camera_mondo = None
        self.camera_ui = None
        self.velocita = 4

        self.setup()

    def setup(self):
        self.player = Player()
        self.player.center_x = 150
        self.player.center_y = ALTEZZA_TERRENO + 200
        self.lista_player.append(self.player)

        try:
            sfondo = arcade.Sprite("assets/background.png")
            scala_x = SCREEN_WIDTH / sfondo.texture.width
            scala_y = SCREEN_HEIGHT / sfondo.texture.height
            scala = max(scala_x, scala_y)
            sfondo.scale = scala
            sfondo.center_x = SCREEN_WIDTH / 2
            sfondo.center_y = SCREEN_HEIGHT / 2
        except Exception as e:
            print(f"Errore caricando sfondo: {e}")
            sfondo = arcade.SpriteSolidColor(SCREEN_WIDTH, SCREEN_HEIGHT, arcade.color.AZURE)
            sfondo.center_x = SCREEN_WIDTH / 2
            sfondo.center_y = SCREEN_HEIGHT / 2
        self.sfondo_list.append(sfondo)

        self.camera_mondo = arcade.Camera2D()
        self.camera_ui = arcade.Camera2D()

    def aggiorna_camera(self):
        target_x = self.player.center_x
        target_y = self.player.center_y

        target_x = max(SCREEN_WIDTH / 2, min(target_x, WORLD_WIDTH - SCREEN_WIDTH / 2))
        target_y = max(SCREEN_HEIGHT / 2, min(target_y, WORLD_HEIGHT - SCREEN_HEIGHT / 2))

        self.camera_mondo.position = (target_x, target_y)

    def on_draw(self):
        self.clear()

        self.camera_ui.use()
        self.sfondo_list.draw()

        self.camera_mondo.use()
        self.lista_player.draw()

    def on_update(self, delta_time):
        if self.player.sinistra:
            self.player.center_x -= self.velocita
        if self.player.destra:
            self.player.center_x += self.velocita

        self.player.vel_y -= GRAVITA
        self.player.center_y += self.player.vel_y

        if self.player.bottom <= ALTEZZA_TERRENO:
            self.player.bottom = ALTEZZA_TERRENO
            self.player.vel_y = 0
            self.player.a_terra = True
        else:
            self.player.a_terra = False

        if self.player.left < 0:
            self.player.left = 0
        if self.player.right > WORLD_WIDTH:
            self.player.right = WORLD_WIDTH

        self.player.update_animation(delta_time)
        self.aggiorna_camera()

    def on_key_press(self, tasto, modificatori):
        if tasto in (arcade.key.LEFT, arcade.key.A):
            self.player.sinistra = True
        elif tasto in (arcade.key.RIGHT, arcade.key.D):
            self.player.destra = True

    def on_key_release(self, tasto, modificatori):
        if tasto in (arcade.key.LEFT, arcade.key.A):
            self.player.sinistra = False
        elif tasto in (arcade.key.RIGHT, arcade.key.D):
            self.player.destra = False

def main():
    Gioco(SCREEN_WIDTH, SCREEN_HEIGHT, "Gioco")
    arcade.run()

if __name__ == "__main__":
    main()