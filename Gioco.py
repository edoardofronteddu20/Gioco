import arcade
import random  
import math
from nemico import Nemico  # Importa la classe Nemico dal file nemico.py

class Gioco(arcade.Window):
    def __init__(self, larghezza, altezza, titolo):
        super().__init__(larghezza, altezza, titolo)
        self.sprite = None
        self.lista_sprite = arcade.SpriteList()
        self.lista_nemici = arcade.SpriteList()  # Lista per i nemici
        
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False
        
        self.velocita = 4
        self.score = 0  # Punteggio
        
        arcade.set_background_color(arcade.color.WHITE)
        
        self.setup()
    
    def setup(self):
        self.sprite = arcade.Sprite("./assets/sprite.png")
        self.sprite.center_x = 300
        self.sprite.center_y = 100
        self.sprite.scale = 0.2 
        self.lista_sprite.append(self.sprite)
        
        # Spawna un nemico
        self.spawn_nemico()

    def spawn_nemico(self):
        nemico = Nemico()  # Crea un nemico usando la classe importata
        self.lista_nemici.append(nemico)  # Aggiungi il nemico alla lista

    def on_draw(self):
        self.clear()  # Pulisce lo schermo
        self.lista_sprite.draw()  # Crea lo sprite principale
        self.lista_nemici.draw()  # Crea i nemici
        arcade.draw_text(f"Punteggio: {self.score}", 10, self.height - 30, arcade.color.BLACK, 20)

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
        
        if self.sprite.center_x < 0:
            self.sprite.center_x = 0
        elif self.sprite.center_x > self.width:
            self.sprite.center_x = self.width
        
        if self.sprite.center_y < 0:
            self.sprite.center_y = 0
        elif self.sprite.center_y > self.height:
            self.sprite.center_y = self.height
        
        # Flip orizzontale in base alla direzione del movimento
        if change_x < 0:  # Se va a sinistra
            self.sprite.scale = (-0.2, 0.2)  # Flip orizzontale
        elif change_x > 0:  # Se va a destra
            self.sprite.scale = (0.2, 0.2)  # Posizione normale
        
        # Aggiorna i nemici
        for nemico in self.lista_nemici:
            nemico.update(self.sprite.center_x, self.sprite.center_y)

        # Controlla le collisioni con i nemici
        self.check_collision()
    
    def check_collision(self):
        for nemico in self.lista_nemici:
            if arcade.check_for_collision(self.sprite, nemico):
                nemico.distruggere()
                self.score += 1  
                self.spawn_nemico() 

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
    gioco = Gioco(1000, 800, "Gioco")
    arcade.run()

if __name__ == "__main__":
    main()