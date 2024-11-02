import gurobipy as gp
from gurobipy import GRB

# Function to read data from a text file and return n, m, times, and machines
def read_data_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    n, m = map(int, lines[0].split())

    times = []
    machines = []

    for line in lines[1:]:
        data = list(map(int, line.split()))
        times.append(data)
        machine_order = list(range(m))
        machine_order.sort(key=lambda x: data[x * 2])
        machines.append(machine_order)

    return n, m, times, machines

# Function to solve the job scheduling problem using Gurobi's CP solver
def solve_job_scheduling_cp(n, m, times, machines):
    model = gp.Model("JSSP_CP")

    # Create start time variables for each task
    start_times = {}
    for j in range(n):
        for i in range(m):
            start_times[j, i] = model.addVar(vtype=GRB.INTEGER, name=f'start_time_{j}_{i}')

    # Set objective to minimize the makespan (completion time)
    c_max = model.addVar(vtype=GRB.INTEGER, name='c_max')
    model.setObjective(c_max, GRB.MINIMIZE)

    # Add constraints to ensure task sequencing and completion times
    for j in range(n):
        for i in range(1, m):
            model.addConstr(start_times[j, machines[j][i]] - start_times[j, machines[j][i-1]] >= times[j][machines[j][i-1]])

        last_machine = machines[j][m - 1]
        model.addConstr(c_max >= start_times[j, last_machine] + times[j][last_machine])

    # Set the time limit for the solver (20 minutes)
    model.Params.TimeLimit = 20 * 60

    # Optimize the CP model
    model.optimize()

    # Extract and return the results
    if model.status == GRB.OPTIMAL:
        completion_time = c_max.x
        schedule = {}
        for j in range(n):
            for i in range(m):
                schedule[j, machines[j][i]] = start_times[j, machines[j][i]].x
        return completion_time, schedule
    else:
        return None

if __name__ == "__main__":
    # Specify the path to your input file
    # file_path = 'C:\\Users\\xuefx\\PycharmProjects\\coppc\\ft06.txt' #30
    # file_path = 'C:\\Users\\xuefx\\PycharmProjects\\coppc\\ft10.txt'  #completion time:393
    # file_path = 'C:\\Users\\xuefx\\PycharmProjects\\coppc\\la01.txt' #165
    # file_path = 'C:\\Users\\xuefx\\PycharmProjects\\coppc\\la05.txt' #164
    file_path = 'C:\\Users\\xuefx\\PycharmProjects\\coppc\\la04.txt'  # 600
    # Read data from the input file
    n, m, times, machines = read_data_from_file(file_path)

    # Solve the job scheduling problem using Gurobi's CP solver
    result = solve_job_scheduling_cp(n, m, times, machines)

    # Print the results
    if result is not None:
        completion_time, schedule = result
        print("Completion time:", completion_time)
        for j in range(n):
            for i in range(m):
                print(f"Task {j+1} starts on machine {machines[j][i]+1} at time {schedule[j, machines[j][i]]}")
    else:
        print("No solution found.")