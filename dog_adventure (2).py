# This is a comment to test git

import pygame
import random

# Initialize Pygame
pygame.init()
print("Pygame initialized")

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
RED = (255, 0, 0)
SKY_BLUE = (135, 206, 235)
GREEN = (34, 139, 34)
GRAVITY = 1
JUMP_STRENGTH = 15
ANIMAL_SIZE = 60
ANIMAL_WIDTH = 32
DOG_WIDTH = 90
DOG_HEIGHT = 60
XP_PER_ANIMAL = 10
XP_FOR_LEVEL_2 = 30
XP_FOR_LEVEL_3 = 100
MIN_ANIMAL_DISTANCE = 200
GRASS_HEIGHT = SCREEN_HEIGHT // 3  # Adjusted grass height

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dog Adventure")
print("Screen setup complete")

# Load textures
def load_image(filename, width, height):
    image = pygame.image.load(filename).convert_alpha()
    return pygame.transform.scale(image, (width, height))

# Ensure you set the correct path to your images here
grass_texture = load_image("grass.png", SCREEN_WIDTH, GRASS_HEIGHT)
cloud_image = load_image("cloud.png", 100, 60)
dog_image = load_image("Dog.png", DOG_WIDTH, DOG_HEIGHT)
animal_image = load_image("animal.png", ANIMAL_SIZE, ANIMAL_SIZE)

print("Textures loaded")

# Font setup
font = pygame.font.SysFont(None, 35)

# Classes

class Dog(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = dog_image
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = SCREEN_HEIGHT - DOG_HEIGHT - GRASS_HEIGHT // 3  # Adjusted to sit on the grass
        self.vel_y = 0
        self.is_jumping = False
        self.xp = 0
        self.level = 1
        print("Dog initialized")

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.vel_y = -JUMP_STRENGTH
            self.is_jumping = True

        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        if self.rect.y >= SCREEN_HEIGHT - self.rect.height - GRASS_HEIGHT // 3:
            self.rect.y = SCREEN_HEIGHT - self.rect.height - GRASS_HEIGHT // 3
            self.vel_y = 0
            self.is_jumping = False

    def gain_xp(self, amount):
        self.xp += amount
        print(f"XP gained: {self.xp}")
        if self.level == 1 and self.xp >= XP_FOR_LEVEL_2:
            self.level = 2
            print("Level up to 2")
        elif self.level == 2 and self.xp >= XP_FOR_LEVEL_3:
            self.level = 3
            print("Level up to 3")

def display_win_animation(screen):
    font = pygame.font.SysFont(None, 75)
    text = font.render("You Win!", True, (255, 215, 0))
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(3000)

def draw_ui(screen, dog):
    xp_text = font.render(f"XP: {dog.xp}", True, BLACK)
    level_text = font.render(f"Level: {dog.level}", True, BLACK)
    screen.blit(xp_text, (10, 10))
    screen.blit(level_text, (10, 40))

class Animal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = animal_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = SCREEN_HEIGHT - ANIMAL_SIZE - GRASS_HEIGHT // 3  # Adjusted to sit on the grass
        print(f"Animal created at ({x}, {y})")

def create_animal(existing_animals):
    attempts = 0
    while attempts < 50:  # Limit the number of attempts to avoid infinite loop
        x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH * 2)
        y = SCREEN_HEIGHT - ANIMAL_SIZE - GRASS_HEIGHT // 3
        if all(abs(x - animal.rect.x) > MIN_ANIMAL_DISTANCE for animal in existing_animals):
            animal = Animal(x, y)
            print("Animal created")
            return animal
        attempts += 1
    # If unable to find a valid position, return None
    print("Failed to create a valid animal position after many attempts")
    return None

def create_animals(num_animals):
    animals = pygame.sprite.Group()
    for _ in range(num_animals):
        animal = create_animal(animals)
        if animal:
            animals.add(animal)
    print("Animals created")
    return animals

# Main loop
def main():
    clock = pygame.time.Clock()
    dog = Dog()
    animals = create_animals(10)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(animals)
    all_sprites.add(dog)
    print("All sprites added")

    cloud_x = [random.randint(0, SCREEN_WIDTH) for _ in range(5)]
    cloud_y = [random.randint(0, SCREEN_HEIGHT // 2) for _ in range(5)]
    print("Clouds initialized")

    # Grass position and scrolling speed
    grass_x = 0
    grass_speed = 2

    running = True
    game_won = False

    print("Starting game loop")
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        all_sprites.update()

        if not game_won:
            # Move animals
            for animal in animals:
                animal.rect.x -= 5
                if animal.rect.x < -ANIMAL_SIZE:
                    animal.rect.x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH * 2)
                    animal.rect.y = SCREEN_HEIGHT - ANIMAL_SIZE - GRASS_HEIGHT // 3

            # Check for collisions
            collisions = pygame.sprite.spritecollide(dog, animals, False)
            for animal in collisions:
                if dog.rect.y + dog.rect.height <= animal.rect.y + 10:
                    animals.remove(animal)
                    dog.gain_xp(XP_PER_ANIMAL)
                    dog.vel_y = -5  # Tiny bounce upon landing on an animal
                    # Add a new animal to replace the removed one
                    new_animal = create_animal(animals)
                    if new_animal:
                        animals.add(new_animal)
                        all_sprites.add(new_animal)

            # Check if the dog has reached level 3
            if dog.level == 3:
                game_won = True

        # Draw everything
        screen.fill(SKY_BLUE)

        # Draw clouds with scrolling
        for i in range(len(cloud_x)):
            screen.blit(cloud_image, (cloud_x[i], cloud_y[i]))
            cloud_x[i] -= 1
            if cloud_x[i] < -100:
                cloud_x[i] = SCREEN_WIDTH

        # Draw grass with scrolling
        screen.blit(grass_texture, (grass_x, SCREEN_HEIGHT - GRASS_HEIGHT // 3))
        screen.blit(grass_texture, (grass_x + grass_texture.get_width(), SCREEN_HEIGHT - GRASS_HEIGHT // 3))  # Draw a second grass texture right after the first
        grass_x -= grass_speed
        if grass_x <= -grass_texture.get_width():
            grass_x = 0

        # Draw each animal
        for animal in animals:
            screen.blit(animal.image, animal.rect)
            print(f"Animal at ({animal.rect.x}, {animal.rect.y})")

        # Draw the dog last to ensure it appears in front
        screen.blit(dog.image, dog.rect)

        # Draw UI
        draw_ui(screen, dog)

        # Display the win animation if the game is won
        if game_won:
            display_win_animation(screen)
            running = False

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    if 

if __name__ == "__main__":
    main()
    #Adding another comment testing branches for git
