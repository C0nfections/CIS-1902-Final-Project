class GameStateManager:
    def __init__(self):
        self.current_state = 'start'

    def set_state(self, state):
        self.current_state = state

    def get_state(self):
        return self.current_state