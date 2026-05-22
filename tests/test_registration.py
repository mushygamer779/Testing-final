import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users

@pytest.fixture(scope="module")
def setup_database():
    """Фикстура для настройки базы данных перед тестами и её очистки после."""
    create_db()
    yield
    try:
        os.remove('users.db')
    except PermissionError:
        pass

@pytest.fixture
def connection():
    """Фикстура для получения соединения с базой данных и его закрытия после теста."""
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()


def test_create_db(setup_database, connection):
    """Тест создания базы данных и таблицы пользователей."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "Таблица 'users' должна существовать в базе данных."

def test_add_new_user(setup_database, connection):
    """Тест добавления нового пользователя."""
    add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Пользователь должен быть добавлен в базу данных."

def test_authinticate_user_success(setup_database):
    """Тест успешной аутентификации пользователя."""
    add_user('cat', 'authuser@example.com', '12345')
    assert authenticate_user('cat', '12345'), "Пользователь должен быть успешно аутентифицирован."

def test_display_users(setup_database, connection):
    """Тест отображения списка пользователей."""
    add_user('pop','pop@example.com', '12345')
    cursor = connection.cursor()
    cursor.execute("SELECT username, email FROM users;")
    users = cursor.fetchall()
    assert users, "Список пользователей не должен быть пустым."

def test_user_choice_invalid_input(monkeypatch):
    """Тест обработки неверного ввода при выборе действия."""
    from registration.registration import user_choice
    
    # 1. Simulate the user typing '3' (an invalid input)
    monkeypatch.setattr('builtins.input', lambda _: '3')
    
    # 2. Call the function (it will automatically use '3' instead of pausing)
    choice = user_choice()
    
    # 3. Assert that the choice is indeed invalid (not '1' or '2')
    assert choice not in ['1', '2'], "Выбор не должен быть 1 или 2, если ввод неверный."

# Возможные варианты тестов:
"""
Тест добавления пользователя с существующим логином.
Тест успешной аутентификации пользователя.
Тест аутентификации несуществующего пользователя.
Тест аутентификации пользователя с неправильным паролем.
Тест отображения списка пользователей.
"""