import arcade

# Costanti
GRAVITA = 0.5
VELOCITA_SALTO = 11
VELOCITA_NORMALE = 5
VELOCITA_SPRINT = 9 # Velocità aumentata per lo scatto

class Gioco(arcade.Window):
    def __init__(self, larghezza, altezza, titolo):
        super().__init__(larghezza, altezza, titolo)

        self.sfondo_list = arcade.SpriteList()
        self.lista_sprite = arcade.SpriteList()
        self.pavimento_list = arcade.SpriteList()
        self.piattaforme_superiori = arcade.SpriteList()

        self.sprite = None
        self.physics_engine = None
        self.scala = 0.15
        
        # Texture per lo scambio
        self.texture_idle = None
        self.texture_run = None

        # Variabili stato
        self.left_pressed = False
        self.right_pressed = False
        self.shift_pressed = False
        self.salti_effettuati = 0

        self.setup()

    def setup(self):
        # SFONDO
        sfondo = arcade.Sprite("./assets/background.png")
        sfondo.center_x = self.width / 2
        sfondo.center_y = self.height / 2
        sfondo.width = self.width
        sfondo.height = self.height
        self.sfondo_list.append(sfondo)

        # CARICAMENTO TEXTURE
        self.texture_idle = arcade.load_texture("./assets/sprite.png")
        self.texture_run = arcade.load_texture("./assets/run.png")

        # GIOCATORE - SPAWN IN ALTO A SINISTRA
        self.sprite = arcade.Sprite()
        self.sprite.texture = self.texture_idle
        self.sprite.scale = self.scala
        self.sprite.center_x = 100 
        self.sprite.center_y = 450 
        self.lista_sprite.append(self.sprite)

        # 1. IL PAVIMENTO
        pavimento = arcade.SpriteSolidColor(1000, 40, arcade.color.TRANSPARENT_BLACK)
        pavimento.center_x = 500
        pavimento.center_y = 40 
        self.pavimento_list.append(pavimento)

        # 2. PIATTAFORME SUPERIORI
        coords_piani = [
            [350, 190, 700, 20], # Secondo piano
            [170, 345, 340, 20], # Terzo Sinistra
            [830, 345, 340, 20], # Terzo Destra
        ]

        for c in coords_piani:
            p = arcade.SpriteSolidColor(int(c[2]), int(c[3]), arcade.color.TRANSPARENT_BLACK)
            p.center_x = c[0]
            p.center_y = c[1]
            self.piattaforme_superiori.append(p)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.sprite,
            platforms=self.piattaforme_superiori,
            walls=self.pavimento_list,
            gravity_constant=GRAVITA
        )

    def on_draw(self):
        self.clear()
        self.sfondo_list.draw()
        self.lista_sprite.draw()

    def on_update(self, delta_time):
        if self.physics_engine.can_jump():
            self.salti_effettuati = 0

        # Gestione Velocità e Texture (Sprint)
        velocita_attuale = VELOCITA_NORMALE
        
        if self.shift_pressed and (self.left_pressed or self.right_pressed):
            velocita_attuale = VELOCITA_SPRINT
            self.sprite.texture = self.texture_run
        else:
            self.sprite.texture = self.texture_idle

        # Movimento
        self.sprite.change_x = 0
        if self.left_pressed and not self.right_pressed:
            self.sprite.change_x = -velocita_attuale
            self.sprite.scale = (-self.scala, self.scala)
        elif self.right_pressed and not self.left_pressed:
            self.sprite.change_x = velocita_attuale
            self.sprite.scale = (self.scala, self.scala)

        # Limiti bordi
        if self.sprite.left < 0: self.sprite.left = 0
        if self.sprite.right > self.width: self.sprite.right = self.width

        self.physics_engine.update()

    def on_key_press(self, tasto, modificatori):
        if tasto == arcade.key.W or tasto == arcade.key.SPACE:
            if self.salti_effettuati < 2:
                self.sprite.change_y = VELOCITA_SALTO
                self.salti_effettuati += 1
        elif tasto == arcade.key.S:
            self.sprite.center_y -= 5
        elif tasto == arcade.key.A:
            self.left_pressed = True
        elif tasto == arcade.key.D:
            self.right_pressed = True
        elif tasto == arcade.key.LSHIFT or tasto == arcade.key.RSHIFT:
            self.shift_pressed = True

    def on_key_release(self, tasto, modificatori):
        if tasto == arcade.key.A:
            self.left_pressed = False
        elif tasto == arcade.key.D:
            self.right_pressed = False
        elif tasto == arcade.key.LSHIFT or tasto == arcade.key.RSHIFT:
            self.shift_pressed = False

def main():
    Gioco(1000, 600, "Caverna - Sprint Mode")
    arcade.run()

if __name__ == "__main__":
    main()