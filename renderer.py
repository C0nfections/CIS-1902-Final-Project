import pygame

class Renderer:
    def __init__(self, screen: pygame.Surface, grid_size: int, tile_size: int):
        self.screen = screen
        self.grid_size = grid_size
        self.tile_size = tile_size
        self.grid_width = tile_size * grid_size
        self.score_panel_width = 200
        self.colors = {
            'background': (187, 173, 160),
            'score_panel': (170, 156, 143),  # Slightly darker than background
            'empty_cell': (205, 193, 180),
            'text_dark': (119, 110, 101),
            'text_light': (249, 246, 242),
            'tiles': {
                2: (238, 228, 218),
                4: (237, 224, 200),
                8: (242, 177, 121),
                16: (245, 149, 99),
                32: (246, 124, 95),
                64: (246, 94, 59),
                128: (237, 207, 114),
                256: (237, 204, 97),
                512: (237, 200, 80),
                1024: (237, 197, 63),
                2048: (237, 194, 46)
            }
        }
        self.fonts = {
            'score_label': pygame.font.Font(None, 36),
            'score_value': pygame.font.Font(None, 48),
            'tile': pygame.font.Font(None, 80)
        }

    def draw_game(self, game) -> None:
        self.screen.fill(self.colors['background'])
        
        pygame.draw.rect(
            self.screen,
            self.colors['score_panel'],
            (self.grid_width, 0, self.score_panel_width, self.screen.get_height())
        )
        
        self.draw_scores(game.score, game.best_score)
        self.draw_grid()
        
        for tile in game.board.tiles.values():
            self.draw_tile(tile)
        
        pygame.display.flip()

    def draw_scores(self, score: int, best_score: int) -> None:
        score_x = self.grid_width + 20
        
        score_label = self.fonts['score_label'].render("Score", True, self.colors['text_dark'])
        score_value = self.fonts['score_value'].render(str(score), True, self.colors['text_light'])
        
        self.screen.blit(score_label, (score_x, 50))
        self.screen.blit(score_value, (score_x, 90))
        
        best_label = self.fonts['score_label'].render("Best", True, self.colors['text_dark'])
        best_value = self.fonts['score_value'].render(str(best_score), True, self.colors['text_light'])
        
        self.screen.blit(best_label, (score_x, 180))
        self.screen.blit(best_value, (score_x, 220))

    def draw_grid(self) -> None:
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                self.draw_cell(row, col)

    def draw_cell(self, row: int, col: int) -> None:
        pygame.draw.rect(
            self.screen,
            self.colors['empty_cell'],
            (
                col * self.tile_size + 4,
                row * self.tile_size + 4,
                self.tile_size - 8,
                self.tile_size - 8
            ),
            border_radius=8
        )

    def draw_tile(self, tile) -> None:
        color = self.colors['tiles'].get(tile.value, self.colors['tiles'][2048])
        text_color = self.colors['text_dark'] if tile.value in [2, 4] else self.colors['text_light']
        
        pygame.draw.rect(
            self.screen,
            color,
            (
                tile.x + 4,
                tile.y + 4,
                self.tile_size - 8,
                self.tile_size - 8
            ),
            border_radius=8
        )
        
        text = self.fonts['tile'].render(str(tile.value), True, text_color)
        text_rect = text.get_rect(
            center=(
                tile.x + self.tile_size // 2,
                tile.y + self.tile_size // 2
            )
        )
        self.screen.blit(text, text_rect)