import arcade

class Gioco(arcade.Window):
    def __init__(self, larghezza, altezza, titolo):
        super().__init__(larghezza, altezza, titolo)

        self.sfondo_list = arcade.SpriteList()
        self.lista_sprite = arcade.SpriteList()
        
        self.sprite = None
        self.sfondo_sprite = None

        # Variabili movimento
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False
        self.velocita = 5
        self.scala_originale = 0.2 

        self.setup()

    def setup(self):
        # SFONDO
        self.sfondo_sprite = arcade.Sprite("./assets/background.png")
        self.sfondo_sprite.center_x = self.width / 2
        self.sfondo_sprite.center_y = self.height / 2
        self.sfondo_sprite.width = self.width
        self.sfondo_sprite.height = self.height
        self.sfondo_list.append(self.sfondo_sprite)

        # GIOCATORE
        self.sprite = arcade.Sprite("./assets/sprite.png", scale=self.scala_originale)
        self.sprite.center_x = self.width / 2
        self.sprite.center_y = self.height / 2
        self.lista_sprite.append(self.sprite)

    def on_draw(self):
        self.clear()
        self.sfondo_list.draw()
        self.lista_sprite.draw()

    def on_update(self, delta_time):
        # Movimento e Flip
        if self.up_pressed:
            self.sprite.center_y += self.velocita
        if self.down_pressed:
            self.sprite.center_y -= self.velocita
        
        if self.left_pressed:
            self.sprite.center_x -= self.velocita
            # Flip a sinistra: scala X negativa
            self.sprite.scale = (-self.scala_originale, self.scala_originale)
            
        if self.right_pressed:
            self.sprite.center_x += self.velocita
            # Torna a destra: scala X positiva
            self.sprite.scale = (self.scala_originale, self.scala_originale)

        # Limiti schermo
        self.sprite.center_x = max(0, min(self.width, self.sprite.center_x))
        self.sprite.center_y = max(0, min(self.height, self.sprite.center_y))

    def on_key_press(self, tasto, modificatori):
        if tasto == arcade.key.W: self.up_pressed = True
        elif tasto == arcade.key.S: self.down_pressed = True
        elif tasto == arcade.key.A: self.left_pressed = True
        elif tasto == arcade.key.D: self.right_pressed = True

    def on_key_release(self, tasto, modificatori):
        if tasto == arcade.key.W: self.up_pressed = False
        elif tasto == arcade.key.S: self.down_pressed = False
        elif tasto == arcade.key.A: self.left_pressed = False
        elif tasto == arcade.key.D: self.right_pressed = False

def main():
    Gioco(1000, 600, "Gioco")
    arcade.run()

if __name__ == "__main__":
    main()