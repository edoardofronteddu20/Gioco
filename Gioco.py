import arcade
import random


class Gioco(arcade.Window):
    def __init__(self, larghezza, altezza, titolo):
        super().__init__(larghezza, altezza, titolo)
        
        self.player_sprite = None
        self.bg_sprite = None

        self.player_list = arcade.SpriteList()
        self.bg_list = arcade.SpriteList()
        self.platform_list = arcade.SpriteList()
        
        # Movimento
        self.left_pressed = False
        self.right_pressed = False
        self.space_pressed = False  # <-- aggiunto per salto continuo
        
        # Velocità e gravità
        self.change_x = 0
        self.change_y = 0
        self.velocita = 4
        self.gravity = -1
        self.jump_strength = 10  # forza del salto continuo
        
        self.setup()

    def setup(self):
        # Sfondo
        self.bg_sprite = arcade.Sprite("./assets/background.png")
        scale_x = self.width / self.bg_sprite.width
        scale_y = self.height / self.bg_sprite.height
        self.bg_sprite.scale = min(scale_x, scale_y)
        self.bg_sprite.center_x = self.width / 2
        self.bg_sprite.center_y = self.height / 2
        self.bg_list.append(self.bg_sprite)
        
        # Player
        self.player_sprite = arcade.Sprite("./assets/sprite.png", scale=0.2)
        self.player_sprite.center_x = 300
        self.player_sprite.center_y = 100
        self.player_list.append(self.player_sprite)
        
        # Piattaforme manuali (trasparenti)
        posizioni_piattaforme = [
            # Da completare: (x, y, larghezza, altezza)
        ]

        for x, y, larg, alt in posizioni_piattaforme:
            piattaforma = arcade.SpriteSolidColor(larg, alt, (0,0,0,0))  # trasparente
            piattaforma.center_x = x
            piattaforma.center_y = y
            self.platform_list.append(piattaforma)

    def on_draw(self):
        self.clear()
        self.bg_list.draw()
        self.platform_list.draw()
        self.player_list.draw()

    def on_update(self, delta_time):
        # Movimento orizzontale
        self.change_x = 0
        if self.left_pressed:
            self.change_x = -self.velocita
            self.player_sprite.scale = (-0.2, 0.2)
        elif self.right_pressed:
            self.change_x = self.velocita
            self.player_sprite.scale = (0.2, 0.2)
        
        self.player_sprite.center_x += self.change_x
        
        # --- SALTO CONTINUO CON GRAVITÀ ---
        if self.space_pressed:
            self.change_y = self.jump_strength
        else:
            self.change_y += self.gravity
        
        self.player_sprite.center_y += self.change_y
        # ----------------------------------
        
        # Collisioni con piattaforme
        collisions = arcade.check_for_collision_with_list(self.player_sprite, self.platform_list)
        if collisions:
            self.player_sprite.bottom = max(platform.top for platform in collisions)
            self.change_y = 0
        
        # Limiti dello schermo
        if self.player_sprite.left < 0:
            self.player_sprite.left = 0
        if self.player_sprite.right > self.width:
            self.player_sprite.right = self.width
        if self.player_sprite.bottom < 0:
            self.player_sprite.bottom = 0
            self.change_y = 0
        if self.player_sprite.top > self.height:
            self.player_sprite.top = self.height
            self.change_y = 0

    def on_key_press(self, key, modifiers):
        if key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.D:
            self.right_pressed = True
        elif key == arcade.key.SPACE:
            self.space_pressed = True  # <-- aggiunto

    def on_key_release(self, key, modifiers):
        if key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.D:
            self.right_pressed = False
        elif key == arcade.key.SPACE:
            self.space_pressed = False  # <-- aggiunto

def main():
    gioco = Gioco(1600, 800, "Gioco Platformer")
    arcade.run()

if __name__ == "__main__":
    main()
