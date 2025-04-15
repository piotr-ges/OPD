import math
import random
import heapq

class Task:
    def __init__(self, r, p, q, index):
        self.r = r  # czas gotowości
        self.p = p  # czas przetwarzania
        self.q = q  # czas dostarczenia
        self.index = index  # numer zadania z pliku

    def __lt__(self, other):
        return self.q > other.q


def read_tasks_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    n = int(lines[0])
    tasks = []
    for i, line in enumerate(lines[1:n + 1]):
        r, p, q = map(int, line.split())
        tasks.append(Task(r, p, q, i))

    return tasks


def simple_schedule(tasks):
    time = 0
    c_max = 0
    schedule = []

    for task in tasks:

        time = max(time, task.r)
        time += task.p
        c_max = max(c_max, time + task.q)
        schedule.append(task.index)

    return c_max, schedule

def sortR_schedule(tasks):
    time = 0
    c_max = 0
    schedule = []

    tasks.sort(key=lambda x: x.r)

    for task in tasks:
        time = max(time, task.r)
        time += task.p
        c_max = max(c_max, time + task.q)
        schedule.append(task.index)

    return c_max, schedule

#Po zakończeniu pierwszego zadania patrzymy jakie są dostępne i sortujemy je po q rosnąco
def sortRQ_schedule(tasks):pass


def shuffle_schedule(tasks):
    n = len(tasks)
    time = 0
    c_max = 0
    schedule = []
    tasks.sort(key=lambda x: x.r)

    #Początkowy c_max
    for task in tasks:
        time = max(time, task.r)
        time += task.p
        c_max = max(c_max, time + task.q)

    prev_c_max = c_max

    for i in range(n):
        for j in range(n):
            tasks[i], tasks[j] = tasks[j], tasks[i]
            time = 0
            c_max = 0
            #Liczenie c_max
            for task in tasks:
                time = max(time, task.r)
                time += task.p
                c_max = max(c_max, time + task.q)

            #Sprawdzenie czy obecny c_max jest lepszy od poprzedniego
            if c_max <= prev_c_max:
                prev_c_max = c_max
            else:
                tasks[i], tasks[j] = tasks[j], tasks[i]

    #Tworzenie harmonogramu na podstawie zmian
    for task in tasks:
        schedule.append(task.index)

    return c_max, schedule


def schrage_schedule(tasks):
    n = len(tasks)
    time = 0
    c_max = 0
    schedule = []
    available_tasks = []
    i=0

    tasks.sort(key=lambda x: x.r)

    while available_tasks or i < n:
        while i < n and tasks[i].r <= time:
            heapq.heappush(available_tasks, tasks[i])
            i += 1

        if available_tasks:
            task = heapq.heappop(available_tasks)
            schedule.append(task.index)
            time += task.p
            c_max = max(c_max, time + task.q)
        else:
            time = tasks[i].r

    return c_max, schedule

def shuffle_Schrage_schedule(tasks):
    n = len(tasks)
    time = 0
    c_max = 0
    schedule = []
    task_dict = {task.index: task for task in tasks}
    prev_c_max, task_order = schrage_schedule(tasks)
    tasks = [task_dict[i] for i in task_order]

    for i in range(n):
        for j in range(n):
            tasks[i], tasks[j] = tasks[j], tasks[i]
            time = 0
            c_max = 0
            #Liczenie c_max
            for task in tasks:
                time = max(time, task.r)
                time += task.p
                c_max = max(c_max, time + task.q)

            #Sprawdzenie czy obecny c_max jest lepszy od poprzedniego
            if c_max <= prev_c_max:
                prev_c_max = c_max
            else:
                tasks[i], tasks[j] = tasks[j], tasks[i]

    #Tworzenie harmonogramu na podstawie zmian
    for task in tasks:
        schedule.append(task.index)

    return c_max, schedule


data_table = ["data.txt", "data2.txt", "data3.txt", "data4.txt"]
result_sum = 0
for i in range(4):
    print("------ Zestaw danych nr.", i + 1, "------")
    tasks = read_tasks_from_file(data_table[i])
    c_max, schedule = shuffle_schedule(tasks)
    print("Cmax:", c_max)
    print("Kolejność zadań:", schedule)
    result_sum += c_max

print("\nSuma wyników:", result_sum)

#Za tydzień symulowane wyrzarzanie
#Jednak nie było był schrage
