from utils import load_db, save_db

def register_user(username, password, role="user"): #функция, которая принимает имя, пароль и роль
    db = load_db()

    if username in db["users"]:
        print("Пользователь с таким именем уже существует!")
        return False

    db["users"][username] = {
        "password": password,
        "role": role,
        "tasks": []
    }

    save_db(db)
    print(f"Пользователь {username} успешно зарегистрирован!")
    return True

def login_user(username, password): #проверка логина и пароля
    db = load_db()

    if username not in db["users"]:
        print("Пользователь не найдеН!")
        return None
    
    if db["users"][username]["password"] != password:
        print("Неверный пароль!")
        return None
    
    print(f"Добро пожаловать, {username}!")
    return username
