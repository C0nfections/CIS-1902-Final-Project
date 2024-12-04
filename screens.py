import pygame
from game import Game
from renderer import Renderer
from button import Button
from fastapi import BackgroundTasks, FastAPI, HTTPException, Request

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
                self.game_state_manager.get_screen('end').set_final_score(self.game.get_score())
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
        self.text = None
        self.text_rect = None
        self.text_lines = []

        button_x = (self.display.get_width() - 400) // 2
        button_y = self.display.get_height() // 2 + 100
        self.button = Button(
            x=button_x,
            y=button_y,
            width=400,
            height=80,
            text="Add score to leaderboard",
            font=pygame.font.Font(None, 40),
            text_color=(255, 255, 255),
            button_color=(50, 150, 50),
            hover_color=(70, 200, 70),
            action=self.add_score_to_leaderboard  # Function that adds the score to leaderboard (to implement)
        )


    def set_game_screen(self, game_screen) -> None:
        self.game_screen = game_screen

    def add_score_to_leaderboard(self):
        pass
        # TO IMPLEMENT

        # """Submit the score to the FastAPI backend."""
        # username = "Player1"  # Replace with user input or dynamic data
        # data = {"username": username, "score": self.score}
        
        # try:
        #     response = requests.post(f"{self.api_url}/submit_score", json=data)
        #     if response.status_code == 200:
        #         print("Score submitted successfully!")
        #     else:
        #         print("Failed to submit score:", response.json())
        # except requests.RequestException as e:
        #     print("Error submitting score:", e)
        
    
    def set_final_score(self, score: int) -> None:
        self.text_lines = [
            "Game Over!",
            f"Score: {score}.",
            "Press R to Restart.",
        ]

    def update(self) -> bool:
        self.display.fill((150, 20, 20))

        for i, line in enumerate(self.text_lines):
            rendered_text = self.font.render(line, True, (255, 255, 255))
            text_rect = rendered_text.get_rect(
                center=(self.display.get_width() // 2, self.display.get_height() // 2 + i * 50 - 50)
            )
            self.display.blit(rendered_text, text_rect)

        self.button.draw(self.display)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    if self.game_screen:
                        self.game_screen.reset_game()
                    self.game_state_manager.set_state('game')

            self.button.handle_event(event)

        return True