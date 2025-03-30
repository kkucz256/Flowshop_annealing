import random
import os
import itertools
import time
from simulated_annealing import simulated_annealing_func


class Problem():
    def __init__(self, from_file, file_name = None, machines_no = None, tasks_no = None, times_range = None, seed = None):
        self.tasks = {}
        
        if from_file == 0:
            if machines_no == None or tasks_no == None or times_range == None:
                print("Missing parameters, if you don't want to generate from file, provide all parameters")
                return
            else:
                if seed is None:
                    random.seed(int(time.time()*1000))
                else:
                    random.seed(seed)
                for _ in range(tasks_no):
                    tasks = random.sample(range(times_range[0],times_range[1]), machines_no)
                    self.tasks.append(tasks)
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
            
    def bruteforce(self):
            if not self.tasks:
                print("No tasks loaded.")
                return

            num_tasks = len(self.tasks)
            num_machines = len(self.tasks[1])
            best_order = None
            best_makespan = float('inf')

            for perm in itertools.permutations(range(num_tasks)):
                completion = [[0] * num_machines for _ in range(num_tasks)]

                for i, task_idx in enumerate(perm):
                    for j in range(num_machines):
                        time = self.tasks[task_idx+1][j]
                        if i == 0 and j == 0:
                            completion[i][j] = time
                        elif i == 0:
                            completion[i][j] = completion[i][j - 1] + time
                        elif j == 0:
                            completion[i][j] = completion[i - 1][j] + time
                        else:
                            completion[i][j] = max(completion[i - 1][j], completion[i][j - 1]) + time

                makespan = completion[-1][-1]
                if makespan < best_makespan:
                    best_makespan = makespan
                    best_order = perm

            print("\nBest order of tasks:", [f"T{i+1}" for i in best_order])
            print("Minimum makespan:", best_makespan)

    def simulated_annealing(self, T0, T_stop, alpha):
        best_order, best_makespan = simulated_annealing_func(self.tasks, T0, T_stop, alpha)
        print("\nBest order of tasks:", [f"T{i}" for i in best_order])
        print("Minimum makespan:", best_makespan)

                
