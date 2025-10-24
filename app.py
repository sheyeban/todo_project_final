from utils import ensure_db
from users import register_user, login_user


def task_menu(username):
    from utils import load_db, save_db
    from datetime import datetime, timedelta

    db = load_db()

    while True:
        print(f"\n=== Меню задач для {username} ===")
        print("1. Добавить задачу")
        print("2. Показать все задачи")
        print("3. Отметить выполненной")
        print("4. Удалить задачу")
        print("5. Показать выполненные задачи")
        print("6. Редактировать задачу")
        print("7. Выйти в главное меню")

        choice = input("Введите пункт: ")

        #добавление задачи
        if choice == "1":
            title = input("Введите название задачи: ")
            priority = input("Введите приоритет (низкий/средний/высокий): ")
            deadline_str = input("Введите дедлайн (ГГГГ-ММ-ДД ЧЧ:ММ): ")

            try:
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")
                deadline_str = deadline.strftime("%Y-%m-%d %H:%M")
            except ValueError:
                print("Неверный формат даты, дедлайн не будет установлен.")
                deadline_str = None

            new_task = {
                "title": title,
                "priority": priority,
                "deadline": deadline_str,
                "done": False
            }

            db["users"][username]["tasks"].append(new_task)
            save_db(db)
            print("Задача добавлена.")

        #показать все задачи
        elif choice == "2":
            tasks = db["users"][username]["tasks"]
            if not tasks:
                print("Пока нет задач.")
            else:
                sort_choice = input("Сортировать по приоритету? (да/нет): ").lower()
                if sort_choice == "да":
                    priority_order = {"высокий": 1, "средний": 2, "низкий": 3}
                    tasks = sorted(tasks, key=lambda x: priority_order.get(x["priority"], 4))

                now = datetime.now()
                for i, t in enumerate(tasks, start=1):
                    status = "✓" if t["done"] else "✗"
                    line = f"{i}. [{status}] {t['title']} (приоритет: {t['priority']})"

                    if t["deadline"]:
                        try:
                            deadline = datetime.strptime(t["deadline"], "%Y-%m-%d %H:%M")
                            remaining = deadline - now
                            if remaining < timedelta(hours=0):
                                line += " — просрочено"
                            elif remaining <= timedelta(hours=24):
                                line += " — горит (меньше 24 часов)"
                        except ValueError:
                            pass

                    print(line)

        #отметить задачу выполненной
        elif choice == "3":
            tasks = db["users"][username]["tasks"]
            if not tasks:
                print("Нет задач для отметки.")
            else:
                for i, t in enumerate(tasks, start=1):
                    print(f"{i}. {t['title']}")
                num = int(input("Введите номер выполненной задачи: ")) - 1
                if 0 <= num < len(tasks):
                    tasks[num]["done"] = True
                    save_db(db)
                    print("Задача отмечена как выполненная.")

        #удалить задачу
        elif choice == "4":
            tasks = db["users"][username]["tasks"]
            if not tasks:
                print("Нет задач для удаления.")
            else:
                for i, t in enumerate(tasks, start=1):
                    print(f"{i}. {t['title']}")
                num = int(input("Введите номер задачи для удаления: ")) - 1
                if 0 <= num < len(tasks):
                    del tasks[num]
                    save_db(db)
                    print("Задача удалена.")

        #показать выполненные задачи
        elif choice == "5":
            tasks = db["users"][username]["tasks"]
            completed = [t for t in tasks if t["done"]]
            if not completed:
                print("Нет выполненных задач.")
            else:
                for i, t in enumerate(completed, start=1):
                    print(f"{i}. {t['title']} (приоритет: {t['priority']}, дедлайн: {t['deadline']})")

        #редактировать задачу
        elif choice == "6":
            tasks = db["users"][username]["tasks"]
            if not tasks:
                print("Нет задач для редактирования.")
            else:
                for i, t in enumerate(tasks, start=1):
                    print(f"{i}. {t['title']} (приоритет: {t['priority']}, дедлайн: {t['deadline']})")
                num = int(input("Введите номер задачи для редактирования: ")) - 1
                if 0 <= num < len(tasks):
                    task = tasks[num]
                    print("Что изменить:")
                    print("1. Название")
                    print("2. Приоритет")
                    print("3. Дедлайн")
                    field = input("Выберите пункт: ")

                    if field == "1":
                        new_title = input("Введите новое название: ")
                        task["title"] = new_title
                    elif field == "2":
                        new_priority = input("Введите новый приоритет (низкий/средний/высокий): ")
                        task["priority"] = new_priority
                    elif field == "3":
                        new_deadline = input("Введите новый дедлайн (ГГГГ-ММ-ДД ЧЧ:ММ): ")
                        try:
                            datetime.strptime(new_deadline, "%Y-%m-%d %H:%M")
                            task["deadline"] = new_deadline
                        except ValueError:
                            print("Неверный формат даты.")
                    else:
                        print("Неверный выбор.")

                    save_db(db)
                    print("Задача обновлена.")

        #выход в главное меню
        elif choice == "7":
            print("Возврат в главное меню.")
            break

        else:
            print("Неверный пункт меню. Попробуйте снова.")


def main():
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
            print("До встречи.")
            break

        else:
            print("Неверный пункт меню. Попробуйте снова.")


main()
