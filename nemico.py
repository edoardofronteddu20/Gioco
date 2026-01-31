import random  
import math
import arcade  # Assicurati che arcade sia importato nel file nemico.py

class Nemico(arcade.Sprite):
    def __init__(self, img_path="./assets/nemico.png", velocita=1.5):
        super().__init__(img_path)
        self.scale = 0.2  # Impostiamo la scala iniziale (solo orizzontale, 0.2)
        self.center_x = random.randint(50, 950)  # Posizione casuale
        self.center_y = random.randint(600, 800)  # Posizione casuale
        self.velocita = velocita
    
    def update(self, player_x, player_y):
        # Calcola la direzione verso il giocatore
        delta_x = player_x - self.center_x
        delta_y = player_y - self.center_y
        
        # Calcola la distanza tra il nemico e il giocatore
        distanza = math.sqrt(delta_x**2 + delta_y**2)

        if distanza > 0:
            # Normalizza la direzione (vettore unitario) per il movimento
            direzione_x = delta_x / distanza
            direzione_y = delta_y / distanza

            # Muove il nemico verso il giocatore
            self.center_x += direzione_x * self.velocita
            self.center_y += direzione_y * self.velocita

            # Aggiungi logica per girare il nemico in base alla direzione
            if direzione_x < 0:  # Se il nemico si muove verso sinistra
                self.scale = (-0.2, 0.2)  # Flip orizzontale
            elif direzione_x > 0:  # Se il nemico si muove verso destra
                self.scale = (0.2, 0.2)  # Orientamento normale (orizzontale positivo, verticale invariato)

    def distruggere(self):
        self.remove_from_sprite_lists()
