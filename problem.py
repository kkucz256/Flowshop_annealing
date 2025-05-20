import random
import os
import itertools
import time
import numpy as np


class Problem():
    def __init__(self, from_file, file_name = None, machines_no = None, tasks_no = None, times_range = None, seed = None):
        self.tasks = {}
        
        if from_file == 0:
            if machines_no is None or tasks_no is None or times_range is None:
                print("Missing parameters, if you don't want to generate from file, provide all parameters")
                return
            else:
                if seed is None:
                    random.seed(int(time.time() * 1000))
                else:
                    random.seed(seed)

                self.tasks = {}
                for task_id in range(1, tasks_no + 1):
                    tasks = random.choices(range(times_range[0], times_range[1] + 1), k=machines_no)
                    self.tasks[task_id] = tasks

                self.printTasks()

        elif from_file == 1:
            if file_name == None:
                print("Missing file name, if you want to generate from file, provide a valid file name")
                return
            elif not os.path.isfile(file_name):
                print(f"File '{file_name}' does not exist or is not a file.")
                return
            else:
                with open(file_name) as f:
                    lines = f.readlines()
                    for i in range(1,len(lines)):
                        items_in_line = lines[i].strip().split(",")
                        tasks_to_append = []
                        for j in range(1,len(items_in_line)):
                            try:
                                tasks_to_append.append(int(items_in_line[j]))
                            except ValueError:
                                print(f"Error: Incorrect data format in line {i + 1}, column {j + 1}, should be an integer and currently it is {items_in_line[j]}")
                                return 
                            
                        self.tasks[i] = tasks_to_append
                self.printTasks()
        
    def printTasks(self):
        for key, val in self.tasks.items():
            print(f"T{key}",":",val)

    def makespan(self, order):
        matrix = []
        for i, current_task in enumerate(order):
            row = []
            for j, task_time in enumerate(self.tasks[current_task]):
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
            
    def bruteforce(self):
            if not self.tasks:
                print("No tasks loaded.")
                return

            num_tasks = len(self.tasks)
            num_machines = len(self.tasks[1])
            best_order = None
            best_makespan = float('inf')

            for perm in itertools.permutations(range(1, num_tasks+1)):
                makespan = self.makespan(perm)
                if makespan < best_makespan:
                    best_makespan = makespan
                    best_order = perm

            return best_order, best_makespan

    def simulated_annealing(self, T0, T_stop, alpha):
        if not self.tasks:
            print("No tasks loaded.")
            return

        best_order = []
        best_makespan = float('inf')

        T = T0

        Order = list(range(1, len(self.tasks)+1))
        random.shuffle(Order)
        

        while T > T_stop:
            new_Order = Order[:]
            i, j = 0, 0
            while i==j:
                i, j = random.randint(0, len(Order)-1), random.randint(0, len(Order)-1)
            new_Order[i], new_Order[j] = new_Order[j], new_Order[i]

            Order_makespan = self.makespan(Order)
            new_Order_makespan = self.makespan(new_Order)

            diff = new_Order_makespan - Order_makespan

            if diff <= 0 or random.random() < np.exp((-1)*diff/T):
                Order = new_Order
                if new_Order_makespan < best_makespan:
                    best_order = Order[:]
                    best_makespan = new_Order_makespan
            
            T *= alpha

        return best_order, best_makespan
    
    def neh(self):
        if not self.tasks:
            print("No tasks loaded.")
            return

        total_times = {task_id: sum(times) for task_id, times in self.tasks.items()}
        sorted_tasks = sorted(total_times, key=total_times.get, reverse=True)

        partial_schedule = [sorted_tasks[0]]
        for task in sorted_tasks[1:]:
            best_makespan = float('inf')
            best_schedule = []

            for i in range(len(partial_schedule) + 1):
                temp_schedule = partial_schedule[:i] + [task] + partial_schedule[i:]
                current_makespan = self.makespan(temp_schedule)
                if current_makespan < best_makespan:
                    best_makespan = current_makespan
                    best_schedule = temp_schedule

            partial_schedule = best_schedule

        return partial_schedule, self.makespan(partial_schedule)
