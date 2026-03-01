import os
import json


FILENAME = "tasks.json"


def load_tasks():
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, "r", encoding="utf-8") as file:
        return json.load(file)

def save_tasks(tasks):
    with open(FILENAME, "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=4)

def show_tasks(tasks):
    if not tasks:
        print("\nСписок задач пуст.\n")
        return

    print("\nСписок задач:")
    for i, task in enumerate(tasks, start=1):
        status = "+" if task["done"] else " "
        print(f"{i}. [{status}]: {task['title']}")
    print()

def add_tasks(tasks):
    title = input("Введите название задачи: ")
    tasks.append({"title": title, "done": False})
    save_tasks(tasks)
    print("Задача добавлена!\n")

def complete_tasks(tasks):
    show_tasks(tasks)
    try:
        index = int(input("Введите номер выполненной задачи: ")) - 1
        tasks[index]["done"] = True
        save_tasks(tasks)
        print("Статус задачи изменен!\n")
    except (ValueError, IndexError):
        print("Задачи под таким номером нет.\n")

def delete_tasks(tasks):
    show_tasks(tasks)
    try:
        index = int(input("Введите номер задачи, которую нужно удалить"))
        deleted = tasks.pop(index)
        save_tasks(tasks)
        print(f"Задача '{deleted['title']}' удалена!\n")
    except (ValueError, IndexError):
        print("Задачи под таким номером нет.\n")

def main():
    tasks = load_tasks()

    while True:
        print("/=== TODO LIST ===\\\n")
        print("1. Показать задачи")
        print("2. Добавить задачу")
        print("3. Отметить выполненной")
        print("4. Удалить задачу")
        print("5. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            show_tasks(tasks)
        if choice == "2":
            add_tasks(tasks)
        if choice == "3":
            complete_tasks(tasks)
        if choice == "4":
            delete_tasks(tasks)
        if choice == "5":
            print("Завершение программы.")
            break
        else:
            print("Нет такого действия.\n")

if __name__ == "__main__":
    main()


