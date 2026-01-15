import os
import time
import re
import sys

def ask_latin_name(prompt="Введи своє ім'я (латинськими літерами, напр. Ivan): "):
    pattern = re.compile(r"^[A-Za-z]+$")
    while True:
        name = input(prompt).strip()
        if not name:
            print("Ім'я не може бути пустим. Спробуй ще.")
            continue
        if pattern.match(name):
            return name
        print("Невірний формат. Використай тільки латинські літери (A-Z).")

def yes_no(prompt):
    ans = input(prompt + " [y/N]: ").strip().lower()
    return ans in ("y", "yes", "так", "t", "yep")

def main():
    user = ask_latin_name()
    folder_name = f"Щоденник_{user}"
    if os.path.exists(folder_name):
        print(f"Папка '{folder_name}' вже існує.")
    else:
        try:
            os.mkdir(folder_name)
            print(f"Папку '{folder_name}' створено.")
        except Exception as e:
            print("Помилка при створенні папки:", e)
            sys.exit(1)

    file_name = "Мої_записи.txt"
    file_path = os.path.join(folder_name, file_name)

    print("\nДодай запис у щоденник читача.")
    book = input("Назва книги: ").strip()
    quote = input("Улюблена цитата з цієї книги: ").strip()

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    entry_lines = [
        f"Дата: {timestamp}",
        f"Книга: {book or '—'}",
        f"Цитата: {quote or '—'}",
        "-" * 40,
    ]
    try:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write("\n".join(entry_lines) + "\n")
        print(f"\nЗапис додано до файлу: {file_path}")
    except Exception as e:
        print("Помилка при записі у файл:", e)
        sys.exit(1)

    # Читання файлу та вивід вмісту
    print("\n--- Вміст файлу щоденника ---")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            print(content if content else "(файл порожній)")
    except Exception as e:
        print("Помилка при читанні файлу:", e)
        sys.exit(1)

    # Опціональне видалення файлу
    print()
    if yes_no(f"Бажаєш видалити файл '{file_name}'?"):
        try:
            os.remove(file_path)
            print(f"Файл '{file_name}' видалено.")
            # якщо папка порожня, запропонувати видалити її
            try:
                if not os.listdir(folder_name):
                    if yes_no(f"Папка '{folder_name}' порожня. Видалити папку?"):
                        os.rmdir(folder_name)
                        print(f"Папка '{folder_name}' видалена.")
            except Exception:
                pass
        except Exception as e:
            print("Не вдалося видалити файл:", e)
    else:
        print("Видалення скасовано. Файл збережено.")

if __name__ == "__main__":
    main()