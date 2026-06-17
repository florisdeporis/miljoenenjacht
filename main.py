import pygame
import sys

pygame.init()
breedte, hoogte = 600, 400
scherm = pygame.display.set_mode((breedte, hoogte))
pygame.display.set_caption("Unix Stuiter Cirkel")
klok = pygame.time.Clock()

x, y = 100, 100
stap_x, stap_y = 6, 6

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    x += stap_x
    y += stap_y

    if x > breedte - 20 or x < 20: stap_x *= -1
    if y > hoogte - 20 or y < 20: stap_y *= -1

    scherm.fill((15, 15, 15)) # Bijna zwart
    pygame.draw.circle(scherm, (255, 100, 0), (x, y), 20) # Oranje cirkel
    pygame.display.flip()
    klok.tick(60)