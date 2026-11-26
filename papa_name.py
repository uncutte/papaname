"""Имя папы по отчеству.

Запуск:  python papa_name.py
Нужен только Python 3 (tkinter идёт в комплекте на Windows/macOS).
Вводишь отчество (или ФИО целиком) - показывает имя отца.
"""
import re

NAMES = """
Александр Алексей Альберт Анатолий Андрей Антон Аркадий Арсений Артём Артур Богдан Борис
Вадим Валентин Валерий Василий Виктор Виталий Владимир Владислав Всеволод Вячеслав
Геннадий Георгий Герман Глеб Григорий Даниил Денис Дмитрий Евгений Егор Захар Иван Игорь
Илья Кирилл Константин Лев Леонид Лука Максим Марк Матвей Михаил Никита Николай Олег
Павел Пётр Роман Руслан Святослав Семён Сергей Станислав Степан Тимофей Тимур Фёдор
Филипп Эдуард Юрий Яков Ярослав Фома Кузьма Савва Ринат Рустам Ильдар Ренат Марат Айрат
Вениамин Игнат Ростислав Прохор Тарас Арсен Давид Самуил Абрам Исаак Моисей Соломон
Назар Макар Мирон Нестор Орест Елисей Платон Родион Савелий Трофим Эмиль Эрик Юлиан Ян
Остап Ефим Емельян Герасим Гавриил Гордей Климент Аким Влас Анвар Рамиль Эльдар Руфат
Заур Азамат Мурат Булат Ильназ Данил Любомир Мстислав Радик Рафаэль Лазарь Харитон
Аполлон Афанасий Демьян Дорофей Евдоким Иннокентий Касьян Меркурий Модест Назарий
Онисим Панкрат Парфён Порфирий Сидор Тихон Трифон Устин Фадей Феликс Эммануил Ермолай
""".split()

SPECIAL = {
    "Павел": "Павлович", "Лев": "Львович", "Яков": "Яковлевич", "Михаил": "Михайлович",
    "Даниил": "Данилович", "Гавриил": "Гаврилович", "Илья": "Ильич", "Лука": "Лукич",
    "Кузьма": "Кузьмич", "Фома": "Фомич", "Никита": "Никитич", "Савва": "Саввич",
    "Дмитрий": "Дмитриевич", "Георгий": "Георгиевич", "Пётр": "Петрович",
    "Рафаэль": "Рафаэльевич", "Эммануил": "Эммануилович", "Эмиль": "Эмильевич",
    "Харитон": "Харитонович", "Афанасий": "Афанасьевич",
}


def norm(s: str) -> str:
    return s.lower().replace("ё", "е")


def patronymic(name: str) -> str:
    if name in SPECIAL:
        return SPECIAL[name]
    if name.endswith("ий"):
        return name[:-2] + "ьевич"
    if name.endswith(("й", "ь")):
        return name[:-1] + "евич"
    return name + "ович"


# обратная таблица: отчество -> имя
REVERSE = {}
for _n in NAMES:
    REVERSE.setdefault(norm(patronymic(_n)), _n)
# мелкие частые варианты написания
REVERSE.update({norm("Даниилович"): "Даниил", norm("Гавриилович"): "Гавриил"})


def to_male(word: str):
    """Женское отчество -> мужское. Возвращает None, если это не отчество."""
    w = norm(word)
    if w.endswith("инична"):
        return w[:-6] + "ич"
    if w.endswith("ична"):
        return w[:-4] + "ич"
    if w.endswith("овна"):
        return w[:-4] + "ович"
    if w.endswith("евна"):
        return w[:-4] + "евич"
    if w.endswith(("ович", "евич", "ич")):
        return w
    return None


def father_name(text: str):
    """Возвращает (имя, точно_ли) или None."""
    for word in re.findall(r"[А-Яа-яЁё]+", text):
        m = to_male(word)
        if m is None:
            continue
        if m in REVERSE:
            return REVERSE[m], True
        # нет в словаре - пробуем угадать
        if m.endswith("ович") and len(m) > 5:
            return m[:-4].capitalize(), False
        if m.endswith("евич") and len(m) > 5:
            stem = m[:-4]
            if stem.endswith("ь"):
                return (stem[:-1] + "ий").capitalize(), False
            return stem.capitalize() + "й / ь", False
        if m.endswith("ич") and len(m) > 3:
            return m[:-2].capitalize() + "а / я", False
    return None


def main():
    import tkinter as tk

    BG, FG, ACC, MUTED = "#1e1f26", "#f2f2f2", "#7aa2ff", "#8b8fa3"
    root = tk.Tk()
    root.title("Имя папы по отчеству")
    root.geometry("460x260")
    root.configure(bg=BG)
    root.resizable(False, False)

    tk.Label(root, text="Введи отчество или ФИО", bg=BG, fg=MUTED,
             font=("Segoe UI", 11)).pack(pady=(22, 6))

    var = tk.StringVar()
    entry = tk.Entry(root, textvariable=var, font=("Segoe UI", 16), justify="center",
                     bg="#2a2c36", fg=FG, insertbackground=FG, relief="flat")
    entry.pack(padx=40, fill="x", ipady=8)
    entry.focus_set()

    tk.Label(root, text="Папа:", bg=BG, fg=MUTED, font=("Segoe UI", 11)).pack(pady=(22, 0))
    result = tk.Label(root, text="—", bg=BG, fg=ACC, font=("Segoe UI", 28, "bold"))
    result.pack()
    note = tk.Label(root, text="", bg=BG, fg=MUTED, font=("Segoe UI", 9))
    note.pack()

    def update(*_):
        text = var.get().strip()
        if not text:
            result.config(text="—"); note.config(text="")
            return
        r = father_name(text)
        if r is None:
            result.config(text="?"); note.config(text="Отчество не распознано")
        else:
            name, exact = r
            result.config(text=name)
            note.config(text="" if exact else "Нет в словаре, это предположение")

    var.trace_add("write", update)
    root.mainloop()


if __name__ == "__main__":
    main()
