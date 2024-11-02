from z3 import *

# Parameters for the problem: number of disks and towers
def tower_of_hanoi_z3_optimized(num_disks, num_towers):
    # Create Z3 optimization solver
    opt = Optimize()

    # Maximum possible steps is arbitrary, just needs to be large enough
    max_steps = 200 # Max possible steps as an upper bound (arbitrary large enough)

    # Variables: on(d, tw, t), obj(d, t), from(tw, t), to(tw, t)
    on = [[[Bool(f"on_{d}_{tw}_{t}") for t in range(max_steps + 1)] for tw in range(num_towers)] for d in range(num_disks)]
    obj = [[Bool(f"obj_{d}_{t}") for t in range(max_steps)] for d in range(num_disks)]
    from_tower = [[Bool(f"from_{tw}_{t}") for t in range(max_steps)] for tw in range(num_towers)]
    to_tower = [[Bool(f"to_{tw}_{t}") for t in range(max_steps)] for tw in range(num_towers)]

    # Variable to count the steps
    steps = Int('steps')
    opt.add(steps >= 0)
    opt.add(steps <= max_steps)

    # Initial condition: All disks are on the first tower at step 0
    for d in range(num_disks):
        opt.add(on[d][0][0])  # Disk d is on the first tower at time 0
        for tw in range(1, num_towers):
            opt.add(Not(on[d][tw][0]))  # Disk d is not on other towers at time 0

    # Final condition: All disks are on the last tower at the final step
    # Instead of using `steps` as an index, create constraints for all possible steps
    for d in range(num_disks):
        for t in range(max_steps + 1):
            # Disk d must be on the last tower if t is equal to steps
            opt.add(Implies(steps == t, on[d][num_towers - 1][t]))
            # Disk d must NOT be on any other tower at step t
            for tw in range(num_towers - 1):
                opt.add(Implies(steps == t, Not(on[d][tw][t])))

    # Precondition I: No disk can be moved if a smaller disk is on the same tower
    for d in range(1, num_disks):
        for tw in range(num_towers):
            for t in range(max_steps):
                smaller_on_same_tower = Or([on[sd][tw][t] for sd in range(d)])
                opt.add(Implies(And(on[d][tw][t], smaller_on_same_tower), Not(obj[d][t])))

    # Precondition II: No disk can be moved to a tower with a smaller disk already there
    for d in range(1, num_disks):
        for tw in range(num_towers):
            for t in range(max_steps):
                smaller_on_target_tower = Or([on[sd][tw][t] for sd in range(d)])
                opt.add(Implies(And(obj[d][t], to_tower[tw][t]), Not(smaller_on_target_tower)))

    # Uniqueness of from and to variables (one move per time step)
    for t in range(max_steps):
        opt.add(Or([from_tower[tw][t] for tw in range(num_towers)]))  # At least one tower is the from tower
        opt.add(Or([to_tower[tw][t] for tw in range(num_towers)]))  # At least one tower is the to tower
        for tw in range(num_towers):
            # From one tower only at each step
            opt.add(Implies(from_tower[tw][t], And([Not(from_tower[tw2][t]) for tw2 in range(num_towers) if tw2 != tw])))
            # To one tower only at each step
            opt.add(Implies(to_tower[tw][t], And([Not(to_tower[tw2][t]) for tw2 in range(num_towers) if tw2 != tw])))
    for t in range(max_steps):
        # 确保每个时间步 t 只有一个盘子在移动
        opt.add(Or([obj[d][t] for d in range(num_disks)]))  # 至少有一个盘子在移动
        for d in range(num_disks):
            opt.add(Implies(obj[d][t], And([Not(obj[d2][t]) for d2 in range(num_disks) if d2 != d])))  # 只移动一个盘子
    # Non-moving disks
    for d in range(num_disks):
        for tw in range(num_towers):
            for t in range(max_steps - 1):
                # 如果盘子 d 没有在时间 t 移动，并且它在塔 tw 上，那么在下一步 t + 1 中，它应该仍然在塔 tw 上。
                opt.add(Implies(And(Not(obj[d][t]), on[d][tw][t]), on[d][tw][t + 1]))

    #unisequence of obj tower
    for t in range(max_steps):
        for tw in range(num_towers):
            # 如果盘子从塔 tw 移动，那么目标塔必须与原塔不同
            opt.add(Not(And(from_tower[tw][t], to_tower[tw][t])))

    for d in range(num_disks):
        for tw in range(num_towers):
            for tw2 in range(num_towers):
                if tw != tw2:  # 确保 tw 和 tw2 是不同的塔
                    for t in range(max_steps - 1):
                        # 如果盘子 d 在时间 t 从塔 tw 移动到塔 tw2，
                        # 那么它在 t + 1 时应该在塔 tw2 上，且不在其他塔上
                        opt.add(Implies(
                            And(obj[d][t], from_tower[tw][t], to_tower[tw2][t]),
                            And(
                                on[d][tw2][t + 1],  # 确保盘子在目标塔上
                                And([Not(on[d][tw3][t + 1]) for tw3 in range(num_towers) if tw3 != tw2])  # 确保不在其他塔上
                            )
                        ))

    # Optimize the step count
    opt.minimize(steps)

    # Check if the solution is feasible
    if opt.check() == sat:
        model = opt.model()
        print(f"Solved in {model[steps]} steps")
    else:
        print("No solution found")

# Example usage: Solve Tower of Hanoi with 3 disks, 3 towers
tower_of_hanoi_z3_optimized(4, 3)
