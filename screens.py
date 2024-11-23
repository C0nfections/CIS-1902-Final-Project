import pygame
from game import Game
from renderer import Renderer

class StartScreen:
    def __init__(self, display: pygame.Surface, game_state_manager):
        self.display = display
        self.game_state_manager = game_state_manager
        self.font = pygame.font.Font(None, 60)
        self.text = self.font.render("Press Any Key to Start", True, (255, 255, 255))
        self.text_rect = self.text.get_rect(
            center=(self.display.get_width() // 2, self.display.get_height() // 2)
        )

    def update(self) -> bool:
        self.display.fill((70, 130, 180))
        self.display.blit(self.text, self.text_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                self.game_state_manager.set_state('game')
        return True

class GameScreen:
    def __init__(self, display: pygame.Surface, game_state_manager, grid_size: int, tile_size: int):
        self.display = display
        self.game_state_manager = game_state_manager
        self.game = Game()
        self.renderer = Renderer(display, grid_size, tile_size)
        self.clock = pygame.time.Clock()

    def reset_game(self) -> None:
        self.game.reset()

    def handle_input(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN and not self.game.moving:
                if event.key == pygame.K_r:
                    self.game.reset()
                elif event.key == pygame.K_LEFT:
                    self.game.process_movement("left")
                elif event.key == pygame.K_RIGHT:
                    self.game.process_movement("right")
                elif event.key == pygame.K_UP:
                    self.game.process_movement("up")
                elif event.key == pygame.K_DOWN:
                    self.game.process_movement("down")
        
        return True

    def update(self) -> bool:
        if not self.handle_input():
            return False

        if self.game.moving:
            self.game.update()
            
            if not self.game.moving and self.game.is_game_over():
                self.game_state_manager.set_state('end')
        
        self.renderer.draw_game(self.game)
        self.clock.tick(60)

        return True

class EndScreen:
    def __init__(self, display: pygame.Surface, game_state_manager):
        self.display = display
        self.game_state_manager = game_state_manager
        self.game_screen = None
        self.font = pygame.font.Font(None, 60)
        self.text = self.font.render("Game Over! Press R to Restart", True, (255, 255, 255))
        self.text_rect = self.text.get_rect(
            center=(self.display.get_width() // 2, self.display.get_height() // 2)
        )

    def set_game_screen(self, game_screen) -> None:
        self.game_screen = game_screen

    def update(self) -> bool:
        self.display.fill((150, 20, 20))
        self.display.blit(self.text, self.text_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    if self.game_screen:
                        self.game_screen.reset_game()
                    self.game_state_manager.set_state('game')
        return True