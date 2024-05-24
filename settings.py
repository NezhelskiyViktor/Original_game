# Конфигурационные настройки игры
class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 720
        self.caption = "Колобок: возвращение домой"
        self.fps = 60
        self.music_volume = 0.125
        self.sound_volume = 0.125
        self.sound = True
        self.music = True
        self.show_move = False
        self.difficulty_level = 0
        self.game_state = 1
