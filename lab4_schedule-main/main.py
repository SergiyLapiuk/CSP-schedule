from time import time
from heuristics import *  # Імпортує функції гейстурик та допоміжні функції
from structures import *  # Імпортує структури даних для розкладу

# Функція для друку розкладу
def print_schedule(solution: Schedule):
    for day in week_schedule:  # Прохід по дням тижня
        print("\n" + "=" * 100)
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
