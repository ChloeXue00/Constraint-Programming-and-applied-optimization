from z3 import *

def sort_bricks_case1(n_bricks, n_slots, init, goal):
    ts = 1

    while True:
        # s = Solver()
        opt = Optimize()

        bricks = range(n_bricks)
        slots = range(n_slots)
        timesteps = range(ts)

        on = [[[Bool(f'on_{b}_{s}_{t}') for t in timesteps] for s in slots] for b in bricks]
        obj = [[Bool(f'obj_{b}_{t}') for t in timesteps] for b in bricks]
        to = [[Bool(f'to_{s}_{t}') for t in timesteps] for s in slots]
        start = [[Bool(f'start_{s}_{t}') for t in timesteps] for s in slots]

        # Constraint 1  only one start position
        for b in bricks:
            for s in slots:
                for t in timesteps:
                    opt.add(Implies(And(on[b][s][t], obj[b][t]),
                                  And(start[s][t], And([Not(start[s2][t]) for s2 in slots if s2 != s]))))

        # Constraint 2: only one end position
        for s in slots:
            for t in timesteps:
                opt.add(to[s][t] == And([Not(to[s2][t]) for s2 in slots if s2 != s]))

        # Constraint 3: one bricks can be moved at each timestep
        for b in bricks:
            for t in timesteps:
                opt.add(obj[b][t] == And([Not(obj[b2][t]) for b2 in bricks if b2 != b]))

        # Constraint 4: the brick not being moved will stay for the next timestep
        for b in bricks:
            for s in slots:
                for t in range(ts - 1):
                    opt.add(Implies(And(Not(obj[b][t]), on[b][s][t]),
                                  And(on[b][s][t + 1], And([Not(on[b][s2][t + 1]) for s2 in slots if s2 != s]))))

        # Constraint 5: start and end position can't be the same
        for s in slots:
            for t in timesteps:
                opt.add(Implies(start[s][t], Not(to[s][t])))

        # Constraint 6 only move to one position
        for b in bricks:
            for t in range(ts - 1):
                for s in slots:
                    for s2 in slots:
                        if s2 != s:
                            opt.add(Implies(And(obj[b][t], And(start[s][t], to[s2][t])),
                                          And(on[b][s2][t + 1], And([Not(on[b][s3][t + 1]) for s3 in slots if s3 != s2]))))

        # Constraint 7 (Initial and goal positions)
        for b in bricks:
            opt.add(And(on[b][init[b] - 1][0], on[b][goal[b] - 1][ts - 1]))

        # Check the solution
        if opt.check() == sat:
            m = opt.model()
            print("Current position:")
            for t in timesteps:
                for s in slots:
                    for b in bricks:
                        print(m[on[b][s][t]], end=" ")
                    print("Slot")
                print(f"Time step - {t}")
            break
        else:
            ts += 1

    return [ts - 1, m]

# Parameters
bricks = 3
slots = 5
init = [1, 2, 3]
goal = [4, 5, 1]

bricks = 4
slots = 5
init = [1, 2, 3,4]
goal = [4, 5, 1,2]

[ts1, m1] = sort_bricks_case1(bricks, slots, init, goal)
print(f'Time steps needed to sort bricks in case 1 is {ts1}')
