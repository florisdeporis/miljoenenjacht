import pygame
import sys
import random
from pygame.locals import *

pygame.init()
breedte, hoogte = 600, 400
scherm = pygame.display.set_mode((breedte, hoogte))
pygame.display.set_caption("Miljoenenjacht")
klok = pygame.time.Clock()

# --- KLEUREN & FONTS ---
WIT = (255, 255, 255)
ZWART = (0, 0, 0)
GOUD = (255, 215, 0)
ROOD = (200, 0, 0)
GROEN = (0, 200, 0)
BLAUW = (0, 0, 200)

# Standaard lettertype instellen (grootte 24 voor tekst, 60 voor grote titels)
font_klein = pygame.font.Font(None, 24)
font_groot = pygame.font.Font(None, 60)
font_mega = pygame.font.Font(None, 120)

# Een vaste lijst van alle 26 bedragen (voor het geldbord)
ALLE_BEDRAGEN = [
    0.01, 0.20, 0.50, 1, 5, 10, 20, 50, 100, 500, 1000, 2500,
    5000, 10000, 25000, 50000, 100000, 200000, 300000, 400000,
    500000, 750000, 1000000, 2000000, 2500000, 5000000
]

def teken_koffers(prompt_tekst, ingetypt):
    scherm.fill(BLAUW) # Mooie donkerblauwe studio-achtergrond
    
    # Teken de vraag en wat de speler typt
    tekst_prompt = font_klein.render(prompt_tekst + " " + ingetypt, True, WIT)
    scherm.blit(tekst_prompt, (20, 20))
    
    # Teken het grid met koffers
    for i in range(26):
        koffer_nr = i + 1
        rij = i // 7       # 7 koffers per rij
        kolom = i % 7      
        
        x = 50 + kolom * 70  # x-positie op het scherm
        y = 80 + rij * 70    # y-positie op het scherm
        
        if koffer_nr in koffer_nummers:
            # Koffer is nog dicht: teken een gouden blokje met het nummer
            pygame.draw.rect(scherm, GOUD, (x, y, 60, 50))
            tekst_nr = font_klein.render(str(koffer_nr), True, ZWART)
            scherm.blit(tekst_nr, (x + 20, y + 15))
        else:
            # Koffer is open: teken een leeg, donkergrijs vlak (of laat hem weg)
            pygame.draw.rect(scherm, (50, 50, 50), (x, y, 60, 50))

def teken_bord(prompt_tekst, ingetypt):
    scherm.fill(ZWART)
    
    # Vraag / Typ-veld bovenaan
    tekst_prompt = font_klein.render(prompt_tekst + " " + ingetypt, True, WIT)
    scherm.blit(tekst_prompt, (20, 20))
    
    # We splitsen de 26 bedragen in twee kolommen van 13
    voor_kolom_links = ALLE_BEDRAGEN[:13]
    voor_kolom_rechts = ALLE_BEDRAGEN[13:]
    
    for i in range(13):
        y_pos = 60 + i * 25
        
        # LINKER KOLOM
        bedrag_links = voor_kolom_links[i]
        if bedrag_links in overgebleven_koffers:
            # Teken rood of blauw blok met het bedrag
            pygame.draw.rect(scherm, ROOD, (50, y_pos, 150, 20))
            tekst_links = font_klein.render(f"€ {bedrag_links}", True, WIT)
            scherm.blit(tekst_links, (55, y_pos + 2))
        else:
            # Leeg blok als het bedrag weg is
            pygame.draw.rect(scherm, (30, 30, 30), (50, y_pos, 150, 20))
            
        # RECHTER KOLOM
        bedrag_rechts = voor_kolom_rechts[i]
        if bedrag_rechts in overgebleven_koffers:
            # Teken gouden blok met het bedrag
            pygame.draw.rect(scherm, GOUD, (350, y_pos, 150, 20))
            tekst_rechts = font_klein.render(f"€ {bedrag_rechts}", True, ZWART)
            scherm.blit(tekst_rechts, (355, y_pos + 2))
        else:
            pygame.draw.rect(scherm, (30, 30, 30), (350, y_pos, 150, 20))

def teken_linda(prompt_tekst, ingetypt, deal_status=""):
    # Dit is de "camera" gericht op Linda. We gebruiken nu gewoon een kleur.
    scherm.fill((200, 150, 200)) # Een zacht paarse studio-kleur
    
    # Wat zegt Linda?
    tekst_linda = font_groot.render("Linda:", True, ZWART)
    scherm.blit(tekst_linda, (50, 50))
    
    tekst_prompt = font_klein.render(prompt_tekst + " " + ingetypt, True, ZWART)
    scherm.blit(tekst_prompt, (50, 120))
    
    # Als er een deal of no deal is gesloten, schrijf het met koeienletters over het scherm
    if deal_status == "DEAL":
        tekst_deal = font_mega.render("DEAL", True, GROEN)
        scherm.blit(tekst_deal, (150, 200))
    elif deal_status == "NO DEAL":
        tekst_no_deal = font_mega.render("NO DEAL", True, ROOD)
        scherm.blit(tekst_no_deal, (60, 200))

def wacht_op_invoer(huidig_scherm_teken_functie, prompt_tekst=""):
    """Vervangt input(). Wacht tot de speler een getal of ja/nee typt in Pygame."""
    ingetypt = ""
    while True:
        # Teken hier steeds je scherm, anders bevriest het beeld!
        huidig_scherm_teken_functie(prompt_tekst, ingetypt)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN: # Speler drukt op Enter
                    return ingetypt
                elif event.key == K_BACKSPACE:
                    ingetypt = ingetypt[:-1]
                else:
                    ingetypt += event.unicode
        
        pygame.display.flip()
        klok.tick(30)

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
    gemiddelde = sum(overgebleven_koffers) / aantal_koffers
    
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
    0.01, 0.20, 0.50, 1, 5, 10, 20, 50, 100, 500, 1000, 2500,
    5000, 10000, 25000, 50000, 100000, 200000, 300000, 400000,
    500000, 750000, 1000000, 2000000, 2500000, 5000000
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
    print("Je had 5 koffers mogen openmaken.")
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
else:
    print("Je had 4 koffers mogen openmaken.")

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
else:
    print("Je had 3 koffers mogen openmaken.")

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
else:
    print("Je had 2 koffers mogen openmaken.")

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
else:
    print("Je had 1 koffer mogen openmaken.")

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
    else:
        print("Je had 1 koffer mogen openmaken.")

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
else:
    print("We gaan de laatste koffer openmaken.")

print(koffer_nummers)
gekozen_koffer = random.choice(overgebleven_koffers)
print(f"Er zit €{gekozen_koffer} in de laatste koffer.")
overgebleven_koffers.remove(gekozen_koffer)
jouw_koffer = random.choice(overgebleven_koffers)
if accepteren == "ja":
    if jouw_koffer > bod:
        print(f"Dat betekend dat er €{jouw_koffer} in jouw koffer zat. Je had dus meer dan €{bod} kunnen winnen als je was doorgespeeld.")
    else:
        print(f"Dat betekend dat er €{jouw_koffer} in jouw koffer zat. Dat is minder dan jouw €{bod}, dus het is goed dat je bent gestopt!")
else:
    print(f"Dat betekend dat er €{jouw_koffer} in jouw koffer zit en dat je dus €{jouw_koffer} hebt gewonnen!")
    