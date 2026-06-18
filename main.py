import pygame
import sys
import random
from pygame.locals import *

pygame.init()
breedte, hoogte = 600, 400
scherm = pygame.display.set_mode((breedte, hoogte))
pygame.display.set_caption("Miljoenenjacht")
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
        2:  0.9600   # Bij 2 koffers (finale): bank biedt 96% van het gemiddelde
    }
    
    # Als de functie wordt aangeroepen op een moment dat er geen standaard bod is,
    # (bijvoorbeeld als er 19 koffers zijn), geven we 'None' terug.
    if aantal_koffers not in ronde_factoren:
        return None

    # 2. Bereken de Verwachte Waarde (het gemiddelde)
    gemiddelde = sum(int(overgebleven_koffers)) / aantal_koffers
    
    # 3. Vermenigvuldig met de juiste factor uit de dictionary
    factor = ronde_factoren[aantal_koffers]
    ruw_bod = gemiddelde * factor
    
    # 4. Afronden voor televisie
    # round(bedrag, -3) is een handige Python-truc om af te ronden 
    # op het dichtstbijzijnde duizendtal (bijv. 84982.5 wordt 85000.0).
    bod_afgerond = round(ruw_bod, -3)
    
    return int(bod_afgerond)

koffer_nummers = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
    15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26
]
overgebleven_koffers = [
    '0,01', '0,20', '0,50', '1', '5', '10', '20', '50', '100', '500', '1.000', '2.500',
    '5.000', '10.000', '25.000', '50.000', '100.000', '200.000', '300.000', '400.000',
    '500.000', '750.000', '1.000.000', '2.000.000', '2.500.000', '5.000.000'
]
aantal_koffers = len(overgebleven_koffers)

print(koffer_nummers)
jouw_koffer = int(input("Kies een koffer waarvan jij denkt dat er €5.000.000 in zit."))
koffer_nummers.remove(jouw_koffer)
print("Je mag 6 koffers openmaken.")
while aantal_koffers > 20:
    print(koffer_nummers)
    koffer_nummers.remove(int(input("Kies een koffer om open te maken.")))
    gekozen_koffer = random.choice(overgebleven_koffers)
    print(f"Er zit €{gekozen_koffer} in.")
    overgebleven_koffers.remove(gekozen_koffer)
    print(f"Je houdt deze bedragen over: {overgebleven_koffers}")
    aantal_koffers = len(overgebleven_koffers)
bod = bereken_bankbod(overgebleven_koffers)
print(f"De bank biedt €{bod}")
accepteren = input("Wil je het bod van de bank accepteren? (ja/nee)")
if accepteren == "ja":
    print(f"DEAL, je hebt €{bod} gewonnen! We gaan kijken wat je had kunnen winnen als je door was gespeeld.")
else:
    print("NO DEAL, je mag 5 koffers openmaken.")

while aantal_koffers > 15:
    print(koffer_nummers)
    koffer_nummers.remove(int(input("Kies een koffer om open te maken.")))
    gekozen_koffer = random.choice(overgebleven_koffers)
    print(f"Er zit €{gekozen_koffer} in.")
    overgebleven_koffers.remove(gekozen_koffer)
    print(f"Je houdt deze bedragen over: {overgebleven_koffers}")
    aantal_koffers = len(overgebleven_koffers)
if accepteren != "ja":
    bod = bereken_bankbod(overgebleven_koffers)
    print(f"De bank biedt €{bod}")
    accepteren = input("Wil je het bod van de bank accepteren? (ja/nee)")
    if accepteren == "ja":
        print(f"DEAL, je hebt €{bod} gewonnen! We gaan kijken wat je had kunnen winnen als je door was gespeeld.")
    else:
        print("NO DEAL, je mag 4 koffers openmaken.")

while aantal_koffers > 11:
    print(koffer_nummers)
    koffer_nummers.remove(int(input("Kies een koffer om open te maken.")))
    gekozen_koffer = random.choice(overgebleven_koffers)
    print(f"Er zit €{gekozen_koffer} in.")
    overgebleven_koffers.remove(gekozen_koffer)
    print(f"Je houdt deze bedragen over: {overgebleven_koffers}")
    aantal_koffers = len(overgebleven_koffers)
if accepteren != "ja":
    bod = bereken_bankbod(overgebleven_koffers)
    print(f"De bank biedt €{bod}")
    accepteren = input("Wil je het bod van de bank accepteren? (ja/nee)")
    if accepteren == "ja":
        print(f"DEAL, je hebt €{bod} gewonnen! We gaan kijken wat je had kunnen winnen als je door was gespeeld.")
    else:
        print("NO DEAL, je mag 3 koffers openmaken.")

while aantal_koffers > 8:
    print(koffer_nummers)
    koffer_nummers.remove(int(input("Kies een koffer om open te maken.")))
    gekozen_koffer = random.choice(overgebleven_koffers)
    print(f"Er zit €{gekozen_koffer} in.")
    overgebleven_koffers.remove(gekozen_koffer)
    print(f"Je houdt deze bedragen over: {overgebleven_koffers}")
    aantal_koffers = len(overgebleven_koffers)
if accepteren != "ja":
    bod = bereken_bankbod(overgebleven_koffers)
    print(f"De bank biedt €{bod}")
    accepteren = input("Wil je het bod van de bank accepteren? (ja/nee)")
    if accepteren == "ja":
        print(f"DEAL, je hebt €{bod} gewonnen! We gaan kijken wat je had kunnen winnen als je door was gespeeld.")
    else:
        print("NO DEAL, je mag 2 koffers openmaken.")

while aantal_koffers > 6:
    print(koffer_nummers)
    koffer_nummers.remove(int(input("Kies een koffer om open te maken.")))
    gekozen_koffer = random.choice(overgebleven_koffers)
    print(f"Er zit €{gekozen_koffer} in.")
    overgebleven_koffers.remove(gekozen_koffer)
    print(f"Je houdt deze bedragen over: {overgebleven_koffers}")
    aantal_koffers = len(overgebleven_koffers)
if accepteren != "ja":
    bod = bereken_bankbod(overgebleven_koffers)
    print(f"De bank biedt €{bod}")
    accepteren = input("Wil je het bod van de bank accepteren? (ja/nee)")
    if accepteren == "ja":
        print(f"DEAL, je hebt €{bod} gewonnen! We gaan kijken wat je had kunnen winnen als je door was gespeeld.")
    else:
        print("NO DEAL, je mag 1 koffer openmaken.")

while aantal_koffers > 3:
    print(koffer_nummers)
    koffer_nummers.remove(int(input("Kies een koffer om open te maken.")))
    gekozen_koffer = random.choice(overgebleven_koffers)
    print(f"Er zit €{gekozen_koffer} in.")
    overgebleven_koffers.remove(gekozen_koffer)
    print(f"Je houdt deze bedragen over: {overgebleven_koffers}")
    aantal_koffers = len(overgebleven_koffers)
    if accepteren != "ja":
        bod = bereken_bankbod(overgebleven_koffers)
        print(f"De bank biedt €{bod}")
        accepteren = input("Wil je het bod van de bank accepteren? (ja/nee)")
        if accepteren == "ja":
            print(f"DEAL, je hebt €{bod} gewonnen! We gaan kijken wat je had kunnen winnen als je door was gespeeld.")
        else:
            print("NO DEAL, je mag 1 koffer openmaken.")

print(koffer_nummers)
koffer_nummers.remove(int(input("Kies een koffer om open te maken.")))
gekozen_koffer = random.choice(overgebleven_koffers)
print(f"Er zit €{gekozen_koffer} in.")
overgebleven_koffers.remove(gekozen_koffer)
print(f"Je houdt deze bedragen over: {overgebleven_koffers}")
aantal_koffers = len(overgebleven_koffers)
if accepteren != "ja":
    bod = bereken_bankbod(overgebleven_koffers)
    print(f"De bank biedt €{bod}")
    accepteren = input("Wil je het bod van de bank accepteren? (ja/nee)")
    if accepteren == "ja":
        print(f"DEAL, je hebt €{bod} gewonnen! We gaan de laatste koffer openmaken.")
    else:
        print("NO DEAL, we gaan de laatste koffer openmaken.")

print(koffer_nummers)
gekozen_koffer = random.choice(overgebleven_koffers)
print(f"Er zit €{gekozen_koffer} in de laatste koffer.")
overgebleven_koffers.remove(gekozen_koffer)
jouw_koffer = random.choice(overgebleven_koffers)
if accepteren == "ja":
    print(f"Dat betekend dat er €{jouw_koffer} in jouw koffer zat.")
else:
    print(f"Dat betekend dat er €{jouw_koffer} in jouw koffer zit en dat je dus €{jouw_koffer} hebt gewonnen!")