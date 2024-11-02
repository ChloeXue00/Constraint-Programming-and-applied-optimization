import gurobipy as gp
from gurobipy import *


# Function to read job scheduling data from a text file
def read_job_scheduling_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

        # Extract n and m values from the first line
        n, m = map(int, lines[0].split())

        # Initialize lists for times and machines
        times = []
        machines = []

        # Read the remaining lines and extract times and machines data
        for line in lines[1:]:
            data = list(map(int, line.split()))
            machine_process_pairs = [(data[i], data[i + 1]) for i in range(0, len(data), 2)]
            machines.append([pair[0] for pair in machine_process_pairs])
            times.append([pair[1] for pair in machine_process_pairs])

        # Read updated travel times from a separate file or data source
        travel_times = [
            [28.4, 10.4, 10.8, 23.6, 18.2, 25.4, 26.6],
            [14.0, 14.4, 22.8, 25.4, 13.0, 12.8, 27.0],
            [28.4, 23.2, 18.2, 13.0, 10.8, 8.4, 26.6],
            [14.0, 10.8, 10.4, 23.2, 15.6, 25.4, 20.0],
            [28.4, 14.4, 8.4, 25.4, 13.0, 12.8, 27.0],
            [14.0, 23.6, 18.2, 13.0, 12.4, 22.8, 10.6]
        ]

    return n, m, times, machines, travel_times


# Function to solve the job scheduling problem

def solve_job_scheduling(n, m, times, machines):
    # Calculate a large constant M
    M = sum(times[i][j] for i in range(n) for j in range(m))

    # Create the Gurobi model
    model = gp.Model('JSSP')
    model.Params.TimeLimit = 20 * 60

    # Define decision variables
    c = model.addVar(name="C", vtype=GRB.INTEGER)
    x = [[model.addVar(name='x({},{})'.format(j + 1, i + 1), vtype=GRB.INTEGER)
          for i in range(m)] for j in range(n)]
    y = [[[model.addVar(name='y({},{},{})'.format(j + 1, k + 1, i + 1), vtype=GRB.BINARY)
           for i in range(m)] for k in range(n)] for j in range(n)]

    # Set the objective function to minimize completion time (C)
    model.setObjective(c, GRB.MINIMIZE)



    for j in range(n):
        for i in range(1, m):
            machine_start = x[j][machines[j][i]]
            machine_end = x[j][machines[j][i - 1]]
            # Add travel time to the constraint
            travel_time = travel_times[j][machines[j][i - 1]]
            model.addConstr(machine_start - machine_end >= times[j][machines[j][i - 1]] + travel_time)

    # Constraints for task sequencing between jobs
    for j in range(n):
        for k in range(n):
            if k != j:
                for i in range(m):
                    model.addConstr(x[j][i] - x[k][i] + M * y[j][k][i] >= times[k][i])
                    model.addConstr(-x[j][i] + x[k][i] - M * y[j][k][i] >= times[j][i] - M)

    # Constraints for job completion time
    for j in range(n):
        last_machine = x[j][machines[j][m - 1]]
        model.addConstr(c - last_machine >= times[j][machines[j][m - 1]])

    # Optimize the model
    model.optimize()

    return model


# Entry point of the script
if __name__ == "__main__":
    # Specify the file name (without full path) in the same directory as the script
    file_name = 'C:\\Users\\xuefx\\PycharmProjects\\coppc\\ft06.txt'

    # Construct the full file path by combining the current directory and the file name
    file_path = file_name

    # Read job scheduling data including updated travel times from the specified file
    n, m, times, machines, travel_times = read_job_scheduling_data(file_path)

    # Solve the job scheduling problem using the extracted data
    model = solve_job_scheduling(n, m, times, machines)

    # Print the results
    if model.status == GRB.OPTIMAL:
        print("Completion time: ", model.objVal)
        for j in range(n):
            for i in range(m):
                print("task %d starts on machine %d at time %g " % (
                j + 1, i + 1, model.getVarByName('x({},{})'.format(j + 1, i + 1)).x))
    else:
        print("No solution found.")