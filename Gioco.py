import arcade
import random
import time
import os

# Costanti
LARGHEZZA = 800
ALTEZZA = 600
TITOLO = "Ashen Blade - Gem Hunter di Edo"
VELOCITA = 5
TEMPO_MAX = 1

class Gioco(arcade.Window):
    def __init__(self):
        super().__init__(LARGHEZZA, ALTEZZA, TITOLO)
        arcade.set_background_color(arcade.color.BLACK)
        
        self.player = None
        self.player_list = arcade.SpriteList()
        self.gemme_lista = arcade.SpriteList()
        
        # tasti
        self.up = self.down = self.left = self.right = False
        
        self.livello = 1
        self.punti = 0
        self.secondi = TEMPO_MAX
        self.timer_spawn = 0
        
        self.pausa = False
        self.finito = False

    def setup(self):
        if os.path.exists("assets/player.png"):
            self.player = arcade.Sprite("assets/player.png", 1.2)
        else:
            self.player = arcade.SpriteCircle(15, arcade.color.BLUE)
            
        self.player.center_x = 400
        self.player.center_y = 300
        self.player_list.append(self.player)

    def spawna_gemma(self):
        files = ["", "ama", "gri", "azu", "strip4", "roj"]
        path = f"assets/spr_coin_{files[self.livello]}.png"
        
        if os.path.exists(path):
            # Carico la texture grossa
            base = arcade.load_texture(path)
            w = base.width // 4
            h = base.height
            
            gemma = arcade.Sprite(scale=2.5)
            gemma.frames = [] 
            
            for i in range(4):
                # Taglio il pezzettino
                immagine_tagliata = base.image.crop((i*w, 0, (i+1)*w, h))
                # Creo la texture dal pezzettino (corretto per le nuove versioni)
                tex = arcade.Texture(image=immagine_tagliata, name=f"{path}_{i}")
                gemma.frames.append(tex)
            
            gemma.texture = gemma.frames[0]
            gemma.cur_frame = 0
            gemma.anim_timer = 0
            
            gemma.center_x = random.randint(50, 750)
            gemma.center_y = random.randint(50, 550)
            self.gemme_lista.append(gemma)

    def on_draw(self):
        self.clear()
        self.gemme_lista.draw()
        self.player_list.draw()
        
        arcade.draw_text(f"LIVELLO: {self.livello}", 10, 570, arcade.color.WHITE, 14)
        arcade.draw_text(f"PUNTI: {self.punti}", 10, 550, arcade.color.GOLD, 14)
        arcade.draw_text(f"TEMPO: {int(self.secondi)}", 10, 530, arcade.color.RED, 14)
        
        if self.pausa and not self.finito:
            arcade.draw_lrbt_rectangle_filled(0, 800, 0, 600, (0, 0, 0, 150))
            arcade.draw_text("PAUSA", 400, 300, arcade.color.WHITE, 50, anchor_x="center")
            arcade.draw_text("Premi ESC per tornare al gioco", 400, 100, arcade.color.GRAY, 15, anchor_x="center")

        if self.finito:
            arcade.draw_lrbt_rectangle_filled(0, 800, 0, 600, (20, 20, 40, 240))
            arcade.draw_text("Tempo finito", 400, 350, arcade.color.WHITE, 40, anchor_x="center")
            arcade.draw_text(f"{self.punti} PT", 400, 280, arcade.color.GOLD, 50, anchor_x="center")
            arcade.draw_text("Premi R per rifare", 400, 100, arcade.color.GRAY, 15, anchor_x="center")

    def on_update(self, delta_time):
        if self.pausa or self.finito:
            return 
            
        # Animazione gemme
        for g in self.gemme_lista:
            g.anim_timer += delta_time
            if g.anim_timer > 0.15:
                g.anim_timer = 0
                g.cur_frame = (g.cur_frame + 1) % 4
                g.texture = g.frames[g.cur_frame]
        
        # Movimento
        if self.up: self.player.center_y += VELOCITA
        if self.down: self.player.center_y -= VELOCITA
        if self.left: self.player.center_x -= VELOCITA
        if self.right: self.player.center_x += VELOCITA
        
        self.player.left = max(0, self.player.left)
        self.player.right = min(800, self.player.right)
        self.player.bottom = max(0, self.player.bottom)
        self.player.top = min(600, self.player.top)
        
        # Spawn
        self.timer_spawn += delta_time
        if self.timer_spawn > (2.0 - (self.livello * 0.2)):
            self.spawna_gemma()
            self.timer_spawn = 0
            
        # Collisioni
        beccate = arcade.check_for_collision_with_list(self.player, self.gemme_lista)
        for g in beccate:
            g.remove_from_sprite_lists()
            self.punti += (self.livello * 10)
            
        # Tempo
        self.secondi -= delta_time
        if self.secondi <= 0:
            if self.livello < 5:
                self.livello += 1
                self.secondi = TEMPO_MAX
                self.gemme_lista.clear()
            else:
                self.finito = True

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE: self.pausa = not self.pausa
        if key in [arcade.key.UP, arcade.key.W]: self.up = True
        if key in [arcade.key.DOWN, arcade.key.S]: self.down = True
        if key in [arcade.key.LEFT, arcade.key.A]: self.left = True
        if key in [arcade.key.RIGHT, arcade.key.D]: self.right = True
        
        if key == arcade.key.R and self.finito:
            self.livello = 1
            self.punti = 0
            self.secondi = TEMPO_MAX
            self.finito = False
            self.gemme_lista.clear()
            self.player.center_x = 400
            self.player.center_y = 300

    def on_key_release(self, key, modifiers):
        if key in [arcade.key.UP, arcade.key.W]: self.up = False
        if key in [arcade.key.DOWN, arcade.key.S]: self.down = False
        if key in [arcade.key.LEFT, arcade.key.A]: self.left = False
        if key in [arcade.key.RIGHT, arcade.key.D]: self.right = False

def main():
    game = Gioco()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()