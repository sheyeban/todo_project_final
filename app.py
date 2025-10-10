from utils import ensure_db, load_db, save_db
from users import register_user, login_user

def main(): #главная функция программы(меню)
    ensure_db()

    print("Добро пожаловать в To-Do List!")

    while True:
        print("\nМеню:")
        print("1. Войти")
        print("2. Зарегистрироваться")
        print("3. Выйти")

        choice = input("Выберите пункт: ")

        if choice == "1":
            username = input("Введите имя пользователя: ")
            password = input("Введите пароль: ")
            user = login_user(username, password)
            if user:
                task_menu(user)
        
        elif choice == "2":
            username = input("Придумайте имя пользователя: ")
            password = input("Придумайте пароль: ")
            register_user(username, password)
        
        elif choice == "3":
            print("До встречи!")
            break

        else:
            print("Неверный пункт меню. Попробуйте снова!")

def task_menu(username): #меню задач
    from utils import load_db, save_db
    db = load_db()

    while True:
        print(f"\n=== Меню задач для {username} ===")
        print("1. Добавить задачу")
        print("2. Показать все задачи")
        print("3. Отметить выполненной")
        print("4. Удалить задачу")
        print("5. Выйти в главное меню")

        choice = input("Введите пункт: ")

        if choice == "1": #добавление задачи
            title = input("Введите название задачи: ")
            new_task = {
                "title": title,
                "priority": "средний",
                "deadline": None,
                "done": False
            }
            db["users"][username]["tasks"].append(new_task)
            save_db(db)
            print("Задача добавлена!")

        elif choice == "2": #показать задачи
            tasks = db["users"][username]["tasks"]
            if not tasks:
                print("Пока нет задач")
            else:
                for i, t in enumerate(tasks, start=1):
                    status = "✓" if t["done"] else "✗"
                    print(f"{i}. [{status}] {t['title']} (приоритет: {t['priority']})")

        elif choice == "3": #отметить задачи выполненными
            tasks = db["users"][username]["tasks"]
            if not tasks:
                print("Нет задач для отметки")
            else:
                for i, t in enumerate(tasks, start=1):
                    print(f"{i}. {t['title']}")
                num = int(input("Введите номер выполненной задачи: ")) - 1
                if 0 <= num < len(tasks):
                    tasks[num]["done"] = True
                    save_db(db)
                    print("Задача отмечена как выполненная!")

        elif choice == "4": #удалить задачи
            tasks = db["users"][username]["tasks"]
            if not tasks:
                print("Нет задач для удаления")
            else:
                for i, t in enumerate(tasks, start=1):
                    print(f"{i}. {t['title']}")
                num = int(input("Введите номер задачи дляя удаления: ")) - 1
                if 0 <= num < len(tasks):
                    del tasks[num]
                    save_db(db)
                    print("Задача удалена!")
        
        elif choice == "5": #выйти в главное меню
            print("Возврат в главное меню...")
            break
            
        else:
            print("Неверный пункт меню. Попробуйте снова!")
main()