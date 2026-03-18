import arcade

# --- Costanti per il mondo ---
WORLD_WIDTH = 5000
WORLD_HEIGHT = 800  
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

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
            self._registra(nome, tutti, durata, loop, default)
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
        if not self.animazione_corrente: return
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

        self.direzione = "giu"
        self.su = self.giu = self.sinistra = self.destra = False

    def update_animation(self, delta_time: float = 1 / 60):
        dx = dy = 0
        if self.su: dy += 1
        if self.giu: dy -= 1
        if self.sinistra: dx -= 1
        if self.destra: dx += 1

        if dy > 0: self.direzione = "su"
        elif dy < 0: self.direzione = "giu"
        elif dx < 0: self.direzione = "sinistra"
        elif dx > 0: self.direzione = "destra"

        if dx < 0: self.width = -abs(self.width)
        elif dx > 0: self.width = abs(self.width)

        if dx != 0 or dy != 0:
            self.imposta_animazione(f"walk_{self.direzione}")
        else:
            self.imposta_animazione(f"idle_{self.direzione}")
        super().update_animation(delta_time)

class Gioco(arcade.Window):
    def __init__(self, larghezza, altezza, titolo):
        super().__init__(larghezza, altezza, titolo)
        self.player = None
        self.lista_player = arcade.SpriteList()
        self.sfondo_cielo = arcade.SpriteList()
        self.sfondo_montagne = arcade.SpriteList()
        self.sfondo_alberi = arcade.SpriteList()
        
        self.camera_mondo = None
        self.camera_ui = None
        self.velocita = 6
        self.setup()

    def setup(self):
        self.player = Player()
        self.player.center_x = 150
        self.player.center_y = 200
        self.lista_player.append(self.player)

        # Metodo di emergenza per creare rettangoli colorati compatibile con ogni versione
        def crea_rettangolo_sicuro(w, h, colore):
            # Creiamo uno sprite "vuoto" e usiamo una texture generica
            s = arcade.SpriteCircle(1, colore) # Creiamo un puntino
            s.width = w  # Lo allunghiamo fino a farlo diventare un rettangolo
            s.height = h
            return s

        for x in range(0, WORLD_WIDTH, 1000):
            # 1. CIELO
            try:
                cielo = arcade.Sprite("assets/cielo_pixel.png")
                cielo.width, cielo.height = 1000, 800
            except:
                cielo = crea_rettangolo_sicuro(1000, 800, arcade.color.AZURE)
            cielo.left, cielo.bottom = x, 0
            self.sfondo_cielo.append(cielo)

            # 2. MONTAGNE
            m = crea_rettangolo_sicuro(1000, 500, arcade.color.COOL_GREY)
            m.left, m.bottom = x, 0
            self.sfondo_montagne.append(m)

            # 3. ALBERI
            a = crea_rettangolo_sicuro(1000, 250, arcade.color.BITTER_LEMON)
            a.left, a.bottom = x, 0
            self.sfondo_alberi.append(a)

        self.camera_mondo = arcade.Camera2D()
        self.camera_ui = arcade.Camera2D()

    def aggiorna_camera(self):
        cam_x, cam_y = self.camera_mondo.position
        target_x = cam_x + (self.player.center_x - cam_x) * 0.1
        target_y = cam_y + (self.player.center_y - cam_y) * 0.1

        target_x = max(SCREEN_WIDTH / 2, min(target_x, WORLD_WIDTH - SCREEN_WIDTH / 2))
        target_y = max(SCREEN_HEIGHT / 2, min(target_y, WORLD_HEIGHT - SCREEN_HEIGHT / 2))

        self.camera_mondo.position = (target_x, target_y)

    def on_draw(self):
        self.clear()
        pos_reale = self.camera_mondo.position

        self.camera_mondo.position = (pos_reale[0] * 0.9, pos_reale[1])
        self.camera_mondo.use()
        self.sfondo_cielo.draw()

        self.camera_mondo.position = (pos_reale[0] * 0.6, pos_reale[1])
        self.camera_mondo.use()
        self.sfondo_montagne.draw()

        self.camera_mondo.position = (pos_reale[0] * 0.3, pos_reale[1])
        self.camera_mondo.use()
        self.sfondo_alberi.draw()

        self.camera_mondo.position = pos_reale
        self.camera_mondo.use()
        self.lista_player.draw()
        
        self.camera_ui.use()
        arcade.draw_text(f"Posizione: {int(self.player.center_x)}", 20, 20, arcade.color.WHITE, 12)

    def on_update(self, delta_time):
        self.player.update_animation(delta_time)
        if self.player.su: self.player.center_y += self.velocita
        if self.player.giu: self.player.center_y -= self.velocita
        if self.player.sinistra: self.player.center_x -= self.velocita
        if self.player.destra: self.player.center_x += self.velocita

        # --- GESTIONE BORDI (SINISTRA, ALTO, BASSO) ---
        if self.player.left < 0: self.player.left = 0
        if self.player.bottom < 0: self.player.bottom = 0
        if self.player.top > WORLD_HEIGHT: self.player.top = WORLD_HEIGHT
        if self.player.right > WORLD_WIDTH: self.player.right = WORLD_WIDTH

        self.aggiorna_camera()

    def on_key_press(self, tasto, modificatori):
        if tasto in (arcade.key.UP, arcade.key.W): self.player.su = True
        elif tasto in (arcade.key.DOWN, arcade.key.S): self.player.giu = True
        elif tasto in (arcade.key.LEFT, arcade.key.A): self.player.sinistra = True
        elif tasto in (arcade.key.RIGHT, arcade.key.D): self.player.destra = True

    def on_key_release(self, tasto, modificatori):
        if tasto in (arcade.key.UP, arcade.key.W): self.player.su = False
        elif tasto in (arcade.key.DOWN, arcade.key.S): self.player.giu = False
        elif tasto in (arcade.key.LEFT, arcade.key.A): self.player.sinistra = False
        elif tasto in (arcade.key.RIGHT, arcade.key.D): self.player.destra = False

def main():
    Gioco(1000, 800, "Gioco Ichigo")
    arcade.run()

if __name__ == "__main__":
    main()