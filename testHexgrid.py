import hexgrid, ant, fsa
import math
import pygame

map = hexgrid.Hexgrid(13, 21)
testAnt = ant.Ant((0, 0, 0))
testAnt.setMap(map)
antSprite = ant.AntSprite(testAnt)
testAnt.move()

# main loop
running = True
clock = pygame.time.Clock()
while running:
    # event handling
    for event in pygame.event.get():
        # check for quit
        if event.type == pygame.QUIT:
            running = False
            break

    map.render()
    antSprite.draw(map.screen)
    pygame.display.flip()
    clock.tick(5)

pygame.quit()
