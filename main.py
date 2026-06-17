import pygame
import sys

pygame.init()
breedte, hoogte = 600, 400
scherm = pygame.display.set_mode((breedte, hoogte))
pygame.display.set_caption("Unix Stuiter Cirkel")
klok = pygame.time.Clock()

def bereken_bankbod(overgebleven_koffers):
    """
    Berekent het bod van de bank op basis van de lijst met overgebleven kofferbedragen.
    """
    aantal_koffers = len(overgebleven_koffers)
    
    # 1. De look-up table voor de ronde-percentages (aantal koffers : percentage)
    ronde_factoren = {
        20: 0.1334,
        15: 0.1993,
        11: 0.3216,
        8:  0.3527,
        6:  0.5020,
        5:  0.6645,
        4:  0.7650,  # Bij 4 koffers: bank biedt ~76,5% van het gemiddelde
        3:  0.8800,  # Bij 3 koffers: bank biedt 88% van het gemiddelde
    }
    
    # Als de functie wordt aangeroepen op een moment dat er geen standaard bod is,
    # (bijvoorbeeld als er 19 koffers zijn), geven we 'None' terug.
    if aantal_koffers not in ronde_factoren:
        return None

    # 2. Bereken de Verwachte Waarde (het gemiddelde)
    gemiddelde = sum(overgebleven_koffers) / aantal_koffers
    
    # 3. Vermenigvuldig met de juiste factor uit de dictionary
    factor = ronde_factoren[aantal_koffers]
    ruw_bod = gemiddelde * factor
    
    # 4. Afronden voor televisie
    # round(bedrag, -3) is een handige Python-truc om af te ronden 
    # op het dichtstbijzijnde duizendtal (bijv. 84982.5 wordt 85000.0).
    bod_afgerond = round(ruw_bod, -3)
    
    return int(bod_afgerond)

# --- VOORBEELD VAN HOE JE DE FUNCTIE AANROEPT ---
# Stel dit is je lijst na de eerste ronde (20 koffers over)
koffers_ronde_1 = [
    0.01, 0.20, 0.50, 1, 5, 50, 1000, 5000, 10000, 25000, 
    50000, 200000, 300000, 400000, 500000, 750000, 1000000, 
    2000000, 2500000, 5000000
]

bod = bereken_bankbod(koffers_ronde_1)
print(f"De bank biedt: € {bod}") 
# Output zal exact "De bank biedt: € 85000" zijn.