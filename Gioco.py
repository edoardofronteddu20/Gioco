import arcade
import random
import math
from nemico import Nemico

class Gioco(arcade.Window):
    def __init__(self, larghezza, altezza, titolo):
        super().__init__(larghezza, altezza, titolo)

        self.sprite = None
        self.lista_sprite = arcade.SpriteList()
        self.lista_nemici = arcade.SpriteList()

        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False

        self.velocita = 4
        self.Punteggio = 0

        self.raggio_attacco = 80
        self.attaccando = False
        self.tempo_attacco = 0.0
        self.durata_attacco = 0.2  # secondi

        arcade.set_background_color(arcade.color.WHITE)
        self.setup()

    def setup(self):
        self.sprite = arcade.Sprite(scale=0.2)

        # 🔹 carichiamo le texture
        self.texture_idle = arcade.load_texture("./assets/sprite.png")
        self.texture_attack = arcade.load_texture("./assets/attack.png")

        self.sprite.texture = self.texture_idle
        self.sprite.center_x = 300
        self.sprite.center_y = 100

        self.lista_sprite.append(self.sprite)

        self.spawn_nemico()

    def spawn_nemico(self):
        nemico = Nemico()
        self.lista_nemici.append(nemico)

    def on_draw(self):
        self.clear()
        self.lista_sprite.draw()
        self.lista_nemici.draw()

        arcade.draw_text(
            f"Punteggio: {self.Punteggio}",
            10, self.height - 30,
            arcade.color.BLACK, 20
        )

    def on_update(self, delta_time):
        change_x = 0
        change_y = 0

        if self.up_pressed:
            change_y += self.velocita
        if self.down_pressed:
            change_y -= self.velocita
        if self.left_pressed:
            change_x -= self.velocita
        if self.right_pressed:
            change_x += self.velocita

        self.sprite.center_x += change_x
        self.sprite.center_y += change_y

        self.sprite.center_x = max(0, min(self.width, self.sprite.center_x))
        self.sprite.center_y = max(0, min(self.height, self.sprite.center_y))

        # flip orizzontale
        if change_x < 0:
            self.sprite.scale = (-0.2, 0.2)
        elif change_x > 0:
            self.sprite.scale = (0.2, 0.2)

        # aggiorna nemici
        for nemico in self.lista_nemici:
            nemico.update(self.sprite.center_x, self.sprite.center_y)

        # ⏱️ gestione ritorno a idle
        if self.attaccando:
            self.tempo_attacco += delta_time
            if self.tempo_attacco >= self.durata_attacco:
                self.sprite.texture = self.texture_idle
                self.attaccando = False
                self.tempo_attacco = 0.0

    # 🖱️ CLICK SINISTRO = ATTACCO + CAMBIO PNG
    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT and not self.attaccando:
            # cambia sprite
            self.sprite.texture = self.texture_attack
            self.attaccando = True

            # controllo nemici vicini
            for nemico in self.lista_nemici:
                distanza = math.dist(
                    (self.sprite.center_x, self.sprite.center_y),
                    (nemico.center_x, nemico.center_y)
                )

                if distanza <= self.raggio_attacco:
                    nemico.distruggere()
                    self.Punteggio += 1
                    self.spawn_nemico()
                    break

    def on_key_press(self, tasto, modificatori):
        if tasto in (arcade.key.UP, arcade.key.W):
            self.up_pressed = True
        elif tasto in (arcade.key.DOWN, arcade.key.S):
            self.down_pressed = True
        elif tasto in (arcade.key.LEFT, arcade.key.A):
            self.left_pressed = True
        elif tasto in (arcade.key.RIGHT, arcade.key.D):
            self.right_pressed = True

    def on_key_release(self, tasto, modificatori):
        if tasto in (arcade.key.UP, arcade.key.W):
            self.up_pressed = False
        elif tasto in (arcade.key.DOWN, arcade.key.S):
            self.down_pressed = False
        elif tasto in (arcade.key.LEFT, arcade.key.A):
            self.left_pressed = False
        elif tasto in (arcade.key.RIGHT, arcade.key.D):
            self.right_pressed = False


def main():
    Gioco(1000, 600, "Gioco")
    arcade.run()


if __name__ == "__main__":
    main()
