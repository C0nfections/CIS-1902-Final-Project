import pygame
from game import Game
from renderer import Renderer
import requests


class StartScreen:
    def __init__(self, display: pygame.Surface, game_state_manager):
        self.display = display
        self.game_state_manager = game_state_manager
        self.background_color = (237, 194, 46)
        self.text_color = (119, 110, 101)

        self.font_large = pygame.font.Font(None, 60)
        self.font_medium = pygame.font.Font(None, 40)

        self.title = self.font_large.render("2048", True, self.text_color)
        self.title_rect = self.title.get_rect(
            center=(self.display.get_width() // 2, self.display.get_height() // 3)
        )

        self.play_text = self.font_medium.render(
            "Press SPACE to Play", True, self.text_color
        )
        self.play_rect = self.play_text.get_rect(
            center=(self.display.get_width() // 2, self.display.get_height() // 2)
        )

        self.leaderboard_text = self.font_medium.render(
            "Press L for Leaderboard", True, self.text_color
        )
        self.leaderboard_rect = self.leaderboard_text.get_rect(
            center=(self.display.get_width() // 2, self.display.get_height() // 2 + 60)
        )

    def update(self) -> bool:
        self.display.fill(self.background_color)
        self.display.blit(self.title, self.title_rect)
        self.display.blit(self.play_text, self.play_rect)
        self.display.blit(self.leaderboard_text, self.leaderboard_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.game_state_manager.set_state("game")
                elif event.key == pygame.K_l:
                    self.game_state_manager.set_state("leaderboard")
        return True


class GameScreen:
    def __init__(
        self,
        display: pygame.Surface,
        game_state_manager,
        grid_size: int,
        tile_size: int,
    ):
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

            if not self.game.moving:
                if self.game.win and not self.game.has_shown_win:
                    self.game_state_manager.set_state("win")
                    self.game.has_shown_win = True
                elif self.game.is_game_over():
                    self.game_state_manager.set_state("end")

        self.renderer.draw_game(self.game)
        self.clock.tick(60)

        return True


class EndScreen:
    def __init__(self, display: pygame.Surface, game_state_manager):
        self.display = display
        self.game_state_manager = game_state_manager
        self.game_screen = None
        self.score_screen = None
        self.font = pygame.font.Font(None, 60)
        self.text = self.font.render("Game Over!", True, (255, 255, 255))
        self.text_rect = self.text.get_rect(
            center=(self.display.get_width() // 2, self.display.get_height() // 2 - 50)
        )
        self.instruction = pygame.font.Font(None, 36).render(
            "Press ENTER to submit score or R to restart", True, (255, 255, 255)
        )
        self.instruction_rect = self.instruction.get_rect(
            center=(self.display.get_width() // 2, self.display.get_height() // 2 + 50)
        )

    def set_game_screen(self, game_screen) -> None:
        self.game_screen = game_screen

    def set_score_screen(self, score_screen) -> None:
        self.score_screen = score_screen

    def update(self) -> bool:
        self.display.fill((150, 20, 20))
        self.display.blit(self.text, self.text_rect)
        self.display.blit(self.instruction, self.instruction_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    if self.game_screen:
                        self.game_screen.reset_game()
                    self.game_state_manager.set_state("game")
                elif event.key == pygame.K_RETURN:
                    if self.score_screen and self.game_screen:
                        self.score_screen.set_score(self.game_screen.game.score)
                        self.game_state_manager.set_state("submit_score")
        return True


class WinScreen:
    def __init__(self, display: pygame.Surface, game_state_manager):
        self.display = display
        self.game_state_manager = game_state_manager
        self.game_screen = None
        self.score_screen = None
        self.font = pygame.font.Font(None, 60)
        self.text = self.font.render("You Won!", True, (255, 255, 255))
        self.text_rect = self.text.get_rect(
            center=(self.display.get_width() // 2, self.display.get_height() // 2 - 50)
        )
        self.instruction = pygame.font.Font(None, 36).render(
            "Press ENTER to submit score, C to continue, R to restart, or ESC for menu",
            True,
            (255, 255, 255),
        )
        self.instruction_rect = self.instruction.get_rect(
            center=(self.display.get_width() // 2, self.display.get_height() // 2 + 50)
        )

    def set_game_screen(self, game_screen) -> None:
        self.game_screen = game_screen

    def set_score_screen(self, score_screen) -> None:
        self.score_screen = score_screen

    def update(self) -> bool:
        self.display.fill((50, 150, 50))
        self.display.blit(self.text, self.text_rect)
        self.display.blit(self.instruction, self.instruction_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    if self.game_screen:
                        self.game_screen.reset_game()
                    self.game_state_manager.set_state("game")
                elif event.key == pygame.K_c:
                    self.game_state_manager.set_state("game")
                elif event.key == pygame.K_RETURN:
                    if self.score_screen and self.game_screen:
                        self.score_screen.set_score(self.game_screen.game.score)
                        self.game_state_manager.set_state("submit_score")
                elif event.key == pygame.K_ESCAPE:
                    if self.game_screen:
                        self.game_screen.reset_game()
                    self.game_state_manager.set_state("start")
        return True


class LeaderboardScreen:
    def __init__(self, display: pygame.Surface, game_state_manager):
        self.display = display
        self.game_state_manager = game_state_manager
        self.font_title = pygame.font.Font(None, 60)
        self.font_scores = pygame.font.Font(None, 36)
        self.font_instructions = pygame.font.Font(None, 24)
        self.leaderboard = []
        self.error_message = None
        self.colors = {
            "background": (70, 130, 180),
            "text": (255, 255, 255),
            "highlight": (255, 215, 0),
            "instructions": (200, 200, 200),
            "error": (255, 100, 100),
        }
        self.update_leaderboard()

    def update_leaderboard(self) -> None:
        try:
            response = requests.get("http://127.0.0.1:8000/get-leaderboard/", timeout=5)
            if response.status_code == 200:
                self.leaderboard = response.json()
                self.error_message = None
            else:
                self.error_message = f"Server error: {response.status_code}"
        except requests.RequestException:
            self.error_message = "Cannot connect to server. Is it running?"

    def draw_header(self) -> None:
        title = self.font_title.render("Leaderboard", True, self.colors["text"])
        title_rect = title.get_rect(center=(self.display.get_width() // 2, 50))
        self.display.blit(title, title_rect)

        if not self.error_message:
            headers = ["Rank", "Player", "Score"]
            header_widths = [100, 200, 150]
            start_x = 50
            for header, width in zip(headers, header_widths):
                text = self.font_scores.render(header, True, self.colors["highlight"])
                self.display.blit(text, (start_x, 120))
                start_x += width

    def draw_scores(self) -> None:
        if self.error_message:
            error_text = self.font_scores.render(
                self.error_message, True, self.colors["error"]
            )
            error_rect = error_text.get_rect(
                center=(self.display.get_width() // 2, 200)
            )
            self.display.blit(error_text, error_rect)

            retry_text = self.font_instructions.render(
                "Press R to retry", True, self.colors["text"]
            )
            retry_rect = retry_text.get_rect(
                center=(self.display.get_width() // 2, 250)
            )
            self.display.blit(retry_text, retry_rect)
            return

        start_y = 180
        line_height = 40

        if not self.leaderboard:
            no_scores = self.font_scores.render(
                "No scores yet!", True, self.colors["text"]
            )
            no_scores_rect = no_scores.get_rect(
                center=(self.display.get_width() // 2, start_y)
            )
            self.display.blit(no_scores, no_scores_rect)
            return

        for i, entry in enumerate(self.leaderboard[:10]):
            y_pos = start_y + i * line_height

            rank_text = self.font_scores.render(f"#{i+1}", True, self.colors["text"])
            self.display.blit(rank_text, (50, y_pos))

            name = entry.get("name", "Unknown")
            name_text = self.font_scores.render(name, True, self.colors["text"])
            self.display.blit(name_text, (150, y_pos))

            score = entry.get("score", 0)
            score_text = self.font_scores.render(f"{score}", True, self.colors["text"])
            self.display.blit(score_text, (350, y_pos))

    def draw_instructions(self) -> None:
        instructions = self.font_instructions.render(
            "Press ESC to return to menu", True, self.colors["instructions"]
        )
        instructions_rect = instructions.get_rect(
            center=(self.display.get_width() // 2, self.display.get_height() - 30)
        )
        self.display.blit(instructions, instructions_rect)

    def update(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state_manager.set_state("start")
                elif event.key == pygame.K_r and self.error_message:
                    self.update_leaderboard()

        self.display.fill(self.colors["background"])
        self.draw_header()
        self.draw_scores()
        self.draw_instructions()
        pygame.display.flip()

        return True


class ScoreSubmissionScreen:
    def __init__(self, display: pygame.Surface, game_state_manager):
        self.display = display
        self.game_state_manager = game_state_manager
        self.game_screen = None
        self.font = pygame.font.Font(None, 48)
        self.name = ""
        self.score = 0
        self.error_message = None
        self.colors = {
            "background": (70, 130, 180),
            "text": (255, 255, 255),
            "input": (200, 200, 200),
            "error": (255, 100, 100),
        }

    def set_game_screen(self, game_screen) -> None:
        self.game_screen = game_screen

    def set_score(self, score: int) -> None:
        self.score = score

    def submit_score(self) -> None:
        if not self.name:
            return

        try:
            response = requests.post(
                "http://localhost:8000/submit-score/",
                json={"name": self.name, "score": self.score},
            )
            print(f"Score submission response: {response.status_code}")
            if response.status_code == 200:
                print("Score submitted successfully")
                if self.game_screen:
                    self.game_screen.reset_game()
                self.game_state_manager.set_state("start")
        except requests.RequestException as e:
            self.error_message = "Failed to submit score. Is the server running?"
            print(f"Failed to submit score: {e}")

    def update(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.name:
                    self.submit_score()
                elif event.key == pygame.K_ESCAPE:
                    if self.game_screen:
                        self.game_screen.reset_game()
                    self.game_state_manager.set_state("start")
                elif event.key == pygame.K_BACKSPACE:
                    self.name = self.name[:-1]
                elif len(self.name) < 15 and event.unicode.isalnum():
                    self.name += event.unicode

        self.display.fill(self.colors["background"])

        score_text = self.font.render(
            f"Your Score: {self.score}", True, self.colors["text"]
        )
        score_rect = score_text.get_rect(center=(self.display.get_width() // 2, 100))
        self.display.blit(score_text, score_rect)

        prompt = self.font.render("Enter your name:", True, self.colors["text"])
        prompt_rect = prompt.get_rect(center=(self.display.get_width() // 2, 200))
        self.display.blit(prompt, prompt_rect)

        input_text = self.font.render(f"{self.name}_", True, self.colors["input"])
        input_rect = input_text.get_rect(center=(self.display.get_width() // 2, 300))
        self.display.blit(input_text, input_rect)

        instructions = pygame.font.Font(None, 36).render(
            "Press ENTER to submit or ESC to cancel", True, self.colors["text"]
        )
        instructions_rect = instructions.get_rect(
            center=(self.display.get_width() // 2, 400)
        )
        self.display.blit(instructions, instructions_rect)

        pygame.display.flip()
        return True
