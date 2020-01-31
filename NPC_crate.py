# Class for interactable crates in the game
# Ideally when the player collides with a crate
# it will move 1 tile in the direction of the player's movement.

class Crate:
    def __init__(self, x, y, image='./assets/NPCs/large_box.png'):

        super().__init__(x, y)

        #movement speed
        self.delta = 350

        #crate position
        self.x = x
        self.y = y

        #crate image
        self.image = pygame.image.load(image).convert_alpha
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()

