import pygame
from game_state_manager import GameStateManager
from screens import (
    StartScreen,
    GameScreen,
    EndScreen,
    WinScreen,
    LeaderboardScreen,
    ScoreSubmissionScreen,
)


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
    win_screen = WinScreen(screen, game_state_manager)
    leaderboard_screen = LeaderboardScreen(screen, game_state_manager)
    score_submission_screen = ScoreSubmissionScreen(screen, game_state_manager)

    end_screen.set_game_screen(game_screen)
    end_screen.set_score_screen(score_submission_screen)
    win_screen.set_game_screen(game_screen)
    win_screen.set_score_screen(score_submission_screen)
    score_submission_screen.set_game_screen(game_screen)

    previous_state = None
    running = True

    while running:
        current_state = game_state_manager.get_state()

        if current_state != previous_state:
            if current_state == "leaderboard":
                leaderboard_screen.update_leaderboard()
            previous_state = current_state

        if current_state == "start":
            running = start_screen.update()
        elif current_state == "game":
            running = game_screen.update()
        elif current_state == "end":
            running = end_screen.update()
        elif current_state == "win":
            running = win_screen.update()
        elif current_state == "leaderboard":
            running = leaderboard_screen.update()
        elif current_state == "submit_score":
            running = score_submission_screen.update()

    pygame.quit()


if __name__ == "__main__":
    main()
