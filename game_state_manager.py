class GameStateManager:
    def __init__(self):
        self.current_state = 'start'
        self.screens = {}

    def set_state(self, state):
        self.current_state = state

    def get_state(self):
        return self.current_state
    
    def register_screen(self, name: str, screen):
        self.screens[name] = screen

    def get_screen(self, name: str):
        return self.screens.get(name)