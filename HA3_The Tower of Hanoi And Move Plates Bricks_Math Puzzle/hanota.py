from z3 import *

# Parameters for the problem: number of disks, towers, and steps
def tower_of_hanoi_z3(num_disks, num_towers, max_steps):
    # Create Z3 solver
    solver = Solver()

    # Variables: on(d, tw, t), obj(d, t), from(tw, t), to(tw, t)
    on = [[[Bool(f"on_{d}_{tw}_{t}") for t in range(max_steps + 1)] for tw in range(num_towers)] for d in range(num_disks)]
    obj = [[Bool(f"obj_{d}_{t}") for t in range(max_steps)] for d in range(num_disks)]
    from_tower = [[Bool(f"from_{tw}_{t}") for t in range(max_steps)] for tw in range(num_towers)]
    to_tower = [[Bool(f"to_{tw}_{t}") for t in range(max_steps)] for tw in range(num_towers)]

    # Initial condition: All disks are on the first tower at step 0
    for d in range(num_disks):
        solver.add(on[d][0][0])
        for tw in range(1, num_towers):
            solver.add(Not(on[d][tw][0]))

    # Final condition: All disks are on the last tower at final step
    for d in range(num_disks):
        solver.add(on[d][num_towers - 1][max_steps])
        for tw in range(num_towers - 1):
            solver.add(Not(on[d][tw][max_steps]))

    # Precondition I: No disk can be moved if a smaller disk is on the same tower
    for d in range(1, num_disks):
        for tw in range(num_towers):
            for t in range(max_steps):
                smaller_on_same_tower = Or([on[sd][tw][t] for sd in range(d)])
                solver.add(Implies(And(on[d][tw][t], smaller_on_same_tower), Not(obj[d][t])))

    # Precondition II: No disk can be moved to a tower with a smaller disk already there
    for d in range(1, num_disks):
        for tw in range(num_towers):
            for t in range(max_steps):
                smaller_on_target_tower = Or([on[sd][tw][t] for sd in range(d)])
                solver.add(Implies(And(obj[d][t], to_tower[tw][t]), Not(smaller_on_target_tower)))

    # Uniqueness of from and to variables (one move per time step)
    for t in range(max_steps):
        solver.add(Or([from_tower[tw][t] for tw in range(num_towers)]))
        solver.add(Or([to_tower[tw][t] for tw in range(num_towers)]))
        for tw in range(num_towers):
            solver.add(Implies(from_tower[tw][t], And([Not(from_tower[tw2][t]) for tw2 in range(num_towers) if tw2 != tw])))
            solver.add(Implies(to_tower[tw][t], And([Not(to_tower[tw2][t]) for tw2 in range(num_towers) if tw2 != tw])))

    # Objective: Minimize the number of steps
    step_count = Int('steps')
    solver.add(step_count <= max_steps)

    # Check satisfiability and get the result
    if solver.check() == sat:
        model = solver.model()
        print(f"Solved in {model[step_count]} steps")
    else:
        print("No solution found")

# Example usage: Solve Tower of Hanoi with 3 disks, 3 towers, and up to 15 steps
tower_of_hanoi_z3(5, 3, 256)
