import random
import numpy as np

def makespan(order, tasks):
    matrix = []
    for i, current_task in enumerate(order):
        row = []
        for j, task_time in enumerate(tasks[current_task]):
            if i == 0 and j == 0:
                row.append(task_time)
            elif i == 0 and j !=0:
                row.append(task_time + row[j-1])
            elif j==0:
                row.append(task_time + matrix[i-1][j])
            else:
                row.append(task_time + max(row[j-1], matrix[i-1][j]))
        matrix.append(row)
    return matrix[-1][-1]
                


def simulated_annealing_func(tasks, T0, T_stop, alpha):
    best_order = []
    best_makespan = float('inf')

    T = T0

    Order = list(range(1, len(tasks)+1))
    random.shuffle(Order)
    

    while T > T_stop:
        new_Order = Order[:]
        i, j = 0, 0
        while i==j:
            i, j = random.randint(0, len(Order)-1), random.randint(0, len(Order)-1)
        new_Order[i], new_Order[j] = new_Order[j], new_Order[i]

        #print(new_Order)

        Order_makespan = makespan(Order, tasks)
        new_Order_makespan = makespan(new_Order, tasks)

        diff = new_Order_makespan - Order_makespan

        if diff <= 0 or random.random() < np.exp((-1)*diff/T):
            Order = new_Order
            if new_Order_makespan < best_makespan:
                best_order = Order[:]
                best_makespan = new_Order_makespan
        
        T *= alpha

    return best_order, best_makespan

if __name__ == "__main__":
    tasks = {
        1:[3, 2, 2],  # Zadanie 1: (M1: 3, M2: 2, M3: 2)
        2:[4, 3, 1],  # Zadanie 2: (M1: 4, M2: 3, M3: 1)
        3:[2, 5, 3],  # Zadanie 3: (M1: 2, M2: 5, M3: 3)
        4:[5, 2, 4],  # Zadanie 4: (M1: 5, M2: 2, M3: 4)
        5:[3, 4, 2],  # Zadanie 5: (M1: 3, M2: 4, M3: 2)
    }

    # Parametry algorytmu symulowanego wyżarzania
    T0 = 10000  # Początkowa temperatura
    T_stop = 1  # Temperatura końcowa
    alpha = 0.95  # Współczynnik chłodzenia

    # Uruchomienie algorytmu
    best_order, best_makespan = simulated_annealing_func(tasks, T0, T_stop, alpha)

    # Wynik
    print("Najlepsza kolejność zadań:", best_order)
    print("Najkrótszy czas wykonania (makespan):", best_makespan)
