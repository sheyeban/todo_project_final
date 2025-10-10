import json #чтение/запись json
import os #проверка существования файла

DATA_PATH = os.path.join("data", "tasks.json") #делает путь универсальным

def load_db(): #загрузить базу данных
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data 

def save_db(data): #сохранить базу данных
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def ensure_db(): #проверка существования файла базы, если нет - создает пустой
    if not os.path.exists(DATA_PATH):
        os.makedirs("data", exist_ok=True)
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump({"users": {}}, f, indent=4, ensure_ascii=False)


