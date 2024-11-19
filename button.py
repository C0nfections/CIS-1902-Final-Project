import pygame

class Button:
    def __init__(self, x, y, width, height, text, font, text_color, button_color, hover_color, action=None):
        """
            x (int): X-coordinate of the button.
            y (int): Y-coordinate of the button.
            width (int): Width of the button.
            height (int): Height of the button.
            text (str): Text displayed on the button.
            font (pygame.font.Font): Font for the button text.
            text_color (tuple): Color of the text (RGB).
            button_color (tuple): Default button color (RGB).
            hover_color (tuple): Button color when hovered (RGB).
            action (function): Function to call when the button is clicked.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.button_color = button_color
        self.hover_color = hover_color
        self.action = action
        self.is_hovered = False

    def draw(self, screen):
        # Change color if the button is hovered
        color = self.hover_color if self.is_hovered else self.button_color

        # Draw the button rectangle
        pygame.draw.rect(screen, color, self.rect, border_radius=8)

        # Render the text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)

        # Draw the text
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered and self.action:
                self.action()