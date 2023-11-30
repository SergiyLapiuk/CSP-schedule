from time import time
from copy import copy
from collections import namedtuple

# Визначення графіка тижня та часових слотів
week_schedule = {1: "Понеділок", 2: "Вівторок", 3: "Середа", 4: "Четвер", 5: "П'ятниця"}
time_schedule = {
    1: "8:40-10:15",
    2: "10:35-12:10",
    3: "12:20-13:55",
}

# Основні класи даних, використовуючи namedtuple
Classroom = namedtuple("Classroom", "room is_big")
Time = namedtuple("Time", "weekday time")
Teacher = namedtuple("Teacher", "name")
Subject = namedtuple("Subject", "name")
Group = namedtuple("Group", "name")
Lesson = namedtuple("Lesson", "teacher subject group is_lecture per_week")
Schedule = namedtuple("Schedule", "lessons classrooms times")
DomainEl = namedtuple("DomainEl", "day time room")


# Прикладні дані для створення розкладу
# Список аудиторій
classrooms = [
    Classroom(1, True),
    Classroom(7, True),
    Classroom(12, True),
    Classroom(27, False),
    Classroom(35, False),
    Classroom(33, False),
    #  Classroom(205, False),
]

# Створення часових слотів для розкладу
schedule = [
    Time(w, n)
    for w in range(1, len(week_schedule.keys()) + 1)
    for n in range(1, len(week_schedule.keys()) + 1)
]

# Список викладачів
teachers = [
    Teacher(name)
    for name in (
        "0 Шевченко",
        "1 Коваленко",
        "2 Бондаренко",
        "3 Кравчук",
        "4 Ткаченко",
        "5 Мельник",
        "6 Лисенко",
        "7 Гончаренко",
        "8 Кузьменко",
        "9 Павленко",
        "10 Кличко",
        "11 Петренко",
        "12 Василенко",
        "13 Грищенко",
        "14 Демченко",
        "15 Тарасенко",
        "16 Савченко",
        "17 Зінченко",
        "18 Циганков",
    )
]

# Список предметів
subjects = [
    Subject(name)
    for name in (
        "0 Матан",
        "1 АГ",
        "2 Прог",
        "3 ООП",
        "4 Матлог",
        "5 ТА",
        "6 ДискМат",
        "7 ОС",
        "8 СисПрог",
        "9 Філософія",
        "10 НОС",
        "11 ЧМ",
        "12 ДифРів",
        "13 КМ",
        "14 Алгоритміка",
        "15 ІС",
        "16 ТПР",
        "17 БД",
    )
]

# Список груп
groups = [
    Group(name)
    for name in (
        "K-14",
        "K-15",
        "K-16",
        "K-17",
        "K-18",
    )
]

# Список уроків
lessons = [
    Lesson(teachers[0], subjects[0], groups[0], False, 1),
    Lesson(teachers[1], subjects[1], groups[0:5], True, 1),
    Lesson(teachers[2], subjects[2], groups[0], True, 2),
    Lesson(teachers[2], subjects[2], groups[0], True, 2),
    Lesson(teachers[3], subjects[12], groups[0], True, 1),
    Lesson(teachers[4], subjects[4], groups[0:5], True, 1),
    Lesson(teachers[5], subjects[4], groups[0], False, 1),
    Lesson(teachers[5], subjects[15], groups[0], True, 1),
    Lesson(teachers[9], subjects[6], groups[0:5], True, 1),
    Lesson(teachers[13], subjects[4], groups[0], False, 1),
    Lesson(teachers[13], subjects[16], groups[0], True, 2),
    Lesson(teachers[13], subjects[16], groups[0], True, 2),
    Lesson(teachers[5], subjects[4], groups[1], False, 1),
    Lesson(teachers[5], subjects[4], groups[2], False, 1),
    Lesson(teachers[6], subjects[4], groups[1], False, 1),
    Lesson(teachers[7], subjects[4], groups[2], False, 1),
    Lesson(teachers[8], subjects[3], groups[1:3], True, 1),
    Lesson(teachers[10], subjects[7], groups[1], False, 2),
    Lesson(teachers[10], subjects[7], groups[1], False, 2),
    Lesson(teachers[10], subjects[7], groups[2], False, 2),
    Lesson(teachers[10], subjects[7], groups[2], False, 2),
    Lesson(teachers[11], subjects[8], groups[1:3], True, 2),
    Lesson(teachers[11], subjects[8], groups[1:3], True, 2),
    Lesson(teachers[12], subjects[9], groups[1:3], True, 2),
    Lesson(teachers[12], subjects[9], groups[1:3], True, 2),
    Lesson(teachers[18], subjects[10], groups[1:3], True, 1),
    Lesson(teachers[5], subjects[4], groups[3], False, 1),
    Lesson(teachers[5], subjects[4], groups[4], False, 1),
    Lesson(teachers[6], subjects[4], groups[3], False, 1),
    Lesson(teachers[6], subjects[4], groups[4], False, 1),
    Lesson(teachers[14], subjects[12], groups[3:5], True, 2),
    Lesson(teachers[14], subjects[12], groups[3:5], True, 2),
    Lesson(teachers[15], subjects[13], groups[3:5], False, 1),
    Lesson(teachers[16], subjects[11], groups[3:5], True, 2),
    Lesson(teachers[16], subjects[11], groups[3:5], True, 2),
    Lesson(teachers[17], subjects[14], groups[3:5], True, 1),
    Lesson(teachers[17], subjects[17], groups[3:5], True, 1),
]

def run_mrv():
    return backtrack(mrv, init_domains(), Schedule([], [], []))


def run_lcv():
    return backtrack(lcv, init_domains(), Schedule([], [], []))


def run_degree():
    return backtrack(degree, init_domains(), Schedule([], [], []))


def run_forward_checking():
    return backtrack(forward_checking, init_domains(), Schedule([], [], []))

# Ініціалізує домени для кожного уроку
def init_domains():
    domain = {}
    buf = []
    buf_lecture = []
    # Створює доменні елементи для кожного дня, часового слоту та аудиторії
    for day in week_schedule.keys():
        for time_slot in time_schedule.keys():
            for room in classrooms:
                buf.append(DomainEl(day, time_slot, room))
                if room.is_big:
                    buf_lecture.append(DomainEl(day, time_slot, room))
    # Призначає домени для уроків
    for i in range(len(lessons)):
        if lessons[i].is_lecture:
            domain[i] = copy(buf_lecture)
        else:
            domain[i] = copy(buf)
    return domain

# Minimum Remaining Values еврістика для вибору уроку
def mrv(domain):
    min_len = len(week_schedule) * len(classrooms) * len(time_schedule) * 2
    ind = list(domain.keys())[0]
    for key, value in domain.items():
        if len(value) < min_len:
            min_len = len(value)
            ind = key
    return ind

# Degree еврістика для вибору уроку
def degree(domain):
    counts = {}
    for key in domain:
        counts[key] = 0 if lessons[key].is_lecture else 1
        for i in domain:
            if i == key:
                continue
            if lessons[key].teacher == lessons[i].teacher:
                counts[key] += 1
            counts[key] += len(
                set(map(str, lessons[key].group)) & set(map(str, lessons[i].group))
            )

    ind = list(counts.keys())[0]
    max = 0
    for key, value in counts.items():
        if value > max:
            max = value
            ind = key
    return ind

# LCV еврістика для вибору уроку
def lcv(domain):
    counts = {}
    # Підраховує кількість можливих варіантів для інших уроків
    for i in domain:
        counts[i] = 0
        for key in domain:
            if i == key:
                continue

            for d in domain[key]:
                if not (
                    d.day == domain[i][0].day
                    and d.time == domain[i][0].time
                    and d.room == domain[i][0].room
                ) and not (
                    d.day == domain[i][0].day
                    and d.time == domain[i][0].time
                    and (
                        lessons[key].teacher == lessons[i].teacher
                        or set(map(str, lessons[key].group))
                        & set(map(str, lessons[i].group))
                    )
                ):
                    counts[i] += 1

    ind = list(counts.keys())[0]
    max = 0
    for key, value in counts.items():
        if value > max:
            max = value
            ind = key
    return ind

# Forward Checking еврістика для вибору уроку
def forward_checking(domain):
    return list(domain.keys())[0]

# Функція зворотного відстеження для пошуку рішення
def backtrack(heuristic, domain, schedule):
    if not domain:
        return schedule
    ind = heuristic(domain)
    if ind == -1:
        return None
    for d in domain[ind]:
        sch_copy = copy(schedule)
        sch_copy.times.append(Time(d.day, d.time))
        sch_copy.classrooms.append(d.room)
        sch_copy.lessons.append(lessons[ind])

        dom_copy = copy(domain)
        dom_copy.pop(ind)
        dom_copy = update_domain(dom_copy, lessons[ind], d.day, d.time, d.room)

        res = backtrack(heuristic, dom_copy, sch_copy)
        if res:
            return res

    return None

# Оновлює домени після вибору уроку
def update_domain(domain, lesson, day, time, room):
    for key in domain:
        buf = []
        for d in domain[key]:
            if not (d.day == day and d.time == time and d.room == room) and not ( # ОБМЕЖЕННЯ
                d.day == day
                and d.time == time
                and (
                    lessons[key].teacher == lesson.teacher
                    or set(map(str, lessons[key].group)) & set(map(str, lesson.group))
                )
            ):
                buf.append(d)
        domain[key] = buf

    return domain

# Функція для друку розкладу
def print_schedule(solution: Schedule):
    for day in week_schedule:  # Прохід по дням тижня
        print("\n" + "-" * 100)
        print(f"{week_schedule[day].upper()}")
        for time in time_schedule:  # Прохід по часових слотах
            print("\n\n" + time_schedule[time])
            for c in classrooms:  # Прохід по аудиторіям
                print(f"\n{c}", end="\t\t")
                for i in range(len(solution.lessons)):  # Перевірка та вивід занять
                    if (solution.times[i].weekday == day and
                        solution.times[i].time == time and
                        solution.classrooms[i].room == c.room):
                        print(solution.lessons[i], end="")

# Основна функція
def main():
    # Запуск алгоритму MRV та друк результату
    solution = run_mrv()
    print_schedule(solution)

    # Вимірювання часу виконання для MRV
    start_time = time()
    run_mrv()
    print()
    print(f"MRV: {time() - start_time}")

    # Вимірювання часу виконання для LCV
    start_time = time()
    run_lcv()
    print(f"LCV: {time() - start_time}")

    # Вимірювання часу виконання для Degree heuristic
    start_time = time()
    run_degree()
    print(f"Degree: {time() - start_time}")

    # Вимірювання часу виконання для Forward checking
    start_time = time()
    run_forward_checking()
    print(f"Forward checking: {time() - start_time}")

# Запуск програми
if __name__ == "__main__":
    main()
