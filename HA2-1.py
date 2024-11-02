from gurobipy import *
"""##
1. decision variables: let x_ij represent the start time of jobs j on machine i
2. objective function: minimize the makespan: minC_max
3. constrains:  
    Precedence Constraints: Ensure each job follows the machine order: 
       x_ij + p_ij <=  x_(i+1),j    
    Machine Constraints: Ensure that no two jobs occupy the same machine at the same time:
       x_ij + p_ij <= x_ik,  i,j != k
    makespan contraint:
        C_max >= x_ij + p_ij
##"""

def solve_jsp_milp(jobs_data):
    n_jobs = len(jobs_data)
    n_machines = len(jobs_data[0])

    model = Model('jsp')

    start_times = model.addVars(n_jobs,n_machines,vtype=GRB.INTEGER,name='start_time')

    makespan= model.addVar(vtype=GRB.INTEGER,name='makespan')

    model.setObjective(makespan,GRB.MINIMIZE)

    for job in range(n_jobs):
        for i in range(1,len(jobs_data[0])):
            machine_prev , proc_time_prev= jobs_data[job][i-1]
            machine_curr, _ = jobs_data[job][i]
            model.addConstr(
                start_times[job, machine_prev] + proc_time_prev <= start_times[job, machine_curr],
                name = f'precedence_job{job}_machine{machine_prev}_to_machine{machine_curr}'
            )

    for machine in range(n_machines):
        for job1 in range(n_jobs):
            for job2 in range(job1+1,n_jobs):
                proc_time1 = jobs_data[job1][machine][1]
                proc_time2 = jobs_data[job2][machine][1]

                model.addConstr(
                    start_times[job1,machine] + proc_time1 <= start_times[job2,machine],
                    name=f"no_overlap_job{job1}_job{job2}_on_machine{machine}_1")
                model.addConstr(
                    start_times[job2,machine] + proc_time2 <= start_times[job1,machine],
                    name = f'no_overlap_job{job1}_job{job2}_on_machine{machine}_2'
                )

    for job in range(n_jobs):
        machine_last,proc_time_last = jobs_data[job][-1]
        model.addConstr(
            makespan >= start_times[job,machine_last] + proc_time_last,
            name =f'makespan_job{job}'
        )

    # 3. Makespan constraints: Ensure that the makespan is greater than or equal to each job's last finish time
    for job in range(n_jobs):
        machine_last, proc_time_last = jobs_data[job][-1]  # Last machine and its processing time
        model.addConstr(
            makespan >= start_times[job, machine_last] + proc_time_last,
            name=f"makespan_job{job}"
        )

    model.optimize()

    if model.status == GRB.OPTIMAL:
        print(f'Optimal makespan:{makespan.X}')
        for job in range(n_jobs):
            for machine in range(n_machines):
                print(f'Job {job} on Machine {machine} starts at {start_time[job,machine].X}')
    else:
        print('No optimal solution found')

    # If the model is infeasible, find out why
    if model.status == GRB.INFEASIBLE:
        print("The model is infeasible; finding conflicting constraints...")
        model.computeIIS()
        model.write("infeasible_model.ilp")  # Save the IIS to a file



ft06_data = [
    [(2, 1), (0, 3), (1, 6), (3, 7), (5, 3), (4, 6)],  # Job 1
    [(1, 8), (2, 5), (4, 10), (5, 10), (0, 10), (3, 4)],  # Job 2
    [(2, 5), (3, 4), (5, 8), (0, 9), (1, 1), (4, 7)],  # Job 3
    [(1, 5), (0, 5), (2, 5), (3, 3), (4, 8), (5, 9)],  # Job 4
    [(2, 9), (1, 3), (4, 5), (5, 4), (0, 3), (3, 1)],  # Job 5
    [(1, 3), (3, 3), (5, 9), (0, 10), (4, 4), (2, 1)]   # Job 6
]

solve_jsp_milp(ft06_data)

ft10_data = [
    [(0,29), (1, 78), (2, 9), (3, 36), (4, 49), (5, 11),(6,62), (7,56),(8,44),(9,21)],  # Job 1
    [(0, 43), (2, 90), (4, 75), (9, 11), (3, 69), (1, 28),(6,46),(5,46),(7,72),(8,30)],  # Job 2
    [(1,91), (0, 85), (3, 39), (2, 74), (8, 90), (5, 10),(7,12),(6,89),(9,45),(4,33)],  # Job 3
    [(1, 81), (2, 95), (0, 71), (4, 99), (6, 9), (8 ,52), (7,85), (3,98), (9,22), (5,43)],  # Job 4
    [(2,14),(0 ,6), (1, 22), (5,61),(3,26),(4,69), (8,21), (7,49), (9,72),(6,53)],      # Job 5
    [ (2,84), (1,2), (5,52), (3,95), (8,48), (9,72), (0,47), (6,65), (4,6), (7,25)],# Job 6
    [(1,46), (0,37), (3,61), (2,13), (6,32), (5,21), (9,32), (8,89), (7,30), (4,55)],# Job 7
    [(2,31), (0,86), (1,46), (5,74), (4,32), (6,88), (8,19), (9,48), (7,36), (3,79)],# Job 8
    [(0,76), (1,69), (3,76), (5,51), (2,85), (9,11), (6,40), (7,89), (4,26), (8,74)],# Job 9
    [(1,85), (0,13), (2,61), (6,7), (8,64), (9,76), (5,47), (3,52), (4,90), (7,45)] # Job 10
]

solve_jsp_milp(ft10_data)

lab01_data = [
   [(1,21), (0,53), (4,95), (3,55),(2,34)],
    [(0,21), (3,52), (4,16), (2,26), (1,71)],
    [(3,39), (4,98), (1,42), (2,31), (0,12)],
    [(1,77), (0,55), (4,79), (2,66), (3,77)],
    [(0,83), (3,34), (2, 64), (1, 19), (4, 37)],
    [(1,54), (2,43), (4, 79), (0, 92),(3, 62)],
    [(3,69), (4,77), (1,87), (2,87), (0,93)],
    [(2,38), (0,60), (1,41), (3,24), (4,83)],
    [(3,17), (1,49), (4,25), (0,44), (2,98)],
    [(4,77), (3,79), (2,43), (1,75), (0,96)]
]
solve_jsp_milp(lab01_data)

# Testing with different data (e.g., 8 jobs and 6 machines)

