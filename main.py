from problem import Problem


print("Welcome to flowshop scheduling problem solver!")
text = ""
while text not in ("f", "r"):
    text = input("Please choose one of the following options (r - for random task data, or f - for file input): ").lower()

if text == "f":
    file_name = input("Enter the file name (e.g., data.csv): ")
    problem = Problem(from_file=1, file_name=file_name)
else:
    try:
        machines_no = int(input("Enter number of machines: "))
        tasks_no = int(input("Enter number of tasks: "))
        times_min = int(input("Enter minimum processing time (>= 0): "))
        times_max = int(input("Enter maximum processing time (> min): "))

        if machines_no < 1 or tasks_no < 1:
            print("Number of machines and tasks must be at least 1.")
            exit()

        if times_min < 0 or times_max < 0:
            print("Processing times must be non-negative.")
            exit()

        if times_max <= times_min:
            print("Maximum processing time must be greater than minimum.")
            exit()

        seed_input = input("Enter seed value for random generation: ")
        seed = int(seed_input) if seed_input.strip() != "" else None
        
        times_range = (times_min, times_max)
        problem = Problem(from_file=0, machines_no=machines_no, tasks_no=tasks_no, times_range=times_range, seed=seed)
        problem.printTasks()

    except ValueError:
        print("Invalid input. Please enter numeric values.")
        exit()
    


algo_choice = ""
while algo_choice not in ("a", "b", "n"):
    algo_choice = input("Choose algorithm: (a - simulated annealing, b - brute force, n - neh): ").lower()

if algo_choice == "b":
    best_order, best_makespan = problem.bruteforce()
    print("\nBest order of tasks:", [f'T{i}' for i in best_order])
    print("Minimum makespan:", best_makespan)
elif algo_choice == "a":
    T0 = int(input("Enter T0: "))
    T_stop = int(input("Enter T_stop: "))
    alpha = float(input("Enter alpha: "))
    best_order, best_makespan = problem.simulated_annealing(T0, T_stop, alpha)
    print("\nBest order of tasks:", [f"T{i}" for i in best_order])
    print("Minimum makespan:", best_makespan)
if algo_choice == "n":
    best_order, best_makespan = problem.neh()
    print("\nBest order of tasks:", [f"T{i}" for i in best_order])
    print("Minimum makespan:", best_makespan)
