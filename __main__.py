import pygame
import league

if __name__ == "__main__":
    e = league.Engine('Free Palestine')
    e.init_pygame()

    e.events[pygame.QUIT] = e.stop
    e.run()
