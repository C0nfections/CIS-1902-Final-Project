import pygame
from game_state_manager import GameStateManager
from screens import StartScreen, GameScreen, EndScreen

def main():
    pygame.init()
    
    GRID_SIZE = 4
    TILE_SIZE = 800 // GRID_SIZE
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 800
    
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("2048")
    
    game_state_manager = GameStateManager()
    
    start_screen = StartScreen(screen, game_state_manager)
    game_screen = GameScreen(screen, game_state_manager, GRID_SIZE, TILE_SIZE)
    end_screen = EndScreen(screen, game_state_manager)
    end_screen.set_game_screen(game_screen)

    game_state_manager.register_screen('start', start_screen)
    game_state_manager.register_screen('game', game_screen)
    game_state_manager.register_screen('end', end_screen)

    end_screen.set_game_screen(game_screen)
    
    running = True
    while running:
        current_state = game_state_manager.get_state()
        
        if current_state == 'start':
            running = start_screen.update()
        elif current_state == 'game':
            running = game_screen.update()
        elif current_state == 'end':
            running = end_screen.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()
