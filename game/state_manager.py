# Управление состояниями игры

class StateManager:
    def __init__(self):
        self.running = True
        self.current_level = 0
        self.state = 'game'
#        self.state = 'menu'  # Начальное состояние - главное меню

    def update(self):
        if self.state == 'menu':
            self.update_menu()
        elif self.state == 'game':
            self.update_game()
        elif self.state == 'game_over':
            self.update_game_over()

    def draw(self, screen):
        if self.state == 'menu':
            self.draw_menu(screen)
        elif self.state == 'game':
            self.draw_game(screen)
        elif self.state == 'game_over':
            self.draw_game_over(screen)

    def update_menu(self):
        # Логика обновления главного меню
        pass

    def draw_menu(self, screen):
        # Логика рисования главного меню
        pass

    def update_game(self):
        # Логика обновления игры (уровня)
        pass

    def draw_game(self, screen):
        # Логика рисования игры (уровня)
        pass

    def update_game_over(self):
        # Логика обновления экрана завершения игры
        pass

    def draw_game_over(self, screen):
        # Логика рисования экрана завершения игры
        pass

    def change_state(self, new_state):
        self.state = new_state
