import sqlite3

# Название файла базы данных SQLite
DATABASE_NAME = 'game.db'


def init_database():
    """
    Функция для создания базы данных и необходимых таблиц.
    Если таблицы уже существуют, они не будут пересозданы.
    """
    # Подключение к базе данных (если базы нет, она будет создана)
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Создание таблицы settings для хранения настроек игры
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS settings (
        id INTEGER PRIMARY KEY,
        use_music INTEGER NOT NULL DEFAULT 1,
        use_sound_effects INTEGER NOT NULL DEFAULT 1,
        music_volume REAL NOT NULL DEFAULT 1.0,
        sound_effects_volume REAL NOT NULL DEFAULT 1.0,
        show_intro INTEGER NOT NULL DEFAULT 1,
        difficulty_level INTEGER NOT NULL DEFAULT 1
    )
    ''')

    # Создание таблицы game_state для хранения состояния игры
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS game_state (
        id INTEGER PRIMARY KEY,
        selected_difficulty INTEGER NOT NULL DEFAULT 1,
        current_level INTEGER NOT NULL DEFAULT 1,
        score INTEGER NOT NULL DEFAULT 0,
        elapsed_time TEXT NOT NULL DEFAULT '00:00:00',
        lives INTEGER NOT NULL DEFAULT 5
    )
    ''')

    # Проверка на наличие записей в таблице settings и добавление записи по умолчанию, если она отсутствует
    cursor.execute('SELECT COUNT(*) FROM settings')
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO settings (id) VALUES (1)')

    # Проверка на наличие записей в таблице game_state и добавление записи по умолчанию, если она отсутствует
    cursor.execute('SELECT COUNT(*) FROM game_state')
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO game_state (id) VALUES (1)')

    # Сохранение изменений и закрытие соединения с базой данных
    conn.commit()
    conn.close()


def get_settings():
    """
    Функция для получения текущих настроек игры из таблицы settings.
    Возвращает словарь с настройками.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM settings WHERE id = 1')
    row = cursor.fetchone()
    conn.close()

    if row:
        settings = {
            'use_music': row[1],
            'use_sound_effects': row[2],
            'music_volume': row[3],
            'sound_effects_volume': row[4],
            'show_intro': row[5],
            'difficulty_level': row[6]
        }
        return settings
    return None


def get_game_state():
    """
    Функция для получения текущего состояния игры из таблицы game_state.
    Возвращает словарь с состоянием игры.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM game_state WHERE id = 1')
    row = cursor.fetchone()
    conn.close()

    if row:
        game_state = {
            'selected_difficulty': row[1],
            'current_level': row[2],
            'score': row[3],
            'elapsed_time': row[4],
            'lives': row[5]
        }
        return game_state
    return None


def update_settings(use_music, use_sound_effects, music_volume, sound_effects_volume, show_intro, difficulty_level):
    """
    Функция для обновления настроек игры в таблице settings.

    Параметры:
    use_music (int): Использование музыки (1 - включено, 0 - выключено)
    use_sound_effects (int): Использование звуковых эффектов (1 - включено, 0 - выключено)
    music_volume (float): Громкость музыки (от 0.0 до 1.0)
    sound_effects_volume (float): Громкость звуковых эффектов (от 0.0 до 1.0)
    show_intro (int): Показ начальной заставки (1 - включено, 0 - выключено)
    difficulty_level (int): Уровень сложности (от 1 до 10)
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE settings
    SET use_music = ?, use_sound_effects = ?, music_volume = ?, sound_effects_volume = ?, show_intro = ?, difficulty_level = ?
    WHERE id = 1
    ''', (use_music, use_sound_effects, music_volume, sound_effects_volume, show_intro, difficulty_level))
    conn.commit()
    conn.close()


def update_game_state(selected_difficulty, current_level, score, elapsed_time, lives):
    """
    Функция для обновления состояния игры в таблице game_state.

    Параметры:
    selected_difficulty (int): Выбранный уровень сложности (от 1 до 10)
    current_level (int): Текущий уровень игры (от 1 до 10)
    score (int): Текущее количество набранных очков (>= 0)
    elapsed_time (str): Время, прошедшее от начала игры (формат 'HH:MM:SS')
    lives (int): Текущее количество жизней персонажа (>= 0)
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE game_state
    SET selected_difficulty = ?, current_level = ?, score = ?, elapsed_time = ?, lives = ?
    WHERE id = 1
    ''', (selected_difficulty, current_level, score, elapsed_time, lives))
    conn.commit()
    conn.close()


"""

ПРИМЕР ИСПОЛЬЗОВАНИЯ:

import game_database

# Инициализация базы данных (создание таблиц и запись значений по умолчанию)
game_database.init_database()

# Получение текущих настроек игры
settings = game_database.get_settings()
print("Current settings:", settings)

# Обновление настроек игры
game_database.update_settings(1, 1, 0.5, 0.5, 1, 5)

# Получение текущего состояния игры
game_state = game_database.get_game_state()
print("Current game state:", game_state)

# Обновление состояния игры
game_database.update_game_state(3, 2, 150, '00:30:00', 3)

"""
